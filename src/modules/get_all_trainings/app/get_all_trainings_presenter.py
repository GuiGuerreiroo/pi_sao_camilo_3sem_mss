from src.shared.environments import Environments
from .get_all_trainings_controller import GetAllTrainingsController
from .get_all_trainings_usecase import GetAllTrainingsUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_training_repo()
usecase = GetAllTrainingsUseCase(repo)
controller = GetAllTrainingsController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)

    response = controller(httpRequest)

    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()