from typing import List, Optional

from src.shared.domain.entities.training import Training
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.domain.enums.symptoms import SYMPTOMS
from src.shared.domain.repositories.training_repository_interface import ITrainingRepository


class TrainingRepositoryMock(ITrainingRepository):
    trainings: List[Training]

    def __init__(self):
        self.trainings = [
            Training(
                training_id="660e8400-e29b-41d4-a716-446655440002",
                user_id="550e8400-e29b-41d4-a716-446655440002",
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
            ),
            Training(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                modality=MODALITY.CICLISMO,
                start_date=1630100000000,
                end_date=1630107200000,
                duration=7200,
                environment_temperature=22.0,
                environment_humidity=50.0,
                urine_color=URINE_COLOR.TRANSLUCIDO,
                pre_training_symptoms=[SYMPTOMS.NONE],
                pre_training_weight=70.0,
                pre_training_hydration=300.0,
                during_training_hydration=500.0,
                during_training_urine_elimination=200.0,
                post_training_symptoms=[SYMPTOMS.NONE],
                post_training_weight=69.0,
                soaked_clothes=False,
                training_intensity=8,
                weight_difference=1.0,
                ajusted_weight_difference=1.3,
                sudorese=0.65,
                weight_variation_percentage=1.42,
                ai_suggestion="Remember to hydrate more."
            )
        ]

    def create_training(self, new_training: Training) -> Optional[Training]:
        self.trainings.append(new_training)
        return new_training

    def get_training(self, user_id: str, training_id: str) -> Optional[Training]:
        for training in self.trainings:
            if training.user_id == str(user_id) and training.training_id == str(training_id):
                return training
        return None

    def get_all_trainings_by_user(self, user_id: str) -> List[Training]:
        return [training for training in self.trainings if training.user_id == str(user_id)]

    def delete_training(self, user_id: str, training_id: str) -> Optional[Training]:
        for pos, training in enumerate(self.trainings):
            if training.user_id == str(user_id) and training.training_id == str(training_id):
                self.trainings.pop(pos)
                return training
        return None
