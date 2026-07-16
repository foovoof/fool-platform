"""
cyber/standards/stix/serializers.py

STIX Serializers.

Serializes/deserializes STIX objects.
"""
from __future__ import annotations

import json
from typing import Any

from cyber.standards.models import StixObject


class StixSerializer:
    """
    Serializes/deserializes STIX objects.
    
    Supports JSON only.
    No file I/O. No network.
    """
    
    @staticmethod
    def serialize(obj: dict[str, Any]) -> str:
        """
        Serialize a STIX object to JSON.
        
        Args:
            obj: STIX object dictionary
            
        Returns:
            JSON string
        """
        return json.dumps(obj, indent=2)
    
    @staticmethod
    def serialize_bundle(objects: list[dict[str, Any]], spec_version: str = "2.1") -> str:
        """
        Serialize a STIX bundle to JSON.
        
        Args:
            objects: List of STIX objects
            spec_version: STIX spec version
            
        Returns:
            JSON string
        """
        bundle = {
            "type": "bundle",
            "id": f"bundle--{uuid_hex()}",
            "spec_version": spec_version,
            "objects": objects,
        }
        return json.dumps(bundle, indent=2)
    
    @staticmethod
    def deserialize(json_str: str) -> dict[str, Any]:
        """
        Deserialize JSON to STIX object.
        
        Args:
            json_str: JSON string
            
        Returns:
            STIX object dictionary
        """
        return json.loads(json_str)
    
    @staticmethod
    def deserialize_bundle(json_str: str) -> dict[str, Any]:
        """
        Deserialize JSON to STIX bundle.
        
        Args:
            json_str: JSON string
            
        Returns:
            STIX bundle dictionary
        """
        bundle = json.loads(json_str)
        
        if bundle.get("type") != "bundle":
            raise ValueError("Invalid STIX bundle")
        
        return bundle
    
    @staticmethod
    def to_dict(obj: dict[str, Any]) -> dict[str, Any]:
        """
        Convert STIX object to dictionary.
        
        Args:
            obj: STIX object
            
        Returns:
            Dictionary
        """
        return obj.copy()
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """
        Create STIX object from dictionary.
        
        Args:
            data: Dictionary
            
        Returns:
            STIX object
        """
        return data.copy()


def uuid_hex() -> str:
    """Generate a UUID hex string."""
    import uuid
    return uuid.uuid4().hex
