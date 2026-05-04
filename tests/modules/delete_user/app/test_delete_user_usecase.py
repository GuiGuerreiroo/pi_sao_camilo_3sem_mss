import pytest
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:
    def test_delete_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)

        user = usecase(user_id="550e8400-e29b-41d4-a716-446655440002")

        assert user.name == "Guilherme"

    def test_delete_user_usecase_invalid_id(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="invalid")
