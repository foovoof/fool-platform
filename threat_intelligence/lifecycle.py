"""
threat_intelligence/lifecycle.py

Lifecycle Module.

Provides lifecycle management for threat intelligence entities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from threat_intelligence.models.enums import LifecycleStatus


@dataclass(frozen=True)
class LifecycleTransition:
    """Lifecycle transition."""
    from_status: str
    to_status: str
    reason: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    transitioned_by: str = ""


@dataclass(frozen=True)
class LifecycleState:
    """Current lifecycle state."""
    status: str = LifecycleStatus.NEW.value
    transitions: tuple[LifecycleTransition, ...] = field(default_factory=tuple)
    last_updated: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "transitions": [t.__dict__ for t in self.transitions],
            "last_updated": self.last_updated,
        }


class IndicatorLifecycle:
    """
    Lifecycle manager for indicators.
    
    Valid transitions:
    - new -> observed
    - observed -> deployed
    - observed -> revoked
    - deployed -> revoked
    - revoked -> expired
    """
    
    VALID_TRANSITIONS: dict[str, set[str]] = {
        LifecycleStatus.NEW.value: {
            LifecycleStatus.IN_PROGRESS.value,
            LifecycleStatus.STABLE.value,
        },
        LifecycleStatus.IN_PROGRESS.value: {
            LifecycleStatus.STABLE.value,
            LifecycleStatus.DEGRADED.value,
            LifecycleStatus.DEPRECATED.value,
        },
        LifecycleStatus.STABLE.value: {
            LifecycleStatus.DEGRADED.value,
            LifecycleStatus.DEPRECATED.value,
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.DEGRADED.value: {
            LifecycleStatus.STABLE.value,
            LifecycleStatus.DEPRECATED.value,
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.DEPRECATED.value: {
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.ARCHIVED.value: set(),
    }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        if from_status not in cls.VALID_TRANSITIONS:
            return False
        return to_status in cls.VALID_TRANSITIONS[from_status]
    
    @classmethod
    def get_valid_transitions(cls, from_status: str) -> set[str]:
        """Get valid transitions from a status."""
        return cls.VALID_TRANSITIONS.get(from_status, set())


class CampaignLifecycle:
    """
    Lifecycle manager for campaigns.
    
    Valid transitions:
    - planned -> active
    - active -> on_hold
    - active -> completed
    - on_hold -> active
    - on_hold -> cancelled
    - completed -> archived
    - cancelled -> archived
    """
    
    VALID_TRANSITIONS: dict[str, set[str]] = {
        LifecycleStatus.NEW.value: {
            LifecycleStatus.IN_PROGRESS.value,
        },
        LifecycleStatus.IN_PROGRESS.value: {
            LifecycleStatus.STABLE.value,
            LifecycleStatus.DEPRECATED.value,
        },
        LifecycleStatus.STABLE.value: {
            LifecycleStatus.DEPRECATED.value,
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.DEPRECATED.value: {
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.ARCHIVED.value: set(),
    }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        if from_status not in cls.VALID_TRANSITIONS:
            return False
        return to_status in cls.VALID_TRANSITIONS[from_status]
    
    @classmethod
    def get_valid_transitions(cls, from_status: str) -> set[str]:
        """Get valid transitions from a status."""
        return cls.VALID_TRANSITIONS.get(from_status, set())


class ReportLifecycle:
    """
    Lifecycle manager for reports.
    
    Valid transitions:
    - draft -> review
    - review -> published
    - review -> draft
    - published -> archived
    """
    
    VALID_TRANSITIONS: dict[str, set[str]] = {
        LifecycleStatus.NEW.value: {
            LifecycleStatus.IN_PROGRESS.value,
        },
        LifecycleStatus.IN_PROGRESS.value: {
            LifecycleStatus.STABLE.value,
            LifecycleStatus.DEPRECATED.value,
        },
        LifecycleStatus.STABLE.value: {
            LifecycleStatus.DEPRECATED.value,
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.DEPRECATED.value: {
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.ARCHIVED.value: set(),
    }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        if from_status not in cls.VALID_TRANSITIONS:
            return False
        return to_status in cls.VALID_TRANSITIONS[from_status]
    
    @classmethod
    def get_valid_transitions(cls, from_status: str) -> set[str]:
        """Get valid transitions from a status."""
        return cls.VALID_TRANSITIONS.get(from_status, set())


class FindingLifecycle:
    """
    Lifecycle manager for findings.
    
    Valid transitions:
    - new -> in_progress
    - in_progress -> stable
    - stable -> archived
    """
    
    VALID_TRANSITIONS: dict[str, set[str]] = {
        LifecycleStatus.NEW.value: {
            LifecycleStatus.IN_PROGRESS.value,
        },
        LifecycleStatus.IN_PROGRESS.value: {
            LifecycleStatus.STABLE.value,
            LifecycleStatus.DEPRECATED.value,
        },
        LifecycleStatus.STABLE.value: {
            LifecycleStatus.DEPRECATED.value,
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.DEPRECATED.value: {
            LifecycleStatus.ARCHIVED.value,
        },
        LifecycleStatus.ARCHIVED.value: set(),
    }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        if from_status not in cls.VALID_TRANSITIONS:
            return False
        return to_status in cls.VALID_TRANSITIONS[from_status]
    
    @classmethod
    def get_valid_transitions(cls, from_status: str) -> set[str]:
        """Get valid transitions from a status."""
        return cls.VALID_TRANSITIONS.get(from_status, set())


class LifecycleService:
    """
    Service for managing entity lifecycles.
    
    Coordinates lifecycle transitions across entity types.
    """
    
    def __init__(self) -> None:
        self._lifecycles: dict[str, LifecycleState] = {}
    
    def get_lifecycle(self, entity_id: str) -> LifecycleState:
        """Get lifecycle state for an entity."""
        if entity_id not in self._lifecycles:
            self._lifecycles[entity_id] = LifecycleState()
        return self._lifecycles[entity_id]
    
    def transition(
        self,
        entity_id: str,
        to_status: str,
        reason: str = "",
        transitioned_by: str = "",
        lifecycle_class: type = IndicatorLifecycle,
    ) -> tuple[bool, str]:
        """
        Attempt to transition an entity.
        
        Args:
            entity_id: Entity ID
            to_status: Target status
            reason: Reason for transition
            transitioned_by: User performing transition
            lifecycle_class: Lifecycle class to use
            
        Returns:
            Tuple of (success, message)
        """
        current = self.get_lifecycle(entity_id)
        from_status = current.status
        
        if lifecycle_class.can_transition(from_status, to_status):
            transition = LifecycleTransition(
                from_status=from_status,
                to_status=to_status,
                reason=reason,
                transitioned_by=transitioned_by,
            )
            
            new_state = LifecycleState(
                status=to_status,
                transitions=current.transitions + (transition,),
                last_updated=datetime.now(timezone.utc).isoformat(),
            )
            self._lifecycles[entity_id] = new_state
            return (True, f"Transitioned from {from_status} to {to_status}")
        
        return (False, f"Invalid transition from {from_status} to {to_status}")
    
    def get_valid_transitions(
        self, entity_id: str, lifecycle_class: type = IndicatorLifecycle
    ) -> set[str]:
        """Get valid transitions for an entity."""
        current = self.get_lifecycle(entity_id)
        return lifecycle_class.get_valid_transitions(current.status)
