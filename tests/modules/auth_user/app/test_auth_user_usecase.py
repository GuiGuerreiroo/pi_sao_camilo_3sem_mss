from src.modules.auth_user.app.auth_user_usecase import AuthUserUseCase
import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_AuthUserUsecase:
    def test_auth_user_success(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "IdToken": "mock_id_token",
                "AccessToken": "mock_access_token",
                "RefreshToken": "mock_refresh_token",
                "ExpiresIn": 3600,
                "TokenType": "Bearer"
            }
        }

        result = usecase(email="test@test.com", password="Password123!")

        assert result["id_token"] == "mock_id_token"
        assert result["access_token"] == "mock_access_token"
        assert result["refresh_token"] == "mock_refresh_token"
        usecase.cognito.initiate_auth.assert_called_once()
        
    def test_auth_user_challenge(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.initiate_auth.return_value = {
            "ChallengeName": "NEW_PASSWORD_REQUIRED",
            "Session": "mock_session"
        }

        result = usecase(email="test@test.com", password="Password123!")

        assert result["challenge_name"] == "NEW_PASSWORD_REQUIRED"
        assert result["session"] == "mock_session"

    def test_auth_user_client_error(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('NotAuthorizedException', (ClientError,), {})
        usecase.cognito.initiate_auth.side_effect = ExceptionClass(
            error_response={'Error': {'Code': 'NotAuthorizedException', 'Message': 'Incorrect username or password.'}},
            operation_name='InitiateAuth'
        )

        with pytest.raises(ClientError):
            usecase(email="test@test.com", password="WrongPassword!")
