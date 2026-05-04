import pytest
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetAllUsersUsecase:

    def test_get_all_users_usecase(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo=repo)
        
        users = usecase()
        
        assert type(users) == list
        assert len(users) == 5
        assert users[0].name == "Guilherme"
