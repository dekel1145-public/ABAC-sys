from components.user_manager import UserManager
from components.models.attribute_models import AttributeCollection, NewAttributeValue
from components.models.user_models import User
from exceptions import (
    UserAlreadyExists,
    InvalidAttributeType,
    AttributeNotFound,
    UserNotFound,
    UserHasNoAttribute,
)
from fastapi import APIRouter, HTTPException


user_router = APIRouter(tags=["users"])
user_manager = UserManager()


@user_router.get("/{user_id}")
async def get_user(user_id: str):
    try:
        return await user_manager.get_user(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("")
async def create_user(user: User):
    try:
        return await user_manager.create_user(user.user_id, user.attributes)
    except (UserAlreadyExists, InvalidAttributeType, AttributeNotFound) as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.put("/{user_id}")
async def update_user(user_id: str, updated_attributes: AttributeCollection):
    try:
        return await user_manager.update_user(user_id, updated_attributes.attributes)
    except (UserNotFound, InvalidAttributeType, AttributeNotFound) as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.patch("/{user_id}/attributes/{attribute_name}")
async def update_user_attribute(
    user_id: str, attribute_name: str, value: NewAttributeValue
):
    try:
        return await user_manager.update_user_attribute(
            user_id, attribute_name, value.value
        )
    except (
        UserNotFound,
        InvalidAttributeType,
        AttributeNotFound,
        UserHasNoAttribute,
    ) as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{user_id}/attributes/{attribute_name}")
async def delete_user_attribute(user_id: str, attribute_name: str):
    try:
        return await user_manager.delete_user_attribute(user_id, attribute_name)
    except (UserNotFound, AttributeNotFound, UserHasNoAttribute) as e:
        raise HTTPException(status_code=400, detail=str(e))
