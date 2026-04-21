from src.shared.helpers.external_interfaces.http_codes import Forbidden
from botocore.exceptions import ClientError
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .confirm_user_usecase import ConfirmUserUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

class ConfirmUserController:
    def __init__(self, usecase: ConfirmUserUseCase):
        self.ConfirmUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try: 
            email= request.data.get('email')

            if email is None:
                raise MissingParameters('email')

            if not isinstance(email, str):
                raise WrongTypeParameter('email', 'str', f"{type(email)}")

            code= request.data.get('code')

            if code is None:
                raise MissingParameters('code')

            if not isinstance(code, str):
                raise WrongTypeParameter('code', 'str', f"{type(code)}")

            result= self.ConfirmUserUseCase(
                email=email,
                code=code
            )

            viewmodel = {
                'user': result.model_dump(mode='json'),
                'message': 'Conta ativada com sucesso!'
            }

            response = OK(viewmodel)

            return response

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ClientError as err:
            aws_code = err.response.get('Error', {}).get('Code')
            message = err.response.get('Error', {}).get('Message', str(err))

            if aws_code == 'CodeMismatchException':
                return BadRequest(body='Código de verificação incorreto.')
            if aws_code == 'ExpiredCodeException':
                return BadRequest(body='O código expirou. Solicite um novo.')
            if aws_code == 'LimitExceededException':
                return Forbidden(body='Muitas tentativas erradas. Tente mais tarde.')
            if aws_code == 'NotAuthorizedException':
                return Forbidden(body='Usuário já foi confirmado.')

            return InternalServerError(body=message)

        except Exception as err:
            return InternalServerError(body=str(err))
        