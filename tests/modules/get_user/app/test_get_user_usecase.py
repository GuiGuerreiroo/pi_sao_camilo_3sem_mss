from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserUsecase:

    def test_get_user(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        user = usecase(user_id=repo.users[1].user_id)

        assert user == repo.users[1]
        assert user.name == "João"
        assert user.email == "21.00678-2@maua.br"

    def test_get_user_with_different_user(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        user = usecase(user_id=repo.users[0].user_id)

        assert user == repo.users[0]
        assert user.name == "Guilherme"

    def test_get_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        user = usecase(user_id="00000000-0000-0000-0000-000000000000")

        assert user is None
