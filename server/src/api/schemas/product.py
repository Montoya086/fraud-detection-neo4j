from pydantic import BaseModel

class DeleteProductsPayload(BaseModel):
    product_ids: str

class ProductCreationPayload(BaseModel):
    bank_id: str
    tipo: str
    limite_credito: float
    condiciones: str
