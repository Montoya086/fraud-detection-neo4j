from fastapi import APIRouter

TransactionRouter = APIRouter(
    prefix="/bankpal/transaction",
    tags=["transaction"]
)