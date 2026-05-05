from src.shared.helpers.external_interfaces.http_codes import OK
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.modules.get_all_groups_by_supporter.app.get_all_groups_by_supporter_usecase import GetAllGroupsBySupporterUseCase
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import NotFound, BadRequest, InternalServerError, Forbidden
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError

class GetAllGroupsBySupporterController:
    def __init__(self, usecase: GetAllGroupsBySupporterUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if not isinstance(requester_user.user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(requester_user.user_id))

            if requester_user.role != ROLE.SUPPORT.value:
                raise ForbiddenAction("user")

            groups= self.usecase(
                user_id=requester_user.user_id
            )

            viewmodel = {
                "groups": [
                    {
                        "group_id": str(group_id),
                        "athletes_list_id": [athlete.model_dump(mode="json", exclude_none=True) for athlete in group_data["athletes_list_id"]],
                        "supporter_list_id": [supporter.model_dump(mode="json", exclude_none=True) for supporter in group_data["supporter_list_id"]],
                    }
                    for group_id, group_data in groups.items()
                ],
                "message": "Trainings athletes linked to the supporter retrieved successfully"
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