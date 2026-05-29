import pytest
import json
from unittest.mock import MagicMock
from src.modules.forgot_password.app.forgot_password_presenter import lambda_handler
from src.modules.forgot_password.app import forgot_password_presenter

class Test_ForgotPasswordPresenter:
    def test_forgot_password_presenter_success(self):
        forgot_password_presenter.usecase.cognito = MagicMock()
        forgot_password_presenter.usecase.cognito.forgot_password.return_value = {}
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path", 
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "http": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": '{"email": "25.00178-5@maua.br"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "Código de recuperação de senha enviado para o email com sucesso!"

    def test_forgot_password_presenter_missing_email(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path", 
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {
                "http": {
                    "method": "POST",
                }
            },
            "body": '{}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Field email is missing"
