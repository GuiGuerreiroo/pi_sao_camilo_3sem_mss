from typing import List
from src.shared.domain.entities.training import Training
from src.shared.domain.repositories.training_repository_interface import ITrainingRepository

class GetAllTrainingsUseCase:
    def __init__(self, repo: ITrainingRepository):
        self.repo = repo

    def __call__(self, user_id: str) -> List[Training] | []:
        trainings = self.repo.get_all_trainings_by_user(user_id=user_id)

        # if there are no trainings the method it self will return an empty list

        return trainings