from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_events_targets as targets
)
from constructs import Construct
import os

from components.apigw_construct import ApigwConstruct
from components.dynamo_construct import DynamoConstruct
from components.cognito_construct import CognitoConstruct
from components.lambda_construct import LambdaConstruct
from components.bedrock_construct import BedrockConstruct
from components.vectors_bucket_construct import VectorsBucketConstruct
from components.bucket_construct import BucketConstruct
from components.event_bridge_construct import EventBridgeConstruct

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

        self.cognito_construct= CognitoConstruct(self, "SaoCamiloUserPool")

        self.s3_bucket_construct= BucketConstruct(self)

        self.s3_vectors_bucket_construct= VectorsBucketConstruct(self)

        self.bedrock_construct= BedrockConstruct(
            self,
            vector_bucket_arn=self.s3_vectors_bucket_construct.vector_bucket_arn,
            vector_index_arn=self.s3_vectors_bucket_construct.vector_index_arn,
            bucket_arn=self.s3_bucket_construct.s3_bucket_context_files.bucket_arn
        )

        self.event_bridge_construct= EventBridgeConstruct(self, self.s3_bucket_construct.s3_bucket_context_files.bucket_name)

        # permitindo que a kb_role do bedrock leia arquivos do s3
        self.s3_bucket_construct.s3_bucket_context_files.grant_read(self.bedrock_construct.kb_role)

        # permitindo que a role assumida pelo bedrock tenha acesso ao s3 vectors
        vector_bucket_policy=self.s3_vectors_bucket_construct.grant_bedrock_access(role_arn=self.bedrock_construct.kb_role.role_arn)
        
        # fazendo o bedrock esperar pela policy ser criada e atrelada a ele
        self.bedrock_construct.knowledge_base.node.add_dependency(vector_bucket_policy)

        ENVIRONMENT_VARIABLES= {
            "STAGE": stage,
            "REGION": self.region,
            "SAO_CAMILO_TABLE_NAME": self.dynamo_construct.sao_camilo_table.table_name,
            "DYNAMO_PARTITION_KEY": self.dynamo_construct.PARTITION_KEY_NAME,
            "DYNAMO_SORT_KEY": self.dynamo_construct.SORT_KEY_NAME,
            "COGNITO_CLIENT_ID": self.cognito_construct.client.user_pool_client_id,
            "COGNITO_USER_POOL_ID": self.cognito_construct.user_pool.user_pool_id,
            "KNOWLEDGE_BASE_ID": self.bedrock_construct.knowledge_base.attr_knowledge_base_id,
            "DATA_SOURCE_ID": self.bedrock_construct.data_source.attr_data_source_id
        }
        

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

        # add the lambda to be trigged by the event bridge when the .pdf object is added to s3
        self.event_bridge_construct.trigger_ingestion_rule.add_target(
            targets.LambdaFunction(
                handler=self.lambda_construct.bedrock_ingestion
            )
        )

        # cognito access
        cognito_policy = iam.PolicyStatement(
            actions=[
                "cognito-idp:SignUp",
                "cognito-idp:InitiateAuth",
                "cognito-idp:AdminInitiateAuth",
                "cognito-idp:ConfirmSignUp",
                "cognito-idp:ResendConfirmationCode",
                "cognito-idp:AdminDeleteUser"
            ],
            resources=["*"]
        )

        for fn in self.lambda_construct.functions_that_need_cognito_iam_policy:
            fn.add_to_role_policy(cognito_policy)

        # dynamo access
        for fn in self.lambda_construct.functions_that_need_db_access:
            self.dynamo_construct.sao_camilo_table.grant_read_write_data(fn)

        # bedrock access
        bedrock_policy= iam.PolicyStatement(
            actions=[
                "bedrock:RetrieveAndGenerate",
                "bedrock:Retrieve",
                "bedrock:StartIngestionJob",
                "bedrock:InvokeModel"
            ],
            resources=[
                # this one gives acces to the Kb it self
                self.bedrock_construct.knowledge_base.attr_knowledge_base_arn,
                
                # this line line below it gives access to the datasource and Jobs inside KB
                f"{self.bedrock_construct.knowledge_base.attr_knowledge_base_arn}/*",
                
                # give access to all LLMs
                "arn:aws:bedrock:*::foundation-model/*"
            ]
        )

        for fn in self.lambda_construct.functions_that_need_bedrock_access:
            fn.add_to_role_policy(bedrock_policy)