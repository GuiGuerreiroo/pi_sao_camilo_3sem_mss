import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from src.modules.forgot_password.app.forgot_password_usecase import ForgotPasswordUseCase
from src.shared.helpers.errors.usecase_errors import UserExpiredError, UserNeedsConfirmationError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_ForgotPasswordUseCase:
    def test_forgot_password_success(self):
        repo = UserRepositoryMock()
        usecase = ForgotPasswordUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.forgot_password.return_value = {}

        # The user '25.00178-5@maua.br' (Guilherme) is CONFIRMED in the mock
        email = "25.00178-5@maua.br"
        
        response = usecase(email=email)
        
        assert response is True
        
        usecase.cognito.forgot_password.assert_called_once_with(
            ClientId=usecase.client_id,
            Username=email
        )

    def test_forgot_password_unconfirmed_user(self):
        repo = UserRepositoryMock()
        usecase = ForgotPasswordUseCase(repo=repo)
        
        usecase.cognito = MagicMock()

        # The user '21.00458-7@maua.br' is UNCONFIRMED in the mock
        email = "21.00458-7@maua.br"
        
        with pytest.raises(UserNeedsConfirmationError):
            usecase(email=email)

    def test_forgot_password_client_error(self):
        repo = UserRepositoryMock()
        usecase = ForgotPasswordUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('LimitExceededException', (ClientError,), {})
        usecase.cognito.forgot_password.side_effect = ExceptionClass(
            error_response={'Error': {'Code': 'LimitExceededException', 'Message': 'Attempt limit exceeded'}},
            operation_name='ForgotPassword'
        )

        with pytest.raises(ClientError):
            usecase(email="25.00178-5@maua.br")
