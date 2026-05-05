from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.entities.group import Group
from typing import List
from src.shared.domain.repositories.group_repository_interface import IGroupRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class CreateGroupUseCase:
    def __init__(self, repo: IGroupRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(
        self, 
        athletes_list_id: List[str], 
        supporter_list_id: List[str]
    ):

        athletes_list = []
        supporter_list = []

        for athlete in athletes_list_id:
            athlete= self.user_repo.get_user(athlete)
            
            if athlete is None:
                raise NoItemsFound("athlete not in DB")

            if athlete.role != ROLE.USER:
                raise ForbiddenAction("athlete role must be USER")
            athletes_list.append(athlete)

        for supporter in supporter_list_id:
            supporter= self.user_repo.get_user(supporter)

            if supporter is None:
                raise NoItemsFound("supporter not in DB")

            if supporter.role != ROLE.SUPPORT:
                raise ForbiddenAction("supporter role must be SUPPORTER")

            supporter_list.append(supporter)


        new_group = Group(
            athlete_list_id=athletes_list_id,
            supporter_list_id=supporter_list_id,
        )
    
        self.repo.create_group(new_group)

        return new_group, athletes_list, supporter_list