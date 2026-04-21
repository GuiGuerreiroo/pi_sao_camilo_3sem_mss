from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import NoItemsFound, UserExpiredError, UserAlreadyConfirmedError
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Gone, Forbidden
from .resend_code_usecase import ResendCodeUseCase

class ResendCodeController:
    def __init__(self, usecase: ResendCodeUseCase):
        self.ResendCodeUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try: 
            email= request.data.get('email')

            if email is None:
                raise MissingParameters('email')

            if not isinstance(email, str):
                raise WrongTypeParameter('email', 'str', f"{type(email)}")

            result= self.ResendCodeUseCase(
                email=email
            )

            viewmodel = {
                'message': 'Código reenviado com sucesso!'
            }

            response = OK(viewmodel)

            return response

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except UserExpiredError as err:
            return Gone(body=err.message)

        except UserAlreadyConfirmedError as err:
            return Forbidden(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))