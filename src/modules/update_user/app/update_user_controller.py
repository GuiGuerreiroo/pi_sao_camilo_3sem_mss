from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if not isinstance(requester_user.user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(requester_user.user_id))

            new_name = request.data.get('new_name')
            if new_name is not None:
                if not isinstance(new_name, str):
                    raise WrongTypeParameter('new_name', 'str', type(new_name))
            
            new_email = request.data.get('new_email')
            if new_email is not None:   
                if not isinstance(new_email, str):
                    raise WrongTypeParameter('new_email', 'str', type(new_email))

            # won't be allowed to change ROLE

            new_height = request.data.get('new_height')
            if new_height is not None:
                if not isinstance(new_height, float):
                    if isinstance(new_height, int):
                        new_height = float(new_height)
                    else:
                        raise WrongTypeParameter('new_height', 'float', type(new_height))

            user = self.UpdateUserUsecase(
                user_id=requester_user.user_id, 
                new_name=new_name,
                new_email=new_email,
                new_height=new_height
            )

            viewmodel = {
                'user': user.model_dump(mode='json', exclude_none=True),
                'message': 'the user was updated successfully'
            }

            return OK(viewmodel)

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=str(err))
