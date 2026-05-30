from typing import List
from typing import Optional
from src.shared.domain.entities.group import Group
from abc import ABC, abstractmethod

class IGroupRepository(ABC):
    
    @abstractmethod
    def create_group(self, new_group: Group) -> Optional[Group]:
        pass

    @abstractmethod
    def get_group(self, group_id: str) -> Optional[Group]:
        """
        If group not found return None
        """
        pass

    @abstractmethod
    def get_all_groups(self) -> List[Group]:
        pass

    @abstractmethod
    def get_all_groups_by_supporter_id(self, supporter_id: str) -> List[Group]:
        pass

    @abstractmethod
    def update_group(self, group_id: str, new_supporter_list_id: List[str] | None, new_athlete_list_id: List[str] | None) -> Optional[Group]:
        """
        If group not found return None
        """
        pass

    @abstractmethod
    def delete_group(self, group_id: str) -> Optional[Group]:
        """
        If group not found return None
        """
        pass