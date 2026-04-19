from src.shared.environments import Environments
import uuid
from .create_user_cognito_usecase import CreateUserCognitoUseCase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, IsNotInstanceOfUuid4, NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Conflict, Forbidden, InternalServerError, NotFound
import os

class CreateUserCognitoController:

    def __init__(self, usecase: CreateUserCognitoUseCase):
        self.usecase= usecase

    def __call__(self, event: dict):
        try:
            if event.get('triggerSource') != "PostConfirmation_ConfirmSignUp": 
                return
            
            user_attributes= event['request']['userAttributes']

            # id unico gerado pelo cognito
            user_id= user_attributes.get('sub')

            if user_id is None:
                raise MissingParameters('user_id')
            
            try:
                uuid.UUID(user_id)

            except ValueError:
                raise IsNotInstanceOfUuid4('user_id')

            email= user_attributes.get('email')

            if email is None:
                raise MissingParameters('email')
            
            name= user_attributes.get('name')

            if name is None:
                raise MissingParameters('name')
            

            # accessing the arguments that were send through the clientMetadata from the frontend

            client_metadata= event['request'].get('clientMetadata', {})

            role_str= client_metadata.get('role')

            try:
                role_enum= ROLE(role_str)
            
            except ValueError:
                raise WrongTypeParameter(
                    fieldName="role",
                    fieldTypeExpected=f"one of {[role.name for role in ROLE]}",
                    fieldTypeReceived=role_str
                )
            
            match role_enum:
                case ROLE.USER:
                    height= client_metadata.get('height')

                    if height is None:
                        raise MissingParameters('height')
                    
                    try: 
                        height_float = float(height)
                
                    except ValueError:
                        raise WrongTypeParameter(
                            fieldName='height', 
                            fieldTypeExpected='float', 
                            fieldTypeReceived=height
                        )
                    
                    self.usecase(
                        user_id=user_id,
                        email=email,
                        name=name,
                        role=role_enum,
                        height=height_float
                    )

                case ROLE.SUPPORT:

                    self.usecase(
                        user_id=user_id,
                        email=email,
                        name=name,
                        role=role_enum
                    )    

                case ROLE.ADM:
                    raise ForbiddenAction("administrator role")
        
        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except DuplicatedItem as err:
            return Conflict(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)
        
        except IsNotInstanceOfUuid4 as err:
            return BadRequest(body=err.message)
        
        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))