import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from pydantic import ValidationError

from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import uuid

class Test_CreateUserUsecase:

    def test_create_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.sign_up.return_value = {
            'UserSub': str(uuid.uuid4())
        }

        user = usecase(
            name="Vitor Choueri", 
            email="branco@branco.branco",
            password="Password123!",
            role=ROLE.USER,
            height=1.80
        )

        assert repo.users[-1] == user
        assert user.name == "Vitor Choueri"
        assert user.email == "branco@branco.branco"
        assert user.role == ROLE.USER
        usecase.cognito.sign_up.assert_called_once()

    def test_create_user_invalid_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        usecase.cognito.sign_up.return_value = {
            'UserSub': str(uuid.uuid4())
        }

        with pytest.raises(ValidationError):
            usecase(
                name="V", 
                email="branco@branco.branco",
                password="Password123!",
                role=ROLE.USER,
                height=1.80
            )

    def test_create_user_duplicated_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo=repo)
        
        usecase.cognito = MagicMock()
        ExceptionClass = type('UsernameExistsException', (Exception,), {})
        usecase.cognito.exceptions.UsernameExistsException = ExceptionClass
        usecase.cognito.sign_up.side_effect = ExceptionClass("User already exists")
        
        usecase.cognito.admin_get_user.return_value = {
            'UserStatus': 'CONFIRMED'
        }

        with pytest.raises(DuplicatedItem):
            usecase(
                name="Vitor Choueri", 
                email="branco@branco.branco",
                password="Password123!",
                role=ROLE.USER,
                height=1.80
            )