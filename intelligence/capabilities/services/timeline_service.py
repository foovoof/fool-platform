"""
intelligence/capabilities/services/timeline_service.py

Timeline Service.

Service for timeline capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class TimelineService:
    """Service for timeline capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Timeline",
            description="Generic timeline capability",
            capability_type=CapabilityType.TIMELINE,
        )
    
    def execute(self, events: list, inputs: dict | None = None) -> dict:
        """Execute timeline capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.TIMELINE,
            objective="Generate Timeline",
            inputs={"events": events, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
