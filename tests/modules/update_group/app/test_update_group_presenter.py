import json
from src.modules.update_group.app.update_group_presenter import lambda_handler

class Test_UpdateGroupPresenter:
    def test_update_group_presenter(self):
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
            "body": '{"group_id": "660e8400-e29b-41d4-a716-446655440001", "new_athlete_list_id": ["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"]}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)

        assert response["statusCode"] == 200
        
        body = json.loads(response["body"])
        assert body["message"] == "Group was updated successfully"
        assert body["group"]["group_id"] == "660e8400-e29b-41d4-a716-446655440001"
