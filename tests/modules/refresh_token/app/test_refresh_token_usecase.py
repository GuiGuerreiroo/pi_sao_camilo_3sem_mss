from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUseCase
import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_RefreshTokenUsecase:
    def test_refresh_token_success(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "IdToken": "mock_id_token",
                "AccessToken": "mock_access_token",
                "RefreshToken": "mock_refresh_token_new",
                "ExpiresIn": 3600,
                "TokenType": "Bearer"
            }
        }

        result = usecase(refresh_token="mock_refresh_token")

        assert result["id_token"] == "mock_id_token"
        assert result["access_token"] == "mock_access_token"
        assert result["refresh_token"] == "mock_refresh_token_new"
        usecase.cognito.initiate_auth.assert_called_once_with(
            ClientId=usecase.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": "mock_refresh_token"
            }
        )
        
    def test_refresh_token_challenge(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.initiate_auth.return_value = {
            "ChallengeName": "NEW_PASSWORD_REQUIRED",
            "Session": "mock_session"
        }

        result = usecase(refresh_token="mock_refresh_token")

        assert result["challenge_name"] == "NEW_PASSWORD_REQUIRED"
        assert result["session"] == "mock_session"

    def test_refresh_token_client_error(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('NotAuthorizedException', (ClientError,), {})
        usecase.cognito.initiate_auth.side_effect = ExceptionClass(
            error_response={'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid Refresh Token'}},
            operation_name='InitiateAuth'
        )

        with pytest.raises(ClientError):
            usecase(refresh_token="invalid_refresh_token")
