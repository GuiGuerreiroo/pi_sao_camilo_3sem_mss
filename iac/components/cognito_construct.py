from aws_cdk import (
    RemovalPolicy, aws_cognito as cognito, Duration
)
import os
from constructs import Construct

class CognitoConstruct(Construct):

    def __init__(
        self, 
        scope: Construct,
        construct_id: str,
        **kwargs 
    ) -> None:
        super().__init__(scope, construct_id,  **kwargs )

        self.github_ref_name= os.environ.get("GITHUB_REF_NAME", "dev")

        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY


        self.user_pool= cognito.UserPool(
            self,
            f"ProjetoNutriEsportivaSaoCamiloUserPool",
            user_pool_name=f"nutri-esportiva-pool-{self.github_ref_name}",
            self_sign_up_enabled=True,
            sign_in_aliases= cognito.SignInAliases(email=True),
            auto_verify= cognito.AutoVerifiedAttrs(email=True),
            account_recovery= cognito.AccountRecovery.EMAIL_ONLY,
            password_policy= cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
                temp_password_validity=Duration.days(7)
            ),
            standard_attributes= cognito.StandardAttributes(
                email= cognito.StandardAttribute(required=True, mutable=False),
                fullname= cognito.StandardAttribute(required=True, mutable=True),
            ),
            user_verification=cognito.UserVerificationConfig(
                email_subject="Bem vindo ao sistema de autenticação Nutri Esportiva São Camilo",
                email_body=(
                    "Olá!\n\nObrigado por se registrar no Nutri Esportiva São Camilo.\n\n"
                    "Clique no link abaixo para verificar seu e-mail e ativar sua conta:\n\n"
                    "{##Verify Email##}\n\n"
                    "Se você não se registrou no Nutri Esportiva São Camilo, por favor ignore este e-mail."
                ),
                email_style=cognito.VerificationEmailStyle.LINK,
            ),
            removal_policy=REMOVAL_POLICY,
        )

        self.client= self.user_pool.add_client(
            f"ProjetoNutriEsportivaSaoCamiloAppClient",
            user_pool_client_name=f"nutri-esportiva-client-{self.github_ref_name}",
            auth_flows= cognito.AuthFlow(
                admin_user_password= True,
                user_password= True,
                user_srp= True,
            ),
            generate_secret= False,
            prevent_user_existence_errors= True,
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(7)
        )

        