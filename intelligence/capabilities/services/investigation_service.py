"""
intelligence/capabilities/services/investigation_service.py

Investigation Service.

Service for investigation capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class InvestigationService:
    """Service for investigation capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Investigation",
            description="Generic investigation capability",
            capability_type=CapabilityType.INVESTIGATION,
        )
    
    def execute(self, target: str, inputs: dict | None = None) -> dict:
        """Execute investigation capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.INVESTIGATION,
            objective=f"Investigation: {target}",
            inputs={"target": target, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
