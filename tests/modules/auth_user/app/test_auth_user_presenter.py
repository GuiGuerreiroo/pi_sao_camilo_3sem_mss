import json
from unittest.mock import MagicMock
from src.modules.auth_user.app.auth_user_presenter import lambda_handler
from src.modules.auth_user.app import auth_user_presenter

class Test_AuthUserPresenter:
    def test_auth_user(self):
        auth_user_presenter.usecase.cognito = MagicMock()
        auth_user_presenter.usecase.cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "IdToken": "mock_id_token",
                "AccessToken": "mock_access_token",
                "RefreshToken": "mock_refresh_token",
                "ExpiresIn": 3600,
                "TokenType": "Bearer"
            }
        }

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "body": json.dumps({
                "email": "test@test.com",
                "password": "Password123!"
            })
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["id_token"] == "mock_id_token"
