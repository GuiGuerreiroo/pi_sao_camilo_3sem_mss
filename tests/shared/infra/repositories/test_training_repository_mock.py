from src.shared.domain.entities.training import Training
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.domain.enums.symptoms import SYMPTOMS
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
import uuid


class Test_TrainingRepositoryMock:
    def test_get_training(self):
        repo = TrainingRepositoryMock()
        training = repo.get_training(
            user_id="550e8400-e29b-41d4-a716-446655440002",
            training_id="660e8400-e29b-41d4-a716-446655440002"
        )

        assert training is not None
        assert training.user_id == "550e8400-e29b-41d4-a716-446655440002"
        assert training.training_id == "660e8400-e29b-41d4-a716-446655440002"
        assert training.modality == MODALITY.CORRIDA

    def test_get_training_not_found(self):
        repo = TrainingRepositoryMock()
        training = repo.get_training("non-existent", "non-existent")
        assert training is None

    def test_get_all_trainings_by_user(self):
        repo = TrainingRepositoryMock()
        trainings = repo.get_all_trainings_by_user("550e8400-e29b-41d4-a716-446655440002")
        
        assert len(trainings) == 2
        assert trainings[0].user_id == "550e8400-e29b-41d4-a716-446655440002"
        assert trainings[1].user_id == "550e8400-e29b-41d4-a716-446655440002"

    def test_create_training(self):
        repo = TrainingRepositoryMock()
        new_training = Training(
            user_id=str(uuid.uuid4()),
            modality=MODALITY.CAMINHADA,
            start_date=1630200000000,
            end_date=1630203600000,
            duration=3600,
            environment_temperature=20.0,
            environment_humidity=50.0,
            urine_color=URINE_COLOR.TRANSLUCIDO,
            pre_training_symptoms=[SYMPTOMS.NONE],
            pre_training_weight=65.0,
            pre_training_hydration=200.0,
            during_training_hydration=100.0,
            during_training_urine_elimination=0.0,
            post_training_symptoms=[SYMPTOMS.NONE],
            post_training_weight=64.8,
            soaked_clothes=False,
            training_intensity=4,
            weight_difference=0.2,
            ajusted_weight_difference=0.3,
            sudorese=0.3,
            weight_variation_percentage=0.3
        )

        initial_size = len(repo.trainings)
        repo.create_training(new_training)

        assert len(repo.trainings) == initial_size + 1
        assert repo.trainings[-1].user_id == new_training.user_id
        assert repo.trainings[-1].modality == MODALITY.CAMINHADA

    def test_delete_training(self):
        repo = TrainingRepositoryMock()
        training = repo.delete_training(
            user_id="550e8400-e29b-41d4-a716-446655440002",
            training_id="660e8400-e29b-41d4-a716-446655440002"
        )
        assert training is not None
        assert training.training_id == "660e8400-e29b-41d4-a716-446655440002"
        
        # Verify it was removed
        assert repo.get_training("550e8400-e29b-41d4-a716-446655440001", "660e8400-e29b-41d4-a716-446655440002") is None

    def test_delete_training_not_found(self):
        repo = TrainingRepositoryMock()
        training = repo.delete_training("non-existent", "non-existent")
        assert training is None
