import json
import os

import pytest


class Test_GetUserPresenter:

    def test_get_user_presenter(self):
        os.environ["STAGE"] = "TEST"

        from src.modules.get_user.app.get_user_presenter import lambda_handler
        from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

        mock_repo = UserRepositoryMock()
        expected_user = mock_repo.users[1]

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "headers": {
                "Content-Type": "application/json"
            },
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "test-api",
                "authentication": None,
                "authorizer": {
                    "claims": {
                        "sub": expected_user.user_id,
                        "name": expected_user.name,
                        "email": expected_user.email,
                    }
                },
                "domainName": "test.execute-api.sa-east-1.amazonaws.com",
                "domainPrefix": "test",
                "external_interfaces": {
                    "method": "GET",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "127.0.0.1",
                    "userAgent": "pytest"
                },
                "requestId": "test-request-id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200

        body = json.loads(response["body"])
        assert body["user"]["name"] == expected_user.name
        assert body["user"]["email"] == expected_user.email
        assert body["user"]["user_id"] == expected_user.user_id
        assert body["message"] == "User successfully returned"

    def test_get_user_presenter_missing_auth(self):
        os.environ["STAGE"] = "TEST"

        from src.modules.get_user.app.get_user_presenter import lambda_handler

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "headers": {
                "Content-Type": "application/json"
            },
            "queryStringParameters": None,
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "test-api",
                "authentication": None,
                "authorizer": {},
                "domainName": "test.execute-api.sa-east-1.amazonaws.com",
                "domainPrefix": "test",
                "external_interfaces": {
                    "method": "GET",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "127.0.0.1",
                    "userAgent": "pytest"
                },
                "requestId": "test-request-id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": None,
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400

        body = json.loads(response["body"])
        assert body == "Field requester_user is missing"
