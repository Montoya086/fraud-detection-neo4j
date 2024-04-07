from fastapi import APIRouter
from src.api.schemas.response import DefaultResponse
from src.api.schemas.transaction import Transaction
from src.api.components.transaction import evaluate_transaction_action

TransactionRouter = APIRouter(
    prefix="/bankpal/transaction",
    tags=["transaction"]
)

@TransactionRouter.post("/", response_model=DefaultResponse)
async def evaluate_transaction(request: Transaction):
    return evaluate_transaction_action(request)