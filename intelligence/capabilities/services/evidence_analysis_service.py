"""
intelligence/capabilities/services/evidence_analysis_service.py

Evidence Analysis Service.

Service for evidence analysis capability.
"""
from __future__ import annotations

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityType,
    CapabilityDefinition,
)
from intelligence.capabilities.services.capability_service import CapabilityService


class EvidenceAnalysisService:
    """Service for evidence analysis capability."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self._capability_service = CapabilityService()
        self._capability = CapabilityDefinition(
            name="EvidenceAnalysis",
            description="Generic evidence analysis capability",
            capability_type=CapabilityType.EVIDENCE_ANALYSIS,
        )
    
    def execute(self, evidence: list, inputs: dict | None = None) -> dict:
        """Execute evidence analysis capability."""
        task = CapabilityTask(
            capability_id=self._capability.capability_id,
            capability_type=CapabilityType.EVIDENCE_ANALYSIS,
            objective="Analyze Evidence",
            inputs={"evidence": evidence, **(inputs or {})},
        )
        
        result = self._capability_service.execute_task(task)
        return result.to_dict()
