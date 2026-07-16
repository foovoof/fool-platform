"""
threat_intelligence/evidence.py

Evidence Module.

Provides evidence management capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from threat_intelligence.models import (
    EvidenceReference,
    EvidenceBundle,
    EvidenceTimeline,
    EvidenceLineage,
    EvidenceType,
)


@dataclass(frozen=True)
class EvidenceValidation:
    """Evidence validation result."""
    is_valid: bool = True
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)


class EvidenceValidator:
    """
    Validator for evidence.
    """
    
    @classmethod
    def validate(cls, evidence: EvidenceReference) -> EvidenceValidation:
        """Validate evidence reference."""
        errors = []
        warnings = []
        
        if not evidence.id:
            errors.append("Evidence ID is required")
        
        if not evidence.content and not evidence.source_id:
            errors.append("Either content or source_id is required")
        
        if evidence.evidence_type == EvidenceType.DIRECT.value:
            if not evidence.chain_of_custody:
                warnings.append("Direct evidence should have chain of custody")
        
        return EvidenceValidation(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )


class EvidenceChainBuilder:
    """
    Builder for evidence chains.
    """
    
    def __init__(self) -> None:
        self._evidence: list[dict[str, Any]] = []
    
    def add_evidence(
        self,
        evidence_id: str,
        evidence_type: str,
        description: str,
    ) -> EvidenceChainBuilder:
        """Add evidence to chain."""
        self._evidence.append({
            "evidence_id": evidence_id,
            "evidence_type": evidence_type,
            "description": description,
            "added_at": datetime.now(timezone.utc).isoformat(),
        })
        return self
    
    def build(self) -> EvidenceBundle:
        """Build evidence bundle."""
        return EvidenceBundle(
            title="Evidence Chain",
            description=f"Contains {len(self._evidence)} evidence items",
            evidence_items=tuple(self._evidence),
            created_at=datetime.now(timezone.utc).isoformat(),
        )


class EvidenceTimelineBuilder:
    """
    Builder for evidence timelines.
    """
    
    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []
    
    def add_entry(
        self,
        timestamp: str,
        event: str,
        description: str,
        evidence_id: str | None = None,
    ) -> EvidenceTimelineBuilder:
        """Add timeline entry."""
        self._entries.append({
            "timestamp": timestamp,
            "event": event,
            "description": description,
            "evidence_id": evidence_id,
        })
        self._entries.sort(key=lambda x: x["timestamp"])
        return self
    
    def build(self) -> EvidenceTimeline:
        """Build evidence timeline."""
        return EvidenceTimeline(
            timeline_entries=tuple(self._entries),
            created_at=datetime.now(timezone.utc).isoformat(),
        )


class EvidenceLineageBuilder:
    """
    Builder for evidence lineage.
    """
    
    def __init__(self, root_evidence_id: str) -> None:
        self._root_id = root_evidence_id
        self._lineage: list[dict[str, Any]] = []
    
    def add_derivation(
        self,
        parent_id: str,
        child_id: str,
        transformation: str = "",
    ) -> EvidenceLineageBuilder:
        """Add derivation relationship."""
        self._lineage.append({
            "parent_id": parent_id,
            "child_id": child_id,
            "transformation": transformation,
        })
        return self
    
    def build(self) -> EvidenceLineage:
        """Build evidence lineage."""
        return EvidenceLineage(
            parent_evidence=self._root_id,
            child_evidence=tuple(
                entry["child_id"] for entry in self._lineage
            ),
            transformation_history=tuple(
                entry["transformation"] for entry in self._lineage
            ),
            created_at=datetime.now(timezone.utc).isoformat(),
        )


class EvidenceExplanation:
    """
    Provides explanations for evidence.
    """
    
    @staticmethod
    def explain_evidence_bundle(bundle: EvidenceBundle) -> str:
        """Explain an evidence bundle."""
        lines = [
            f"Evidence Bundle: {bundle.title}",
            f"Description: {bundle.description}",
            f"Items: {len(bundle.evidence_items)}",
        ]
        
        if bundle.threat_actor:
            lines.append(f"Threat Actor: {bundle.threat_actor}")
        if bundle.malware:
            lines.append(f"Malware: {bundle.malware}")
        if bundle.campaign:
            lines.append(f"Campaign: {bundle.campaign}")
        
        return "\n".join(lines)
    
    @staticmethod
    def explain_chain_of_custody(lineage: EvidenceLineage) -> str:
        """Explain chain of custody."""
        lines = [
            f"Root Evidence: {lineage.parent_evidence}",
            f"Derivation Count: {len(lineage.child_evidence)}",
        ]
        
        if lineage.transformation_history:
            lines.append("Transformations:")
            for i, transform in enumerate(lineage.transformation_history):
                if transform:
                    lines.append(f"  {i + 1}. {transform}")
        
        return "\n".join(lines)
