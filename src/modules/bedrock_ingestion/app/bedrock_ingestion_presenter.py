from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpResponse
from .bedrock_ingestion_usecase import BedrockIngestionUseCase
from .bedrock_ingestion_controller import BedrockIngestionController

usecase= BedrockIngestionUseCase()

controller= BedrockIngestionController(usecase)

def lambda_handler(event: dict, context: object) -> dict:
    print(event)

    source= event.get("source")

    detail_type= event.get("detail-type")

    if source != "aws.s3" or detail_type != "Object Created":
        http_response= LambdaHttpResponse(
            status_code=400, body="Invalid event source. Expected S3 Object Created event from EventBridge."
        )

        return http_response.toDict()


    http_request= LambdaHttpRequest(data=event)

    response= controller(http_request)

    http_response= LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )

    return http_response.toDict()
