from src.shared.domain.entities.training import Training
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.domain.enums.symptoms import SYMPTOMS
from pydantic import ValidationError
import pytest
import uuid

class Test_Training:
    def test_training_valid(self):
        training = Training(
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
        assert isinstance(training.training_id, str)
        assert training.modality == MODALITY.RUNNING

    def test_training_invalid_user_id(self):
        with pytest.raises(ValidationError):
            Training(
                user_id="invalid-uuid",
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

    def test_training_missing_required_field(self):
        with pytest.raises(ValidationError):
            Training(
                user_id=str(uuid.uuid4()),
                # modality missing
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
