from components.models.resource_models import Resource, PolicyIDs
from components.resource_manager import ResourceManager
from exceptions import (
    ResourceAlreadyExists,
    PolicyNotFound,
    InvalidResource,
    ResourceNotFound,
)
from fastapi import APIRouter, HTTPException

resource_router = APIRouter(tags=["resources"])
resource_manager = ResourceManager()


@resource_router.get("/{resource_id}")
async def get_resource(resource_id: str):
    try:
        return await resource_manager.get_resource(resource_id)
    except ResourceNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))


@resource_router.post("")
async def create_resource(resource: Resource):
    try:
        return await resource_manager.create_resource(
            resource.resource_id, resource.policy_ids
        )
    except (ResourceAlreadyExists, PolicyNotFound, InvalidResource) as e:
        raise HTTPException(status_code=400, detail=str(e))


@resource_router.put("/{resource_id}")
async def update_resource_policies(resource_id: str, new_policy_ids: PolicyIDs):
    try:
        return await resource_manager.update_resource_policies(
            resource_id, new_policy_ids.policy_ids
        )
    except (ResourceNotFound, PolicyNotFound, InvalidResource) as e:
        raise HTTPException(status_code=400, detail=str(e))
