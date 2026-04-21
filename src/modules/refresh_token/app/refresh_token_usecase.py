from botocore.exceptions import ClientError
import boto3
from src.shared.environments import Environments
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class RefreshTokenUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
        
        self.client_id= Environments.get_envs().cognito_client_id
        self.region= Environments.get_envs().region
        self.cognito= boto3.client('cognito-idp', region_name= self.region)

    def __call__(
        self,
        refresh_token
    ) -> dict :
        try:
            response= self.cognito.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters= {
                    "REFRESH_TOKEN": refresh_token
                }
            )

            if "AuthenticationResult" in response and response["AuthenticationResult"] is not None:
                result= response["AuthenticationResult"]

                return {
                    "id_token": result.get("IdToken"),
                    "access_token": result.get("AccessToken"),
                    "refresh_token": result.get("RefreshToken"),
                    "expires_in": result.get("ExpiresIn"),
                    "token_type": result.get("TokenType"),
                }
            return {
                "challenge_name": response.get("ChallengeName"),
                "session": response.get("Session"),
            }
    
        except ClientError as e:
            raise e