from unittest.mock import MagicMock
from src.modules.confirm_user.app.confirm_user_controller import ConfirmUserController
from src.modules.confirm_user.app.confirm_user_usecase import ConfirmUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from botocore.exceptions import ClientError
from src.shared.domain.enums.status_user_enum import USERSTATUS
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class Test_ConfirmUserController:
    def test_confirm_user_controller_success(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.confirm_sign_up.return_value = {}

        controller = ConfirmUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': '21.00458-7@maua.br',
            'code': '123456'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['message'] == 'Conta ativada com sucesso!'
        assert response.body['user']['status'] == USERSTATUS.CONFIRMED.value
        assert 'expires_at' not in response.body['user']

    def test_confirm_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        controller = ConfirmUserController(usecase=usecase)

        request = HttpRequest(body={
            'code': '123456'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"
        
    def test_confirm_user_controller_missing_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        controller = ConfirmUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': '21.00458-7@maua.br'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field code is missing"

    def test_confirm_user_controller_invalid_code_type(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        controller = ConfirmUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': '21.00458-7@maua.br',
            'code': 123456
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field code isn't in the right type" in response.body

    def test_confirm_user_controller_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = MagicMock()
        usecase.side_effect = NoItemsFound("email")

        controller = ConfirmUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'non-existent@test.com',
            'code': '123456'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for email"

    def test_confirm_user_controller_client_error_mismatch(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('CodeMismatchException', (ClientError,), {})
        usecase.cognito.confirm_sign_up.side_effect = ExceptionClass(
            error_response={'Error': {'Code': 'CodeMismatchException', 'Message': 'Invalid code'}},
            operation_name='ConfirmSignUp'
        )

        controller = ConfirmUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': '21.00458-7@maua.br',
            'code': 'wrong_code'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Código de verificação incorreto.'
