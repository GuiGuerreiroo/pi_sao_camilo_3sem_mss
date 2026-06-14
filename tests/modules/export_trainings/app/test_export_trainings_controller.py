import json
from src.modules.export_trainings.app.export_trainings_controller import ExportTrainingsController
from src.modules.export_trainings.app.export_trainings_usecase import ExportTrainingsUseCase
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_ExportTrainingsController:
    def test_export_trainings_controller(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        
        # Inject mock training for athlete
        from src.shared.domain.entities.training import Training
        from src.shared.domain.enums.modality import MODALITY
        from src.shared.domain.enums.usrine_color import URINE_COLOR
        from src.shared.domain.enums.symptoms import SYMPTOMS

        repo_t.trainings.append(
            Training(
                training_id="660e8400-e29b-41d4-a716-446655440005",
                user_id="550e8400-e29b-41d4-a716-446655440001",
                modality=MODALITY.CORRIDA,
                start_date=1630000000000,
                end_date=1630003600000,
                duration=3600,
                environment_temperature=25.5,
                environment_humidity=60.0,
                urine_color=URINE_COLOR.AMARELO,
                pre_training_symptoms=[SYMPTOMS.NONE],
                pre_training_weight=70.0,
                pre_training_hydration=500.0,
                during_training_hydration=200.0,
                during_training_urine_elimination=0.0,
                post_training_symptoms=[SYMPTOMS.NONE],
                post_training_weight=69.5,
                soaked_clothes=True,
                training_intensity=7,
                weight_difference=0.5,
                ajusted_weight_difference=0.7,
                sudorese=0.7,
                weight_variation_percentage=0.71,
                ai_suggestion="Great training!"
            )
        )

        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        controller = ExportTrainingsController(usecase=usecase)

        request = HttpRequest(body={
            'athlete_id': '550e8400-e29b-41d4-a716-446655440001',
            'training_id_list': ['660e8400-e29b-41d4-a716-446655440005']
        })
        request.data['requester_user'] = {
            'name': 'Guilherme Supporter',
            'email': 'supporter@maua.br',
            'sub': '550e8400-e29b-41d4-a716-446655440002',
            'custom:role': 'SUPPORT'
        }

        response = controller(request=request)

        assert response.status_code == 200
        assert type(response.body) == str
        assert response.headers['Content-Type'] == 'application/pdf'

    def test_export_trainings_controller_missing_requester_user(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        controller = ExportTrainingsController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field requester_user is missing"

    def test_export_trainings_controller_forbidden_role(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        controller = ExportTrainingsController(usecase=usecase)

        request = HttpRequest(body={
            'athlete_id': '550e8400-e29b-41d4-a716-446655440001',
            'training_id_list': ['660e8400-e29b-41d4-a716-446655440005']
        })
        request.data['requester_user'] = {
            'name': 'João User',
            'email': 'user@maua.br',
            'sub': '550e8400-e29b-41d4-a716-446655440001',
            'custom:role': 'USER'
        }

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this supporter"

    def test_export_trainings_controller_missing_athlete_id(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        controller = ExportTrainingsController(usecase=usecase)

        request = HttpRequest(body={
            'training_id_list': ['660e8400-e29b-41d4-a716-446655440005']
        })
        request.data['requester_user'] = {
            'name': 'Guilherme Supporter',
            'email': 'supporter@maua.br',
            'sub': '550e8400-e29b-41d4-a716-446655440002',
            'custom:role': 'SUPPORT'
        }

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field athlete_id is missing"
