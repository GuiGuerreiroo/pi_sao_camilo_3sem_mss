from typing import List
from src.shared.domain.entities.group import Group
from typing import Optional
from boto3.dynamodb.conditions import Key
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.domain.repositories.group_repository_interface import IGroupRepository

class GroupRepositoryDynamo(IGroupRepository):
    
    @staticmethod
    def partition_key_format(group_id: str) -> str:
        return f"GROUP#{group_id}"
    
    @staticmethod
    def sort_key_format() -> str:
        return f"#METADATA"

    @staticmethod
    def partition_key_format_mapping(supporter_id: str) -> str:
        return f"SUPPORTER#{supporter_id}"

    @staticmethod
    def sort_key_format_mapping(group_id: str) -> str:
        return f"GROUP#{group_id}"

    @staticmethod
    def remove_prefix(param: str):
        
        partes = param.split('#', 1) 
        
        if len(partes) > 1:
            param = partes[1]
            
        return param
    
    def __init__(self):
        self.dynamo = DynamoDatasource(
            endpoint_url=Environments.get_envs().endpoint_url,
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key,
        )

    def create_group(self, new_group: Group) -> Optional[Group]:
        item= new_group.model_dump(exclude_none=True, mode="json")

        self.dynamo.put_item(
            item=item,
            partition_key=self.partition_key_format(new_group.group_id),
            sort_key=self.sort_key_format()
        )

        for supporter_id in new_group.supporter_list_id:

            map_item= {'entity': 'mapping'}

            self.dynamo.put_item(
                item=map_item,
                partition_key=self.partition_key_format_mapping(supporter_id),
                sort_key=self.sort_key_format_mapping(new_group.group_id)
            )

        return new_group
        
       
    def get_group(self, group_id: str) -> Optional[Group]:
        pk= self.dynamo.partition_key
        sk= self.dynamo.sort_key

        item= self.dynamo.get_item(
            partition_key=self.partition_key_format(group_id),
            sort_key=self.sort_key_format()
        )

        if not item.get("Item"):
            return None

        item= item["Item"]
        item["group_id"]= self.remove_prefix(item["group_id"])

        item.pop(pk, None)
        item.pop(sk, None)

        group= Group.model_validate(item)

        return group
        
    def get_all_groups(self) -> List[Group]:
        filter_exp = Key(self.dynamo.sort_key).eq(self.sort_key_format())

        items_dict = self.dynamo.scan_items(filter_expression=filter_exp)

        items = items_dict.get("Items", [])

        groups=[]

        for item in items:
            item["group_id"]= self.remove_prefix(item["group_id"])

            item.pop("PK", None)
            item.pop("SK", None)

            group= Group.model_validate(item)

            groups.append(group)

        return groups


    def get_all_groups_by_supporter_id(self, supporter_id: str) -> List[Group]:
        pk= self.dynamo.partition_key
        sk= self.dynamo.sort_key

        items= self.dynamo.query(
            key_condition_expression= 
                Key(pk).eq(self.partition_key_format_mapping(supporter_id)) &
                Key(sk).begins_with('GROUP#')
        )

        items = items.get("Items", [])

        response= []

        for item in items:
            group_id= self.remove_prefix(item[sk])

            group= self.get_group(group_id)

            # it was alreday validated in Group format inside get_group method
            if group:
                response.append(group)

        return response
    

    def update_group(
        self, 
        group_id: str, 
        new_supporter_list_id: List[str] | None, 
        new_athlete_list_id: List[str] | None
    ) -> Optional[Group]:
        pk= self.dynamo.partition_key
        sk= self.dynamo.sort_key

        old_group= self.get_group(group_id)

        if not old_group:
            return None

        items_to_update= {}

        if new_supporter_list_id:
            items_to_update['supporter_list_id']= new_supporter_list_id

        if new_athlete_list_id:
            items_to_update['athlete_list_id']= new_athlete_list_id

        updated_group= self.dynamo.update_item(
            partition_key=self.partition_key_format(group_id),
            sort_key=self.sort_key_format(),
            update_dict=items_to_update
        )

        updated_group = updated_group.get("Attributes")

        if not updated_group:
            return None

        updated_group["group_id"]= self.remove_prefix(updated_group["group_id"])

        updated_group.pop(pk, None)
        updated_group.pop(sk, None)

        updated_group= Group.model_validate(updated_group)

        if new_supporter_list_id:

            old_supports= set(str(id) for id in old_group.supporter_list_id)
            new_supporters= set(str(id) for id in new_supporter_list_id)

            supporters_ids_to_add= new_supporters - old_supports

            supporters_ids_to_remove= old_supports - new_supporters

            for supporter_id in supporters_ids_to_add:
                map_item= {'entity': 'mapping'}

                self.dynamo.put_item(
                    item=map_item,
                    partition_key=self.partition_key_format_mapping(supporter_id),
                    sort_key=self.sort_key_format_mapping(group_id)
                )

            for supporter_id in supporters_ids_to_remove:
                self.dynamo.delete_item(
                    partition_key=self.partition_key_format_mapping(supporter_id),
                    sort_key=self.sort_key_format_mapping(group_id)
                )

        return updated_group

    def delete_group(self, group_id: str) -> Optional[Group]:
        group= self.get_group(group_id)

        if not group:
            return None

        self.dynamo.delete_item(
            partition_key=self.partition_key_format(group_id),
            sort_key=self.sort_key_format()
        )

        for supporter_id in group.supporter_list_id:
            self.dynamo.delete_item(
                partition_key=self.partition_key_format_mapping(supporter_id),
                sort_key=self.sort_key_format_mapping(group_id)
            )

        return group