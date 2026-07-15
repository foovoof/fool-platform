"""
intelligence/capabilities/services/assessment_service.py

Assessment Service.

Service for assessment capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class AssessmentService:
    """Service for assessment capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Assessment",
            description="Generic assessment capability",
            capability_type=CapabilityType.ASSESSMENT,
        )
    
    def execute(self, subject: str, inputs: dict | None = None) -> dict:
        """Execute assessment capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.ASSESSMENT,
            objective=f"Assessment: {subject}",
            inputs={"subject": subject, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
