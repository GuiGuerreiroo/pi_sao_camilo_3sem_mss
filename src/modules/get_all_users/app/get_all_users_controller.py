from typing import List
from src.shared.helpers.external_interfaces.external_interface import IRequest
from .get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import NotFound, OK, BadRequest, InternalServerError, Forbidden


class GetAllUsersController:
    def __init__(self, usecase: GetAllUsersUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if requester_user.role != ROLE.ADM.value:
                raise ForbiddenAction('user')

            all_users_list: List[User] = self.usecase()

            viewmodel = {
                'users': [user.model_dump(mode='json', exclude_none=True) for user in all_users_list],
                'message': 'All users has been retrieved'
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

        except ForbiddenAction as err:

            return Forbidden(body=err.message)

        except Exception as err:

            return InternalServerError(body=str(err))
