from pydantic import *
from typing import List
import uuid


class Group(BaseModel):
    group_id: UUID4= Field(
        description="Id do grupo",
        default_factory=lambda: str(uuid.uuid4())
    )

    athlete_list_id: List[UUID4]= Field(
        description="Lista de ids dos atletas",
    )

    supporter_list_id: List[UUID4]= Field(
        description="Lista de ids dos apoiadores",
    )

    model_config= ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    # @field_validator("group_id")
    # @classmethod
    # def group_id_valid_uuid4(cls, v: str) -> str:
    #     try:
    #         uuid.UUID(v)

    #     except ValueError:
    #         raise ValueError("Invalid format for group id")
        
    #     return v

    