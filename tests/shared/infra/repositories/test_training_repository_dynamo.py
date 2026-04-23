import os
import uuid
import pytest
from src.shared.domain.entities.training import Training
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.domain.enums.symptoms import SYMPTOMS
from src.shared.infra.repositories.training_repository_dynamo import TrainingRepositoryDynamo

class Test_TrainingRepositoryDynamo:
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_training(self):
        os.environ["STAGE"] = "TEST"

        training_repository = TrainingRepositoryDynamo()
        new_training = Training(
            training_id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            modality=MODALITY.RUNNING,
            start_date=1630000000000,
            end_date=1630003600000,
            duration=3600,
            environment_temperature=25.5,
            environment_humidity=60.0,
            urine_color=URINE_COLOR.YELLOW,
            pre_training_symptoms=[SYMPTOMS.NONE],
            pre_training_weight=70.0,
            pre_training_hydration=500.0,
            clothing_equipment=True,
            during_training_hydration=200.0,
            during_trainin_urine_elimination=0.0,
            post_training_symptoms=[SYMPTOMS.NONE],
            post_training_weight=69.5,
            soaked_clothes=True,
            training_intensity=7,
            weight_difference=0.5,
            ajusted_weight_difference=0.7,
            hydric_balance=200.0,
            sudorese=0.7,
            weight_variation_percentage=0.71
        )

        resp = training_repository.create_training(new_training)

        assert resp is not None
        assert resp.training_id == new_training.training_id
        assert resp.user_id == new_training.user_id

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_training(self):
        os.environ["STAGE"] = "TEST"
        training_repository = TrainingRepositoryDynamo()
        
        new_training = Training(
            training_id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            modality=MODALITY.WALKING,
            start_date=1630000000000,
            end_date=1630003600000,
            duration=3600,
            environment_temperature=25.5,
            environment_humidity=60.0,
            urine_color=URINE_COLOR.YELLOW,
            pre_training_symptoms=[SYMPTOMS.NONE],
            pre_training_weight=70.0,
            pre_training_hydration=500.0,
            clothing_equipment=True,
            during_training_hydration=200.0,
            during_trainin_urine_elimination=0.0,
            post_training_symptoms=[SYMPTOMS.NONE],
            post_training_weight=69.5,
            soaked_clothes=True,
            training_intensity=7,
            weight_difference=0.5,
            ajusted_weight_difference=0.7,
            hydric_balance=200.0,
            sudorese=0.7,
            weight_variation_percentage=0.71
        )
        training_repository.create_training(new_training)
        
        resp = training_repository.get_training(new_training.user_id, new_training.training_id)

        assert resp is not None
        assert resp.training_id == new_training.training_id
        assert resp.user_id == new_training.user_id

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_training_not_found(self):
        os.environ["STAGE"] = "TEST"
        training_repository = TrainingRepositoryDynamo()
        
        resp = training_repository.get_training(str(uuid.uuid4()), str(uuid.uuid4()))
        assert resp is None

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_trainings_by_user(self):
        os.environ["STAGE"] = "TEST"
        training_repository = TrainingRepositoryDynamo()
        
        user_id = str(uuid.uuid4())
        
        new_training = Training(
            training_id=str(uuid.uuid4()),
            user_id=user_id,
            modality=MODALITY.WALKING,
            start_date=1630000000000,
            end_date=1630003600000,
            duration=3600,
            environment_temperature=25.5,
            environment_humidity=60.0,
            urine_color=URINE_COLOR.YELLOW,
            pre_training_symptoms=[SYMPTOMS.NONE],
            pre_training_weight=70.0,
            pre_training_hydration=500.0,
            clothing_equipment=True,
            during_training_hydration=200.0,
            during_trainin_urine_elimination=0.0,
            post_training_symptoms=[SYMPTOMS.NONE],
            post_training_weight=69.5,
            soaked_clothes=True,
            training_intensity=7,
            weight_difference=0.5,
            ajusted_weight_difference=0.7,
            hydric_balance=200.0,
            sudorese=0.7,
            weight_variation_percentage=0.71
        )
        training_repository.create_training(new_training)
        
        resp = training_repository.get_all_trainings_by_user(user_id)
        
        assert len(resp) == 1
        assert resp[0].user_id == user_id

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_training(self):
        os.environ["STAGE"] = "TEST"

        training_repository = TrainingRepositoryDynamo()
        training_to_delete = Training(
            training_id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            modality=MODALITY.RUNNING,
            start_date=1630000000000,
            end_date=1630003600000,
            duration=3600,
            environment_temperature=25.5,
            environment_humidity=60.0,
            urine_color=URINE_COLOR.YELLOW,
            pre_training_symptoms=[SYMPTOMS.NONE],
            pre_training_weight=70.0,
            pre_training_hydration=500.0,
            clothing_equipment=True,
            during_training_hydration=200.0,
            during_trainin_urine_elimination=0.0,
            post_training_symptoms=[SYMPTOMS.NONE],
            post_training_weight=69.5,
            soaked_clothes=True,
            training_intensity=7,
            weight_difference=0.5,
            ajusted_weight_difference=0.7,
            hydric_balance=200.0,
            sudorese=0.7,
            weight_variation_percentage=0.71
        )
        training_repository.create_training(training_to_delete)

        resp = training_repository.delete_training(training_to_delete.user_id, training_to_delete.training_id)

        assert resp is not None
        assert training_repository.get_training(training_to_delete.user_id, training_to_delete.training_id) is None

