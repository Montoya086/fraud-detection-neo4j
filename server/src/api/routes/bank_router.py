from fastapi import APIRouter
from src.api.schemas.response import DefaultResponse
from src.api.schemas.bank import BankHiringPayload, BankFiringPayload
from src.api.components.bank import get_bank_action, get_banks_action, fire_bank_action, hire_bank_action

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

@BankRouter.post("/hire", response_model=DefaultResponse)
async def hire_bank(request: BankHiringPayload):
    return hire_bank_action(request.client_ids)

@BankRouter.post("/fire", response_model=DefaultResponse)
async def fire_bank(request: BankFiringPayload):
    return fire_bank_action(request.worker_ids)
    