import os

from aws_cdk import (
    aws_apigateway as apigw,
    aws_iam as iam
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors

class ApigwConstruct(Construct):
    
    def __init__(
        self, 
        scope, 
        id
    ) -> None:
        # vale a pena fazer ambientes de dev, hml, prod?
        super().__init__(scope, id)

        github_ref_name = (os.environ.get("GITHUB_REF_NAME") or "").lower()
        if "prod" in github_ref_name:
            stage = "PROD"
        elif "homolog" in github_ref_name:
            stage = "HOMOLOG"
        else:
            stage = "DEV"

        self.rest_api= RestApi(
            self,
            id="ProjetoNutriEsportivaSaoCamilo_RestApi",
            description="This is the Sao Camilo's Nutri Esportiva Project RestApi",
            default_cors_preflight_options={
                "allow_origins": Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "PUT", "POST", "DELETE", "OPTIONS"],
                "allow_headers": ["*"]
            },
            deploy_options={
                "stage_name": stage.lower()
            }
        )

        self.api_gateway_resource= self.rest_api.root.add_resource(
            "pnesc-mss",
            default_cors_preflight_options={
                "allow_origins": Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "PUT", "POST", "DELETE", "OPTIONS"],
                "allow_headers": Cors.DEFAULT_HEADERS
            },
        )