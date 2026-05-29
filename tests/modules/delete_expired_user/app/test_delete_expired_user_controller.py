import pytest
from unittest.mock import MagicMock
from src.modules.delete_expired_user.app.delete_expired_user_controller import DeleteExpiredUserController
from src.shared.helpers.errors.controller_errors import MissingParameters

class Test_DeleteExpiredUserController:
    def test_delete_expired_user_controller_success(self):
        usecase = MagicMock()
        usecase.return_value = ["test1@maua.br"]
        
        controller = DeleteExpiredUserController(usecase=usecase)
        
        request = {
            "Records": [
                {
                    "eventName": "REMOVE",
                    "userIdentity": {
                        "principalId": "dynamodb.amazonaws.com"
                    },
                    "dynamodb": {
                        "OldImage": {
                            "email": {
                                "S": "test1@maua.br"
                            }
                        }
                    }
                }
            ]
        }
        
        response = controller(request)
        
        assert response["message"] == "Every user deleted in Dynamo DB was deleted in Cognito"
        assert response["deleted_emails"] == ["test1@maua.br"]
        usecase.assert_called_once_with(["test1@maua.br"])

    def test_delete_expired_user_controller_missing_email(self):
        usecase = MagicMock()
        controller = DeleteExpiredUserController(usecase=usecase)
        
        request = {
            "Records": [
                {
                    "eventName": "REMOVE",
                    "userIdentity": {
                        "principalId": "dynamodb.amazonaws.com"
                    },
                    "dynamodb": {
                        "OldImage": {}
                    }
                }
            ]
        }
        
        with pytest.raises(MissingParameters):
            controller(request)

    def test_delete_expired_user_controller_error(self):
        usecase = MagicMock()
        usecase.side_effect = Exception("Some generic error")
        
        controller = DeleteExpiredUserController(usecase=usecase)
        
        request = {
            "Records": [
                {
                    "eventName": "REMOVE",
                    "userIdentity": {
                        "principalId": "dynamodb.amazonaws.com"
                    },
                    "dynamodb": {
                        "OldImage": {
                            "email": {
                                "S": "test_error@maua.br"
                            }
                        }
                    }
                }
            ]
        }
        
        with pytest.raises(Exception):
            controller(request)
