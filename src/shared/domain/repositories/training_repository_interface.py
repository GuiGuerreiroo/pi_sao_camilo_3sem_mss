from abc import ABC, abstractmethod
from typing import Optional
from src.shared.domain.entities.training import Training

class ITrainingRepository(ABC):
    @abstractmethod
    def create_training(self, training: Training) -> Optional[Training]:
        pass

    @abstractmethod
    def get_training(self, user_id: str, training_id: str) -> Optional[Training]:
        """
        If training not found return None
        """
        pass

    @abstractmethod
    def get_all_trainings_by_user(self, user_id: str) -> list[Training]:
        """
        Return all trainings of a user
        If user isn't linked with a training return an empty list[]
        """
        pass

    @abstractmethod
    def delete_training(self, user_id: str, training_id: str) -> Optional[Training]:
        """
        If training not found return None
        """
        pass
