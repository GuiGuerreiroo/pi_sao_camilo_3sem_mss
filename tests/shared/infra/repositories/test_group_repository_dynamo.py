import os
import uuid
import pytest
from src.shared.domain.entities.group import Group
from src.shared.infra.repositories.group_repository_dynamo import GroupRepositoryDynamo

class Test_GroupRepositoryDynamo:
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_group(self):
        os.environ["STAGE"] = "TEST"
        
        repo = GroupRepositoryDynamo()
        new_group = Group(
            group_id=uuid.uuid4(),
            athlete_list_id=[uuid.uuid4()],
            supporter_list_id=[uuid.uuid4()]
        )
        
        resp = repo.create_group(new_group)
        
        assert resp is not None
        assert str(resp.group_id) == str(new_group.group_id)
        
        # Clean up
        repo.delete_group(str(new_group.group_id))

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_group(self):
        os.environ["STAGE"] = "TEST"
        
        repo = GroupRepositoryDynamo()
        new_group = Group(
            group_id=uuid.uuid4(),
            athlete_list_id=[uuid.uuid4()],
            supporter_list_id=[uuid.uuid4()]
        )
        repo.create_group(new_group)
        
        resp = repo.get_group(str(new_group.group_id))
        
        assert resp is not None
        assert str(resp.group_id) == str(new_group.group_id)
        
        # Clean up
        repo.delete_group(str(new_group.group_id))

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_group_not_found(self):
        os.environ["STAGE"] = "TEST"
        
        repo = GroupRepositoryDynamo()
        resp = repo.get_group(str(uuid.uuid4()))
        
        assert resp is None

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_groups_by_supporter_id(self):
        os.environ["STAGE"] = "TEST"
        
        repo = GroupRepositoryDynamo()
        supporter_id = uuid.uuid4()
        
        new_group = Group(
            group_id=uuid.uuid4(),
            athlete_list_id=[uuid.uuid4()],
            supporter_list_id=[supporter_id]
        )
        repo.create_group(new_group)
        
        resp = repo.get_all_groups_by_supporter_id(str(supporter_id))
        
        assert len(resp) >= 1
        assert any(str(g.group_id) == str(new_group.group_id) for g in resp)
        
        # Clean up
        repo.delete_group(str(new_group.group_id))

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_group(self):
        os.environ["STAGE"] = "TEST"
        
        repo = GroupRepositoryDynamo()
        supporter_id_1 = uuid.uuid4()
        supporter_id_2 = uuid.uuid4()
        
        new_group = Group(
            group_id=uuid.uuid4(),
            athlete_list_id=[uuid.uuid4()],
            supporter_list_id=[supporter_id_1]
        )
        repo.create_group(new_group)
        
        resp = repo.update_group(
            str(new_group.group_id),
            new_supporter_list_id=[str(supporter_id_1), str(supporter_id_2)],
            new_athlete_list_id=None
        )
        
        assert resp is not None
        assert len(resp.supporter_list_id) == 2
        assert any(str(s) == str(supporter_id_2) for s in resp.supporter_list_id)
        
        # Clean up
        repo.delete_group(str(new_group.group_id))

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_group(self):
        os.environ["STAGE"] = "TEST"
        
        repo = GroupRepositoryDynamo()
        new_group = Group(
            group_id=uuid.uuid4(),
            athlete_list_id=[uuid.uuid4()],
            supporter_list_id=[uuid.uuid4()]
        )
        repo.create_group(new_group)
        
        resp = repo.delete_group(str(new_group.group_id))
        
        assert resp is not None
        assert str(resp.group_id) == str(new_group.group_id)
        assert repo.get_group(str(new_group.group_id)) is None
