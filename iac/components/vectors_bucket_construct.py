import os
from constructs import Construct
from aws_cdk import (
    aws_s3vectors as s3vectors,
)


class VectorsBucketConstruct(Construct):
    def __init__(
        self,
        scope: Construct
    ) -> None:
        super().__init__(scope, "ProjetoNutriEsportivaSaoCamilo_VectorsBucket")

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME", "dev")

        stage= self.github_ref_name

        # cria o bucket de vetores
        self.s3_vectors_bucket_context_files= s3vectors.CfnVectorBucket(
            self,
            "ProjetoNutriEsportivaSaoCamilo_Context_File_Vector_Bucket",
            vector_bucket_name=f"projeto-nutri-esportiva-sao-camilo-context-files-vector-{stage.lower()}",
        )

        self.s3_vectors_index= s3vectors.CfnIndex(
            self,
            "ProjetoNutriEsportivaSaoCamilo_Context_File_Vector_Index",
            vector_bucket_name=self.s3_vectors_bucket_context_files.vector_bucket_name,
            index_name="nutri-index",
            dimension=1024,
            data_type="float32",
            distance_metric="cosine"
        )

        # fala para o cloud formation para ele cria o bucket antes de criar o index
        self.s3_vectors_index.node.add_dependency(self.s3_vectors_bucket_context_files)

        self.vector_bucket_arn=self.s3_vectors_bucket_context_files.attr_vector_bucket_arn

        self.vector_index_arn=self.s3_vectors_index.attr_index_arn