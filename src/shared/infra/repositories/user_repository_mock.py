import time
from src.shared.domain.enums.status_user_enum import USERSTATUS
from typing import List, Optional
import uuid

from src.shared.domain.entities.user import User

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    users: List[User]
    future_time = int(time.time()) + (24 * 60 * 60)

    def __init__(self):
        self.users = [
            User(
                user_id="550e8400-e29b-41d4-a716-446655440002",
                name="Guilherme",
                email="25.00178-5@maua.br", 
                role=ROLE.USER,
                height= 1.80,
                status=USERSTATUS.CONFIRMED, 
                expires_at=None              
            ),
            User(
                user_id="550e8400-e29b-41d4-a716-446655440001",
                name="João",
                email="21.00678-2@maua.br", 
                role=ROLE.ADM,
                status=USERSTATUS.CONFIRMED, 
                expires_at=None           
            ),
            User(
                user_id="cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a",
                name="Heitor", 
                email="21.00453-7@maua.br", 
                role=ROLE.USER, 
                height= 1.75,   
                status=USERSTATUS.UNCONFIRMED, 
                expires_at=self.future_time      
            ),
            User(
                user_id=str(uuid.uuid4()),
                name="Bruno", 
                email="21.00458-7@maua.br", 
                role=ROLE.USER,
                height= 1.83,
                status=USERSTATUS.UNCONFIRMED, 
                expires_at=self.future_time      
            ),
            User(
                user_id="e0cce9ad-e3ec-41f0-8600-812198c49450",
                name="Pedro", 
                email="20.00789-4@maua.br", 
                role=ROLE.SUPPORT, 
                status=USERSTATUS.CONFIRMED, 
                expires_at=None              
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

    def get_all_users(self) -> List[User]:
        return self.users.copy()
    
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
        new_height: float | None
    ) -> Optional[User]:
        for user in self.users:
            if user.user_id == str(user_id):
                if name is not None:
                    user.name = name
                if new_height is not None:
                    user.height = new_height
                return user
        return None

    def confirm_user_registration(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email == email:
                user.status = USERSTATUS.CONFIRMED
                user.expires_at = None

                return user
        return None
