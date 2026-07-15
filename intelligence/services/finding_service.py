"""
intelligence/services/finding_service.py

Finding Service.

Manages intelligence findings.
"""
from typing import Any

from intelligence.models import IntelligenceFinding, FindingType


class FindingService:
    """
    Service for finding management.
    
    Coordinates:
    - Finding creation
    - Finding retrieval
    - Finding aggregation
    """
    
    def __init__(self) -> None:
        """Initialize the service."""
        self._findings: dict[str, IntelligenceFinding] = {}
    
    def create_finding(
        self,
        finding_type: str,
        title: str,
        description: str,
        confidence: float = 0.5,
        evidence_refs: list[str] | None = None,
        source_task_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new finding.
        
        Args:
            finding_type: Type of finding
            title: Finding title
            description: Finding description
            confidence: Confidence level
            evidence_refs: Evidence references
            source_task_id: Source task ID
            metadata: Optional metadata
            
        Returns:
            Created finding
        """
        finding = IntelligenceFinding(
            finding_type=FindingType(finding_type),
            title=title,
            description=description,
            confidence=confidence,
            evidence_refs=evidence_refs or [],
            source_task_id=source_task_id,
            metadata=metadata or {},
        )
        
        self._findings[finding.finding_id] = finding
        
        return finding.to_dict()
    
    def get_finding(self, finding_id: str) -> dict[str, Any] | None:
        """Get finding by ID."""
        finding = self._findings.get(finding_id)
        if finding:
            return finding.to_dict()
        return None
    
    def list_findings(
        self,
        finding_type: str | None = None,
        source_task_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        List findings with optional filters.
        
        Args:
            finding_type: Optional type filter
            source_task_id: Optional task filter
            
        Returns:
            List of findings
        """
        findings = list(self._findings.values())
        
        if finding_type:
            findings = [
                f for f in findings
                if f.finding_type.value == finding_type
            ]
        
        if source_task_id:
            findings = [
                f for f in findings
                if f.source_task_id == source_task_id
            ]
        
        return [f.to_dict() for f in findings]
    
    def aggregate_findings(
        self,
        finding_ids: list[str],
    ) -> list[dict[str, Any]]:
        """
        Aggregate multiple findings.
        
        Args:
            finding_ids: IDs of findings to aggregate
            
        Returns:
            Aggregated findings
        """
        return [
            self._findings[fid].to_dict()
            for fid in finding_ids
            if fid in self._findings
        ]
