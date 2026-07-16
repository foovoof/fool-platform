"""
threat_intelligence/infrastructure/models/lifecycle.py

Infrastructure Lifecycle Models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from threat_intelligence.infrastructure.models.base import InfrastructureBase, Auditable


@dataclass(frozen=True)
class LifecycleTransition(InfrastructureBase):
    """Lifecycle transition."""
    infrastructure_id: str = ""
    from_status: str = ""
    to_status: str = ""
    reason: str = ""
    transitioned_by: str = ""
    approval_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "infrastructure_id": self.infrastructure_id,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "reason": self.reason,
            "transitioned_by": self.transitioned_by,
            "approval_id": self.approval_id,
        })
        return base


@dataclass(frozen=True)
class LifecycleState(InfrastructureBase):
    """Current lifecycle state."""
    infrastructure_id: str = ""
    status: str = "draft"
    transitions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    last_reviewed: str = ""
    next_review: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        base = super().to_dict()
        base.update({
            "infrastructure_id": self.infrastructure_id,
            "status": self.status,
            "transitions": list(self.transitions),
            "last_reviewed": self.last_reviewed,
            "next_review": self.next_review,
        })
        return base
