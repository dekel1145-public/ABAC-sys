from components.base_manager import BaseManager
from components.policy_manager import PolicyManager
from exceptions import (
    ResourceAlreadyExists,
    InvalidResource,
    ResourceNotFound,
)
from typing import List


class ResourceManager(BaseManager):
    def __init__(self):
        """
        Initialize the ResourceManager.

        This class manages resources, including creation and validation of policies.

        Initializes the prefix for resource keys and an instance of PolicyManager.
        """
        super().__init__()
        self.prefix = "resource"
        self.policy_manager = PolicyManager()

    async def create_resource(self, resource_id: str, policy_ids: List[str]) -> dict:
        """
        Create a new resource with the provided details.
        """
        await self.check_existing_resource(resource_id)
        await self.validate_policies(policy_ids)
        await self.create_new_resource(resource_id, policy_ids)

        return {"resource_id": resource_id, "policy_ids": policy_ids}

    async def check_existing_resource(self, resource_id: str) -> None:
        """
        Check if a resource with the given ID already exists.
        """
        existing_resource = await self.redis.exists(f"{self.prefix}:{resource_id}")
        if existing_resource:
            raise ResourceAlreadyExists(f"Resource '{resource_id}' already exists")

    async def validate_policies(self, policy_ids: list) -> None:
        """
        Validate the list of policy IDs.
        """
        for policy_id in policy_ids:
            await self.policy_manager.get_policy(policy_id)

    async def create_new_resource(self, resource_id: str, policy_ids: list) -> None:
        """
        Create a new resource with the given ID and associated policy IDs.
        """
        await self.redis.sadd(f"{self.prefix}:{resource_id}", *policy_ids)

    async def get_resource(self, resource_id: str) -> dict:
        """
        Retrieve resource details by resource ID.
        """
        exists = await self.redis.exists(f"{self.prefix}:{resource_id}")
        if not exists:
            raise ResourceNotFound(f"Resource '{resource_id}' not found")
        policy_ids = await self.redis.smembers(f"{self.prefix}:{resource_id}")

        return {"resource_id": resource_id, "policy_ids": policy_ids}

    async def get_resource_policies(self, resource_id: str) -> dict:
        """
        Retrieve the policy IDs associated with a resource by resource ID.
        """
        resource = await self.get_resource(resource_id)
        return resource["policy_ids"]

    async def update_resource_policies(
        self, resource_id: str, policy_ids: list
    ) -> dict:
        """
        Update the associated policy IDs for an existing resource.
        """
        await self.get_resource(resource_id)
        await self.validate_policies(policy_ids)
        await self.redis.delete(f"{self.prefix}:{resource_id}")
        await self.create_new_resource(resource_id, policy_ids)

        return {"resource_id": resource_id, "policy_ids": policy_ids}
