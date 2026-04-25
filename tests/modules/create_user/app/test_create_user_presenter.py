import json
import uuid
from unittest.mock import MagicMock
from src.modules.create_user.app.create_user_presenter import lambda_handler
from src.modules.create_user.app import create_user_presenter

class Test_CreateUserPresenter:

    def test_create_user(self):
        create_user_presenter.usecase.cognito = MagicMock()
        create_user_presenter.usecase.cognito.sign_up.return_value = {
            'UserSub': str(uuid.uuid4())
        }

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "requestContext": {
                "authorizer": {
                }
            },
            "body": json.dumps({
                "email": "test@test.com",
                "name": "Test User",
                "password": "Password123!",
                "role": "USER",
                "height": 1.75
            })
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert body["message"] == "User successfully created"
        assert body["user"]["name"] == "Test User"
        assert body["user"]["email"] == "test@test.com"
