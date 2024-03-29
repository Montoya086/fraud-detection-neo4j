from fastapi import APIRouter
from src.api.schemas.response import DefaultResponse
from src.api.schemas.account import AccountCreationPayload
from src.api.components.account import create_account_action, get_account_by_number, delete_account_action

AccountRouter = APIRouter(
    prefix="/bankpal/account",
    tags=["account"]
)

@AccountRouter.get("/{account_number}", response_model=DefaultResponse)
async def get_account(account_number: str):
    return get_account_by_number(account_number)

@AccountRouter.post("/", response_model=DefaultResponse)
async def create_account(request: AccountCreationPayload):
    return create_account_action(request)

@AccountRouter.delete("/{account_number}", response_model=DefaultResponse)
async def delete_account(account_number: str):
    return delete_account_action(account_number)