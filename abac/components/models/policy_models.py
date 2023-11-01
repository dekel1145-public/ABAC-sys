from pydantic import BaseModel
from typing import List


class Condition(BaseModel):
    attribute_name: str
    operator: str
    value: str | int | bool

    model_config = {
        "json_schema_extra": {
            "examples": [{"attribute_name": "war", "operator": "=", "value": "hamas"}]
        }
    }


class Policy(BaseModel):
    policy_id: str
    conditions: List[Condition]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "policy_id": "most_secure",
                    "conditions": [
                        {
                            "attribute_name": "works_at",
                            "operator": "starts_with",
                            "value": "met",
                        },
                        {"attribute_name": "age", "operator": ">", "value": 50},
                        {"attribute_name": "happy", "operator": "=", "value": True},
                    ],
                }
            ]
        }
    }
