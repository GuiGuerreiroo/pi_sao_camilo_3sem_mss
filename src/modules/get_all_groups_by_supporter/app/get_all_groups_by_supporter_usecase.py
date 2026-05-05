from src.shared.domain.entities.user import User
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.repositories.group_repository_interface import IGroupRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.training_repository_interface import ITrainingRepository

class GetAllGroupsBySupporterUseCase:
    def __init__(self, repo: IGroupRepository, user_repo: IUserRepository, training_repo: ITrainingRepository):
        self.repo = repo
        self.user_repo = user_repo
        self.training_repo = training_repo

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

                athlete_trainings = self.training_repo.get_all_trainings_by_user(athlete_id)

                athletes_list.append({
                    "athlete_data": athlete,
                    "trainings_data": athlete_trainings
                })

            groups_list[group.group_id] = {
                "athletes_list": athletes_list,
            }


        return groups_list



        
    