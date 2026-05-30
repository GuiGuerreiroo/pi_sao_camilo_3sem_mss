import uuid
from typing import List, Optional
from src.shared.domain.entities.group import Group
from src.shared.domain.repositories.group_repository_interface import IGroupRepository

class GroupRepositoryMock(IGroupRepository):
    def __init__(self):
        self.groups: List[Group] = [
            Group(
                group_id="660e8400-e29b-41d4-a716-446655440001",
                athlete_list_id=["550e8400-e29b-41d4-a716-446655440001"],
                supporter_list_id=["550e8400-e29b-41d4-a716-446655440002"]
            ),
            Group(
                group_id="660e8400-e29b-41d4-a716-446655440002",
                athlete_list_id=["cde87c2e-d1ab-4bb1-8630-189f2d2c8c6a"],
                supporter_list_id=["550e8400-e29b-41d4-a716-446655440002"]
            )
        ]

    def create_group(self, new_group: Group) -> Optional[Group]:
        self.groups.append(new_group)
        return new_group

    def get_group(self, group_id: str) -> Optional[Group]:
        for group in self.groups:
            if str(group.group_id) == group_id:
                return group
        return None

    def get_all_groups(self) -> List[Group]:
        return self.groups

    def get_all_groups_by_supporter_id(self, supporter_id: str) -> List[Group]:
        matching_groups = []
        for group in self.groups:
            if any(str(supporter) == supporter_id for supporter in group.supporter_list_id):
                matching_groups.append(group)
        return matching_groups

    def update_group(self, group_id: str, new_supporter_list_id: List[str] | None, new_athlete_list_id: List[str] | None) -> Optional[Group]:
        for group in self.groups:
            if str(group.group_id) == group_id:
                if new_supporter_list_id is not None:
                    group.supporter_list_id = [uuid.UUID(s) for s in new_supporter_list_id]
                if new_athlete_list_id is not None:
                    group.athlete_list_id = [uuid.UUID(a) for a in new_athlete_list_id]
                return group
        return None

    def delete_group(self, group_id: str) -> Optional[Group]:
        for idx, group in enumerate(self.groups):
            if str(group.group_id) == group_id:
                return self.groups.pop(idx)
        return None
