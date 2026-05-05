import pytest
from src.modules.get_all_groups_by_supporter.app.get_all_groups_by_supporter_usecase import GetAllGroupsBySupporterUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound
import uuid

class Test_GetAllGroupsBySupporterUseCase:
    def test_get_all_groups_by_supporter_usecase(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        training_repo = TrainingRepositoryMock()
        usecase = GetAllGroupsBySupporterUseCase(repo=repo, user_repo=user_repo, training_repo=training_repo)
        
        # Pedro's ID
        groups = usecase(user_id="e0cce9ad-e3ec-41f0-8600-812198c49450")
        
        assert isinstance(groups, dict)
        assert len(groups) == 0
        assert groups == {}

    def test_get_all_groups_by_supporter_usecase_valid(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        training_repo = TrainingRepositoryMock()
        usecase = GetAllGroupsBySupporterUseCase(repo=repo, user_repo=user_repo, training_repo=training_repo)
        
        # Using Guilherme's ID because he is listed as a supporter in the mock groups
        user_id = "550e8400-e29b-41d4-a716-446655440002"
        groups = usecase(user_id=user_id)
        
        assert len(groups) == 2
        group_1_id = uuid.UUID("660e8400-e29b-41d4-a716-446655440001")
        assert group_1_id in groups
        
        # Joao is the athlete in group 1
        assert len(groups[group_1_id]["athletes_list"]) == 1
        assert str(groups[group_1_id]["athletes_list"][0]["athlete_data"].user_id) == "550e8400-e29b-41d4-a716-446655440001"
