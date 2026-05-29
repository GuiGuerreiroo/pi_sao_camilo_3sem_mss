import pytest
from unittest.mock import MagicMock
from src.modules.delete_expired_user.app.delete_expired_user_presenter import lambda_handler
from src.modules.delete_expired_user.app import delete_expired_user_presenter

class Test_DeleteExpiredUserPresenter:
    def test_delete_expired_user_presenter_success(self):
        delete_expired_user_presenter.usecase.client = MagicMock()
        delete_expired_user_presenter.usecase.client.admin_delete_user.return_value = {}

        event = {
            "Records": [
                {
                    "eventSource": "aws:dynamodb",
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

        response = lambda_handler(event, None)

        assert response["message"] == "Every user deleted in Dynamo DB was deleted in Cognito"
        assert response["deleted_emails"] == ["test1@maua.br"]

    def test_delete_expired_user_presenter_invalid_event_format(self):
        event = {
            "NotRecords": []
        }

        with pytest.raises(ValueError, match="Invalid event format"):
            lambda_handler(event, None)

    def test_delete_expired_user_presenter_invalid_event_source(self):
        event = {
            "Records": [
                {
                    "eventSource": "not:aws:dynamodb"
                }
            ]
        }

        with pytest.raises(ValueError, match="Invalid event source"):
            lambda_handler(event, None)
