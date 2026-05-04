from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK,NotFound, BadRequest, InternalServerError, Forbidden
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from .get_all_trainings_usecase import GetAllTrainingsUseCase

class GetAllTrainingsController:
    
    def __init__(self, usecase: GetAllTrainingsUseCase):
        self.GetAllTrainingsUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse: 
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if not isinstance(requester_user.user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(requester_user.user_id))

            if requester_user.role != ROLE.USER.value:
                raise ForbiddenAction("user")

            trainings_list = self.GetAllTrainingsUseCase(user_id=requester_user.user_id)

            viewmodel= {
                'trainings': [training.model_dump(mode='json', exclude_none=True) for training in trainings_list],
                'message': 'Trainings returned successfully'
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
        