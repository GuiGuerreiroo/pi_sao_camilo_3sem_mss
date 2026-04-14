from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class CreateUserCognitoUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo= repo

    def __call__(
        self, 
        user_id: str,
        email: str,
        name: str,
        role: ROLE,
        height: float | None= None
    ):
        
        if self.repo.get_user_by_email(email) is not None:
            raise DuplicatedItem(email)
        
        match role:
                case ROLE.USER:
                    user= User(
                        user_id= user_id,
                        name= name,
                        role=role,
                        height=height
                    )
                    

                case ROLE.SUPPORT:
                    user= User(
                        user_id= user_id,
                        name= name,
                        role=role,
                    )

        if not user:
            raise Exception

        self.repo.create_user(user)