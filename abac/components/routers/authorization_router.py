from fastapi import APIRouter, HTTPException
from components.authorization_manager import AuthorizationManager
from exceptions import UserNotFound, ResourceNotFound

authorization_router = APIRouter(tags=["authorization"])
authorization_manager = AuthorizationManager()


@authorization_router.get("")
async def is_authorized(user_id: str, resource_id: str):
    try:
        decision = await authorization_manager.is_authorized(user_id, resource_id)
        return {"allowed": decision}
    except (UserNotFound, ResourceNotFound) as e:
        raise HTTPException(status_code=400, detail=str(e))
