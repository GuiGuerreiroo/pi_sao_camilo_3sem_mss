from src.shared.helpers.external_interfaces.http_codes import Forbidden
from botocore.exceptions import ClientError
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .auth_user_usecase import AuthUserUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

class AuthUserController:

    def __init__(self, usecase: AuthUserUseCase):
        self.AuthUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            email= request.data.get('email')

            if email is None:
                raise MissingParameters('email')

            if not isinstance(email, str):
                raise WrongTypeParameter('email', 'str', f"{type(email)}")

            password= request.data.get('password')

            if password is None:
                raise MissingParameters('password')

            if not isinstance(password, str):
                raise WrongTypeParameter('password', 'str', f"{type(password)}")

            result= self.AuthUserUseCase(
                email=email,
                password=password
            )

            response = OK(result)

            return response

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except ClientError as err:
            code = err.response.get('Error', {}).get('Code')
            message = err.response.get('Error', {}).get('Message', str(err))

            if code in ['NotAuthorizedException', 'UserNotFoundException']:
                return Forbidden(body={'message': 'Token de atualização inválido ou expirado'})
            if code == 'UserNotConfirmedException':
                return Forbidden(body={'message': 'Usuário não confirmado'})
            if code in ['TooManyRequestsException', 'LimitExceededException']:
                return Forbidden(body={'message': 'Muitas tentativas. Tente novamente mais tarde'})
            if code in ['InvalidParameterException', 'InvalidSmsRoleAccessPolicyException', 'InvalidSmsRoleTrustRelationshipException']:
                return BadRequest(body=message)

            return InternalServerError(body=message)

        except Exception as err:
            return InternalServerError(body=str(err))