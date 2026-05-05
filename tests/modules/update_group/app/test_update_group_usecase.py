import pytest
from src.modules.update_group.app.update_group_usecase import UpdateGroupUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction

class Test_UpdateGroupUseCase:
    def test_update_group_usecase(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        
        group_id = "660e8400-e29b-41d4-a716-446655440001"
        
        updated_group, athletes_list, supporter_list = usecase(
            group_id=group_id,
            new_athlete_list_id=["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"],
            new_supporter_list_id=["e0cce9ad-e3ec-41f0-8600-812198c49450"]
        )
        
        assert str(updated_group.group_id) == group_id
        assert str(updated_group.athlete_list_id[0]) == "cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"

    def test_update_group_usecase_group_not_found(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(NoItemsFound) as err:
            usecase(
                group_id="invalid-id",
                new_athlete_list_id=["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"],
                new_supporter_list_id=None
            )
            
        assert err.value.message == "No items found for group"

    def test_update_group_usecase_athlete_not_found(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(NoItemsFound) as err:
            usecase(
                group_id="660e8400-e29b-41d4-a716-446655440001",
                new_athlete_list_id=["not-found-id"],
                new_supporter_list_id=None
            )
            
        assert err.value.message == "No items found for athlete not in DB"

    def test_update_group_usecase_athlete_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(ForbiddenAction) as err:
            usecase(
                group_id="660e8400-e29b-41d4-a716-446655440001",
                new_athlete_list_id=["e0cce9ad-e3ec-41f0-8600-812198c49450"], # This user is a supporter
                new_supporter_list_id=None
            )
            
        assert err.value.message == "That action is forbidden for this athlete role must be USER"

    def test_update_group_usecase_supporter_not_found(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(NoItemsFound) as err:
            usecase(
                group_id="660e8400-e29b-41d4-a716-446655440001",
                new_athlete_list_id=None,
                new_supporter_list_id=["not-found-id"]
            )
            
        assert err.value.message == "No items found for supporter not in DB"

    def test_update_group_usecase_supporter_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(ForbiddenAction) as err:
            usecase(
                group_id="660e8400-e29b-41d4-a716-446655440001",
                new_athlete_list_id=None,
                new_supporter_list_id=["550e8400-e29b-41d4-a716-446655440001"] # This user is an athlete (USER)
            )
            
        assert err.value.message == "That action is forbidden for this supporter role must be SUPPORTER"
