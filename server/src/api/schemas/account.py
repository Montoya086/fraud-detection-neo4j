from pydantic import BaseModel, validator

class AccountCreationPayload(BaseModel):
    tipo: str
    saldo: float
    cliente_id: str
    bank_id: str

class AccountsUpgradePayload(BaseModel):
    account_numbers: list[str]
    is_premium: bool

class GetAllAccountsPayload(BaseModel):
    order_by: str = "balance"
    order: str = "asc"
    