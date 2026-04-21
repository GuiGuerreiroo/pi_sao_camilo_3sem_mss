from src.shared.domain.enums.status_user_enum import USERSTATUS
from botocore.exceptions import ClientError
import boto3
import time
from src.shared.environments import Environments
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, UnconfirmedUserError

class CreateUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo= repo

        self.client_id= Environments.get_envs().cognito_client_id
        self.region= Environments.get_envs().region
        self.cognito= boto3.client('cognito-idp', region_name= self.region)

    def __call__(
        self,
        email: str,
        name: str,
        password: str,
        role: ROLE,
        height: float | None= None
    ):
        try:
            response= self.cognito.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'name', 'Value': name},
                    {'Name': 'email', 'Value': email},
                    {'Name': 'role', 'Value': role.value}
                ]
            )
            user_id= response['UserSub']

        except self.cognito.exceptions.UsernameExistsException:
            raise DuplicatedItem(email)

        except ClientError as e:
            raise e

        # just for test latter should be 24 hours
        future_time = int(time.time()) + (24 * 60 * 60)

        user= User(
            user_id= user_id,
            name= name,
            email= email,
            role=role,
            height=height,
            status=USERSTATUS.UNCONFIRMED,
            expires_at=future_time
        )

        return self.repo.create_user(user)