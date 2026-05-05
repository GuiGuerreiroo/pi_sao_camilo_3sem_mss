from .delete_group_controller import DeleteGroupController
from .delete_group_usecase import DeleteGroupUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_group_repo()
usecase = DeleteGroupUseCase(repo=repo)
controller = DeleteGroupController(usecase)

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)

    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)

    response = controller(http_request)

    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return http_response.toDict()
