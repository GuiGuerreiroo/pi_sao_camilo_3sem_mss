import pytest
from unittest.mock import MagicMock
import json
from datetime import datetime
import os

from src.modules.create_training.app.create_training_presenter import lambda_handler
from src.modules.create_training.app import create_training_presenter
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_CreateTrainingPresenter:
    def test_create_training_presenter(self):
        # Setting mock environments
        os.environ['STAGE'] = 'TEST'
        
        # Mocking bedrock client
        create_training_presenter.usecase.client = MagicMock()
        create_training_presenter.usecase.client.retrieve_and_generate.return_value = {
            'output': {
                'text': 'Mocked AI feedback'
            }
        }
        
        repo_user = UserRepositoryMock()
        user_id = repo_user.users[0].user_id
        start_date = int(datetime.now().timestamp() * 1000) - 7200000
        end_date = int(datetime.now().timestamp() * 1000) - 3600000

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
                "parameter1": "value1,value2",
                "parameter2": "value"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "api-id",
                "authentication": {
                    "clientCert": {
                        "clientCertPem": "CERT_CONTENT",
                        "subjectDN": "www.example.com",
                        "issuerDN": "Example issuer",
                        "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                        "validity": {
                            "notBefore": "May 28 12:30:02 2019 GMT",
                            "notAfter": "Aug  5 09:36:04 2021 GMT"
                        }
                    }
                },
                "authorizer": {
                    "jwt": {
                        "claims": {
                            "claim1": "value1",
                            "claim2": "value2"
                        },
                        "scopes": [
                            "scope1",
                            "scope2"
                        ]
                    },
                    "claims": {
                        "sub": user_id,
                        "name": "Test User",
                        "email": "test@test.com",
                        "custom:role": "USER"
                    }
                },
                "domainName": "id.execute-api.us-east-1.amazonaws.com",
                "domainPrefix": "id",
                "http": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "192.0.2.1",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:39 +0000",
                "timeEpoch": 1583348619267
            },
            "body": json.dumps({
                "modality": "NATAÇÃO",
                "start_date": start_date,
                "end_date": end_date,
                "duration": 60.0,
                "environment_temperature": 25.0,
                "environment_humidity": 60.0,
                "urine_color": "YELLOW",
                "pre_training_symptoms": [],
                "pre_training_weight": 70.0,
                "pre_training_hydration": 500.0,
                "during_training_hydration": 250.0,
                "during_training_urine_elimination": 0.0,
                "post_training_symptoms": [],
                "post_training_weight": 69.5,
                "soaked_clothes": True,
                "training_intensity": 7.0
            }),
            "pathParameters": {
                "parameter1": "value1"
            },
            "isBase64Encoded": False,
            "stageVariables": {
                "stageVariable1": "value1",
                "stageVariable2": "value2"
            }
        }

        response = lambda_handler(event, None)

        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['message'] == 'Training successfully created and reviewed by AI'
        assert body['training']['modality'] == 'NATAÇÃO'
        assert body['training']['user_id'] == user_id
