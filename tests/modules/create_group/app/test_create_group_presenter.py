import json
from src.modules.create_group.app.create_group_presenter import lambda_handler

class Test_CreateGroupPresenter:
    def test_create_group_presenter(self):
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
                        "name": "João",
                        "email": "joao@maua.br",
                        "sub": "550e8400-e29b-41d4-a716-446655440001",
                        "custom:role": "ADM"
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
            "body": '{"athletes_list_id": ["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"], "supporter_list_id": ["e0cce9ad-e3ec-41f0-8600-812198c49450"]}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)

        assert response["statusCode"] == 201
        
        body = json.loads(response["body"])
        assert body["message"] == "Group created successfully"
        assert body["group"]["group_id"] is not None
        assert body["group"]["athletes_list_id"][0]["user_id"] == "cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"
