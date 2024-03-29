from fastapi import APIRouter
from src.api.schemas.response import DefaultResponse
from src.api.components.bank import get_bank_action, get_banks_action

BankRouter = APIRouter(
    prefix="/bankpal/bank",
    tags=["bank"]
)

@BankRouter.get("/{name}")
async def get_banks(name: str = None):
    return get_banks_action(name)

@BankRouter.get("/details/{bank_id}", response_model=DefaultResponse)
async def get_bank(bank_id: str):
    return get_bank_action(bank_id)