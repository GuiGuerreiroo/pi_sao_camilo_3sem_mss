from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Guilherme',
                'email': '25.00178-5@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440002',
                'custom:role': 'USER'
            },
            'new_name': 'Guilherme Atualizado'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user']['name'] == 'Guilherme Atualizado'
        assert response.body['message'] == "the user was updated successfully"

    def test_update_user_controller_missing_requester_user(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'new_name': 'Branco do Branco Branco da Silva'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field requester_user is missing"

    def test_update_user_controller_invalid_new_name(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Guilherme',
                'email': '25.00178-5@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440002',
                'custom:role': 'USER'
            },
            'new_name': 123
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_name isn't in the right type.\n Received: <class 'int'>.\n Expected: str"

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Nobody',
                'email': 'nobody@maua.br',
                'sub': 'non-existent',
                'custom:role': 'USER'
            },
            'new_name': 'Ghost'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for user_id'
