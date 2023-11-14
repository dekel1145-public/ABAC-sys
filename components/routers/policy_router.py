from fastapi import APIRouter, HTTPException
from components.models.policy_models import Policy, Condition
from typing import List
from components.policy_manager import PolicyManager
from exceptions import (
    PolicyAlreadyExists,
    InvalidPolicyConditions,
    AttributeNotFound,
    InvalidAttributeType,
    PolicyNotFound,
)

policy_router = APIRouter(tags=["policies"])
policy_manager = PolicyManager()


@policy_router.get("/{policy_id}")
async def get_policy(policy_id: str):
    try:
        return await policy_manager.get_policy(policy_id)
    except PolicyNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))


@policy_router.post("")
async def create_policy(policy: Policy):
    try:
        return await policy_manager.create_policy(policy.policy_id, policy.conditions)
    except (
        PolicyAlreadyExists,
        InvalidPolicyConditions,
        AttributeNotFound,
        InvalidAttributeType,
    ) as e:
        raise HTTPException(status_code=400, detail=str(e))


@policy_router.put("/{policy_id}")
async def update_policy_conditions(policy_id: str, conditions: List[Condition]):
    try:
        return await policy_manager.update_policy_conditions(policy_id, conditions)
    except (
        PolicyNotFound,
        InvalidPolicyConditions,
        AttributeNotFound,
        InvalidAttributeType,
    ) as e:
        raise HTTPException(status_code=400, detail=str(e))
