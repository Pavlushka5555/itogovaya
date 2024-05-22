from re import T
from typing import Type, Dict, Any


def serialize_model(model: Type[T], data: Dict[str, Any]) -> T:
    if "_id" in data:
        data["id"] = str(data["_id"])
    return model(**data)