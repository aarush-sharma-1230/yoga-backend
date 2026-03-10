from typing import Any
from bson import ObjectId
from fastapi.encoders import jsonable_encoder as fastapi_jsonable_encoder


def jsonable_encoder(obj: Any, **kwargs) -> Any:
    """
    Custom JSON encoder that handles MongoDB ObjectIds by converting them to strings.
    Extends FastAPI's default jsonable_encoder to automatically serialize ObjectIds.
    """
    if isinstance(obj, ObjectId):
        return str(obj)

    if isinstance(obj, dict):
        return {key: jsonable_encoder(value, **kwargs) for key, value in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [jsonable_encoder(item, **kwargs) for item in obj]

    return fastapi_jsonable_encoder(obj, **kwargs)
