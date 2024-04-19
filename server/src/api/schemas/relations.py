from pydantic import BaseModel
from typing import Optional

class RelationUpdatePayload(BaseModel):
    relation_ids: list[str]
    details: Optional[str] = None

class RelationDeletePayload(BaseModel):
    relation_ids: list[str]