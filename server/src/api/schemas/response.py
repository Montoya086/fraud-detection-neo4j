from pydantic import BaseModel
from typing import Any

class DefaultResponse(BaseModel):
    message: str
    status: int
    data: Any