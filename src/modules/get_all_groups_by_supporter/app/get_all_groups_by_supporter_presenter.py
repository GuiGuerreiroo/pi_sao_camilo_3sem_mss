from .get_all_groups_by_supporter_controller import GetAllGroupsBySupporterController
from .get_all_groups_by_supporter_usecase import GetAllGroupsBySupporterUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_group_repo()
user_repo = Environments.get_user_repo()
training_repo= Environments.get_training_repo()

usecase = GetAllGroupsBySupporterUseCase(repo, user_repo, training_repo)
controller = GetAllGroupsBySupporterController(usecase)

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)

    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)

    response = controller(http_request)

    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return http_response.toDict()