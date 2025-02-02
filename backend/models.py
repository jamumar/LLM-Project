from pydantic import BaseModel
from typing import List

class Entity(BaseModel):
    entity: str
    type: str

class EntityResponse(BaseModel):
    openai_results: List[Entity]
    huggingface_results: List[Entity]