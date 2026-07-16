"""
threat_intelligence/infrastructure/lifecycle.py

Infrastructure Lifecycle Service.
"""
from __future__ import annotations

from typing import Any

from threat_intelligence.infrastructure.models import LifecycleState, LifecycleTransition


class InfrastructureLifecycleService:
    """
    Service for managing infrastructure lifecycle.
    
    Handles status transitions and validation.
    """
    
    VALID_TRANSITIONS: dict[str, list[str]] = {
        "draft": ["observed", "archived"],
        "observed": ["validated", "archived"],
        "validated": ["published", "archived"],
        "published": ["active", "deprecated", "archived"],
        "active": ["deprecated", "archived"],
        "deprecated": ["active", "archived"],
        "revoked": ["archived"],
        "archived": [],
    }
    
    def __init__(self) -> None:
        self._states: dict[str, LifecycleState] = {}
    
    def get_lifecycle(self, infrastructure_id: str) -> LifecycleState | None:
        """Get lifecycle for infrastructure."""
        return self._states.get(infrastructure_id)
    
    def can_transition(self, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        valid_targets = self.VALID_TRANSITIONS.get(from_status, [])
        return to_status in valid_targets
    
    def transition(
        self,
        infrastructure_id: str,
        to_status: str,
        reason: str = "",
        transitioned_by: str = "",
    ) -> tuple[bool, str]:
        """
        Attempt a status transition.
        
        Returns:
            Tuple of (success, message)
        """
        lifecycle = self._states.get(infrastructure_id)
        
        if not lifecycle:
            lifecycle = LifecycleState(
                infrastructure_id=infrastructure_id,
                status="draft",
            )
            self._states[infrastructure_id] = lifecycle
        
        from_status = lifecycle.status
        
        if not self.can_transition(from_status, to_status):
            return (False, f"Cannot transition from {from_status} to {to_status}")
        
        transition = LifecycleTransition(
            infrastructure_id=infrastructure_id,
            from_status=from_status,
            to_status=to_status,
            reason=reason,
            transitioned_by=transitioned_by,
        )
        
        updated_transitions = list(lifecycle.transitions) + [transition.to_dict()]
        
        updated_lifecycle = LifecycleState(
            infrastructure_id=infrastructure_id,
            status=to_status,
            transitions=tuple(updated_transitions),
            last_reviewed=lifecycle.last_reviewed,
            next_review=lifecycle.next_review,
        )
        
        self._states[infrastructure_id] = updated_lifecycle
        
        return (True, f"Transitioned from {from_status} to {to_status}")
    
    def get_status(self, infrastructure_id: str) -> str | None:
        """Get current status."""
        lifecycle = self._states.get(infrastructure_id)
        return lifecycle.status if lifecycle else None
    
    def get_transition_history(self, infrastructure_id: str) -> list[dict[str, Any]]:
        """Get transition history."""
        lifecycle = self._states.get(infrastructure_id)
        if not lifecycle:
            return []
        return list(lifecycle.transitions)
