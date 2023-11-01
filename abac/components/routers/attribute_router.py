from components.attribute_manager import AttributeManager
from components.models.attribute_models import NewAttribute
from exceptions import AttributeNotFound, AttributeAlreadyExists, AttributeWrongType
from fastapi import APIRouter, HTTPException

attribute_router = APIRouter(tags=["attributes"])
attribute_manager = AttributeManager()


@attribute_router.get("/{name}")
async def get_attribute(name: str):
    try:
        return await attribute_manager.get_attribute(name)
    except AttributeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@attribute_router.post("")
async def create_attribute(new_attribute: NewAttribute):
    try:
        return await attribute_manager.create_attribute(
            attribute_name=new_attribute.attribute_name,
            attribute_type=new_attribute.attribute_type,
        )
    except (AttributeAlreadyExists, AttributeWrongType) as e:
        raise HTTPException(status_code=400, detail=str(e))
