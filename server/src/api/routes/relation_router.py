from fastapi import APIRouter
from src.api.schemas.response import DefaultResponse
from src.api.schemas.relations import RelationUpdatePayload, RelationDeletePayload
from src.api.components.relation import update_relations_action, delete_relations_action

RelationRouter = APIRouter(
    prefix="/bankpal/relation",
    tags=["relation"]
)

@RelationRouter.put("/", response_model=DefaultResponse)
async def update_relation(request: RelationUpdatePayload):
    return update_relations_action(request)

@RelationRouter.delete("/", response_model=DefaultResponse)
async def delete_relation(request: RelationDeletePayload):
    return delete_relations_action(request)