from .create_user_cognito_controler import CreateUserCognitoController
from .create_user_cognito_usecase import CreateUserCognitoUseCase
from src.shared.environments import Environments

repo= Environments.get_user_repo()

usecase= CreateUserCognitoUseCase(repo)

controller= CreateUserCognitoController(usecase)

def lambda_handler(event, contex):
    print(event)

    response= controller(event)

    if response and hasattr(response, 'status_code') and response.status_code >= 400:
       error_msg = f"Failed to create user in DynamoDB: {response.body}"
       print(error_msg)
       raise Exception(error_msg)

    print("Registered with success")
    return event