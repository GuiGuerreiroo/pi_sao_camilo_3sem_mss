from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserController:
    def test_delete_user_controller(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Guilherme',
                'email': '25.00178-5@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440002',
                'custom:role': 'USER'
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user']['name'] == 'Guilherme'
        assert response.body['message'] == "User was deleted successfully"

    def test_delete_user_controller_missing_requester_user(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field requester_user is missing"

    def test_delete_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Nobody',
                'email': 'nobody@maua.br',
                'sub': 'non-existent',
                'custom:role': 'USER'
            }
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for user'
