import pytest
from src.modules.get_all_groups.app.get_all_groups_usecase import GetAllGroupsUseCase
from src.modules.get_all_groups.app.get_all_groups_controller import GetAllGroupsController
from src.shared.infra.repositories.group_repository_mock import GroupRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.domain.enums.role_enum import ROLE

class Test_GetAllGroupsController:
    def test_get_all_groups_controller(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetAllGroupsUseCase(repo=repo, user_repo=user_repo)
        controller = GetAllGroupsController(usecase=usecase)
        
        # Admin user
        request = HttpRequest(body={
            "requester_user": {
                "sub": "770e8400-e29b-41d4-a716-446655440000",
                "name": "Admin Name",
                "email": "admin@gmail.com",
                "custom:role": "ADM",
                "custom:is_active": "true"
            }
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["message"] == "Groups retrieved successfully"
        assert len(response.body["groups"]) == 2

    def test_get_all_groups_controller_forbidden(self):
        repo = GroupRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = GetAllGroupsUseCase(repo=repo, user_repo=user_repo)
        controller = GetAllGroupsController(usecase=usecase)
        
        # Supporter user
        request = HttpRequest(body={
            "requester_user": {
                "sub": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Guilherme",
                "email": "gui@gmail.com",
                "custom:role": "SUPPORT",
                "custom:is_active": "true"
            }
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"
