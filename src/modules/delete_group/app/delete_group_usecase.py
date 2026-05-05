from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.entities.group import Group
from src.shared.domain.repositories.group_repository_interface import IGroupRepository

class DeleteGroupUseCase:
    def __init__(self, repo: IGroupRepository):
        self.repo = repo

    def __call__(
        self, 
        group_id: str
    ) -> Group:
        
        deleted_group = self.repo.delete_group(group_id=group_id)

        if deleted_group is None:
            raise NoItemsFound("group")

        return deleted_group
