from fastapi import APIRouter

ProductRouter = APIRouter(
    prefix="/bankpal/product",
    tags=["product"]
)