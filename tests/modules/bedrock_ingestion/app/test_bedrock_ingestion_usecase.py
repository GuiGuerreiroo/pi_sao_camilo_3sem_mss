import pytest
from unittest.mock import MagicMock, patch
from src.modules.bedrock_ingestion.app.bedrock_ingestion_usecase import BedrockIngestionUseCase
from src.shared.helpers.errors.usecase_errors import DataIngestionError

class TestBedrockIngestionUseCase:
    @patch("boto3.client")
    @patch.dict("os.environ", {"KNOWLEDGE_BASE_ID": "kb-123", "DATA_SOURCE_ID": "ds-456"})
    def test_bedrock_ingestion_usecase_success(self, mock_boto3_client):
        mock_client_instance = MagicMock()
        mock_boto3_client.return_value = mock_client_instance
        
        mock_client_instance.start_ingestion_job.return_value = {
            "ingestionJob": {
                "ingestionJobId": "job-789",
                "status": "STARTING"
            }
        }

        usecase = BedrockIngestionUseCase()
        response = usecase(bucket_name="my-bucket", object_key="my-file.txt")

        assert response["job_id"] == "job-789"
        assert response["status"] == "STARTING"
        mock_client_instance.start_ingestion_job.assert_called_once_with(
            knowledgeBaseId="kb-123",
            dataSourceId="ds-456",
            description="Auto-triggered by upload of my-file.txt from my-bucket"
        )

    @patch("boto3.client")
    @patch.dict("os.environ", {"KNOWLEDGE_BASE_ID": "kb-123", "DATA_SOURCE_ID": "ds-456"})
    def test_bedrock_ingestion_usecase_failure(self, mock_boto3_client):
        mock_client_instance = MagicMock()
        mock_boto3_client.return_value = mock_client_instance
        
        mock_client_instance.start_ingestion_job.side_effect = Exception("AWS error")

        usecase = BedrockIngestionUseCase()

        with pytest.raises(DataIngestionError) as exc_info:
            usecase(bucket_name="my-bucket", object_key="my-file.txt")
        
        assert "Data ingestion failed: AWS error" in str(exc_info.value)
