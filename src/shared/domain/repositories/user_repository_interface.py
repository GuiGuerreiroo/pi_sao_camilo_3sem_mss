from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        """
        If user not found return None
        """
        pass


    # for now don't need
    # @abstractmethod
    # def get_all_users(self) -> List[User]:
    #     pass

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        If user not found return None
        """
        pass

    @abstractmethod
    def create_user(self, new_user: User) -> Optional[User]:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> Optional[User]:
        """
        If user not found return None
        """
        pass

    @abstractmethod
    def update_user(
        self, 
        user_id: str, 
        name: str | None, 
        new_email: str | None,
        new_role: ROLE | None, 
        new_height: float | None
    ) -> Optional[User]:
        """
        If user not found return None
        """
        pass
