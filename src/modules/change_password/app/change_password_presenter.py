from .change_password_controller import ChangePasswordController
from .change_password_usecase import ChangePasswordUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

usecase = ChangePasswordUseCase()
controller = ChangePasswordController(usecase)

def lambda_handler(event, context):
    http_request= LambdaHttpRequest(data=event)

    response= controller(http_request)

    http_response= LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()