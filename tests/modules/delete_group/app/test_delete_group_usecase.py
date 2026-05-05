import pytest
from src.modules.delete_group.app.delete_group_usecase import DeleteGroupUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class Test_DeleteGroupUseCase:
    def test_delete_group_usecase(self):
        repo = GroupRepositoryMock()
        usecase = DeleteGroupUseCase(repo=repo)
        
        group_id = "660e8400-e29b-41d4-a716-446655440001"
        
        deleted_group = usecase(
            group_id=group_id
        )
        
        assert str(deleted_group.group_id) == group_id
        assert len(repo.groups) == 1

    def test_delete_group_usecase_not_found(self):
        repo = GroupRepositoryMock()
        usecase = DeleteGroupUseCase(repo=repo)
        
        with pytest.raises(NoItemsFound) as err:
            usecase(
                group_id="invalid-id"
            )
            
        assert err.value.message == "No items found for group"
