from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class Test_GetAllUsersController:

    def test_get_all_users_controller(self):
        repo_mock = UserRepositoryMock()
        get_all_users_usecase = GetAllUsersUsecase(repo_mock)
        controller = GetAllUsersController(get_all_users_usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': '21.00678-2@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            }
        })

        response = controller(request)

        assert response.status_code == 200

    def test_get_all_users_controller_forbidden(self):
        repo_mock = UserRepositoryMock()
        get_all_users_usecase = GetAllUsersUsecase(repo_mock)
        controller = GetAllUsersController(get_all_users_usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Guilherme',
                'email': '25.00178-5@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440002',
                'custom:role': 'USER'
            }
        })

        response = controller(request)

        assert response.status_code == 403
