import pytest
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        user = usecase(user_id="550e8400-e29b-41d4-a716-446655440002", new_name="Guilherme Alterado")

        assert user.name == "Guilherme Alterado"

    def test_update_user_usecase_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="invalid")
