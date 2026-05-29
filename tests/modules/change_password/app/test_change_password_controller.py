import pytest
from unittest.mock import MagicMock
from src.modules.change_password.app.change_password_controller import ChangePasswordController
from src.shared.helpers.errors.usecase_errors import (
    CodeMismatchError,
    ExpiredCodeError,
    InvalidPasswordError,
    NoItemsFound
)

class MockRequest:
    def __init__(self, data):
        self.data = data

class Test_ChangePasswordController:
    def test_change_password_controller_success(self):
        usecase = MagicMock()
        usecase.return_value = True
        controller = ChangePasswordController(usecase=usecase)
        
        request = MockRequest(data={
            "email": "test@maua.br",
            "code": "123456",
            "new_password": "NewPassword123!"
        })
        
        response = controller(request)
        
        assert response.status_code == 200
        assert response.body["message"] == "Senha alterada com sucesso!"
        usecase.assert_called_once_with(email="test@maua.br", code="123456", new_password="NewPassword123!")

    def test_change_password_controller_missing_email(self):
        usecase = MagicMock()
        controller = ChangePasswordController(usecase=usecase)
        
        request = MockRequest(data={
            "code": "123456",
            "new_password": "NewPassword123!"
        })
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_change_password_controller_code_mismatch(self):
        usecase = MagicMock()
        usecase.side_effect = CodeMismatchError()
        controller = ChangePasswordController(usecase=usecase)
        
        request = MockRequest(data={
            "email": "test@maua.br",
            "code": "123456",
            "new_password": "NewPassword123!"
        })
        
        response = controller(request)
        
        assert response.status_code == 400
        assert response.body == "Invalid verification code provided, please try again."

    def test_change_password_controller_user_not_found(self):
        usecase = MagicMock()
        usecase.side_effect = NoItemsFound("email")
        controller = ChangePasswordController(usecase=usecase)
        
        request = MockRequest(data={
            "email": "test@maua.br",
            "code": "123456",
            "new_password": "NewPassword123!"
        })
        
        response = controller(request)
        
        assert response.status_code == 404
        assert response.body == "No items found for email"
