import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from src.modules.resend_code.app.resend_code_usecase import ResendCodeUseCase
from src.shared.helpers.errors.usecase_errors import UserExpiredError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.status_user_enum import USERSTATUS

class Test_ResendCodeUseCase:

    def test_resend_code_success(self):
        repo = UserRepositoryMock()
        usecase = ResendCodeUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.resend_confirmation_code.return_value = {}

        # Bruno is UNCONFIRMED in the mock DB
        email = "21.00458-7@maua.br"
        
        result = usecase(email=email)
        
        assert result is True
        usecase.cognito.resend_confirmation_code.assert_called_once_with(
            ClientId=usecase.client_id,
            Username=email
        )

    def test_resend_code_user_expired(self):
        repo = UserRepositoryMock()
        usecase = ResendCodeUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.admin_delete_user.return_value = {}

        # User is not in DB (simulating TTL deletion)
        email = "deleted@test.com"
        
        with pytest.raises(UserExpiredError):
            usecase(email=email)
            
        usecase.cognito.admin_delete_user.assert_called_once_with(
            UserPoolId=usecase.user_pool_id,
            Username=email
        )

    def test_resend_code_user_already_confirmed(self):
        from src.shared.helpers.errors.usecase_errors import UserAlreadyConfirmedError
        repo = UserRepositoryMock()
        usecase = ResendCodeUseCase(repo=repo)
        
        usecase.cognito = MagicMock()

        # Guilherme is CONFIRMED in the mock DB
        email = "25.00178-5@maua.br"
        
        with pytest.raises(UserAlreadyConfirmedError):
            usecase(email=email)
            
        usecase.cognito.resend_confirmation_code.assert_not_called()
