import uuid

import pytest

from src.modules.create_user_cognito.app import create_user_cognito_usecase as create_user_cognito_usecase_module
from src.modules.create_user_cognito.app.create_user_cognito_usecase import CreateUserCognitoUseCase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class FakeUser:
    def __init__(self, user_id: str, name: str, role: ROLE, height: float | None = None):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.height = height


class Test_CreateUserCognitoUsecase:
    def test_create_user_cognito_duplicated_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserCognitoUseCase(repo=repo)

        duplicated_email = repo.users[0].email

        with pytest.raises(DuplicatedItem):
            usecase(
                user_id=str(uuid.uuid4()),
                email=duplicated_email,
                name="Other User",
                role=ROLE.USER,
                height=1.75
            )

    def test_create_user_cognito_support_success(self, monkeypatch):
        repo = UserRepositoryMock()
        usecase = CreateUserCognitoUseCase(repo=repo)

        monkeypatch.setattr(create_user_cognito_usecase_module, "User", FakeUser)

        usecase(
            user_id=str(uuid.uuid4()),
            email="new.support@maua.br",
            name="Support User",
            role=ROLE.SUPPORT
        )

        assert repo.users[-1].name == "Support User"
        assert repo.users[-1].role == ROLE.SUPPORT
