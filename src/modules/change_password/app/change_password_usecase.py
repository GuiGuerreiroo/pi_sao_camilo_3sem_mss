from src.shared.environments import Environments
import boto3
from src.shared.helpers.errors.usecase_errors import NoItemsFound, CodeMismatchError, ExpiredCodeError, InvalidPasswordError
from botocore.exceptions import ClientError

class ChangePasswordUseCase:
    def __init__(self):
        self.client_id = Environments.get_envs().cognito_client_id
        self.region = Environments.get_envs().region
        self.cognito = boto3.client('cognito-idp', region_name=self.region)

    def __call__(
            self,
            email: str,
            code: str,
            new_password: str
        ):
            try:
                
                self.cognito.confirm_forgot_password(
                    ClientId=self.client_id,
                    Username=email,
                    ConfirmationCode=code,
                    Password=new_password
                )
                return True

            except self.cognito.exceptions.CodeMismatchException:
                raise CodeMismatchError()

            except self.cognito.exceptions.ExpiredCodeException:
                raise ExpiredCodeError()

            except self.cognito.exceptions.InvalidPasswordException:
                raise InvalidPasswordError()
            
            except self.cognito.exceptions.UserNotFoundException:
                raise NoItemsFound('email')
            
            except ClientError as e:
                raise e