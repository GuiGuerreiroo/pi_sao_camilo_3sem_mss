import pytest
from src.modules.get_all_groups.app.get_all_groups_usecase import GetAllGroupsUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import uuid

class Test_GetAllGroupsUseCase:
    def test_get_all_groups_usecase(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetAllGroupsUseCase(repo=repo, user_repo=user_repo)
        
        groups = usecase()
        
        # In the mock, there are exactly 2 groups
        assert len(groups) == 2
        group_1_id = uuid.UUID("660e8400-e29b-41d4-a716-446655440001")
        assert group_1_id in groups
        
        # Joao is the athlete in group 1
        assert len(groups[group_1_id]["athletes_list"]) == 1
        assert str(groups[group_1_id]["athletes_list"][0]["athlete_data"].user_id) == "550e8400-e29b-41d4-a716-446655440001"

        # Supporter is included
        assert len(groups[group_1_id]["supporter_list"]) == 1
        assert str(groups[group_1_id]["supporter_list"][0].user_id) == "550e8400-e29b-41d4-a716-446655440002"
