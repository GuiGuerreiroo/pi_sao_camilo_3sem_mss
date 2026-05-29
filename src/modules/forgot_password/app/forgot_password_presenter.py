from .forgot_password_controller import ForgotPasswordController
from .forgot_password_usecase import ForgotPasswordUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()
usecase = ForgotPasswordUseCase(repo)
controller = ForgotPasswordController(usecase)

def lambda_handler(event, context):
    http_request= LambdaHttpRequest(data=event)

    response= controller(http_request)

    http_response= LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return http_response.toDict()