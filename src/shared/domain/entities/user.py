import uuid
from pydantic import *

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.status_user_enum import USERSTATUS

class User(BaseModel):
    user_id: str= Field(
        description="Id do usuário",
        default_factory=lambda: str(uuid.uuid4())
    )

    name: str= Field(
        description="Nome do usuário",
        min_length=2
    )

    email: str= Field(
        description="Email do usuário"
    )

    role: ROLE= Field(
        description="Role do usuário",
        default=ROLE.USER
    )

    status: USERSTATUS= Field(
        description="Status do usuário em relação ao Cognito",
        default= USERSTATUS.UNCONFIRMED
    ) 

    height: float | None= Field(
        description="Altrura do usuário (M)",
        default=None
    )

    expires_at: int | None= Field (
        description="",
        default= None
    )

    # weight: float | None= Field(
    #     description="Peso do usuário (Kg)",
    #     default=None
    # )

    model_config= ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    @field_validator("user_id")
    @classmethod
    def user_id_valid_uuid4(cls, v: str) -> str:
        try:
            uuid.UUID(v)

        except ValueError:
            raise ValueError("Invalid format for user id")
        
        return v