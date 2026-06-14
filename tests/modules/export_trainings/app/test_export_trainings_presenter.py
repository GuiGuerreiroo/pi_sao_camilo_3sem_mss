import json

from src.modules.export_trainings.app.export_trainings_presenter import lambda_handler

class Test_ExportTrainingsPresenter:
    def test_export_trainings_presenter(self):
        # We need to inject the mock training before calling the handler
        # Since the handler instantiates the repository using Environments, 
        # and we are in a test context, Environments should return mocks.
        from src.modules.export_trainings.app.export_trainings_presenter import training_repo, lambda_handler
        from src.shared.domain.entities.training import Training
        from src.shared.domain.enums.modality import MODALITY
        from src.shared.domain.enums.usrine_color import URINE_COLOR
        from src.shared.domain.enums.symptoms import SYMPTOMS

        training_repo.trainings.append(
            Training(
                training_id="660e8400-e29b-41d4-a716-446655440005",
                user_id="550e8400-e29b-41d4-a716-446655440001",
                modality=MODALITY.CORRIDA,
                start_date=1630000000000,
                end_date=1630003600000,
                duration=3600,
                environment_temperature=25.5,
                environment_humidity=60.0,
                urine_color=URINE_COLOR.AMARELO,
                pre_training_symptoms=[SYMPTOMS.NONE],
                pre_training_weight=70.0,
                pre_training_hydration=500.0,
                during_training_hydration=200.0,
                during_training_urine_elimination=0.0,
                post_training_symptoms=[SYMPTOMS.NONE],
                post_training_weight=69.5,
                soaked_clothes=True,
                training_intensity=7,
                weight_difference=0.5,
                ajusted_weight_difference=0.7,
                sudorese=0.7,
                weight_variation_percentage=0.71,
                ai_suggestion="Great training!"
            )
        )

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "cookies": [],
            "headers": {},
            "queryStringParameters": {},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims": {
                        "name": "Guilherme",
                        "email": "supporter@maua.br",
                        "sub": "550e8400-e29b-41d4-a716-446655440002",
                        "custom:role": "SUPPORT"
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
            "body": json.dumps({
                "athlete_id": "550e8400-e29b-41d4-a716-446655440001",
                "training_id_list": ["660e8400-e29b-41d4-a716-446655440005"]
            }),
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None
        }

        response = lambda_handler(event=event, context=None)

        assert response["statusCode"] == 200
        assert type(response["body"]) == str
        assert response["isBase64Encoded"] == True
        assert response["headers"]["Content-Type"] == "application/pdf"
