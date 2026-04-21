import os
from constructs import Construct
from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy,
)

class DynamoConstruct(Construct):
    sao_camilo_table: dynamodb.Table
    SAO_CAMILO_TABLE_NAME: str= "ProjetoNutriEsportivaSaoCamiloTable"
    PARTITION_KEY_NAME: str = "PK"
    SORT_KEY_NAME: str = "SK"
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        **kwargs
    )-> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.github_ref_name= os.environ.get("GITHUB_REF_NAME")
        self.stack_name= os.environ.get("STACK_NAME")
        stage= ''

        if 'prod' in self.github_ref_name.lower():
            stage= 'PROD'

        elif 'homolog'in self.github_ref_name.lower():
            stage= 'HOMOLOG'

        else:
            stage= 'DEV'

        
        removal_policy= RemovalPolicy.RETAIN if stage == 'PROD' else RemovalPolicy.DESTROY

        self.sao_camilo_table= dynamodb.Table(
            self,
            "ProjetoNutriesportivaSaoCamilo_Table",
            table_name=f"{self.SAO_CAMILO_TABLE_NAME}-{stage}",
            partition_key=dynamodb.Attribute(
                name= self.PARTITION_KEY_NAME,
                type= dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name= self.SORT_KEY_NAME,
                type= dynamodb.AttributeType.STRING
            ),
            time_to_live_atribute= "expires_at",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy,
            point_in_time_recovery=True if stage == 'PROD' else False
        )

        # configurar as gsis no futuro
        # self.sao_camilo_table.add_global_secondary_index(

        # )