from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, CognitoNotAuthorizedError, CognitoInvalidPasswordError
from src.shared.helpers.external_interfaces.http_codes import OK, Forbidden, NotFound, BadRequest, InternalServerError


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
            
        
            access_token = request.data.get('access_token')
            if access_token is not None:
                if not isinstance(access_token, str):
                    raise WrongTypeParameter('access_token', 'str', type(access_token))

            new_height = request.data.get('new_height')
            if new_height is not None:
                # if the user is from ROLE USER he has the height field
                if requester_user.role == ROLE.USER.value:
                    if not isinstance(new_height, float):
                        if isinstance(new_height, int):
                            new_height = float(new_height)
                        else:
                            raise WrongTypeParameter('new_height', 'float', type(new_height))
                        
                    if new_height <= 0:
                        raise WrongTypeParameter('new_height', 'positive float', new_height)
                else:
                    raise ForbiddenAction('user that doesn\'t have height to update')

            new_name = request.data.get('new_name')
            if new_name is not None:
                if not isinstance(new_name, str):
                    raise WrongTypeParameter('new_name', 'str', type(new_name))
                
                if len(new_name) == 0:
                    raise WrongTypeParameter('new_name', 'non-empty str', 'empty str')
                
                if len(new_name) < 3:
                    raise WrongTypeParameter('new_name', 'str with at least 3 characters', 'str with less than 3 characters')

                if access_token is None:
                    raise MissingParameters('access_token')
                
            # won't be allowed to change ROLE
                    
            old_password = request.data.get('old_password')
            if old_password is not None:
                if not isinstance(old_password, str):
                    raise WrongTypeParameter('old_password', 'str', type(old_password))
                
            new_password = request.data.get('new_password')
            if new_password is not None:
                if not isinstance(new_password, str):
                    raise WrongTypeParameter('new_password', 'str', type(new_password))
                
                if len(new_password) < 6:
                    raise WrongTypeParameter('new_password', 'str with at least 6 characters', 'str with less than 6 characters')

            # this line bellow validates if 3 of the parameters are provided together
            auth_fields = [old_password, new_password]
            if any(auth_fields):
                if not (old_password and new_password and access_token):
                    raise MissingParameters('old_password, new_password and access_token must be provided together, some of them')


            user = self.UpdateUserUsecase(
                user_id=requester_user.user_id, 
                new_name=new_name,
                new_height=new_height,
                old_password=old_password,
                new_password=new_password,
                access_token=access_token
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
        
        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except CognitoNotAuthorizedError as err:
            return Forbidden(body=err.message)

        except CognitoInvalidPasswordError as err:
            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=str(err))
