from unittest.mock import MagicMock
from src.modules.refresh_token.app.refresh_token_controller import RefreshTokenController
from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from botocore.exceptions import ClientError

class Test_RefreshTokenController:
    def test_refresh_token_controller_success(self):
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

        controller = RefreshTokenController(usecase=usecase)

        request = HttpRequest(body={
            'refresh_token': 'mock_refresh_token'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["id_token"] == "mock_id_token"

    def test_refresh_token_controller_missing_token(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUseCase(repo=repo)
        controller = RefreshTokenController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field refresh_token is missing"

    def test_refresh_token_controller_invalid_token_type(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUseCase(repo=repo)
        controller = RefreshTokenController(usecase=usecase)

        request = HttpRequest(body={
            'refresh_token': 123456
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field refresh_token isn't in the right type" in response.body

    def test_refresh_token_controller_client_error(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('NotAuthorizedException', (ClientError,), {})
        usecase.cognito.initiate_auth.side_effect = ExceptionClass(
            error_response={'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid token'}},
            operation_name='InitiateAuth'
        )

        controller = RefreshTokenController(usecase=usecase)

        request = HttpRequest(body={
            'refresh_token': 'invalid_token'
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body['message'] == 'Token de atualização inválido ou expirado'
