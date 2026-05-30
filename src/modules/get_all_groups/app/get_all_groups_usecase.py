from src.shared.domain.entities.user import User
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.group_repository_interface import IGroupRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class GetAllGroupsUseCase:
    def __init__(self, repo: IGroupRepository, user_repo: IUserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def __call__(self):
        groups = self.repo.get_all_groups()

        groups_list = {}

        for group in groups:

            athletes_list = []
            supporter_list = []

            for athlete_id in group.athlete_list_id:
                athlete = self.user_repo.get_user(str(athlete_id))

                if athlete is None:
                    continue

                athletes_list.append({
                    "athlete_data": athlete
                })

            for supporter_id in group.supporter_list_id:
                supporter = self.user_repo.get_user(str(supporter_id))
                if supporter:
                    supporter_list.append(supporter)

            groups_list[group.group_id] = {
                "athletes_list": athletes_list,
                "supporter_list": supporter_list,
            }

        return groups_list
