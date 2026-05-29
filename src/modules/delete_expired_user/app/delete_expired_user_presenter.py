from .delete_expired_user_usecase import DeleteExpiredUserUseCase
from .delete_expired_user_controller import DeleteExpiredUserController

usecase = DeleteExpiredUserUseCase()
controller = DeleteExpiredUserController(usecase)

def lambda_handler(event: dict, context: object) -> dict:
    print(event)

    records = event.get('Records')

    if not records or not isinstance(records, list):
        raise ValueError("Invalid event format. Expected a list of Records from DynamoDB.")
    
    if records[0].get("eventSource") != "aws:dynamodb":
        raise ValueError("Invalid event source. Expected aws:dynamodb Stream event.")
    
    response = controller(event)

    return response


# THE PRESENTER IS FOLLOWING THIS STRUCTURE OF RAISING ERROR BECAUSE THIS IS THE WAY TO TELLING THE LAMBDA TO RETRY THE EVENT