from components.base_manager import BaseManager
from exceptions import AttributeNotFound, AttributeAlreadyExists, AttributeWrongType


class AttributeManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.allowed_types = ["boolean", "string", "integer"]
        self.prefix = "attribute"

    async def get_attribute(self, attribute_name: str) -> dict:
        """
        Retrieve details of a specific attribute by its name
        """
        attribute_type = await self.redis.get(f"{self.prefix}:{attribute_name}")
        if not attribute_type:
            raise AttributeNotFound(f"Attribute '{attribute_name}' not found")
        return {"name": attribute_name, "type": attribute_type}

    async def create_attribute(self, attribute_name: str, attribute_type: str) -> dict:
        """
        Create a new attribute with the given name and type
        """

        # Check if the attribute already exists
        existing_attribute = await self.redis.get(f"{self.prefix}:{attribute_name}")
        if existing_attribute:
            raise AttributeAlreadyExists(f"Attribute '{attribute_name}' already exists")

        # Check if the provided attribute type is allowed
        if attribute_type not in self.allowed_types:
            raise AttributeWrongType(f"Wrong attribute type: {attribute_type}")

        await self.redis.set(f"{self.prefix}:{attribute_name}", attribute_type)
        return {"status": "success"}
