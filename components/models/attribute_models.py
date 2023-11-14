from pydantic import BaseModel
from typing import Dict, Union


class AttributeCollection(BaseModel):
    attributes: Dict[str, Union[str, bool, int]]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"attributes": {"works_at": "meta", "age": 30, "tired": False}}
            ]
        }
    }


class NewAttribute(BaseModel):
    attribute_name: str
    attribute_type: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"attribute_name": "works_at", "attribute_type": "string"}]
        }
    }


class NewAttributeValue(BaseModel):
    value: str | int | bool
