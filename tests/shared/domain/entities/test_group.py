import pytest
import uuid
from pydantic import ValidationError
from src.shared.domain.entities.group import Group

class Test_Group:
    def test_group_creation_valid(self):
        athlete_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        supporter_ids = [str(uuid.uuid4())]
        
        group = Group(
            athlete_list_id=athlete_ids,
            supporter_list_id=supporter_ids
        )
        
        assert str(group.group_id) is not None
        assert [str(a) for a in group.athlete_list_id] == athlete_ids
        assert [str(s) for s in group.supporter_list_id] == supporter_ids
        
    def test_group_creation_with_specific_id(self):
        specific_id = str(uuid.uuid4())
        
        group = Group(
            group_id=specific_id,
            athlete_list_id=[],
            supporter_list_id=[]
        )
        
        assert str(group.group_id) == specific_id
        assert group.athlete_list_id == []
        assert group.supporter_list_id == []
        
    def test_group_creation_invalid_id_type(self):
        with pytest.raises(ValidationError):
            Group(
                group_id="invalid-uuid",
                athlete_list_id=[],
                supporter_list_id=[]
            )
            
    def test_group_creation_invalid_lists(self):
        with pytest.raises(ValidationError):
            Group(
                athlete_list_id=["invalid-uuid"],
                supporter_list_id=[]
            )
            
    def test_group_creation_extra_fields(self):
        with pytest.raises(ValidationError):
            Group(
                athlete_list_id=[],
                supporter_list_id=[],
                extra_field="should fail"
            )
