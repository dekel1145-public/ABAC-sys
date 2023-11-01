from components.base_manager import BaseManager
from components.models.policy_models import Condition
from typing import Any, List
from exceptions import (
    PolicyAlreadyExists,
    InvalidPolicyConditions,
    AttributeNotFound,
    InvalidAttributeType,
    PolicyNotFound,
)


class PolicyManager(BaseManager):
    def __init__(self):
        """
        Initialize the PolicyManager.

        This class manages policies, including creation and validation.

        Initializes the prefix for policy keys.
        """
        super().__init__()
        self.prefix = "policy"

    async def create_policy(self, policy_id: str, conditions: List[Condition]) -> list:
        """
        Create a new policy with the provided details.
        """
        conditions = [condition.model_dump() for condition in conditions]

        await self.check_existing_policy(policy_id)
        await self.validate_policy_conditions(conditions)
        await self.create_new_policy(policy_id, conditions)

        return await self.get_policy(policy_id)

    async def check_existing_policy(self, policy_id: str) -> None:
        """
        Check if a policy with the given ID already exists.
        """
        existing_policy = await self.redis.json().get(f"{self.prefix}:{policy_id}")
        if existing_policy:
            raise PolicyAlreadyExists(f"Policy '{policy_id}' already exists")

    async def get_policy(self, policy_id: str) -> dict:
        """
        Retrieve policy details by policy ID.
        """
        policy = await self.redis.json().get(f"{self.prefix}:{policy_id}")
        if not policy:
            raise PolicyNotFound(f"Policy '{policy_id}' not found")
        return {"policy_id": policy_id, "conditions": policy}

    async def get_policy_conditions(self, policy_id: str) -> list:
        """
        Retrieve the conditions of a policy by policy ID.
        """
        policy = await self.get_policy(policy_id)
        return policy["conditions"]

    async def validate_policy_conditions(self, conditions: list) -> None:
        """
        Validate the conditions of a policy.
        """
        for condition in conditions:
            attribute_type = await self.get_attribute_type(condition["attribute_name"])
            self.validate_condition(
                condition["attribute_name"],
                attribute_type,
                condition["operator"],
                condition["value"],
            )

    async def create_new_policy(self, policy_id: str, conditions: list) -> None:
        """
        Create a new policy with the given ID and conditions.
        """
        await self.redis.json().set(f"{self.prefix}:{policy_id}", ".", conditions)

    def validate_condition(
        self, attribute_name: str, attribute_type: str, operator: str, value: Any
    ) -> None:
        """
        Validate a single condition within a policy.

        Args:
            attribute_name (str): The name of the attribute in the condition.
            attribute_type (str): The type of the attribute.
            operator (str): The operator used in the condition.
            value (Any): The value in the condition.

        Raises:
            InvalidPolicyConditions: If the condition is invalid or incompatible with the attribute type.
            InvalidAttributeType: If the attribute type is invalid.
        """
        if attribute_type == "integer":
            if not isinstance(value, int) or operator not in ("=", ">", "<"):
                raise InvalidPolicyConditions(
                    f"Invalid condition for '{attribute_name}'"
                )
        elif attribute_type == "boolean":
            if not isinstance(value, bool) or operator != "=":
                raise InvalidPolicyConditions(
                    f"Invalid condition for '{attribute_name}'"
                )
        elif attribute_type == "string":
            if not isinstance(value, str) or operator not in ("=", "starts_with"):
                raise InvalidPolicyConditions(
                    f"Invalid condition for '{attribute_name}'"
                )
        else:
            raise InvalidAttributeType(f"Invalid attribute type: '{attribute_type}'")

    async def get_attribute_type(self, attribute_name: str) -> str:
        """
        Retrieve the type of an attribute by attribute name.
        """
        attribute_type = await self.redis.get(f"attribute:{attribute_name}")
        if not attribute_type:
            raise AttributeNotFound(
                f"Attribute '{attribute_name}' not found, create it first"
            )
        return attribute_type

    async def update_policy_conditions(self, policy_id: str, conditions: list) -> list:
        conditions = [condition.model_dump() for condition in conditions]

        await self.get_policy(policy_id)
        await self.validate_policy_conditions(conditions)
        await self.create_new_policy(policy_id, conditions)
        return await self.get_policy(policy_id)
