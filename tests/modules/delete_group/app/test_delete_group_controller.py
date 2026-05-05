from src.modules.delete_group.app.delete_group_controller import DeleteGroupController
from src.modules.delete_group.app.delete_group_usecase import DeleteGroupUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_DeleteGroupController:
    def test_delete_group_controller(self):
        repo = GroupRepositoryMock()
        usecase = DeleteGroupUseCase(repo=repo)
        controller = DeleteGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': 'e0cce9ad-e3ec-41f0-8600-812198c49450',
                'custom:role': 'ADM'
            },
            'group_id': '660e8400-e29b-41d4-a716-446655440001'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['message'] == 'Group was deleted successfully'
        assert response.body['group']['group_id'] == '660e8400-e29b-41d4-a716-446655440001'

    def test_delete_group_controller_missing_group_id(self):
        repo = GroupRepositoryMock()
        usecase = DeleteGroupUseCase(repo=repo)
        controller = DeleteGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': 'e0cce9ad-e3ec-41f0-8600-812198c49450',
                'custom:role': 'ADM'
            }
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field group_id is missing'

    def test_delete_group_controller_forbidden(self):
        repo = GroupRepositoryMock()
        usecase = DeleteGroupUseCase(repo=repo)
        controller = DeleteGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'USER' # USER cannot delete group
            },
            'group_id': '660e8400-e29b-41d4-a716-446655440001'
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this user'
