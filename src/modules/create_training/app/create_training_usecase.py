from typing import Optional
from src.shared.domain.entities.training import Training
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.usrine_color import URINE_COLOR
import boto3
from src.shared.environments import Environments
from src.shared.domain.repositories.training_repository_interface import ITrainingRepository
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from botocore.exceptions import ClientError
from src.shared.helpers.errors.usecase_errors import BedrockIntegrationError
class CreateTrainingUseCase:
    def __init__(self, repo: ITrainingRepository):
        self.repo = repo

        self.client= boto3.client('bedrock-agent-runtime')
        self.knowledge_base_id= Environments.get_envs().knowledge_base_id

    
    def __call__ (
        self,
        user_id: str,
        modality: MODALITY,
        start_date: int,
        end_date: int,
        duration: float,
        environment_temperature: float,
        environment_humidity: float,
        urine_color: URINE_COLOR,
        pre_training_symptoms: list[str] | None,
        pre_training_weight: float,
        pre_training_hydration: float,
        during_training_hydration: float,
        during_training_urine_elimination: float,
        post_training_symptoms: list[str] | None,
        post_training_weight: float,
        soaked_clothes: bool | None,
        training_intensity: int
    ) -> Optional[Training]:

        # Calculamos a variação como Final - Inicial (para que a perda de peso seja representada como - , e o ganho como +)
        weight_difference = post_training_weight - pre_training_weight

        # Calcula a porcentagem de variação em relação ao peso inicial
        weight_variation_percentage = (weight_difference / pre_training_weight) * 100
        
        # pensar sobre esse campo
        # hydric_balance = post_training_weight - pre_training_weight
        pre_training_hydration_target_min = int(pre_training_weight * 5)
        pre_training_hydration_target_max = int(pre_training_weight * 10)

        # Usamos -weight_difference porque a variação está como Final - Inicial (negativa para perdas).
        # Subtrair o valor negativo adiciona o peso perdido (suor) à equação.
        # como as medidas de agua estao em ml, passamos para litros dividindo por 1000
        ajusted_weight_difference= -weight_difference + (during_training_hydration/1000) - (during_training_urine_elimination/1000)

        # duration vira em minutos, portanto temos que transformar para horas dividindo por 60
        sudorese = ajusted_weight_difference / (duration/60)



        # aredondando 2 casas decimais 
        weight_difference = round(weight_difference, 2)
        ajusted_weight_difference = round(ajusted_weight_difference, 2)
        sudorese = round(sudorese, 2)
        weight_variation_percentage = round(weight_variation_percentage, 2)


        # formatando valores para o padrao brasileiro
        weight_diff_br = f"{weight_difference:.2f}".replace('.', ',')
        ajusted_weight_br = f"{ajusted_weight_difference:.2f}".replace('.', ',')
        sudorese_br = f"{sudorese:.2f}".replace('.', ',')
        weight_var_br = f"{weight_variation_percentage:.2f}".replace('.', ',')
        
        # Formatando as temperaturas e pesos originais também por garantia
        temp_br = f"{environment_temperature:.1f}".replace('.', ',')
        peso_br = f"{pre_training_weight:.1f}".replace('.', ',')

        search_query = f"Diretrizes de reposição hídrica, hidratação, taxa de sudorese e cor da urina para um treino de {duration} minutos."


        system_prompt_template= f'''
            <system_prompt>
            Você é um nutricionista esportivo. Use EXCLUSIVAMENTE as informações da sua base de conhecimento para responder. Não utilize conhecimentos prévios.
            </system_prompt>

            <base_de_conhecimento>
            $search_results$
            </base_de_conhecimento>

            <athlete_data>
            - Modalidade: {modality} (Duração: {duration} minutos)
            - Ambiente: {temp_br}°C com {environment_humidity}% de umidade
            - Peso corporal: {peso_br} kg
            - Perda de peso: {weight_diff_br} kg ({weight_var_br}% do peso corporal)
            - Total ingerido: {during_training_hydration} mL
            - Taxa de sudorese: {sudorese_br} L/h
            - Urina pós-treino: {urine_color}
            - Roupas encharcadas: {soaked_clothes}
            - Intensidade do treino: {training_intensity}/10
            - Sintomas pré-treino: {pre_training_symptoms}
            - Sintomas pós-treino: {post_training_symptoms}
            - Hidratação antes deste treino: {pre_training_hydration} mL (Meta ideal era entre {pre_training_hydration_target_min} e {pre_training_hydration_target_max} mL)
            </athlete_data>

            <rules>
            1. MATEMÁTICA ESTRITA: Use apenas valores numéricos baseados nas diretrizes do contexto. Nunca some dois volumes de bebidas diferentes no mesmo intervalo de tempo. A bebida pré-treino é SEMPRE água.
            2. TRADUÇÃO VISUAL E ARREDONDAMENTO: Sempre converta volumes em mL para referências práticas (1 copo = 250 mL, 1 garrafinha = 500 mL). Arredonde rigorosamente para metades ou inteiros lógicos (Ex: NUNCA diga "1,4 copos". Arredonde para "1 copo e meio" ou "2 copos").
            3. LIMITE GÁSTRICO: O limite de esvaziamento gástrico é de 1.0 L/h. Se a taxa de sudorese do atleta for maior que 1.0 L/h, você deve OBRIGATORIAMENTE alertar sobre isso na seção de Atenção.
            4. TOM DE VOZ (O PONTO DE EQUILÍBRIO): Você é um treinador de bolso do atleta. Fale em segunda pessoa ("Você"). Seja encorajador, prático e empático. É PROIBIDO usar jargões técnicos de biologia. Explique o "porquê" das ações usando palavras simples do dia a dia. Máximo de 2 a 3 frases por bloco.
            5. EXCEÇÃO DE SUCESSO: Se a variação de peso for < 1% e a urina for clara, ignore o formato abaixo e gere apenas uma mensagem curta parabenizando o atleta.
            </rules>

            <output_format>
            FEEDBACK DO PRÉ-TREINO DE HOJE:
            [1 a 2 frases avaliando se o volume que o atleta ingeriu antes do treino de hoje foi ideal, insuficiente ou excessivo, e o porquê isso importa.]

            RECUPERAÇÃO HOJE:
            [Volume de reposição com intervalo mínimo e máximo conforme as diretrizes, convertido em garrafinhas de 500 mL ou copos]

            PRÉ-TREINO DO PRÓXIMO TREINO:
            [Volume em mL calculado com base no peso corporal, janela de tempo, indicando ÁGUA, com equivalência em copos ou garrafinhas]

            DURANTE O PRÓXIMO TREINO:
            [Volume por intervalo de 15 minutos e tipo de bebida indicado para a duração da {modality}, com equivalência em copos. Não cite temperatura da água]

            ATENÇÃO PARA O PRÓXIMO TREINO:
            - [Ponto crítico 1: Alerta numérico sobre o cruzamento da taxa de sudorese ({sudorese} L/h) versus o limite gástrico (1.0 L/h)]
            - [Ponto crítico 2: Alerta sobre a cor da urina e sintomas apresentados. Ações específicas]
            </output_format>   
        '''

        try:
            response= self.client.retrieve_and_generate(
                input={
                    'text': search_query
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': self.knowledge_base_id,
                        'modelArn': 'us.anthropic.claude-haiku-4-5-20251001-v1:0',
                        'generationConfiguration': {
                            'promptTemplate': {
                                'textPromptTemplate': system_prompt_template
                            }
                        }
                    }
                }
            )

            bedrock_feedback=  response['output']['text']
        
        except ClientError as e:
            raise BedrockIntegrationError(e.response['Error']['Message'])

        except Exception as e:
            raise BedrockIntegrationError(str(e))

        new_training= Training(
            user_id=user_id,
            modality=modality,
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            environment_temperature=environment_temperature,
            environment_humidity=environment_humidity,
            urine_color=urine_color,
            pre_training_symptoms=pre_training_symptoms,
            pre_training_weight=pre_training_weight,
            pre_training_hydration=pre_training_hydration,
            during_training_hydration=during_training_hydration,
            during_training_urine_elimination=during_training_urine_elimination,
            post_training_symptoms=post_training_symptoms,
            post_training_weight=post_training_weight,
            soaked_clothes=soaked_clothes,
            training_intensity=training_intensity,
            weight_difference=weight_difference,
            ajusted_weight_difference=ajusted_weight_difference,
            sudorese=sudorese,
            weight_variation_percentage=weight_variation_percentage,
            ai_suggestion=bedrock_feedback
        )

        return self.repo.create_training(new_training)