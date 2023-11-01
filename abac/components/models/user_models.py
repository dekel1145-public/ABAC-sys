from components.models.attribute_models import AttributeCollection
from typing import Dict


class User(AttributeCollection):
    user_id: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "elonmusk",
                    "attributes": {"works_at": "X", "age": 52, "tired": True},
                }
            ]
        }
    }
