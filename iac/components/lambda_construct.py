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
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            layers=[self.lambda_layer],
            environment=environment_variables,
            timeout=Duration.seconds(35)
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

        self.create_user_cognito_function= self.create_background_lambda(
            module_name="create_user_cognito",
            environment_variables=environment_variables
        )

        self.get_user_function= self.create_lambda_api_gateway_integration(
            module_name="get_user",
            method="GET",
            mss_api_resource=apigateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.functions_that_need_db_access= [
            self.create_user_cognito_function,
            self.get_user_function
        ]