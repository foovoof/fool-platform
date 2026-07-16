"""OpenIOC Serializers."""
import json
from typing import Any


class OpenIOCSerializer:
    """Serializes/deserializes OpenIOC objects."""
    
    @staticmethod
    def serialize(obj: dict[str, Any]) -> str:
        return json.dumps(obj, indent=2)
    
    @staticmethod
    def deserialize(json_str: str) -> dict[str, Any]:
        return json.loads(json_str)
    
    @staticmethod
    def to_dict(obj: dict[str, Any]) -> dict[str, Any]:
        return obj.copy()
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> dict[str, Any]:
        return data.copy()
