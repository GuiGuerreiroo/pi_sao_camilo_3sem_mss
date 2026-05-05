from src.modules.create_group.app.create_group_controller import CreateGroupController
from src.modules.create_group.app.create_group_usecase import CreateGroupUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_CreateGroupController:
    def test_create_group_controller(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = CreateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            },
            'athletes_list_id': ['cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a'],
            'supporter_list_id': ['e0cce9ad-e3ec-41f0-8600-812198c49450']
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['message'] == 'Group created successfully'
        assert response.body['group']['group_id'] is not None
        assert response.body['group']['athletes_list_id'][0]['user_id'] == 'cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a'
        assert response.body['group']['supporter_list_id'][0]['user_id'] == 'e0cce9ad-e3ec-41f0-8600-812198c49450'

    def test_create_group_controller_missing_athletes(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = CreateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            },
            'supporter_list_id': ['e0cce9ad-e3ec-41f0-8600-812198c49450']
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field athletes_list_id is missing'

    def test_create_group_controller_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = CreateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': 'cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a',
                'custom:role': 'USER' # USER cannot create group
            },
            'athletes_list_id': ['cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a'],
            'supporter_list_id': ['e0cce9ad-e3ec-41f0-8600-812198c49450']
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this user'

    def test_create_group_controller_empty_list(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        controller = CreateGroupController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            },
            'athletes_list_id': [],
            'supporter_list_id': ['e0cce9ad-e3ec-41f0-8600-812198c49450']
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field athletes_list_id is empty. athletes_list_id should not be empty'
