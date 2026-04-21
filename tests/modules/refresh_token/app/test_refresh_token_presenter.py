import json
from unittest.mock import MagicMock
from src.modules.refresh_token.app.refresh_token_presenter import lambda_handler
from src.modules.refresh_token.app import refresh_token_presenter

class Test_RefreshTokenPresenter:
    def test_refresh_token(self):
        refresh_token_presenter.usecase.cognito = MagicMock()
        refresh_token_presenter.usecase.cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "IdToken": "mock_id_token",
                "AccessToken": "mock_access_token",
                "RefreshToken": "mock_refresh_token_new",
                "ExpiresIn": 3600,
                "TokenType": "Bearer"
            }
        }

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "body": json.dumps({
                "refresh_token": "mock_refresh_token"
            })
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["id_token"] == "mock_id_token"
