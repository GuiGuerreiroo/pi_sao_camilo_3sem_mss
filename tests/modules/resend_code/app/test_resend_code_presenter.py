import json
from unittest.mock import MagicMock
from src.modules.resend_code.app.resend_code_presenter import lambda_handler
from src.modules.resend_code.app import resend_code_presenter

class Test_ResendCodePresenter:
    def test_resend_code_presenter_success(self):
        resend_code_presenter.usecase.cognito = MagicMock()
        resend_code_presenter.usecase.cognito.resend_confirmation_code.return_value = {}

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "body": json.dumps({
                "email": "21.00458-7@maua.br"
            })
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["message"] == "Código reenviado com sucesso!"
