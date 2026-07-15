"""
intelligence/capabilities/services/correlation_service.py

Correlation Service.

Service for correlation capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class CorrelationService:
    """Service for correlation capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Correlation",
            description="Generic correlation capability",
            capability_type=CapabilityType.CORRELATION,
        )
    
    def execute(self, entities: list, inputs: dict | None = None) -> dict:
        """Execute correlation capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.CORRELATION,
            objective="Correlation",
            inputs={"entities": entities, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
