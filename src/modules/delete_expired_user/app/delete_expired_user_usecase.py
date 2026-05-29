from src.shared.environments import Environments
import boto3

class DeleteExpiredUserUseCase:

    def __init__(self):
        self.region = Environments.get_envs().region
        self.user_pool_id =  Environments.get_envs().cognito_user_pool_id
        self.client = boto3.client('cognito-idp', region_name=self.region)

    def __call__(
        self,
        emails_to_be_deleted: list[str]
    ):
        deleted_emails=[]

        for email in emails_to_be_deleted:
            try:
                self.client.admin_delete_user(
                    UserPoolId=self.user_pool_id,
                    Username=email
                )

                deleted_emails.append(email)

            except self.client.exceptions.UserNotFoundException:
                # If user is already deleted or never existed, it's safe to ignore
                deleted_emails.append(email)

            except Exception as e:
                print(f"CRITICAL: Failed to delete {email}. Error: {str(e)}")
                raise e

        return deleted_emails