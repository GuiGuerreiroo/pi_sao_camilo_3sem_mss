from src.shared.domain.enums.symptoms import SYMPTOMS
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.domain.enums.modality import MODALITY
import uuid
from pydantic import *

class Training(BaseModel):
    training_id: str= Field(
        description="Id do treinamento",
        default_factory=lambda: str(uuid.uuid4())
    )

    user_id: str= Field(
        description="Id do usuário"
    )

    modality: MODALITY= Field(
        description="Modalidade do treinamento"
    )

    # --- TEMPO ---

    # timestamp miliseconds
    start_date: int= Field(
        description="Data de inicio do treinamento"
    )

    # timestamp miliseconds
    end_date: int= Field(
        description="Data de fim do treinamento"
    )

    # timestamp miliseconds
    duration: int= Field(
        description="Tempo total do treinamento em segundos"
    )

   # --- CLIMA (Condições Ambientais) ---
    environment_temperature: float= Field(
        description="Temperatura ambiente do local do treinamento em °C"
    )

    environment_humidity: float= Field(
        description="Umidade relativa do ar no local do treinamento em %"
    )

    # --- PRÉ-TREINO ---
    urine_color: URINE_COLOR= Field(
        description="Cor da urina do usuário"
    )

    pre_training_symptoms: list[SYMPTOMS]= Field(
        description="Sintomas do usuário antes do treinamento"
    )

    pre_training_weight: float= Field(
        description="Peso do usuário antes do treinamento em Kg"
    )

    pre_training_hydration: float= Field(
        description="Quantidade de hidratação do usuário antes do treinamento em ml"
    )

    clothing_equipment: bool | None = Field(
        description="Usuario esta fazendo o exercicio de short e camiseta ou sem camiseta e short",
        default= True
    )

    # --- DURANTE O TREINO ---
    during_training_hydration: float= Field(
        description="Quantidade de hidratação do usuário durante o treinamento em ml"
    )

    during_trainin_urine_elimination: float= Field(
        description="Quantidade de urina eliminada pelo usuário durante o treinamento em ml"
    )

    # --- PÓS-TREINO ---
    post_training_symptoms: list[SYMPTOMS]= Field(
        description="Sintomas do usuário depois do treinamento"
    )

    post_training_weight: float= Field(
        description="Peso do usuário depois do treinamento em Kg"
    )

    soaked_clothes: bool | None= Field(
        description="Se a roupa do usuário ficou encharcada após o treinamento",
        default= None
    )

    # intencidade de 10 muito alta, de 0 muito fraca
    training_intensity: int= Field(
        description="Intensidade do treinamento de 0 a 10"
    )

    # --- RESULTADOS COMPUTADOS ---
    weight_difference: float= Field(
        description="Diferença de peso do usuário antes e depois do treinamento em Kg (Pré treino - Pós treino)"
    )

    ajusted_weight_difference: float= Field(
        description="Diferença de peso do usuário antes e depois do treinamento em Kg (Weight Difference (Kg) + During Training Hydratation (ml) - During Training Urine Elimination (ml)) unidade pode ser L ou Kg"
    )

    hydric_balance: float= Field(
        description="Balanço hidrico do usuário durante o treinamento em ml (During Training Hydratation (ml) - During Training Urine Elimination (ml))"
    )

    sudorese: float= Field(
        description="Quantidade de suor eliminado pelo usuário durante o treinamento em ml (Ajusted Weight Difference (L/Kg) / Duration (hours))"
    )

    weight_variation_percentage: float= Field(
        description="Porcentagem de variação de peso do usuário antes e depois do treinamento ((Pré treino - Pós treino) / Pré treino) * 100 (%)"
    )

    # --- RESULTADOS DA IA ---
    ai_suggestion: str | None = Field(
        description="Sugestão da IA",
        default= None
    )

    model_config= ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    @field_validator("training_id")
    @classmethod
    def training_id_valid_uuid4(cls, v: str) -> str:
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError("Invalid format for training id")
        
        return v

    @field_validator("user_id")
    @classmethod
    def user_id_valid_uuid4(cls, v: str) -> str:
        try:
            uuid.UUID(v)

        except ValueError:
            raise ValueError("Invalid format for user id")
        
        return v