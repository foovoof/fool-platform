"""
threat_intelligence/campaigns/registry.py

Campaign Registry.
"""
from __future__ import annotations

from typing import Any


class CampaignRegistry:
    """
    Registry for campaign-related types and configurations.
    
    Provides lookup for relationship types, assertion types, etc.
    """
    
    _relationship_types: dict[str, str] = {
        "uses": "Campaign uses an entity",
        "targets": "Campaign targets an entity",
        "delivers": "Campaign delivers an entity",
        "exploits": "Campaign exploits an entity",
        "attributed_to": "Campaign attributed to entity",
        "associated_with": "Campaign associated with entity",
        "part_of": "Entity is part of campaign",
        "operates_in": "Campaign operates in sector/geography",
        "affects": "Campaign affects entity",
        "deploys": "Campaign deploys entity",
        "utilizes": "Campaign utilizes entity",
        "compromises": "Campaign compromises entity",
    }
    
    _assertion_types: dict[str, str] = {
        "observation": "Direct observation",
        "inference": "Inferred from evidence",
        "attribution": "Attribution claim",
        "relationship": "Relationship claim",
        "timeline": "Timeline claim",
        "capability": "Capability claim",
        "intent": "Intent claim",
        "impact": "Impact claim",
    }
    
    _evidence_types: dict[str, str] = {
        "direct": "Direct evidence",
        "circumstantial": "Circumstantial evidence",
        "corroborating": "Corroborating evidence",
        "inconsistent": "Inconsistent evidence",
    }
    
    _status_types: dict[str, str] = {
        "planned": "Campaign is planned",
        "proposed": "Campaign is proposed",
        "active": "Campaign is active",
        "on_hold": "Campaign is on hold",
        "completed": "Campaign is completed",
        "cancelled": "Campaign is cancelled",
        "archived": "Campaign is archived",
    }
    
    _severity_levels: dict[str, str] = {
        "critical": "Critical severity",
        "high": "High severity",
        "medium": "Medium severity",
        "low": "Low severity",
        "informational": "Informational severity",
    }
    
    @classmethod
    def get_relationship_types(cls) -> dict[str, str]:
        """Get all relationship types."""
        return dict(cls._relationship_types)
    
    @classmethod
    def get_relationship_description(cls, relationship_type: str) -> str:
        """Get description for relationship type."""
        return cls._relationship_types.get(relationship_type, "Unknown relationship type")
    
    @classmethod
    def get_assertion_types(cls) -> dict[str, str]:
        """Get all assertion types."""
        return dict(cls._assertion_types)
    
    @classmethod
    def get_assertion_description(cls, assertion_type: str) -> str:
        """Get description for assertion type."""
        return cls._assertion_types.get(assertion_type, "Unknown assertion type")
    
    @classmethod
    def get_evidence_types(cls) -> dict[str, str]:
        """Get all evidence types."""
        return dict(cls._evidence_types)
    
    @classmethod
    def get_evidence_description(cls, evidence_type: str) -> str:
        """Get description for evidence type."""
        return cls._evidence_types.get(evidence_type, "Unknown evidence type")
    
    @classmethod
    def get_status_types(cls) -> dict[str, str]:
        """Get all status types."""
        return dict(cls._status_types)
    
    @classmethod
    def get_status_description(cls, status: str) -> str:
        """Get description for status."""
        return cls._status_types.get(status, "Unknown status")
    
    @classmethod
    def get_severity_levels(cls) -> dict[str, str]:
        """Get all severity levels."""
        return dict(cls._severity_levels)
    
    @classmethod
    def get_severity_description(cls, severity: str) -> str:
        """Get description for severity."""
        return cls._severity_levels.get(severity, "Unknown severity")
