from src.modules.get_all_trainings.app.get_all_trainings_controller import GetAllTrainingsController
from src.modules.get_all_trainings.app.get_all_trainings_usecase import GetAllTrainingsUseCase
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_GetAllTrainingsController:
    def test_get_all_trainings_controller(self):
        repo = TrainingRepositoryMock()
        usecase = GetAllTrainingsUseCase(repo=repo)
        controller = GetAllTrainingsController(usecase=usecase)

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
        assert type(response.body['trainings']) == list
        assert len(response.body['trainings']) > 0
        assert response.body['message'] == 'Trainings returned successfully'

    def test_get_all_trainings_controller_missing_requester_user(self):
        repo = TrainingRepositoryMock()
        usecase = GetAllTrainingsUseCase(repo=repo)
        controller = GetAllTrainingsController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field requester_user is missing"

    def test_get_all_trainings_controller_forbidden_role(self):
        repo = TrainingRepositoryMock()
        usecase = GetAllTrainingsUseCase(repo=repo)
        controller = GetAllTrainingsController(usecase=usecase)

        request = HttpRequest(body={
            'requester_user': {
                'name': 'João',
                'email': '21.00678-2@maua.br',
                'sub': '550e8400-e29b-41d4-a716-446655440001',
                'custom:role': 'ADM'
            }
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"
