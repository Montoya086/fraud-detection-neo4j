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
    order_by: str = "none"
    order: str = "asc"

    @validator('order_by')
    def validate_sort(cls, v):
        allowed = {'none', 'date'}
        if v.lower() not in allowed:
            raise ValueError(f"Order by '{v}' is not allowed.")
        return v
    
    @validator('order')
    def validate_order(cls, v):
        allowed = {'asc', 'desc'}
        if v.lower() not in allowed:
            raise ValueError(f"Order '{v}' is not allowed.")
        return v
    