import os

from aws_cdk import (
    aws_s3,
    RemovalPolicy
)

from constructs import Construct


class BucketConstruct(Construct):
    s3_bucket_context_files: aws_s3.Bucket


    def __init__(
        self,
        scope: Construct
    ) -> None:
        super().__init__(scope, "ProjetoNutriEsportivaSaoCamilo_Bucket")

        self.github_ref_name= os.environ.get("GITHUB_REF_NAME")

        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY
        AUTO_DELETE = False if 'prod' in self.github_ref_name  else True

        stage= ''

        if 'prod' in self.github_ref_name.lower():
            stage= 'PROD'

        elif 'homolog'in self.github_ref_name.lower():
            stage= 'HOMOLOG'

        else:
            stage= 'DEV'
        
        self.s3_bucket_context_files= aws_s3.Bucket(
            self,
            "ProjetoNutriEsportivaSaoCamilo_Context_File_Bucket",
            bucket_name=f"projeto-nutri-esportiva-sao-camilo-context-files-{stage.lower()}",
            versioned=True,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            event_bridge_enabled=True,
            cors=[
                aws_s3.CorsRule(
                    allowed_methods=[
                        aws_s3.HttpMethods.GET, 
                        aws_s3.HttpMethods.PUT, 
                        aws_s3.HttpMethods.POST
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3000
                )
            ],
            removal_policy=REMOVAL_POLICY,
            auto_delete_objects=AUTO_DELETE
        )