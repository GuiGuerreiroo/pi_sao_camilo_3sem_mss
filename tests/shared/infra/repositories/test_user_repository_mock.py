from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:
    def test_get_user(self):
        repo = UserRepositoryMock()
        user = repo.get_user("550e8400-e29b-41d4-a716-446655440001")

        assert user is not None
        assert user.name == "João"
        assert user.email == "21.00678-2@maua.br"
        assert user.user_id == "550e8400-e29b-41d4-a716-446655440001"
        assert user.role == ROLE.ADM

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        user = repo.get_user("non-existent-id")
        assert user is None

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(
            name="Vitor",
            email="dohype@vitin.com",
            role=ROLE.USER,
            height=1.8,
        )

        initial_size = len(repo.users)
        repo.create_user(user)

        assert len(repo.users) == initial_size + 1
        assert repo.users[-1].name == "Vitor"
        assert repo.users[-1].email == "dohype@vitin.com"
        assert repo.users[-1].role == ROLE.USER
        assert repo.users[-1].height == 1.8

    def test_delete_user(self):
        repo = UserRepositoryMock()
        user = repo.delete_user("550e8400-e29b-41d4-a716-446655440001")
        assert user is not None
        assert user.name == "João"
        assert user.email == "21.00678-2@maua.br"
        assert user.user_id == "550e8400-e29b-41d4-a716-446655440001"
        assert user.role == ROLE.ADM

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        user = repo.delete_user("non-existent-id")
        assert user is None

    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user(
            user_id="550e8400-e29b-41d4-a716-446655440001",
            name="Joao Guirao",
            new_email="joao.guirao@maua.br",
            new_role=ROLE.SUPPORT,
            new_height=1.75,
        )

        assert user is not None
        assert user.name == "Joao Guirao"
        assert user.email == "joao.guirao@maua.br"
        assert user.role == ROLE.SUPPORT
        assert user.height == 1.75

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        user = repo.update_user("non-existent-id", "Bruno Guirao", None, None, None)
        assert user is None

    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email("21.00458-7@maua.br")

        assert user is not None
        assert user.name == "Bruno"

