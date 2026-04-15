from src.modules.create_user_cognito.app import create_user_cognito_presenter


class SpyController:
    def __init__(self):
        self.called_with = None

    def __call__(self, event):
        self.called_with = event
        return None


class Test_CreateUserCognitoPresenter:
    def test_lambda_handler_returns_event_and_calls_controller(self, monkeypatch):
        controller = SpyController()
        monkeypatch.setattr(create_user_cognito_presenter, "controller", controller)

        event = {
            "triggerSource": "PostConfirmation_ConfirmSignUp",
            "request": {
                "userAttributes": {
                    "sub": "12345678-1234-1234-1234-123456789012",
                    "email": "event.user@maua.br",
                    "name": "Event User"
                },
                "clientMetadata": {
                    "role": "USER",
                    "height": "1.72"
                }
            },
            "response": {}
        }

        response = create_user_cognito_presenter.lambda_handler(event, None)

        assert response == event
        assert controller.called_with == event
