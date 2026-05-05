from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.entities.group import Group
from typing import List
from src.shared.domain.repositories.group_repository_interface import IGroupRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class UpdateGroupUseCase:
    def __init__(self, repo: IGroupRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(
        self, 
        group_id: str,
        new_supporter_list_id: List[str] | None, 
        new_athlete_list_id: List[str] | None
    ):
    
        athletes_list = []
        supporter_list = []

        if new_athlete_list_id is not None:
            for athlete in new_athlete_list_id:
                athlete= self.user_repo.get_user(athlete)
                
                if athlete is None:
                    raise NoItemsFound("athlete not in DB")

                if athlete.role != ROLE.USER:
                    raise ForbiddenAction("athlete role must be USER")
                athletes_list.append(athlete)

        if new_supporter_list_id is not None:
            for supporter in new_supporter_list_id:
                supporter= self.user_repo.get_user(supporter)

                if supporter is None:
                    raise NoItemsFound("supporter not in DB")

                if supporter.role != ROLE.SUPPORT:
                    raise ForbiddenAction("supporter role must be SUPPORTER")

                supporter_list.append(supporter)
                    
        updated_group = self.repo.update_group(
            group_id=group_id,
            new_supporter_list_id=new_supporter_list_id,
            new_athlete_list_id=new_athlete_list_id
        )

        if updated_group is None:
            raise NoItemsFound("group")

        return updated_group, athletes_list, supporter_list
