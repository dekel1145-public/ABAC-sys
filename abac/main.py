import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from components.routers.attribute_router import attribute_router
from components.routers.user_router import user_router
from components.routers.policy_router import policy_router
from components.routers.resource_router import resource_router
from components.routers.authorization_router import authorization_router
from components.authorization_manager import AuthorizationManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check for database connection
    authorization_manager = AuthorizationManager()
    await authorization_manager.redis.ping()
    yield
    await authorization_manager.redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(attribute_router, prefix="/attributes", tags=["attributes"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(policy_router, prefix="/policies", tags=["policies"])
app.include_router(resource_router, prefix="/resources", tags=["resources"])
app.include_router(
    authorization_router, prefix="/is_authorized", tags=["authorization"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
