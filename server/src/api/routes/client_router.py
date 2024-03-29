from fastapi import APIRouter

ClientRouter = APIRouter(
    prefix="/bankpal/client",
    tags=["client"]
)