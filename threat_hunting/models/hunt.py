"""
threat_hunting/models/hunt.py

Threat Hunting Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_hunting.models.base import (
    HuntBase,
    Auditable,
    Versionable,
    ProvenanceMixin,
    ConfidenceMixin,
)


@dataclass(frozen=True)
class HuntScope:
    """Hunt scope."""
    scope_id: str = ""
    scope_type: str = ""
    description: str = ""
    entity_refs: tuple[str, ...] = field(default_factory=tuple)
    time_range_start: str = ""
    time_range_end: str = ""
    constraints: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "scope_type": self.scope_type,
            "description": self.description,
            "entity_refs": list(self.entity_refs),
            "time_range_start": self.time_range_start,
            "time_range_end": self.time_range_end,
            "constraints": self.constraints,
        }


@dataclass(frozen=True)
class HuntObjective:
    """Hunt objective."""
    objective_id: str = ""
    hunt_id: str = ""
    title: str = ""
    description: str = ""
    priority: int = 1
    status: str = "pending"
    completed: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "objective_id": self.objective_id,
            "hunt_id": self.hunt_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "completed": self.completed,
        }


@dataclass(frozen=True)
class Hunt(HuntBase, Auditable, Versionable):
    """Hunt entity."""
    name: str = ""
    title: str = ""
    description: str = ""
    status: str = "draft"
    priority: int = 3
    scopes: tuple[HuntScope, ...] = field(default_factory=tuple)
    objectives: tuple[HuntObjective, ...] = field(default_factory=tuple)
    hypothesis_ids: tuple[str, ...] = field(default_factory=tuple)
    session_ids: tuple[str, ...] = field(default_factory=tuple)
    finding_ids: tuple[str, ...] = field(default_factory=tuple)
    report_ids: tuple[str, ...] = field(default_factory=tuple)
    related_hunts: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    started_at: str = ""
    completed_at: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "scopes": [s.to_dict() for s in self.scopes],
            "objectives": [o.to_dict() for o in self.objectives],
            "hypothesis_ids": list(self.hypothesis_ids),
            "session_ids": list(self.session_ids),
            "finding_ids": list(self.finding_ids),
            "report_ids": list(self.report_ids),
            "related_hunts": list(self.related_hunts),
            "tags": list(self.tags),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "author": self.author,
            "reason": self.reason,
            "source": self.source,
        })
        return base


@dataclass(frozen=True)
class HuntSession(HuntBase):
    """Hunt session."""
    hunt_id: str = ""
    session_type: str = ""
    status: str = "active"
    started_at: str = ""
    completed_at: str = ""
    graph_version: str = ""
    cti_snapshot: dict[str, Any] = field(default_factory=dict)
    rules_used: tuple[str, ...] = field(default_factory=tuple)
    queries_executed: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    observation_ids: tuple[str, ...] = field(default_factory=tuple)
    finding_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_bundle_ids: tuple[str, ...] = field(default_factory=tuple)
    confidence_updates: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    error_log: tuple[str, ...] = field(default_factory=tuple)
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "session_type": self.session_type,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "graph_version": self.graph_version,
            "cti_snapshot": self.cti_snapshot,
            "rules_used": list(self.rules_used),
            "queries_executed": list(self.queries_executed),
            "observation_ids": list(self.observation_ids),
            "finding_ids": list(self.finding_ids),
            "evidence_bundle_ids": list(self.evidence_bundle_ids),
            "confidence_updates": list(self.confidence_updates),
            "error_log": list(self.error_log),
        })
        return base


@dataclass(frozen=True)
class HuntMetadata(HuntBase):
    """Hunt metadata."""
    hunt_id: str = ""
    metadata_type: str = ""
    key: str = ""
    value: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "hunt_id": self.hunt_id,
            "metadata_type": self.metadata_type,
            "key": self.key,
            "value": self.value,
        })
        return base
