"""
intelligence/capabilities/registry/__init__.py

Capability Registry.

Manages capability definitions and discovery.
"""
from __future__ import annotations

from typing import Any

from intelligence.capabilities.models import (
    CapabilityDefinition,
    CapabilityType,
)


class CapabilityRegistry:
    """
    Registry for intelligence capabilities.
    
    Manages capability definitions and discovery.
    """
    
    def __init__(self) -> None:
        """Initialize the registry."""
        self._capabilities: dict[str, CapabilityDefinition] = {}
        self._by_type: dict[CapabilityType, str] = {}
        self._by_name: dict[str, str] = {}
    
    def register(self, capability: CapabilityDefinition) -> bool:
        """
        Register a capability.
        
        Args:
            capability: Capability to register
            
        Returns:
            True if registered successfully
        """
        if not self._validate_capability(capability):
            return False
        
        self._capabilities[capability.capability_id] = capability
        self._by_type[capability.capability_type] = capability.capability_id
        self._by_name[capability.name.lower()] = capability.capability_id
        
        return True
    
    def unregister(self, capability_id: str) -> bool:
        """
        Unregister a capability.
        
        Args:
            capability_id: ID of capability to unregister
            
        Returns:
            True if unregistered
        """
        capability = self._capabilities.get(capability_id)
        if not capability:
            return False
        
        del self._capabilities[capability_id]
        del self._by_type[capability.capability_type]
        del self._by_name[capability.name.lower()]
        
        return True
    
    def get(self, capability_id: str) -> CapabilityDefinition | None:
        """Get capability by ID."""
        return self._capabilities.get(capability_id)
    
    def get_by_type(self, capability_type: CapabilityType) -> CapabilityDefinition | None:
        """Get capability by type."""
        capability_id = self._by_type.get(capability_type)
        if capability_id:
            return self._capabilities.get(capability_id)
        return None
    
    def get_by_name(self, name: str) -> CapabilityDefinition | None:
        """Get capability by name."""
        capability_id = self._by_name.get(name.lower())
        if capability_id:
            return self._capabilities.get(capability_id)
        return None
    
    def list_all(self) -> list[CapabilityDefinition]:
        """List all registered capabilities."""
        return list(self._capabilities.values())
    
    def list_by_type(self, capability_type: CapabilityType) -> list[CapabilityDefinition]:
        """List capabilities by type."""
        return [
            c for c in self._capabilities.values()
            if c.capability_type == capability_type
        ]
    
    def search(self, query: str) -> list[CapabilityDefinition]:
        """
        Search capabilities by name or description.
        
        Args:
            query: Search query
            
        Returns:
            Matching capabilities
        """
        query_lower = query.lower()
        results = []
        
        for capability in self._capabilities.values():
            if (query_lower in capability.name.lower() or
                query_lower in capability.description.lower()):
                results.append(capability)
        
        return results
    
    def exists(self, capability_id: str) -> bool:
        """Check if capability exists."""
        return capability_id in self._capabilities
    
    def count(self) -> int:
        """Get total capability count."""
        return len(self._capabilities)
    
    def _validate_capability(self, capability: CapabilityDefinition) -> bool:
        """Validate capability before registration."""
        if not capability.capability_id:
            return False
        if not capability.name:
            return False
        if not capability.capability_type:
            return False
        return True


def create_default_registry() -> CapabilityRegistry:
    """
    Create registry with default capability definitions.
    
    Returns:
        Registry with default capabilities
    """
    registry = CapabilityRegistry()
    
    default_capabilities = [
        CapabilityDefinition(
            name="Research",
            description="Generic research capability for investigating topics",
            capability_type=CapabilityType.RESEARCH,
            inputs={"topic": "string"},
            outputs={"findings": "list"},
        ),
        CapabilityDefinition(
            name="Discovery",
            description="Generic discovery capability for finding entities",
            capability_type=CapabilityType.DISCOVERY,
            inputs={"criteria": "object"},
            outputs={"entities": "list"},
        ),
        CapabilityDefinition(
            name="Extraction",
            description="Generic extraction capability for extracting data",
            capability_type=CapabilityType.EXTRACTION,
            inputs={"source": "string", "pattern": "string"},
            outputs={"data": "object"},
        ),
        CapabilityDefinition(
            name="Correlation",
            description="Generic correlation capability for finding relationships",
            capability_type=CapabilityType.CORRELATION,
            inputs={"entities": "list"},
            outputs={"relationships": "list"},
        ),
        CapabilityDefinition(
            name="Investigation",
            description="Generic investigation capability for deep analysis",
            capability_type=CapabilityType.INVESTIGATION,
            inputs={"target": "string"},
            outputs={"findings": "list"},
        ),
        CapabilityDefinition(
            name="Assessment",
            description="Generic assessment capability for evaluating subjects",
            capability_type=CapabilityType.ASSESSMENT,
            inputs={"subject": "string"},
            outputs={"evaluation": "object"},
        ),
        CapabilityDefinition(
            name="Reporting",
            description="Generic reporting capability for generating reports",
            capability_type=CapabilityType.REPORTING,
            inputs={"data": "object", "format": "string"},
            outputs={"report": "string"},
        ),
        CapabilityDefinition(
            name="Timeline",
            description="Generic timeline capability for event sequencing",
            capability_type=CapabilityType.TIMELINE,
            inputs={"events": "list"},
            outputs={"timeline": "list"},
        ),
        CapabilityDefinition(
            name="EvidenceAnalysis",
            description="Generic evidence analysis capability",
            capability_type=CapabilityType.EVIDENCE_ANALYSIS,
            inputs={"evidence": "list"},
            outputs={"analysis": "object"},
        ),
    ]
    
    for capability in default_capabilities:
        registry.register(capability)
    
    return registry
