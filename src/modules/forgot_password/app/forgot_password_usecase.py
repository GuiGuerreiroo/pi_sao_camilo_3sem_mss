from src.shared.domain.enums.status_user_enum import USERSTATUS
from src.shared.helpers.errors.usecase_errors import UserExpiredError, UserAlreadyConfirmedError, UserNeedsConfirmationError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from botocore.exceptions import ClientError
import boto3
from src.shared.environments import Environments
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class ForgotPasswordUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo= repo

        self.user_pool_id = Environments.get_envs().cognito_user_pool_id
        self.client_id = Environments.get_envs().cognito_client_id
        self.region= Environments.get_envs().region
        self.cognito= boto3.client('cognito-idp', region_name= self.region)
       
    def __call__(
            self, 
            email: str
        ):
            user = self.repo.get_user_by_email(email)

            # only confirmed users can reset password
            if user and user.status == USERSTATUS.CONFIRMED:
                try:
                    self.cognito.forgot_password(
                        ClientId=self.client_id,
                        Username=email
                    )
                    return True

                except ClientError as e:
                    raise e
                
            elif user and user.status == USERSTATUS.UNCONFIRMED:
                raise UserNeedsConfirmationError()