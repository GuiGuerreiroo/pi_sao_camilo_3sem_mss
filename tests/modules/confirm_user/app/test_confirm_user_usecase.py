import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from src.modules.confirm_user.app.confirm_user_usecase import ConfirmUserUseCase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.status_user_enum import USERSTATUS

class Test_ConfirmUserUseCase:
    def test_confirm_user_success(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.confirm_sign_up.return_value = {}

        # The user '21.00458-7@maua.br' (Bruno) starts as UNCONFIRMED in the mock
        email = "21.00458-7@maua.br"
        
        confirmed_user = usecase(email=email, code="123456")
        
        assert confirmed_user.status == USERSTATUS.CONFIRMED
        assert confirmed_user.expires_at is None
        
        usecase.cognito.confirm_sign_up.assert_called_once_with(
            ClientId=usecase.client_id,
            Username=email,
            ConfirmationCode="123456"
        )

    def test_confirm_user_not_found_in_db(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.confirm_sign_up.return_value = {}

        # The user does not exist in the DB, though Cognito says it worked
        email = "non-existent@test.com"
        
        with pytest.raises(NoItemsFound):
            usecase(email=email, code="123456")

    def test_confirm_user_client_error(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('CodeMismatchException', (ClientError,), {})
        usecase.cognito.confirm_sign_up.side_effect = ExceptionClass(
            error_response={'Error': {'Code': 'CodeMismatchException', 'Message': 'Invalid code'}},
            operation_name='ConfirmSignUp'
        )

        with pytest.raises(ClientError):
            usecase(email="21.00458-7@maua.br", code="wrong_code")
