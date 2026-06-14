from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from .export_trainings_usecase import ExportTrainingsUseCase
import json

class ExportTrainingsController:
    def __init__(self, usecase: ExportTrainingsUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse: 
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if not isinstance(requester_user.user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(requester_user.user_id))

            if requester_user.role != ROLE.SUPPORT.value:
                raise ForbiddenAction("supporter")

            athlete_id = request.data.get("athlete_id")
            training_id_list = request.data.get("training_id_list")

            if not athlete_id:
                raise MissingParameters("athlete_id")
            
            if not isinstance(athlete_id, str):
                raise WrongTypeParameter("athlete_id", "str", type(athlete_id))
            
            if not training_id_list:
                raise MissingParameters("training_id_list")
            
            for training_id in training_id_list:
                if not isinstance(training_id, str):
                    raise WrongTypeParameter("training_id_list item", "str", type(training_id))
            
            if not isinstance(training_id_list, list):
                raise WrongTypeParameter("training_id_list", "list", type(training_id_list))

            base64_pdf = self.usecase(
                athlete_id=athlete_id, 
                training_id_list=training_id_list, 
                requester_user_id=requester_user.user_id,
                requester_name=requester_user.name
            )

            headers = {
                "Content-Type": "application/pdf",
                "Content-Disposition": "attachment; filename=relatorio_treinos.pdf"
            }
            
            response = OK(base64_pdf)
            response.headers = headers
            return response

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
