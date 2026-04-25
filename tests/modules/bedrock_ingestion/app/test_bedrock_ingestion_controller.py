import pytest
from unittest.mock import MagicMock
from src.modules.bedrock_ingestion.app.bedrock_ingestion_controller import BedrockIngestionController
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.errors.usecase_errors import DataIngestionError

class MockRequest:
    def __init__(self, data: dict):
        self.data = data

class TestBedrockIngestionController:
    def test_bedrock_ingestion_controller_success(self):
        mock_usecase = MagicMock()
        mock_usecase.return_value = {
            "job_id": "job-123",
            "status": "STARTING"
        }

        controller = BedrockIngestionController(usecase=mock_usecase)
        
        request = MockRequest(data={
            "detail": {
                "bucket": {"name": "test-bucket"},
                "object": {"key": "test-file.txt"}
            }
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body["message"] == "Bedrock ingestion started successfully"
        assert response.body["data"]["job_id"] == "job-123"

    def test_bedrock_ingestion_controller_missing_parameters(self):
        mock_usecase = MagicMock()
        controller = BedrockIngestionController(usecase=mock_usecase)

        request = MockRequest(data={
            "detail": {
                "bucket": {"name": ""},
                "object": {"key": ""}
            }
        })

        response = controller(request)

        assert response.status_code == 400
        assert "bucket name ou object key" in response.body

    def test_bedrock_ingestion_controller_data_ingestion_error(self):
        mock_usecase = MagicMock()
        mock_usecase.side_effect = DataIngestionError("AWS timeout")

        controller = BedrockIngestionController(usecase=mock_usecase)

        request = MockRequest(data={
            "detail": {
                "bucket": {"name": "test-bucket"},
                "object": {"key": "test-file.txt"}
            }
        })

        response = controller(request)

        assert response.status_code == 503
        assert "Data ingestion failed: AWS timeout" in response.body
