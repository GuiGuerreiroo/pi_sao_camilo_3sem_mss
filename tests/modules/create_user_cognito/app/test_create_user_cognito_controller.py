import os
import uuid

from src.modules.create_user_cognito.app.create_user_cognito_controler import CreateUserCognitoController
from src.shared.domain.enums.role_enum import ROLE


class SpyUsecase:
    def __init__(self):
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)


class Test_CreateUserCognitoController:
    def _base_event(self):
        return {
            "userPoolId": "pool-123",
            "triggerSource": "PostConfirmation_ConfirmSignUp",
            "request": {
                "userAttributes": {
                    "sub": str(uuid.uuid4()),
                    "email": "cognito.user@maua.br",
                    "name": "Cognito User"
                },
                "clientMetadata": {
                    "role": ROLE.USER.value,
                    "height": "1.80"
                }
            },
            "response": {}
        }

    def test_create_user_cognito_controller_user_role(self):
        os.environ["USER_POOL_ID"] = "pool-123"
        usecase = SpyUsecase()
        controller = CreateUserCognitoController(usecase=usecase)

        event = self._base_event()

        response = controller(event)

        assert response is None
        assert len(usecase.calls) == 1
        assert usecase.calls[0]["email"] == "cognito.user@maua.br"
        assert usecase.calls[0]["name"] == "Cognito User"
        assert usecase.calls[0]["role"] == ROLE.USER
        assert usecase.calls[0]["height"] == 1.8

    def test_create_user_cognito_controller_wrong_user_pool(self):
        os.environ["USER_POOL_ID"] = "pool-allowed"
        usecase = SpyUsecase()
        controller = CreateUserCognitoController(usecase=usecase)

        event = self._base_event()
        event["userPoolId"] = "pool-not-allowed"

        response = controller(event)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user_poo_id"
        assert len(usecase.calls) == 0

    def test_create_user_cognito_controller_missing_height_for_user(self):
        os.environ["USER_POOL_ID"] = "pool-123"
        usecase = SpyUsecase()
        controller = CreateUserCognitoController(usecase=usecase)

        event = self._base_event()
        event["request"]["clientMetadata"].pop("height")

        response = controller(event)

        assert response.status_code == 400
        assert response.body == "Field height is missing"

    def test_create_user_cognito_controller_invalid_role(self):
        os.environ["USER_POOL_ID"] = "pool-123"
        usecase = SpyUsecase()
        controller = CreateUserCognitoController(usecase=usecase)

        event = self._base_event()
        event["request"]["clientMetadata"]["role"] = "MANAGER"

        response = controller(event)

        assert response.status_code == 400
        assert response.body == "Field role isn't in the right type.\n Received: MANAGER.\n Expected: one of ['ADM', 'USER', 'SUPPORT']"

    def test_create_user_cognito_controller_admin_forbidden(self):
        os.environ["USER_POOL_ID"] = "pool-123"
        usecase = SpyUsecase()
        controller = CreateUserCognitoController(usecase=usecase)

        event = self._base_event()
        event["request"]["clientMetadata"]["role"] = ROLE.ADM.value

        response = controller(event)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this administrator role"

    def test_create_user_cognito_controller_ignore_other_trigger_source(self):
        os.environ["USER_POOL_ID"] = "pool-123"
        usecase = SpyUsecase()
        controller = CreateUserCognitoController(usecase=usecase)

        event = self._base_event()
        event["triggerSource"] = "PreSignUp_SignUp"

        response = controller(event)

        assert response is None
        assert len(usecase.calls) == 0
