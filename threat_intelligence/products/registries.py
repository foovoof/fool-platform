"""
threat_intelligence/products/registries.py

Intelligence Products Registries.
"""
from __future__ import annotations


class ProductTypeRegistry:
    """Registry for product types."""
    
    _types: dict[str, str] = {
        "threat_report": "Threat Report",
        "technical_report": "Technical Report",
        "strategic_report": "Strategic Report",
        "operational_report": "Operational Report",
        "tactical_report": "Tactical Report",
        "executive_summary": "Executive Summary",
        "indicator_list": "Indicator List",
        "ioc_bulletin": "IOC Bulletin",
        "ttp_analysis": "TTP Analysis",
        "campaign_report": "Campaign Report",
        "threat_actor_profile": "Threat Actor Profile",
        "malware_analysis": "Malware Analysis",
        "vulnerability_advisory": "Vulnerability Advisory",
        "infrastructure_report": "Infrastructure Report",
    }
    
    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Get all product types."""
        return dict(cls._types)
    
    @classmethod
    def get_description(cls, product_type: str) -> str:
        """Get description for type."""
        return cls._types.get(product_type, "Unknown type")
    
    @classmethod
    def is_valid(cls, product_type: str) -> bool:
        """Check if type is valid."""
        return product_type in cls._types


class ClassificationRegistry:
    """Registry for classification levels."""
    
    _levels: dict[str, str] = {
        "unclassified": "Unclassified",
        "internal": "Internal",
        "confidential": "Confidential",
        "secret": "Secret",
        "top_secret": "Top Secret",
    }
    
    @classmethod
    def get_levels(cls) -> dict[str, str]:
        """Get all classification levels."""
        return dict(cls._levels)
    
    @classmethod
    def get_description(cls, level: str) -> str:
        """Get description for level."""
        return cls._levels.get(level, "Unknown level")


class SensitivityRegistry:
    """Registry for sensitivity levels."""
    
    _levels: dict[str, str] = {
        "public": "Public",
        "restricted": "Restricted",
        "confidential": "Confidential",
        "sensitive": "Sensitive",
        "personal": "Personal",
    }
    
    @classmethod
    def get_levels(cls) -> dict[str, str]:
        """Get all sensitivity levels."""
        return dict(cls._levels)


class AudienceRegistry:
    """Registry for audience types."""
    
    _audiences: dict[str, str] = {
        "executive": "Executive",
        "technical": "Technical",
        "operational": "Operational",
        "tactical": "Tactical",
        "general": "General",
        "specialized": "Specialized",
    }
    
    @classmethod
    def get_audiences(cls) -> dict[str, str]:
        """Get all audience types."""
        return dict(cls._audiences)


class LifecycleRegistry:
    """Registry for lifecycle states."""
    
    _states: dict[str, str] = {
        "draft": "Draft",
        "under_review": "Under Review",
        "validated": "Validated",
        "approved": "Approved",
        "published": "Published",
        "superseded": "Superseded",
        "deprecated": "Deprecated",
        "archived": "Archived",
    }
    
    @classmethod
    def get_states(cls) -> dict[str, str]:
        """Get all lifecycle states."""
        return dict(cls._states)
    
    @classmethod
    def get_valid_transitions(cls) -> dict[str, list[str]]:
        """Get valid state transitions."""
        return {
            "draft": ["under_review", "archived"],
            "under_review": ["validated", "draft", "archived"],
            "validated": ["approved", "under_review", "archived"],
            "approved": ["published", "archived"],
            "published": ["superseded", "deprecated", "archived"],
            "superseded": ["deprecated", "archived"],
            "deprecated": ["archived"],
            "archived": [],
        }


class VersionRegistry:
    """Registry for version management."""
    
    _components: list[str] = ["major", "minor", "patch"]
    
    @classmethod
    def get_components(cls) -> list[str]:
        """Get version components."""
        return list(cls._components)
    
    @classmethod
    def parse_version(cls, version: str) -> tuple[int, int, int]:
        """Parse version string."""
        parts = version.split(".")
        return (
            int(parts[0]) if len(parts) > 0 else 0,
            int(parts[1]) if len(parts) > 1 else 0,
            int(parts[2]) if len(parts) > 2 else 0,
        )


class RelationshipRegistry:
    """Registry for product relationships."""
    
    _relationships: dict[str, str] = {
        "supersedes": "Supersedes product",
        "superseded_by": "Superseded by product",
        "related_to": "Related to product",
        "references": "References product",
        "referenced_by": "Referenced by product",
        "part_of": "Part of product",
        "contains": "Contains product",
    }
    
    @classmethod
    def get_relationships(cls) -> dict[str, str]:
        """Get all relationship types."""
        return dict(cls._relationships)
    
    @classmethod
    def get_description(cls, rel_type: str) -> str:
        """Get description for relationship type."""
        return cls._relationships.get(rel_type, "Unknown relationship")


class AssertionTypeRegistry:
    """Registry for assertion types."""
    
    _types: dict[str, str] = {
        "finding": "Finding",
        "assessment": "Assessment",
        "recommendation": "Recommendation",
        "observation": "Observation",
        "conclusion": "Conclusion",
    }
    
    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Get all assertion types."""
        return dict(cls._types)


class EvidenceTypeRegistry:
    """Registry for evidence types."""
    
    _types: dict[str, str] = {
        "raw_data": "Raw Data",
        "screenshot": "Screenshot",
        "log": "Log",
        "network_capture": "Network Capture",
        "code_sample": "Code Sample",
        "document": "Document",
        "external_reference": "External Reference",
    }
    
    @classmethod
    def get_types(cls) -> dict[str, str]:
        """Get all evidence types."""
        return dict(cls._types)
