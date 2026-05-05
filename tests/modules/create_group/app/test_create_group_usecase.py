import pytest
from src.modules.create_group.app.create_group_usecase import CreateGroupUseCase
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction

class Test_CreateGroupUseCase:
    def test_create_group_usecase(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        
        new_group, athletes_list, supporter_list = usecase(
            athletes_list_id=["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"],
            supporter_list_id=["e0cce9ad-e3ec-41f0-8600-812198c49450"]
        )
        
        assert new_group.group_id is not None
        assert str(new_group.athlete_list_id[0]) == "cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"
        assert len(athletes_list) == 1
        assert len(supporter_list) == 1
        assert athletes_list[0].user_id == "cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"

    def test_create_group_usecase_athlete_not_found(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(NoItemsFound) as err:
            usecase(
                athletes_list_id=["not-found-id"],
                supporter_list_id=["e0cce9ad-e3ec-41f0-8600-812198c49450"]
            )
            
        assert err.value.message == "No items found for athlete not in DB"

    def test_create_group_usecase_athlete_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(ForbiddenAction) as err:
            usecase(
                athletes_list_id=["e0cce9ad-e3ec-41f0-8600-812198c49450"], # This user is a supporter
                supporter_list_id=["e0cce9ad-e3ec-41f0-8600-812198c49450"]
            )
            
        assert err.value.message == "That action is forbidden for this athlete role must be USER"

    def test_create_group_usecase_supporter_not_found(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(NoItemsFound) as err:
            usecase(
                athletes_list_id=["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"],
                supporter_list_id=["not-found-id"]
            )
            
        assert err.value.message == "No items found for supporter not in DB"

    def test_create_group_usecase_supporter_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateGroupUseCase(repo=repo, user_repo=user_repo)
        
        with pytest.raises(ForbiddenAction) as err:
            usecase(
                athletes_list_id=["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"],
                supporter_list_id=["550e8400-e29b-41d4-a716-446655440001"] # This user is an ADM
            )
            
        assert err.value.message == "That action is forbidden for this supporter role must be SUPPORTER"
