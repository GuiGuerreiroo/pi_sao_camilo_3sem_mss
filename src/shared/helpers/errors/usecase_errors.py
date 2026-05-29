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

class UserAlreadyConfirmedError(BaseError):
    def __init__(self, message: str = "Usuário já foi confirmado."):
        super().__init__(message)

class UserNeedsConfirmationError(BaseError):
    def __init__(self, message: str = "O usuário precisa ser confirmado."):
        super().__init__(message)


class DataIngestionError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Data ingestion failed: {message}')

class BedrockIntegrationError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Error generating AI analysis: {message}')

class CognitoNotAuthorizedError(BaseError):
    def __init__(self, message: str = "Invalid or expired access token, or incorrect old password."):
        super().__init__(message)

class CognitoInvalidPasswordError(BaseError):
    def __init__(self, message: str = "New password does not meet security requirements."):
        super().__init__(message)

class CodeMismatchError(BaseError):
    def __init__(self, message: str = "Invalid verification code provided, please try again."):
        super().__init__(message)

class ExpiredCodeError(BaseError):
    def __init__(self, message: str = "Invalid code provided, please request a code again."):
        super().__init__(message)

class InvalidPasswordError(BaseError):
    def __init__(self, message: str = "Invalid password format. Password must meet security requirements."):
        super().__init__(message)