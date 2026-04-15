import os
import uuid
import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryDynamo:
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        new_user = User(
            user_id=str(uuid.uuid4()),
            name="Test Dynamo Create",
            email="test.dynamo.create@maua.br",
            role=ROLE.USER,
            height=1.76
        )

        resp = user_repository.create_user(new_user)

        assert resp is not None
        assert resp.user_id == new_user.user_id
        assert resp.name == new_user.name

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        resp = user_repository.get_user("550e8400-e29b-41d4-a716-446655440001")

        assert resp is not None
        assert resp.user_id == "550e8400-e29b-41d4-a716-446655440001"
        assert resp.name == "João"


    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user_by_email(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        resp = user_repository.get_user_by_email("21.00678-2@maua.br")

        assert resp is not None
        assert resp.email == "21.00678-2@maua.br"

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user_not_found(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        resp = user_repository.get_user(str(uuid.uuid4()))

        assert resp is None

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_to_delete = User(
            user_id=str(uuid.uuid4()),
            name="Test Dynamo Delete",
            email="test.dynamo.delete@maua.br",
            role=ROLE.USER,
            height=1.68
        )
        user_repository.create_user(user_to_delete)

        resp = user_repository.delete_user(user_to_delete.user_id)

        assert resp is not None
        assert resp.get("Attributes") is not None
        assert user_repository.get_user(user_to_delete.user_id) is None

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = UserRepositoryDynamo()
        user_to_update = User(
            user_id=str(uuid.uuid4()),
            name="Test Dynamo Update",
            email="test.dynamo.update@maua.br",
            role=ROLE.USER,
            height=1.7
        )
        user_repository.create_user(user_to_update)

        resp = user_repository.update_user(
            user_id=user_to_update.user_id,
            new_name="Vitor Soller Soller",
            new_email=None,
            new_role=None,
            new_height=None
        )

        assert resp is not None
        assert resp.name == "Vitor Soller Soller"
