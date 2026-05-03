import pytest
from unittest.mock import MagicMock
from datetime import datetime

from src.modules.create_training.app.create_training_usecase import CreateTrainingUseCase
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import BedrockIntegrationError
from botocore.exceptions import ClientError

class Test_CreateTrainingUseCase:
    def test_create_training(self):
        repo = TrainingRepositoryMock()
        repo_user = UserRepositoryMock()
        usecase = CreateTrainingUseCase(repo=repo, repo_user=repo_user)
        
        # mock the bedrock client
        usecase.client = MagicMock()
        usecase.client.retrieve_and_generate.return_value = {
            'output': {
                'text': 'Mocked AI feedback'
            }
        }

        user_id = repo_user.users[0].user_id
        start_date = int(datetime.now().timestamp() * 1000) - 7200000
        end_date = int(datetime.now().timestamp() * 1000) - 3600000
        
        training = usecase(
            user_id=user_id,
            modality=MODALITY.SWIMMING,
            start_date=start_date,
            end_date=end_date,
            duration=60.0,
            environment_temperature=25.0,
            environment_humidity=60.0,
            urine_color=URINE_COLOR.YELLOW,
            pre_training_symptoms=[],
            pre_training_weight=70.0,
            pre_training_hydration=500.0,
            during_training_hydration=250.0,
            during_training_urine_elimination=0.0,
            post_training_symptoms=[],
            post_training_weight=69.5,
            soaked_clothes=True,
            training_intensity=7
        )

        assert training is not None
        assert training.user_id == user_id
        assert training.modality == MODALITY.SWIMMING
        assert training.ai_suggestion == 'Mocked AI feedback'
        
        usecase.client.retrieve_and_generate.assert_called_once()
        assert len(repo.trainings) > 0
        assert repo.trainings[-1].training_id == training.training_id

    def test_create_training_bedrock_client_error(self):
        repo = TrainingRepositoryMock()
        repo_user = UserRepositoryMock()
        usecase = CreateTrainingUseCase(repo=repo, repo_user=repo_user)
        
        usecase.client = MagicMock()
        error_response = {'Error': {'Message': 'Bedrock temporary failure'}}
        usecase.client.retrieve_and_generate.side_effect = ClientError(error_response, 'RetrieveAndGenerate')

        user_id = repo_user.users[0].user_id
        start_date = int(datetime.now().timestamp() * 1000) - 7200000
        end_date = int(datetime.now().timestamp() * 1000) - 3600000
        
        with pytest.raises(BedrockIntegrationError) as exc_info:
            usecase(
                user_id=user_id,
                modality=MODALITY.SWIMMING,
                start_date=start_date,
                end_date=end_date,
                duration=60.0,
                environment_temperature=25.0,
                environment_humidity=60.0,
                urine_color=URINE_COLOR.YELLOW,
                pre_training_symptoms=[],
                pre_training_weight=70.0,
                pre_training_hydration=500.0,
                during_training_hydration=250.0,
                during_training_urine_elimination=0.0,
                post_training_symptoms=[],
                post_training_weight=69.5,
                soaked_clothes=True,
                training_intensity=7
            )
            
        assert exc_info.value.message == 'Error generating AI analysis: Bedrock temporary failure'
