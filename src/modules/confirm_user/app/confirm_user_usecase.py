from src.shared.helpers.errors.usecase_errors import NoItemsFound
from botocore.exceptions import ClientError

from typing import Dict, Any
import boto3
from src.shared.environments import Environments
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class ConfirmUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
        
        self.client_id= Environments.get_envs().cognito_client_id
        self.region= Environments.get_envs().region
        self.cognito= boto3.client('cognito-idp', region_name= self.region)

    def __call__(
        self,
        email: str,
        code: str
    ):
        try:
            response= self.cognito.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=code
            )

            confirmed_user= self.repo.confirm_user_registration(email)

            if confirmed_user is None:
                raise NoItemsFound('email')

            return confirmed_user

        except ClientError as e:
            raise e
        