import json
from unittest.mock import MagicMock
from src.modules.confirm_user.app.confirm_user_presenter import lambda_handler
from src.modules.confirm_user.app import confirm_user_presenter

class Test_ConfirmUserPresenter:
    def test_confirm_user_presenter_success(self):
        confirm_user_presenter.usecase.cognito = MagicMock()
        confirm_user_presenter.usecase.cognito.confirm_sign_up.return_value = {}

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "body": json.dumps({
                "email": "21.00458-7@maua.br",
                "code": "123456"
            })
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Conta ativada com sucesso!"
        assert body["user"]["status"] == "CONFIRMED"
