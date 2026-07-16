"""
cyber/standards/cve/serializers.py

CVE Serializers.
"""
from __future__ import annotations

import json
from typing import Any


class CveSerializer:
    """Serializes/deserializes CVE objects."""
    
    @staticmethod
    def serialize(obj: dict[str, Any]) -> str:
        """Serialize to JSON."""
        return json.dumps(obj, indent=2)
    
    @staticmethod
    def deserialize(json_str: str) -> dict[str, Any]:
        """Deserialize from JSON."""
        return json.loads(json_str)
    
    @staticmethod
    def to_dict(obj: dict[str, Any]) -> dict[str, Any]:
        """Convert to dictionary."""
        return obj.copy()
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Create from dictionary."""
        return data.copy()
