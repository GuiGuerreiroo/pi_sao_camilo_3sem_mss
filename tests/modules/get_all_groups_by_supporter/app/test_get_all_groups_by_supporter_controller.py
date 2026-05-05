from src.modules.get_all_groups_by_supporter.app.get_all_groups_by_supporter_controller import GetAllGroupsBySupporterController
from src.modules.get_all_groups_by_supporter.app.get_all_groups_by_supporter_usecase import GetAllGroupsBySupporterUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_GetAllGroupsBySupporterController:
    def test_get_all_groups_by_supporter_controller(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        training_repo = TrainingRepositoryMock()
        usecase = GetAllGroupsBySupporterUseCase(repo=repo, user_repo=user_repo, training_repo=training_repo)
        controller = GetAllGroupsBySupporterController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'Pedro',
                'email': 'pedro@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440002', # Guilherme's ID
                'custom:role': 'SUPPORT' # Valid role for controller
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['message'] == 'Trainings andathletes linked to the supporter retrieved successfully'
        assert len(response.body['groups']) == 2
        
        # Verify first group data
        group = response.body['groups'][0]
        assert group['group_id'] == '660e8400-e29b-41d4-a716-446655440001'
        assert group['athletes_list'][0]['user_id'] == '550e8400-e29b-41d4-a716-446655440001'
        assert 'trainings' in group['athletes_list'][0]

    def test_get_all_groups_by_supporter_controller_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        training_repo = TrainingRepositoryMock()
        usecase = GetAllGroupsBySupporterUseCase(repo=repo, user_repo=user_repo, training_repo=training_repo)
        controller = GetAllGroupsBySupporterController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': 'joao@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'USER' # USER cannot access this
            }
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this user'
