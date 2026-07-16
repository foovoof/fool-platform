"""
cyber/standards/attack/serializers.py

ATT&CK Serializers.

Serializes/deserializes ATT&CK objects.
"""
from __future__ import annotations

import json
from typing import Any


class AttackSerializer:
    """
    Serializes/deserializes ATT&CK objects.
    """
    
    @staticmethod
    def serialize(obj: dict[str, Any]) -> str:
        """Serialize an ATT&CK object to JSON."""
        return json.dumps(obj, indent=2)
    
    @staticmethod
    def deserialize(json_str: str) -> dict[str, Any]:
        """Deserialize JSON to ATT&CK object."""
        return json.loads(json_str)
    
    @staticmethod
    def to_dict(obj: dict[str, Any]) -> dict[str, Any]:
        """Convert ATT&CK object to dictionary."""
        return obj.copy()
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Create ATT&CK object from dictionary."""
        return data.copy()
