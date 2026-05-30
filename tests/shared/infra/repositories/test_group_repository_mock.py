import uuid
from src.shared.domain.entities.group import Group
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock

class Test_GroupRepositoryMock:
    def test_create_group(self):
        repo = GroupRepositoryMock()
        new_group = Group(
            athlete_list_id=[],
            supporter_list_id=[]
        )
        
        repo.create_group(new_group)
        
        assert len(repo.groups) == 3
        assert repo.groups[2].group_id == new_group.group_id

    def test_get_group(self):
        repo = GroupRepositoryMock()
        
        group = repo.get_group("660e8400-e29b-41d4-a716-446655440001")
        
        assert group is not None
        assert str(group.group_id) == "660e8400-e29b-41d4-a716-446655440001"

    def test_get_group_not_found(self):
        repo = GroupRepositoryMock()
        
        group = repo.get_group("invalid-id")
        
        assert group is None

    def test_get_all_groups(self):
        repo = GroupRepositoryMock()
        
        groups = repo.get_all_groups()
        
        assert len(groups) == 2
        assert str(groups[0].group_id) == "660e8400-e29b-41d4-a716-446655440001"
        assert str(groups[1].group_id) == "660e8400-e29b-41d4-a716-446655440002"

    def test_get_all_groups_by_supporter_id(self):
        repo = GroupRepositoryMock()
        
        groups = repo.get_all_groups_by_supporter_id("550e8400-e29b-41d4-a716-446655440002")
        
        assert len(groups) == 2
        assert str(groups[0].group_id) == "660e8400-e29b-41d4-a716-446655440001"
        assert str(groups[1].group_id) == "660e8400-e29b-41d4-a716-446655440002"

    def test_update_group(self):
        repo = GroupRepositoryMock()
        
        updated_group = repo.update_group(
            "660e8400-e29b-41d4-a716-446655440001",
            new_supporter_list_id=["11111111-1111-1111-1111-111111111111"],
            new_athlete_list_id=["22222222-2222-2222-2222-222222222222"]
        )
        
        assert updated_group is not None
        assert str(updated_group.supporter_list_id[0]) == "11111111-1111-1111-1111-111111111111"
        assert str(updated_group.athlete_list_id[0]) == "22222222-2222-2222-2222-222222222222"

    def test_update_group_not_found(self):
        repo = GroupRepositoryMock()
        
        updated_group = repo.update_group("invalid-id", [], [])
        
        assert updated_group is None

    def test_delete_group(self):
        repo = GroupRepositoryMock()
        
        deleted_group = repo.delete_group("660e8400-e29b-41d4-a716-446655440001")
        
        assert deleted_group is not None
        assert str(deleted_group.group_id) == "660e8400-e29b-41d4-a716-446655440001"
        assert len(repo.groups) == 1

    def test_delete_group_not_found(self):
        repo = GroupRepositoryMock()
        
        deleted_group = repo.delete_group("invalid-id")
        
        assert deleted_group is None
