"""
threat_hunting/models/report.py

Report Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_hunting.models.base import (
    HuntBase,
    Auditable,
    ConfidenceMixin,
)


@dataclass(frozen=True)
class ThreatHuntReport(HuntBase, Auditable, ConfidenceMixin):
    """Threat hunt report."""
    hunt_id: str = ""
    session_ids: tuple[str, ...] = field(default_factory=tuple)
    title: str = ""
    executive_summary: str = ""
    objectives_summary: str = ""
    hypotheses_summary: str = ""
    observations_summary: str = ""
    findings_summary: str = ""
    evidence_summary: str = ""
    recommendations_summary: str = ""
    confidence_summary: str = ""
    hunt_metadata: dict[str, Any] = field(default_factory=dict)
    graph_version: str = ""
    replay_available: bool = True
    replay_data: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "session_ids": list(self.session_ids),
            "title": self.title,
            "executive_summary": self.executive_summary,
            "objectives_summary": self.objectives_summary,
            "hypotheses_summary": self.hypotheses_summary,
            "observations_summary": self.observations_summary,
            "findings_summary": self.findings_summary,
            "evidence_summary": self.evidence_summary,
            "recommendations_summary": self.recommendations_summary,
            "confidence_summary": self.confidence_summary,
            "hunt_metadata": self.hunt_metadata,
            "graph_version": self.graph_version,
            "replay_available": self.replay_available,
            "replay_data": self.replay_data,
            "confidence_level": self.confidence_level,
            "confidence_score": self.confidence_score,
            "confidence_explanation": self.confidence_explanation,
            "author": self.author,
            "reason": self.reason,
        })
        return base


@dataclass(frozen=True)
class ReportSection(HuntBase):
    """Report section."""
    report_id: str = ""
    section_type: str = ""
    title: str = ""
    content: str = ""
    order: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "report_id": self.report_id,
            "section_type": self.section_type,
            "title": self.title,
            "content": self.content,
            "order": self.order,
            "metadata": self.metadata,
        })
        return base


@dataclass(frozen=True)
class HuntExplanation(HuntBase):
    """Hunt explanation."""
    hunt_id: str = ""
    explanation_type: str = ""
    title: str = ""
    description: str = ""
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    cti_object_refs: tuple[str, ...] = field(default_factory=tuple)
    inference_refs: tuple[str, ...] = field(default_factory=tuple)
    relationship_refs: tuple[str, ...] = field(default_factory=tuple)
    assumption_refs: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "explanation_type": self.explanation_type,
            "title": self.title,
            "description": self.description,
            "evidence_refs": list(self.evidence_refs),
            "cti_object_refs": list(self.cti_object_refs),
            "inference_refs": list(self.inference_refs),
            "relationship_refs": list(self.relationship_refs),
            "assumption_refs": list(self.assumption_refs),
        })
        return base
