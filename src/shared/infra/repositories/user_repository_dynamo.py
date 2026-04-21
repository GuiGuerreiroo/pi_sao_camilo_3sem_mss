from decimal import Decimal
import json
from typing import List, Optional
from boto3.dynamodb.conditions import Attr

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class UserRepositoryDynamo(IUserRepository):

    @staticmethod
    def partition_key_format(user_id: str) -> str:
        return f"USER#{user_id}"

    @staticmethod
    def sort_key_format() -> str:
        return f"#PROFILE"
    
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
            sort_key=Environments.get_envs().dynamo_sort_key
        )

    def get_user(self, user_id: str) -> Optional[User]:
        item= self.dynamo.get_item(
            partition_key=self.partition_key_format(user_id=user_id),
            sort_key=self.sort_key_format()
        )

        if not item.get("Item"):
            # it will through an exception in needed route
            return None

        item["Item"]["user_id"]= self.remove_prefix(item["Item"]["user_id"])

        item["Item"].pop("PK", None)
        item["Item"].pop("SK", None)

        user= User.model_validate(item["Item"])

        return user
    
    # for now I don't need this method
    # def get_all_user(self) -> List[User]:
    #     users= self.dynamo.scan_items

    #     return users

    def get_user_by_email(self, email: str) -> Optional[User]:
        # filter_expression= f"email = :email"
        # expression_attribute_values= {":email": email}
        filter_exp = Attr('email').eq(email)

        items= self.dynamo.scan_items(
            filter_expression= filter_exp
        )

        item= items.get("Items", [])

        if not item:
            return None

        item= item[0]

        item['user_id']= self.remove_prefix(item['user_id'])

        item.pop("PK", None)
        item.pop("SK", None)

        user= User.model_validate(item)

        return user

    def create_user(self, new_user: User) -> Optional[User]:
        item= new_user.model_dump_json(exclude_none=True)
        item= json.loads(item)

        self.dynamo.put_item(
            item= item,
            partition_key= self.partition_key_format(new_user.user_id),
            sort_key= self.sort_key_format()
        )

        return new_user

    def delete_user(self, user_id: str) -> Optional[User]:
        user= self.get_user(user_id)

        if not user:
            return None

        resp = self.dynamo.delete_item(
            partition_key= self.partition_key_format(user_id=user.user_id), 
            sort_key=self.sort_key_format()
        )    

        return resp

    def update_user(
        self, 
        user_id: str,
        new_name: str | None, 
        new_email: str | None,
        new_role: ROLE | None, 
        new_height: float | None
    ) -> Optional[User]:

        user = self.get_user(user_id=user_id)

        if not user:
            return None

        item_to_update = {}

        if new_name:
            item_to_update['name'] = new_name

        if new_email:
            item_to_update["email"]= new_email

        if new_role:
            item_to_update["role"]= new_role.value

        if new_height:
            item_to_update["height"]= new_height
        

        update = self.dynamo.update_item(
            partition_key=self.partition_key_format(user_id), 
            sort_key=self.sort_key_format(), 
            update_dict=item_to_update
        )

        updated_user= update.get("Attributes")

        if not updated_user:
            return None


        updated_user["user_id"]= self.remove_prefix(updated_user["user_id"])

        updated_user.pop("PK", None)
        updated_user.pop("SK", None)

        updated_user= User.model_validate(updated_user)

        return updated_user
    
    def confirm_user_registration(self, email: str) -> Optional[User]:

        user= self.get_user_by_email(email)

        if not user:
            return None

        update = self.dynamo.update_item(
            partition_key=self.partition_key_format(user.user_id), 
            sort_key=self.sort_key_format(), 
            update_dict={"status": "CONFIRMED"},
            remove_list=["expires_at"]
        )

        updated_user= update.get("Attributes")

        if not updated_user:
            return None

        updated_user["user_id"]= self.remove_prefix(updated_user["user_id"])

        updated_user.pop("PK", None)
        updated_user.pop("SK", None)

        updated_user= User.model_validate(updated_user)

        return updated_user