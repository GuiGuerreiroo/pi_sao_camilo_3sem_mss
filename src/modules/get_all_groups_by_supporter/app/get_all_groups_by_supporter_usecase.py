from src.shared.domain.entities.user import User
import uuid
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.group_repository_interface import IGroupRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class GetAllGroupsBySupporterUseCase:
    def __init__(self, repo: IGroupRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(
        self, 
        user_id: str
    ):
        # all the group the user id is linked
        groups = self.repo.get_all_groups_by_supporter_id(user_id)

        groups_list= {}

        for group in groups:

            athletes_list = []
            supporter_list = []

            for athlete_id in group.athlete_list_id:
                athlete = self.user_repo.get_user(athlete_id)

                if athlete is None:
                        raise NoItemsFound("No athlete found for the given user id")

                athletes_list.append(athlete)
            
            for supporter_id in group.supporter_list_id:
                supporter = self.user_repo.get_user(supporter_id)
                if supporter is None:
                    raise NoItemsFound("No supporter found for the given user id")
                
                supporter_list.append(supporter)

            groups_list[group.group_id] = {
                "athletes_list_id": athletes_list,
                "supporter_list_id": supporter_list
            }


        return groups_list



        
    