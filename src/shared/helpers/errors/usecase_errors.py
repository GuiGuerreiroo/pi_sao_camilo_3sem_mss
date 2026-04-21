from src.shared.helpers.errors.base_error import BaseError

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'No items found for {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The item alredy exists for this {message}')
        
class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(f'That action is forbidden for this {message}')

class IsNotInstanceOfUuid4(BaseError):
    def __init(self, message: str):
        super().__init__(f'the {message} is not an instance of uuid4')

class UnconfirmedUserError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The user {message} is unconfirmed. A new verification code was sent.')

class UserExpiredError(BaseError):
    def __init__(self, message: str = "Seu tempo de ativação expirou por segurança. Por favor, cadastre-se novamente."):
        super().__init__(message)