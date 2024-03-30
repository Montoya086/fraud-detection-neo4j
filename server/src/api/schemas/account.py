from pydantic import BaseModel

class AccountCreationPayload(BaseModel):
    tipo: str
    saldo: float
    cliente_id: str
    bank_id: str

class AccountsUpgradePayload(BaseModel):
    account_numbers: list[str]
    is_premium: bool
    