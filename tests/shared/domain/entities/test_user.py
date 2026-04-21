from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.status_user_enum import USERSTATUS
from pydantic import ValidationError
import pytest


class Test_User:
    def test_user(self):
        user = User(name="VITOR", email="21.01444-2@maua.br", role=ROLE.USER)
        assert isinstance(user.user_id, str)
        assert user.role == ROLE.USER

    def test_user_name_is_none(self):
        with pytest.raises(ValidationError):
            User(name=None, email="21.01444-2@maua.br", role=ROLE.USER)

    def test_user_name_is_not_str(self):
        with pytest.raises(ValidationError):
            User(name=1, email="21.01444-2@maua.br", role=ROLE.USER)

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(ValidationError):
            User(name="V", email="21.01444-2@maua.br", role=ROLE.USER)

    def test_user_email_is_none(self):
        with pytest.raises(ValidationError):
            User(name="VITOR", email=None, role=ROLE.USER)

    def test_user_user_id_is_not_valid_uuid(self):
        with pytest.raises(ValidationError):
            User(name="VITOR", email="21.01444-2@maua.br", user_id="1", role=ROLE.USER)

    def test_user_role_is_not_role_enum(self):
        with pytest.raises(ValidationError):
            User(name="VITOR", email="21.01444-2@maua.br", role="INVALID_ROLE")

    def test_user_status_is_not_status_enum(self):
        with pytest.raises(ValidationError):
            User(name="VITOR", email="21.01444-2@maua.br", role=ROLE.USER, status="INVALID")

    def test_user_expires_at_is_not_int(self):
        with pytest.raises(ValidationError):
            User(name="VITOR", email="21.01444-2@maua.br", role=ROLE.USER, expires_at="INVALID")
