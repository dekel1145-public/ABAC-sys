from components.base_manager import BaseManager
from components.models.attribute_models import AttributeCollection
from typing import Any
from exceptions import (
    UserAlreadyExists,
    InvalidAttributeType,
    AttributeNotFound,
    UserNotFound,
    UserHasNoAttribute,
)


class UserManager(BaseManager):
    def __init__(self):
        """
        Initialize the UserManager.

        This class manages users, including creation, updates, and attribute validation.

        Initializes the prefix for user keys.
        """
        super().__init__()
        self.prefix = "user"

    async def create_user(self, user_id: str, attributes: AttributeCollection) -> dict:
        """
        Create a new user with the provided details.
        """
        await self.check_existing_user(user_id)
        await self.validate_attributes(attributes)
        await self.create_new_user(user_id, attributes)

        return {"user_id": user_id, "attributes": attributes}

    async def update_user(self, user_id: str, updated_attributes: dict) -> dict:
        """
        Update an existing user's attributes.
        """
        await self.get_user(user_id)
        await self.validate_attributes(updated_attributes)
        await self.delete_user(user_id)
        await self.create_new_user(user_id, updated_attributes)

        return {"user_id": user_id, "attributes": updated_attributes}

    async def check_existing_user(self, user_id: str) -> None:
        """
        Check if a user with the given ID already exists.
        """
        existing_user = await self.redis.hgetall(f"{self.prefix}:{user_id}")
        if existing_user:
            raise UserAlreadyExists(f"User '{user_id}' already exists")

    async def validate_attributes(self, attributes: dict) -> None:
        """
        Validate user attributes.
        """
        for attribute_name, attribute_value in attributes.items():
            attribute_type = await self.get_attribute_type(attribute_name)
            self.validate_attribute_type(
                attribute_name, attribute_type, attribute_value
            )

    async def get_attribute_type(self, attribute_name: str) -> str:
        """
        Get the type of an attribute.
        """
        attribute_type = await self.redis.get(f"attribute:{attribute_name}")
        if not attribute_type:
            raise AttributeNotFound(
                f"Attribute '{attribute_name}' not found, create it first"
            )
        return attribute_type

    def validate_attribute_type(
        self, attribute_name: str, attribute_type: str, attribute_value: Any
    ) -> None:
        """
        Validate the type of an attribute.
        """
        if attribute_type == "integer" and type(attribute_value) != int:
            raise InvalidAttributeType(
                f"Attribute '{attribute_name}' should be an integer"
            )
        elif attribute_type == "boolean" and type(attribute_value) != bool:
            raise InvalidAttributeType(
                f"Attribute '{attribute_name}' should be a boolean"
            )

    async def create_new_user(self, user_id: str, attributes: dict) -> None:
        """
        Create a new user with the given attributes.
        """
        await self.redis.hset(f"{self.prefix}:{user_id}", mapping=attributes)

    async def delete_user(self, user_id: str) -> None:
        """
        Delete an existing user by user ID.
        """
        await self.redis.delete(f"{self.prefix}:{user_id}")

    async def get_user(self, user_id: str) -> dict:
        """
        Get user details by user ID.
        """
        attributes = await self.redis.hgetall(f"{self.prefix}:{user_id}")
        if not attributes:
            raise UserNotFound(f"User '{user_id}' could not be found")
        return {"user_id": user_id, "attributes": attributes}

    async def get_user_attributes(self, user_id: str) -> dict:
        """
        Get a user's attributes by user ID.
        """
        user = await self.get_user(user_id)
        return user["attributes"]

    async def get_user_attribute(self, user_id: str, attribute_name: str) -> Any:
        """
        Get a specific attribute of a user by user ID and attribute name.
        """
        user_attribute_value = await self.redis.hget(
            f"{self.prefix}:{user_id}", attribute_name
        )
        if not user_attribute_value:
            raise UserHasNoAttribute(
                f"User '{user_id}' has no attribute: '{attribute_name}'"
            )
        return user_attribute_value

    async def update_user_attribute(
        self, user_id: str, attribute_name: str, attribute_value: Any
    ) -> dict:
        """
        Update a specific attribute of a user.
        """
        await self.get_user(user_id)
        attribute_type = await self.get_attribute_type(attribute_name)
        self.validate_attribute_type(attribute_name, attribute_type, attribute_value)

        await self.get_user_attribute(user_id, attribute_name)

        await self.redis.hset(
            f"{self.prefix}:{user_id}", attribute_name, attribute_value
        )

        return {
            "user_id": user_id,
            "attribute_name": attribute_name,
            "attribute_value": attribute_value,
        }

    async def delete_user_attribute(self, user_id: str, attribute_name: str) -> dict:
        """
        Delete a specific attribute of a user.
        """
        await self.get_user(user_id)
        await self.get_attribute_type(attribute_name)
        await self.get_user_attribute(user_id, attribute_name)

        await self.redis.hdel(f"{self.prefix}:{user_id}", attribute_name)

        return {
            "user_id": user_id,
            "attribute_name": attribute_name,
            "deleted": True,
        }
