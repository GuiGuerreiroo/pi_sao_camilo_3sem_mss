import pytest
from unittest.mock import MagicMock
from datetime import datetime

from src.modules.create_training.app.create_training_controller import CreateTrainingController
from src.modules.create_training.app.create_training_usecase import CreateTrainingUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_CreateTrainingController:
    def test_create_training_controller(self):
        repo = TrainingRepositoryMock()
        repo_user = UserRepositoryMock()
        usecase = CreateTrainingUseCase(repo=repo, repo_user=repo_user)
        usecase.client = MagicMock()
        usecase.client.retrieve_and_generate.return_value = {
            'output': {
                'text': 'Mocked AI feedback'
            }
        }
        
        controller = CreateTrainingController(usecase=usecase)

        user_id = repo_user.users[0].user_id
        start_date = int(datetime.now().timestamp() * 1000) - 7200000
        end_date = int(datetime.now().timestamp() * 1000) - 3600000

        request = HttpRequest(body={
            "requester_user": {
                "sub": user_id,
                "name": "Test User",
                "email": "test@test.com",
                "custom:role": "USER"
            },
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
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['message'] == 'Training successfully created and reviewed by AI'
        assert response.body['training']['user_id'] == user_id
        assert response.body['training']['modality'] == 'NATAÇÃO'
        assert response.body['training']['ai_suggestion'] == 'Mocked AI feedback'

    def test_create_training_controller_missing_modality(self):
        repo = TrainingRepositoryMock()
        repo_user = UserRepositoryMock()
        usecase = CreateTrainingUseCase(repo=repo, repo_user=repo_user)
        
        controller = CreateTrainingController(usecase=usecase)

        user_id = repo_user.users[0].user_id
        start_date = int(datetime.now().timestamp() * 1000) - 7200000
        end_date = int(datetime.now().timestamp() * 1000) - 3600000

        request = HttpRequest(body={
            "requester_user": {
                "sub": user_id,
                "name": "Test User",
                "email": "test@test.com",
                "custom:role": "USER"
            },
            # "modality": "NATACAO", # missing modality
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
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field modality is missing"
