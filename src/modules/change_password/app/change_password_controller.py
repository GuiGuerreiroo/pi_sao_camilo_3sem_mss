from src.shared.helpers.errors.usecase_errors import NoItemsFound, CodeMismatchError, ExpiredCodeError, InvalidPasswordError
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Gone, Forbidden
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from .change_password_usecase import ChangePasswordUseCase

class ChangePasswordController:
    def __init__(self, usecase: ChangePasswordUseCase):
        self.ChangePasswordUseCase = usecase

    def __call__(self, http_request):
        try:
            email = http_request.data.get('email')

            if email is None:
                raise MissingParameters('email')
            
            if not isinstance(email, str):
                raise WrongTypeParameter('email', 'str', f"{type(email)}")
            
            code = http_request.data.get('code')

            if code is None:
                raise MissingParameters('code')
            
            if not isinstance(code, str):
                raise WrongTypeParameter('code', 'str', f"{type(code)}")
            
            new_password = http_request.data.get('new_password')
            
            if new_password is None:
                raise MissingParameters('new_password')
            
            if not isinstance(new_password, str):
                raise WrongTypeParameter('new_password', 'str', f"{type(new_password)}")
            
            result = self.ChangePasswordUseCase(
                email=email,
                code=code,
                new_password=new_password
            )

            viewmodel = {
                'message': 'Senha alterada com sucesso!'
            }

            return OK(viewmodel)
        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        
        except NoItemsFound as err:
            return NotFound(body=err.message)

        except (CodeMismatchError, ExpiredCodeError, InvalidPasswordError) as err:
                return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))