from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_cognito as cognito,
    aws_apigateway as apigw
)
from constructs import Construct
import os

from components.apigw_construct import ApigwConstruct
from components.dynamo_construct import DynamoConstruct
from components.cognito_construct import CognitoConstruct
from components.lambda_construct import LambdaConstruct

class IacStack(Stack):
    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = kwargs['tags']['stage']

        self.apigw_construct= ApigwConstruct(self, "Apigw")
        self.dynamo_construct= DynamoConstruct(self, "NutriDynamo")

        ENVIRONMENT_VARIABLES= {
            "STAGE": stage,
            "REGION": self.region,
            "SAO_CAMILO_TABLE_NAME": self.dynamo_construct.sao_camilo_table.table_name
        }

        self.cognito_construct= CognitoConstruct(self, "SaoCamiloUserPool")


        api_authorizer= apigw.CognitoUserPoolsAuthorizer(
            self,
            "NutriEsportivaSaoCamiloAuthorizer",
            cognito_user_pools=[self.cognito_construct.user_pool],
            identity_source="method.request.header.Authorization"
        )

        self.lambda_construct= LambdaConstruct(
            self,
            apigateway_resource=self.apigw_construct.api_gateway_resource,
            rest_api=self.apigw_construct.rest_api,
            environment_variables=ENVIRONMENT_VARIABLES,
            authorizer= api_authorizer
        )

        # adicionar a lambda a ser acionada apos a criacao do user no userpool, para fazer sue registro no Banco de dados.
        self.cognito_construct.user_pool.add_trigger(
            cognito.UserPoolOperation.POST_CONFIRMATION,
            self.lambda_construct.create_user_cognito_function
        )


        for fn in self.lambda_construct.functions_that_need_db_access:
            self.dynamo_construct.sao_camilo_table.grant_read_write_data(fn)