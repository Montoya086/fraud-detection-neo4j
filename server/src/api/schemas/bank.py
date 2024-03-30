from pydantic import BaseModel

class BankHiringPayload(BaseModel):
    client_ids: list[str]

class BankFiringPayload(BaseModel):
    worker_ids: list[str]