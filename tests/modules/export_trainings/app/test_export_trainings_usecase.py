import pytest
import base64
from src.modules.export_trainings.app.export_trainings_usecase import ExportTrainingsUseCase
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound

class Test_ExportTrainingsUseCase:
    def test_export_trainings_usecase(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        
        # Using a supporter and athlete linked in the mock data
        # Supporter: 550e8400-e29b-41d4-a716-446655440002
        # Athlete: 550e8400-e29b-41d4-a716-446655440001
        # But wait! Athlete ...0001 has no trainings. 
        # Athlete ...0002 has trainings, and Supporter is ...0002 in Group ...0001 but wait!
        # Let's add a training to Athlete ...0001 temporarily OR use Group 2 where Athlete is cde8... and add training
        
        # Let's modify the repo locally for testing
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

        base64_pdf = usecase(
            athlete_id="550e8400-e29b-41d4-a716-446655440001",
            training_id_list=["660e8400-e29b-41d4-a716-446655440005"],
            requester_user_id="550e8400-e29b-41d4-a716-446655440002",
            requester_name="Test Supporter"
        )
        
        assert type(base64_pdf) == str
        
        # Verify it can be decoded
        try:
            pdf_bytes = base64.b64decode(base64_pdf)
            assert pdf_bytes.startswith(b'%PDF')
        except Exception:
            pytest.fail("Returned string is not a valid base64 PDF")

    def test_export_trainings_usecase_not_linked(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        
        # Try to access athlete not linked to the supporter
        with pytest.raises(ForbiddenAction):
            usecase(
                athlete_id="unlinked-athlete-id",
                training_id_list=["some-training-id"],
                requester_user_id="550e8400-e29b-41d4-a716-446655440002",
                requester_name="Test Supporter"
            )

    def test_export_trainings_usecase_no_trainings_found(self):
        repo_t = TrainingRepositoryMock()
        repo_g = GroupRepositoryMock()
        repo_u = UserRepositoryMock()
        usecase = ExportTrainingsUseCase(training_repo=repo_t, group_repo=repo_g, user_repo=repo_u)
        
        # Athlete is linked, but requested training ID does not exist
        with pytest.raises(NoItemsFound):
            usecase(
                athlete_id="550e8400-e29b-41d4-a716-446655440001",
                training_id_list=["non-existent-training-id"],
                requester_user_id="550e8400-e29b-41d4-a716-446655440002",
                requester_name="Test Supporter"
            )
