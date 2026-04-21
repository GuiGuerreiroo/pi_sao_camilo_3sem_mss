from unittest.mock import MagicMock
from src.modules.auth_user.app.auth_user_controller import AuthUserController
from src.modules.auth_user.app.auth_user_usecase import AuthUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from botocore.exceptions import ClientError

class Test_AuthUserController:
    def test_auth_user_controller_success(self):
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

        controller = AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'test@test.com',
            'password': 'Password123!'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["id_token"] == "mock_id_token"

    def test_auth_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUseCase(repo=repo)
        controller = AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'password': 'Password123!'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_auth_user_controller_invalid_password_type(self):
        repo = UserRepositoryMock()
        usecase = AuthUserUseCase(repo=repo)
        controller = AuthUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'test@test.com',
            'password': 123456
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field password isn't in the right type" in response.body
