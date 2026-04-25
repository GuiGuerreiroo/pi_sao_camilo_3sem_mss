from unittest.mock import MagicMock
from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.role_enum import ROLE
import uuid

class Test_CreateUserControler:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.sign_up.return_value = {
            'UserSub': str(uuid.uuid4())
        }

        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': 'branco@branco.com',
            'name': 'Branco do Branco Branco da Silva',
            'password': 'Password123!',
            'role': 'USER',
            'height': 1.85
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['user']['name'] == repo.users[-1].name
        assert response.body['user']['email'] == repo.users[-1].email
        assert response.body['user']['role'] == ROLE.USER.value
        assert response.body['message'] == "User successfully created"

    def test_create_user_controller_missing_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': '21.01444-2@maua.br',
            'password': 'Password123!',
            'role': 'USER'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field name is missing"

    def test_create_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'name': 'Branco do Branco Branco da Silva',
            'password': 'Password123!',
            'role': 'USER'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_create_user_controller_invalid_role(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': 'branco@branco.com',
            'name': 'Branco',
            'password': 'Password123!',
            'role': 'INVALID_ROLE'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field role isn't in the right type" in response.body

    def test_create_user_controller_pydantic_validation_error_not_caught(self):
        # Depending on how the error is handled, this could result in 500 or 400
        # Right now the controller handles EntityError but Pydantic throws ValidationError.
        # This test ensures we capture what the controller currently returns for a too-short name: 500.
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.sign_up.return_value = {
            'UserSub': str(uuid.uuid4())
        }

        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': 'branco@branco.com',
            'name': 'B',  # Name < 2 chars throws ValidationError
            'password': 'Password123!',
            'role': 'USER',
            'height': 1.80
        })

        response = controller(request=request)

        # Right now the application returns InternalServerError (500) for ValidationError
        assert response.status_code == 500

    def test_create_user_controller_invalid_password_type(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': 'branco@branco.com',
            'name': 'Branco',
            'password': 123456,
            'role': 'USER',
            'height': 1.80
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field password isn't in the right type" in response.body

    def test_create_user_controller_duplicated_email(self):
        repo = UserRepositoryMock()
        usecase = MagicMock()
        from src.shared.helpers.errors.usecase_errors import DuplicatedItem
        usecase.side_effect = DuplicatedItem("branco@branco.com")

        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': 'branco@branco.com',
            'name': 'Branco do Branco Branco da Silva',
            'password': 'Password123!',
            'role': 'USER',
            'height': 1.80
        })

        response = controller(request=request)

        assert response.status_code == 409
        assert response.body == "The item alredy exists for this branco@branco.com"

    def test_create_user_controller_unconfirmed_user(self):
        repo = UserRepositoryMock()
        usecase = MagicMock()
        from src.shared.helpers.errors.usecase_errors import UnconfirmedUserError
        usecase.side_effect = UnconfirmedUserError("branco@branco.com")

        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': 'some-admin-id',
            'email': 'branco@branco.com',
            'name': 'Branco do Branco Branco da Silva',
            'password': 'Password123!',
            'role': 'USER',
            'height': 1.80
        })

        response = controller(request=request)

        assert response.status_code == 409
        assert response.body == "The user branco@branco.com is unconfirmed. A new verification code was sent."
