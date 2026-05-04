from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(
        self, 
        user_id: str, 
        new_name: str | None = None, 
        new_email: str | None = None, 
        new_height: float | None = None
    ) -> User:

        updated_user = self.repo.update_user(
            user_id=user_id, 
            name=new_name,
            new_email=new_email,
            new_height=new_height
        )

        if updated_user is None:
            raise NoItemsFound("user_id")

        return updated_user
