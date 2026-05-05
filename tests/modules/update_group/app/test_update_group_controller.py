from src.modules.update_group.app.update_group_controller import UpdateGroupController
from src.modules.update_group.app.update_group_usecase import UpdateGroupUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_UpdateGroupController:
    def test_update_group_controller(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = UpdateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            },
            'group_id': '660e8400-e29b-41d4-a716-446655440001',
            'new_athlete_list_id': ['cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a'],
            'new_supporter_list_id': ['e0cce9ad-e3ec-41f0-8600-812198c49450']
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['message'] == 'Group was updated successfully'
        assert response.body['group']['group_id'] == '660e8400-e29b-41d4-a716-446655440001'

    def test_update_group_controller_missing_group_id(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = UpdateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            },
            'new_athlete_list_id': ['cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a']
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field group_id is missing'

    def test_update_group_controller_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = UpdateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'USER' # USER cannot update group
            },
            'group_id': '660e8400-e29b-41d4-a716-446655440001',
            'new_athlete_list_id': ['cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a']
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this user'

    def test_update_group_controller_missing_both_lists(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = UpdateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            },
            'group_id': '660e8400-e29b-41d4-a716-446655440001'
            # both new_athlete_list_id and new_supporter_list_id are missing
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field new_athlete_list_id or new_supporter_list_id must be provided (at least one) is missing'

    def test_update_group_controller_empty_list(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = UpdateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': 'e0cce9ad-e3ec-41f0-8600-812198c49450',
                'custom:role': 'ADM'
            },
            'group_id': '660e8400-e29b-41d4-a716-446655440001',
            'new_athlete_list_id': []
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field new_athlete_list_id is empty. new_athlete_list_id should not be empty'
