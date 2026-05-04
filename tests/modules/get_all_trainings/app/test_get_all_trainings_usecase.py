import pytest
from src.modules.get_all_trainings.app.get_all_trainings_usecase import GetAllTrainingsUseCase
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.domain.entities.training import Training

class Test_GetAllTrainingsUseCase:
    def test_get_all_trainings_usecase(self):
        repo = TrainingRepositoryMock()
        usecase = GetAllTrainingsUseCase(repo=repo)
        
        trainings = usecase(user_id="550e8400-e29b-41d4-a716-446655440002")
        
        assert type(trainings) == list
        assert len(trainings) > 0
        assert all(isinstance(t, Training) for t in trainings)
        assert all(t.user_id == "550e8400-e29b-41d4-a716-446655440002" for t in trainings)

    def test_get_all_trainings_usecase_empty(self):
        repo = TrainingRepositoryMock()
        usecase = GetAllTrainingsUseCase(repo=repo)
        
        trainings = usecase(user_id="non-existent")
        
        assert trainings == []
        assert type(trainings) == list
        assert len(trainings) == 0
