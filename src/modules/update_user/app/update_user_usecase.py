import boto3
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound, CognitoNotAuthorizedError, CognitoInvalidPasswordError


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
        self.cognito_client = boto3.client('cognito-idp')

    def __call__(
        self, 
        user_id: str, 
        new_name: str | None = None, 
        new_height: float | None = None,
        old_password: str | None = None,
        new_password: str | None = None,
        access_token: str | None = None
    ) -> User:
        
        if access_token:
            try: 
                if new_name:
                    self.cognito_client.update_user_attributes(
                        AccessToken=access_token,
                        UserAttributes=[
                            {'Name': 'name', 'Value': new_name}
                        ]
                    )

                if old_password and new_password:
                    self.cognito_client.change_password(
                        PreviousPassword=old_password,
                        ProposedPassword=new_password,
                        AccessToken=access_token
                    )

            except self.cognito_client.exceptions.NotAuthorizedException:
                raise CognitoNotAuthorizedError()
        
            except self.cognito_client.exceptions.InvalidPasswordException as e:
                raise CognitoInvalidPasswordError()
            
            except ClientError as e:
                raise Exception(f"Cognito error: {str(e)}")

        updated_user = self.repo.update_user(
            user_id=user_id, 
            name=new_name,
            new_height=new_height
        )

        if updated_user is None:
            raise NoItemsFound("user_id")
        
        return updated_user
