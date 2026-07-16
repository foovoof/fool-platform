"""
threat_intelligence/campaigns/services/lifecycle_service.py

Lifecycle Service.
"""
from __future__ import annotations

from typing import Any

from threat_intelligence.campaigns.models import CampaignLifecycle, LifecycleTransition
from threat_intelligence.campaigns.models.enums import CampaignStatus


class LifecycleService:
    """
    Service for managing campaign lifecycle.
    
    Handles status transitions and validation.
    """
    
    VALID_TRANSITIONS: dict[str, list[str]] = {
        "planned": ["proposed", "active", "cancelled", "archived"],
        "proposed": ["active", "cancelled", "archived"],
        "active": ["on_hold", "completed", "cancelled"],
        "on_hold": ["active", "completed", "cancelled"],
        "completed": ["archived"],
        "cancelled": ["archived"],
        "archived": [],
    }
    
    def __init__(self) -> None:
        self._states: dict[str, CampaignLifecycle] = {}
    
    def get_lifecycle(self, campaign_id: str) -> CampaignLifecycle | None:
        """Get lifecycle for campaign."""
        return self._states.get(campaign_id)
    
    def can_transition(self, from_status: str, to_status: str) -> bool:
        """Check if transition is valid."""
        valid_targets = self.VALID_TRANSITIONS.get(from_status, [])
        return to_status in valid_targets
    
    def transition(
        self,
        campaign_id: str,
        to_status: str,
        reason: str = "",
        transitioned_by: str = "",
    ) -> tuple[bool, str]:
        """
        Attempt a status transition.
        
        Returns:
            Tuple of (success, message)
        """
        lifecycle = self._states.get(campaign_id)
        
        if not lifecycle:
            lifecycle = CampaignLifecycle(
                campaign_id=campaign_id,
                current_status=CampaignStatus.PLANNED.value,
            )
            self._states[campaign_id] = lifecycle
        
        from_status = lifecycle.current_status
        
        if not self.can_transition(from_status, to_status):
            return (False, f"Cannot transition from {from_status} to {to_status}")
        
        transition = LifecycleTransition(
            campaign_id=campaign_id,
            from_status=from_status,
            to_status=to_status,
            reason=reason,
            transitioned_by=transitioned_by,
        )
        
        updated_transitions = list(lifecycle.transitions) + [transition.to_dict()]
        
        updated_lifecycle = CampaignLifecycle(
            campaign_id=campaign_id,
            current_status=to_status,
            transitions=tuple(updated_transitions),
            approval_history=lifecycle.approval_history,
            review_history=lifecycle.review_history,
            last_transition=transition.id,
        )
        
        self._states[campaign_id] = updated_lifecycle
        
        return (True, f"Transitioned from {from_status} to {to_status}")
    
    def get_status(self, campaign_id: str) -> str | None:
        """Get current status."""
        lifecycle = self._states.get(campaign_id)
        return lifecycle.current_status if lifecycle else None
    
    def get_transition_history(self, campaign_id: str) -> list[LifecycleTransition]:
        """Get transition history."""
        lifecycle = self._states.get(campaign_id)
        if not lifecycle:
            return []
        
        return [
            LifecycleTransition(**t) for t in lifecycle.transitions
        ]
