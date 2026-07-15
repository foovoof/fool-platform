"""
intelligence/capabilities/services/discovery_service.py

Discovery Service.

Service for discovery capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class DiscoveryService:
    """Service for discovery capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Discovery",
            description="Generic discovery capability",
            capability_type=CapabilityType.DISCOVERY,
        )
    
    def execute(self, criteria: dict, inputs: dict | None = None) -> dict:
        """Execute discovery capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.DISCOVERY,
            objective="Discovery",
            inputs={"criteria": criteria, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
