from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserController:

    def test_get_user_controller(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': repo.users[1].user_id,
                'name': repo.users[1].name,
                'email': repo.users[1].email,
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user']['user_id'] == repo.users[1].user_id
        assert response.body['user']['name'] == repo.users[1].name
        assert response.body['user']['email'] == repo.users[1].email
        assert response.body['message'] == 'User successfully returned'

    def test_get_user_controller_missing_requester_user(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field requester_user is missing'

    def test_get_user_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo)
        controller = GetUserController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'sub': '00000000-0000-0000-0000-000000000000',
                'name': 'NonExistent',
                'email': 'none@none.com',
            }
        })

        response = controller(request=request)

        # The usecase returns None, so user.model_dump() raises AttributeError
        # which is caught by the generic Exception handler → 500
        assert response.status_code == 500
