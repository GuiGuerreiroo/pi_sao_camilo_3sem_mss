from src.shared.domain.enums.status_user_enum import USERSTATUS
from src.shared.helpers.errors.usecase_errors import UserExpiredError, UserAlreadyConfirmedError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from botocore.exceptions import ClientError
import boto3
from src.shared.environments import Environments
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class ResendCodeUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

        self.user_pool_id = Environments.get_envs().cognito_user_pool_id
        self.client_id = Environments.get_envs().cognito_client_id
        self.region= Environments.get_envs().region
        self.cognito= boto3.client('cognito-idp', region_name= self.region)

    def __call__(
        self,
        email: str
    ):
        user = self.repo.get_user_by_email(email)

        if user and user.status == USERSTATUS.UNCONFIRMED:
            try:
                self.cognito.resend_confirmation_code(
                    ClientId=self.client_id,
                    Username=email
                )
                return True

            except ClientError as e:
                raise e
        
        elif user and user.status == USERSTATUS.CONFIRMED:
            raise UserAlreadyConfirmedError()

        else:
            try:
                self.cognito.admin_delete_user(
                    UserPoolId=self.user_pool_id,
                    Username=email
                )

            except self.cognito.exceptions.UserNotFoundException:
                pass

            except ClientError as e:
                raise e

            # erro para falar que seu usuario foi deletado do banco e precisa se registrar novamente
            raise UserExpiredError()
    