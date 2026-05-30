from aws_cdk import (
    aws_lambda as lambda_,
    Duration,
    aws_apigateway as apigw,
    Stack,
    aws_iam as iam
)
from aws_cdk.aws_apigateway import CognitoUserPoolsAuthorizer, Resource, LambdaIntegration
from constructs import Construct

class LambdaConstruct(Construct):

    def create_lambda_api_gateway_integration(
        self,
        module_name: str,
        method: str,
        mss_api_resource: Resource,
        environment_variables: dict = {"STAGE": "TEST"},
        authorizer= None
    ):
        
        function= lambda_.Function(
            self,
            module_name.title(),
            function_name=f"pnesc-{module_name}",
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(29) #29 seconds because it is the time the api gateway still working before terminating the request
        )

        mss_api_resource.add_resource(
            module_name.replace('_', '-')
        ).add_method(
            method,
            integration=LambdaIntegration(function),
            authorizer= authorizer
        )

        return function
    

    def create_background_lambda(
        self,
        module_name: str,
        environment_variables: dict
    ):
        function= lambda_.Function(
            self,
            module_name.title(),
            function_name=f"pnesc-{module_name}",
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(35)
        )

        return function
    
    def __init__(
        self,
        scope: Construct,
        apigateway_resource: Resource,
        rest_api: apigw.RestApi,
        environment_variables: dict,
        authorizer:CognitoUserPoolsAuthorizer 
    ) -> None:
        
        super().__init__(scope, "ProjetoNutriEsportivaSaoCamilo_Lambdas")

        self.lambda_layer= lambda_.LayerVersion(
            self,
            "ProjetoNutriEsportivaSaoCamilo_Layer",
            # Esse aqui vem do arquivo adjust_layer_direcory.py
            code=lambda_.Code.from_asset("./build"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13]
        )

        self.bedrock_ingestion_function= self.create_background_lambda(
            module_name="bedrock_ingestion",
            environment_variables=environment_variables
        )

        self.auth_user_function= self.create_lambda_api_gateway_integration(
            module_name="auth_user",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        self.create_user_function= self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        self.get_all_users_function= self.create_lambda_api_gateway_integration(
            module_name="get_all_users",
            method="GET",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.refresh_token_function= self.create_lambda_api_gateway_integration(
            module_name="refresh_token",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
             # essa rota nao tem authorizer
        )

        self.confirm_user_function= self.create_lambda_api_gateway_integration(
            module_name="confirm_user",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        self.resend_code_function= self.create_lambda_api_gateway_integration(
            module_name="resend_code",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        self.change_password_function= self.create_lambda_api_gateway_integration(
            module_name="change_password",
            method="PUT",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        self.forgot_password_function= self.create_lambda_api_gateway_integration(
            module_name="forgot_password",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        self.delete_expired_user_function= self.create_background_lambda(
            module_name="delete_expired_user",
            environment_variables=environment_variables
            # essa rota nao tem authorizer
        )

        # this lambda is just used to change the cognito's message depending of what the user is asking
        self.cognito_custom_message_function= self.create_background_lambda(
            module_name="cognito_custom_message",
            environment_variables=environment_variables
        )

        self.get_user_function= self.create_lambda_api_gateway_integration(
            module_name="get_user",
            method="GET",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_user_function= self.create_lambda_api_gateway_integration(
            module_name="update_user",
            method="PUT",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.create_training_function= self.create_lambda_api_gateway_integration(
            module_name="create_training",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_trainings_function= self.create_lambda_api_gateway_integration(
            module_name="get_all_trainings",
            method="GET",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.create_group_function= self.create_lambda_api_gateway_integration(
            module_name="create_group",
            method="POST",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_group_function= self.create_lambda_api_gateway_integration(
            module_name="update_group",
            method="PUT",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_group_function= self.create_lambda_api_gateway_integration(
            module_name="delete_group",
            method="DELETE",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_groups_by_supporter_function= self.create_lambda_api_gateway_integration(
            module_name="get_all_groups_by_supporter",
            method="GET",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.functions_that_need_db_access= [
            self.create_user_function,
            self.get_all_users_function,
            self.get_user_function,
            self.confirm_user_function,
            self.resend_code_function,
            self.create_training_function,
            self.get_all_trainings_function,
            self.create_group_function,
            self.update_group_function,
            self.delete_group_function,
            self.get_all_groups_by_supporter_function,
            self.update_user_function,
            self.forgot_password_function
        ]

        self.functions_that_need_cognito_iam_policy= [
            self.create_user_function,
            self.auth_user_function,
            self.refresh_token_function,
            self.confirm_user_function,
            self.resend_code_function,
            self.update_user_function,
            self.delete_expired_user_function,
            self.change_password_function,
            self.forgot_password_function
        ]

        self.functions_that_need_bedrock_access= [
            self.bedrock_ingestion_function,
            self.create_training_function
        ]