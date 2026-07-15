"""
intelligence/capabilities/services/extraction_service.py

Extraction Service.

Service for extraction capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class ExtractionService:
    """Service for extraction capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Extraction",
            description="Generic extraction capability",
            capability_type=CapabilityType.EXTRACTION,
        )
    
    def execute(self, source: str, pattern: str, inputs: dict | None = None) -> dict:
        """Execute extraction capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.EXTRACTION,
            objective="Extraction",
            inputs={"source": source, "pattern": pattern, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
