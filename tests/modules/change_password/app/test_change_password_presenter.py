import pytest
import json
from unittest.mock import MagicMock
from src.modules.change_password.app.change_password_presenter import lambda_handler
from src.modules.change_password.app import change_password_presenter

class Test_ChangePasswordPresenter:
    def test_change_password_presenter_success(self):
        change_password_presenter.usecase.cognito = MagicMock()
        change_password_presenter.usecase.cognito.confirm_forgot_password.return_value = {}

        event = {
            "body": {
                "email": "test@maua.br",
                "code": "123456",
                "new_password": "NewPassword123!"
            }
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Senha alterada com sucesso!"

    def test_change_password_presenter_missing_fields(self):
        event = {
            "body": {
                "email": "test@maua.br"
            }
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert body == "Field code is missing"
