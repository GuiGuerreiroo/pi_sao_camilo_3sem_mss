from src.shared.environments import Environments
from .export_trainings_controller import ExportTrainingsController
from .export_trainings_usecase import ExportTrainingsUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

training_repo = Environments.get_training_repo()
group_repo = Environments.get_group_repo()
user_repo = Environments.get_user_repo()
usecase = ExportTrainingsUseCase(
    training_repo=training_repo, 
    group_repo=group_repo,
    user_repo=user_repo
)
controller = ExportTrainingsController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)

    httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)

    response = controller(httpRequest)

    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    if response.status_code == 200:
        return httpResponse.toDictBase64()
    
    return httpResponse.toDict()
