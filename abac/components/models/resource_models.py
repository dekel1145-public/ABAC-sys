from pydantic import BaseModel
from typing import List


class PolicyIDs(BaseModel):
    policy_ids: List[str]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "policy_ids": ["one", "two", "five"],
                }
            ]
        }
    }


class Resource(PolicyIDs):
    resource_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "resource_id": "diamond",
                    "policy_ids": ["important", "secure", "rich"],
                }
            ]
        }
    }
