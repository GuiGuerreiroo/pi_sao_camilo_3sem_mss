from src.shared.helpers.errors.controller_errors import MissingItemsError
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from .update_group_usecase import UpdateGroupUseCase
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError

class UpdateGroupController:
    def __init__(self, usecase: UpdateGroupUseCase):
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

            group_id = request.data.get('group_id')
            if group_id is None:
                raise MissingParameters('group_id')

            if not isinstance(group_id, str):
                raise WrongTypeParameter('group_id', 'str', type(group_id))

            new_athlete_list_id = request.data.get('new_athlete_list_id')
            if new_athlete_list_id is not None:
                if not isinstance(new_athlete_list_id, list):
                    raise WrongTypeParameter('new_athlete_list_id', 'list', type(new_athlete_list_id))
                
                if len(new_athlete_list_id) == 0:
                    raise MissingItemsError('new_athlete_list_id', 'new_athlete_list_id should not be empty')
                
                for athlete_id in new_athlete_list_id:
                    if not isinstance(athlete_id, str):
                        raise WrongTypeParameter('new_athlete_list_id', 'str', type(athlete_id))

            new_supporter_list_id = request.data.get('new_supporter_list_id')
            if new_supporter_list_id is not None:
                if not isinstance(new_supporter_list_id, list):
                    raise WrongTypeParameter('new_supporter_list_id', 'list', type(new_supporter_list_id))
                
                if len(new_supporter_list_id) == 0:
                    raise MissingItemsError('new_supporter_list_id', 'new_supporter_list_id should not be empty')
                
                for supporter_id in new_supporter_list_id:
                    if not isinstance(supporter_id, str):
                        raise WrongTypeParameter('new_supporter_list_id', 'str', type(supporter_id))

            if new_athlete_list_id is None and new_supporter_list_id is None:
                raise MissingParameters("new_athlete_list_id or new_supporter_list_id must be provided (at least one)")

            updated_group, athletes_list, supporter_list = self.usecase(
                group_id=group_id,
                new_athlete_list_id=new_athlete_list_id,
                new_supporter_list_id=new_supporter_list_id,
            )

            viewmodel = {
                "group": {
                    "group_id": str(updated_group.group_id),
                    "athletes_list_id": [ athlete.model_dump(mode="json", exclude_none=True) for athlete in athletes_list],
                    "supporter_list_id": [ supporter.model_dump(mode="json", exclude_none=True) for supporter in supporter_list],
                },
                "message": "Group was updated successfully"
            }

            return OK(viewmodel)

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
