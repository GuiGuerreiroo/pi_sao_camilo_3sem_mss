from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
from typing import List
from typing import Optional
import json
from src.shared.environments import Environments

from src.shared.domain.entities.training import Training
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.domain.repositories.training_repository_interface import ITrainingRepository


class TrainingRepositoryDynamo(ITrainingRepository):
    @staticmethod
    def partition_key_format(user_id: str) -> str:
        return f"USER#{user_id}"

    @staticmethod
    def sort_key_format(start_date: int, training_id: str) -> str:
        return f"TRAINING#{start_date}#{training_id}"

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
    
    def create_training(self, new_training: Training) -> Optional[Training]:
        item= new_training.model_dump(exclude_none=True, mode="json")
        # item= json.loads(item)

        self.dynamo.put_item(
            item=item,
            partition_key=self.partition_key_format(new_training.user_id),
            sort_key=self.sort_key_format(new_training.start_date, new_training.training_id)
        )

        return new_training

    def get_training(self, user_id: str, training_id: str) -> Optional[Training]:
        pk= self.dynamo.partition_key
        sk= self.dynamo.sort_key

        items= self.dynamo.query(
            key_condition_expression= 
                Key(pk).eq(self.partition_key_format(user_id)) &
                Key(sk).begins_with('TRAINING#'),
            FilterExpression=Attr('training_id').eq(training_id)
        )

        items = items.get("Items", [])

        if not items:
            return None

        item= items[0]

        item["user_id"]= self.remove_prefix(item["user_id"])
        item["training_id"]= self.remove_prefix(item["training_id"])

        item.pop(pk, None)
        item.pop(sk, None)

        training= Training.model_validate(item)

        return training
    
    def get_all_trainings_by_user(self, user_id: str) -> List[Training]:
        pk= self.dynamo.partition_key
        sk= self.dynamo.sort_key

        query= self.dynamo.query(
            key_condition_expression=
                Key(pk).eq(self.partition_key_format(user_id)) &
                Key(sk).begins_with('TRAINING#'),
            ScanIndexForward=False
        )

        items= query.get("Items", [])

        response= []

        for item in items:

            item["user_id"]= self.remove_prefix(item["user_id"])
            item["training_id"]= self.remove_prefix(item["training_id"])

            item.pop(pk, None)
            item.pop(sk, None)

            response.append(Training.model_validate(item))

        # pensar se vamos devolver com user_id ou se vamos chamar o get_user e passar todo o usuário
        return response

    def delete_training(self, user_id: str, training_id: str) -> Optional[Training]:
        training= self.get_training(
            user_id=user_id, 
            training_id=training_id
        )

        if not training:
            return None

        resp= self.dynamo.delete_item(
            partition_key= self.partition_key_format(user_id=training.user_id),
            sort_key= self.sort_key_format(start_date=training.start_date, training_id=training.training_id)
        )

        return resp
    