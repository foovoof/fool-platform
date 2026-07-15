"""
intelligence/capabilities/services/research_service.py

Research Service.

Service for research capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class ResearchService:
    """Service for research capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Research",
            description="Generic research capability",
            capability_type=CapabilityType.RESEARCH,
        )
    
    def execute(self, topic: str, inputs: dict | None = None) -> dict:
        """Execute research capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.RESEARCH,
            objective=f"Research: {topic}",
            inputs={"topic": topic, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
