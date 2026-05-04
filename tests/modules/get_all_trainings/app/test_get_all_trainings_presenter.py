import json

from src.modules.get_all_trainings.app.get_all_trainings_presenter import lambda_handler

class Test_GetAllTrainingsPresenter:
    def test_get_all_trainings_presenter(self):
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
                "parameter1": "value1",
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims": {
                        "name": "Guilherme",
                        "email": "25.00178-5@maua.br",
                        "sub": "550e8400-e29b-41d4-a716-446655440002",
                        "custom:role": "USER"
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
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
            "body": "{}",
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)

        assert response["statusCode"] == 200
        
        body = json.loads(response["body"])
        assert "trainings" in body
        assert type(body["trainings"]) == list
        assert len(body["trainings"]) > 0
        assert body["message"] == "Trainings returned successfully"
