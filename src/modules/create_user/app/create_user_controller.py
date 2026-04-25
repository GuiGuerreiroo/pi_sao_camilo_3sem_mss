from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_user_usecase import CreateUserUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, DuplicatedItem, UnconfirmedUserError
from src.shared.helpers.external_interfaces.http_codes import Created, NotFound, BadRequest, InternalServerError, Conflict

class CreateUserController:

    def __init__(self, usecase: CreateUserUseCase):
        self.CreateUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            email= request.data.get('email')

            if email is None:
                raise MissingParameters('email')

            if not isinstance(email, str):
                raise WrongTypeParameter('email', 'str', f"{type(email)}")
            
            name= request.data.get('name')

            if name is None:
                raise MissingParameters('name')

            if not isinstance(name, str):
                raise WrongTypeParameter('name', 'str', f"{type(name)}")

            password= request.data.get('password')

            if password is None:
                raise MissingParameters('password')

            if not isinstance(password, str):
                raise WrongTypeParameter('password', 'str', f"{type(password)}")

            role_str= request.data.get('role')

            if role_str is None: 
                raise MissingParameters('role')

            try:
                role_enum= ROLE(role_str)

            except ValueError:
                raise WrongTypeParameter("role", f"one of {[role.name for role in ROLE]}", role_str
                )

            if role_enum == ROLE.USER:  
                height= request.data.get('height')

                if height is None:
                    raise MissingParameters('height')

                if not isinstance(height, float):
                    raise WrongTypeParameter('height', 'float', type(height))

            user= self.CreateUserUseCase(
                email=email,
                name=name,
                password=password,
                role=role_enum,
                height=height
            )

            viewmodel = {
                'user': user.model_dump(mode='json', exclude_none=True),
                'message': 'User successfully created'
            }

            response = Created(viewmodel)
            
            return response

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except (DuplicatedItem, UnconfirmedUserError) as err:
            return Conflict(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))
