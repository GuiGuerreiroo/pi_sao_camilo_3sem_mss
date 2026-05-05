from .update_group_controller import UpdateGroupController
from .update_group_usecase import UpdateGroupUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_group_repo()
user_repo = Environments.get_user_repo()
usecase = UpdateGroupUseCase(repo=repo, user_repo=user_repo)
controller = UpdateGroupController(usecase)

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)

    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)

    response = controller(http_request)

    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return http_response.toDict()
