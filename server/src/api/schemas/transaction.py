from pydantic import BaseModel

class Transaction(BaseModel):
    metodo: str
    monto: float
    to_account_number: str
    from_account_number: str