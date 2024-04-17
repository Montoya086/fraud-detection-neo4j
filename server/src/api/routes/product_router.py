from fastapi import APIRouter
from src.api.schemas.response import DefaultResponse
from src.api.schemas.product import DeleteProductsPayload, ProductCreationPayload
from src.api.components.product import get_products_by_bank, delete_products_action, create_product_action

ProductRouter = APIRouter(
    prefix="/bankpal/product",
    tags=["product"]
)

@ProductRouter.get("/{bank_id}", response_model=DefaultResponse)
async def get_product(bank_id: str):
    return get_products_by_bank(bank_id)

@ProductRouter.delete("/{product_id}", response_model=DefaultResponse)
async def delete_product(product_id: str):
    return delete_products_action(product_id)

@ProductRouter.post("/", response_model=DefaultResponse)
async def create_product(request: ProductCreationPayload):
    return create_product_action(request)