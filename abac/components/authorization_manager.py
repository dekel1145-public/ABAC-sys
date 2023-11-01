from components.base_manager import BaseManager
from components.policy_manager import PolicyManager
from components.resource_manager import ResourceManager
from components.user_manager import UserManager
import asyncio


class AuthorizationManager(BaseManager):
    def __init__(self):
        """
        Initialize the AuthorizationManager.

        This class manages user authorization based on policies and attributes.

        Attributes:
            policy_manager (PolicyManager): Manages policies in the system.
            resource_manager (ResourceManager): Manages resources in the system.
            user_manager (UserManager): Manages user attributes in the system.
        """
        super().__init__()
        self.policy_manager = PolicyManager()
        self.resource_manager = ResourceManager()
        self.user_manager = UserManager()

    async def is_authorized(self, user_id: str, resource_id: str) -> bool:
        """
        Check if a user is authorized to access a resource.

        Args:
            user_id (str): The ID of the user.
            resource_id (str): The ID of the resource.

        Returns:
            bool: True if authorized, False otherwise.
        """
        user_attributes = await self.user_manager.get_user_attributes(user_id)
        resource_policies = await self.resource_manager.get_resource_policies(
            resource_id
        )

        for policy in resource_policies:
            conditions = await self.policy_manager.get_policy_conditions(policy)
            if await self.evaluate_policy(conditions, user_attributes):
                return True

        return False

    async def evaluate_policy(self, conditions: list, user_attributes: dict) -> bool:
        """
        Evaluate a policy's conditions against user attributes.

        Args:
            conditions (list): A list of conditions defining the policy.
            user_attributes (dict): The user's attributes.

        Returns:
            bool: True if the policy's conditions are met, False otherwise.
        """

        async def evaluate_condition(condition):
            attribute_name = condition["attribute_name"]
            operator = condition["operator"]
            value = condition["value"]

            if attribute_name not in user_attributes:
                return False

            user_value = user_attributes[attribute_name]

            # Convert value to appropriate type for comparison
            if type(value) == bool:
                user_value = int(user_value) == 1
            elif type(value) == int:
                user_value = int(user_value)

            if operator == "=":
                if user_value != value:
                    return False
            elif operator == "<":
                if int(user_value) >= int(value):
                    return False
            elif operator == ">":
                if int(user_value) <= int(value):
                    return False
            elif operator == "starts_with":
                if not user_value.startswith(value):
                    return False

            return True

        async def evaluate_conditions(conditions):
            tasks = [evaluate_condition(condition) for condition in conditions]
            results = await asyncio.gather(*tasks)
            return all(results)

        return await evaluate_conditions(conditions)
