from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.account_router import AccountRouter
from src.api.routes.client_router import ClientRouter
from src.api.routes.bank_router import BankRouter
from src.api.routes.product_router import ProductRouter
from src.api.routes.transaction_router import TransactionRouter

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AccountRouter)
app.include_router(ClientRouter)
app.include_router(BankRouter)
app.include_router(ProductRouter)
app.include_router(TransactionRouter)

def run():
    return app