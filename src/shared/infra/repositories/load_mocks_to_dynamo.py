from decimal import Decimal
import boto3
import dotenv

from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.training_repository_dynamo import TrainingRepositoryDynamo
from src.shared.infra.repositories.training_repository_mock import TrainingRepositoryMock
from src.shared.environments import Environments

def setup_dynamo_table():
    dynamo_table_name = "ProjetoNutriEsportivaSaoCamiloTable"
    endpoint_url = "http://localhost:8000"
    partition_key = "PK"
    sort_key = "SK"

    print("Setting up DynamoDB table...")

    dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint_url)
    print("DynamoDB client created")
    tables = dynamo_client.list_tables()['TableNames']

    if dynamo_table_name not in tables:
        print("Creating table...")
        dynamo_client.create_table(
            TableName=dynamo_table_name,
            KeySchema=[
                {
                    'AttributeName': partition_key,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': sort_key,
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': partition_key,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': sort_key,
                    'AttributeType': 'S'
                }

            ],
            BillingMode='PAY_PER_REQUEST',
        )
        print("Waiting for table to be created...")
        dynamo_client.get_waiter('table_exists').wait(TableName=dynamo_table_name)

        print('Loading table...')

        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)

        table = dynamodb.Table(dynamo_table_name)

        print("Adding counter to table")

        table.put_item(
            Item={
                partition_key: 'COUNTER',
                sort_key: 'COUNTER'
            }
        )

        print(f'Table "{dynamo_table_name}" created!')

    else:
        print("Table already exists!")


def load_mock_to_local_dynamo():
    setup_dynamo_table()
    
    user_mock_repo = UserRepositoryMock()
    user_dynamo_repo = UserRepositoryDynamo()
    
    training_mock_repo = TrainingRepositoryMock()
    training_dynamo_repo = TrainingRepositoryDynamo()

    user_count = 0
    training_count = 0

    print('Loading mock user data to dynamo...')
    for user in user_mock_repo.users:
        print(f"Loading user {user.user_id} | {user.name} to dynamo")
        user_dynamo_repo.create_user(user)
        user_count += 1
    print(f"{user_count} users loaded to dynamo!")
    
    print('Loading mock training data to dynamo...')
    for training in training_mock_repo.trainings:
        print(f"Loading training {training.training_id} for user {training.user_id} to dynamo")
        training_dynamo_repo.create_training(training)
        training_count += 1
    print(f"{training_count} trainings loaded to dynamo!")


def load_mock_to_real_dynamo():
    user_mock_repo = UserRepositoryMock()
    user_dynamo_repo = UserRepositoryDynamo()
    
    training_mock_repo = TrainingRepositoryMock()
    training_dynamo_repo = TrainingRepositoryDynamo()

    user_count = 0
    training_count = 0

    print('Loading mock user data to real dynamo...')
    for user in user_mock_repo.users:
        print(f"Loading user {user.user_id} | {user.name} to dynamo")
        user_dynamo_repo.create_user(user)
        user_count += 1
    print(f"{user_count} users loaded to dynamo!")
    
    print('Loading mock training data to real dynamo...')
    for training in training_mock_repo.trainings:
        print(f"Loading training {training.training_id} for user {training.user_id} to dynamo")
        training_dynamo_repo.create_training(training)
        training_count += 1
    print(f"{training_count} trainings loaded to dynamo!")


if __name__ == '__main__':
    dotenv.load_dotenv()
    load_mock_to_local_dynamo()
