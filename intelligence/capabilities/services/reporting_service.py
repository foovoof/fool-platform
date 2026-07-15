"""
intelligence/capabilities/services/reporting_service.py

Reporting Service.

Service for reporting capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class ReportingService:
    """Service for reporting capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="Reporting",
            description="Generic reporting capability",
            capability_type=CapabilityType.REPORTING,
        )
    
    def execute(self, data: dict, format: str = "text", inputs: dict | None = None) -> dict:
        """Execute reporting capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.REPORTING,
            objective="Generate Report",
            inputs={"data": data, "format": format, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
