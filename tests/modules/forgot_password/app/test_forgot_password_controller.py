import pytest
from unittest.mock import MagicMock
from src.modules.forgot_password.app.forgot_password_controller import ForgotPasswordController
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.errors.usecase_errors import UserExpiredError, UserNeedsConfirmationError

class Test_ForgotPasswordController:
    def test_forgot_password_controller_success(self):
        usecase = MagicMock()
        usecase.return_value = True
        
        controller = ForgotPasswordController(usecase=usecase)
        
        request = HttpRequest(body={"email": "25.00178-5@maua.br"})
        
        response = controller(request)
        
        assert response.status_code == 200
        assert response.body['message'] == 'Código de recuperação de senha enviado para o email com sucesso!'
        usecase.assert_called_once_with(email="25.00178-5@maua.br")

    def test_forgot_password_controller_missing_email(self):
        usecase = MagicMock()
        controller = ForgotPasswordController(usecase=usecase)
        
        request = HttpRequest(body={})
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_forgot_password_controller_wrong_type_email(self):
        usecase = MagicMock()
        controller = ForgotPasswordController(usecase=usecase)
        
        request = HttpRequest(body={"email": 123})
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "Field email isn't in the right type.\n Received: <class 'int'>.\n Expected: str"

    def test_forgot_password_controller_user_needs_confirmation(self):
        usecase = MagicMock()
        usecase.side_effect = UserNeedsConfirmationError()
        
        controller = ForgotPasswordController(usecase=usecase)
        
        request = HttpRequest(body={"email": "unconfirmed@test.com"})
        
        response = controller(request)
        
        assert response.status_code == 403
        assert response.body == "O usuário precisa ser confirmado."
