from typing import List, Optional
import uuid

from src.shared.domain.entities.user import User

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(
                name="Guilherme",
                email="25.00178-5@maua.br", 
                role=ROLE.USER
            ),
            User(
                user_id="550e8400-e29b-41d4-a716-446655440001",
                name="João",
                email="21.00678-2@maua.br", 
                role=ROLE.ADM
            ),
            User(
                name="Heitor", 
                email="21.00453-7@maua.br", 
                role=ROLE.USER, 
            ),
            User(
                user_id=str(uuid.uuid4()),
                name="Bruno", 
                email="21.00458-7@maua.br", 
                role=ROLE.USER
            ),
            User(
                name="Pedro", 
                email="20.00789-4@maua.br", 
                role=ROLE.ADM, 
            )
        ]

    def get_user(self, user_id: str) -> Optional[User]:
        for user in self.users:
            if user.user_id == str(user_id):
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email == email:
                return user
        return None

    # def get_all_users(self) -> List[User]:
    #     return self.users.copy()
    
    def create_user(self, new_user: User) -> Optional[User]:
        self.users.append(new_user)
        return new_user

    def delete_user(self, user_id: str) -> Optional[User]:
        for pos, user in enumerate(self.users):
            if user.user_id == str(user_id):
                self.users.pop(pos)
                return user
        return None

    def update_user(
        self,
        user_id: str, 
        name: str | None, 
        new_email: str | None,
        new_role: ROLE | None, 
        new_height: float | None
    ) -> Optional[User]:
        for user in self.users:
            if user.user_id == str(user_id):
                if name is not None:
                    user.name = name
                if new_email is not None:
                    user.email = new_email
                if new_role is not None:
                    user.role = new_role
                if new_height is not None:
                    user.height = new_height
                return user
        return None
