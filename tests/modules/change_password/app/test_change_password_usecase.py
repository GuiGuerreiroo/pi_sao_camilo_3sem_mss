import pytest
from unittest.mock import MagicMock
from src.modules.change_password.app.change_password_usecase import ChangePasswordUseCase
from src.shared.helpers.errors.usecase_errors import (
    CodeMismatchError,
    ExpiredCodeError,
    InvalidPasswordError,
    NoItemsFound
)

def setup_mock_cognito(usecase):
    usecase.cognito = MagicMock()
    usecase.cognito.exceptions.CodeMismatchException = type('CodeMismatchException', (Exception,), {})
    usecase.cognito.exceptions.ExpiredCodeException = type('ExpiredCodeException', (Exception,), {})
    usecase.cognito.exceptions.InvalidPasswordException = type('InvalidPasswordException', (Exception,), {})
    usecase.cognito.exceptions.UserNotFoundException = type('UserNotFoundException', (Exception,), {})

class Test_ChangePasswordUseCase:
    def test_change_password_success(self):
        usecase = ChangePasswordUseCase()
        setup_mock_cognito(usecase)
        usecase.cognito.confirm_forgot_password.return_value = {}

        result = usecase(email="test@maua.br", code="123456", new_password="NewPassword123!")

        assert result is True
        usecase.cognito.confirm_forgot_password.assert_called_once_with(
            ClientId=usecase.client_id,
            Username="test@maua.br",
            ConfirmationCode="123456",
            Password="NewPassword123!"
        )

    def test_change_password_code_mismatch(self):
        usecase = ChangePasswordUseCase()
        setup_mock_cognito(usecase)
        
        usecase.cognito.confirm_forgot_password.side_effect = usecase.cognito.exceptions.CodeMismatchException()

        with pytest.raises(CodeMismatchError):
            usecase(email="test@maua.br", code="123456", new_password="NewPassword123!")

    def test_change_password_expired_code(self):
        usecase = ChangePasswordUseCase()
        setup_mock_cognito(usecase)
        
        usecase.cognito.confirm_forgot_password.side_effect = usecase.cognito.exceptions.ExpiredCodeException()

        with pytest.raises(ExpiredCodeError):
            usecase(email="test@maua.br", code="123456", new_password="NewPassword123!")

    def test_change_password_invalid_password(self):
        usecase = ChangePasswordUseCase()
        setup_mock_cognito(usecase)
        
        usecase.cognito.confirm_forgot_password.side_effect = usecase.cognito.exceptions.InvalidPasswordException()

        with pytest.raises(InvalidPasswordError):
            usecase(email="test@maua.br", code="123456", new_password="NewPassword123!")

    def test_change_password_user_not_found(self):
        usecase = ChangePasswordUseCase()
        setup_mock_cognito(usecase)
        
        usecase.cognito.confirm_forgot_password.side_effect = usecase.cognito.exceptions.UserNotFoundException()

        with pytest.raises(NoItemsFound):
            usecase(email="test@maua.br", code="123456", new_password="NewPassword123!")
