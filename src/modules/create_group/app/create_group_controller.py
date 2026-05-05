from src.shared.domain.entities.user import User
from src.shared.helpers.errors.controller_errors import MissingItemsError
from ast import List
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from .create_group_usecase import CreateGroupUseCase
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import Created,NotFound, BadRequest, InternalServerError, Forbidden
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError

class CreateGroupController:
    def __init__(self, usecase: CreateGroupUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if not isinstance(requester_user.user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(requester_user.user_id))

            if requester_user.role != ROLE.ADM.value:
                raise ForbiddenAction("user")

            athletes_list_id = request.data.get('athletes_list_id')

            if athletes_list_id is None:
                raise MissingParameters('athletes_list_id')

            if not isinstance(athletes_list_id, list):
                raise WrongTypeParameter('athletes_list_id', 'list', type(athletes_list_id))

            if len(athletes_list_id) == 0:
                raise MissingItemsError('athletes_list_id', 'athletes_list_id should not be empty')
            
            for athlete_id in athletes_list_id:
                if not isinstance(athlete_id, str):
                    raise WrongTypeParameter('athletes_list_id', 'str', type(athlete_id))

            supporter_list_id = request.data.get('supporter_list_id')

            if supporter_list_id is None:
                raise MissingParameters('supporter_list_id')

            if not isinstance(supporter_list_id, list):
                raise WrongTypeParameter('supporter_list_id', 'list', type(supporter_list_id))
            
            if len(supporter_list_id) == 0:
                raise MissingItemsError('supporter_list_id', 'supporter_list_id should not be empty')
            
            for supporter_id in supporter_list_id:
                if not isinstance(supporter_id, str):
                    raise WrongTypeParameter('supporter_list_id', 'str', type(supporter_id))

            new_group, athletes_list, supporter_list = self.usecase(
                athletes_list_id=athletes_list_id,
                supporter_list_id=supporter_list_id,
            )

            viewmodel= {
                "group": {
                    "group_id": str(new_group.group_id),
                    "athletes_list_id": [ athlete.model_dump(mode="json", exclude_none=True) for athlete in athletes_list],
                    "supporter_list_id": [ supporter.model_dump(mode="json", exclude_none=True) for supporter in supporter_list],
                },
                "message": "Group created successfully"
            }

            return Created(viewmodel)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except MissingItemsError as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))