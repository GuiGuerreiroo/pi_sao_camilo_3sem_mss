from .delete_expired_user_usecase import DeleteExpiredUserUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters

class DeleteExpiredUserController:
    def __init__(self, usecase: DeleteExpiredUserUseCase):
        self.DeleteExpiredUserUseCase = usecase

    def __call__(self, request: dict) -> dict:
        records = request.get('Records', [])
        emails_to_be_deleted = []

        for record in records:
            email = record.get('dynamodb', {}).get('OldImage', {}).get('email', {}).get('S')

            if email:
                emails_to_be_deleted.append(email)
            else:
                raise MissingParameters('email')
                
        viewmodel = {
            'message': 'No expired users found in this batch to delete.'
        }
            
        if len(emails_to_be_deleted) > 0:
            result = self.DeleteExpiredUserUseCase(emails_to_be_deleted)

            viewmodel['message'] = 'Every user deleted in Dynamo DB was deleted in Cognito'
            viewmodel['deleted_emails'] = result

        return viewmodel