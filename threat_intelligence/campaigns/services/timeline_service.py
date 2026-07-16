"""
threat_intelligence/campaigns/services/timeline_service.py

Timeline Service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from threat_intelligence.campaigns.models import TimelineEvent, Milestone
from threat_intelligence.campaigns.repositories import TimelineEventRepository, MilestoneRepository


class TimelineService:
    """Service for managing campaign timelines."""
    
    def __init__(
        self,
        event_repository: TimelineEventRepository | None = None,
        milestone_repository: MilestoneRepository | None = None,
    ) -> None:
        self._event_repository = event_repository or TimelineEventRepository()
        self._milestone_repository = milestone_repository or MilestoneRepository()
    
    def create_event(
        self,
        campaign_id: str,
        event_type: str,
        timestamp: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> TimelineEvent:
        """Create a new timeline event."""
        event = TimelineEvent(
            id=str(uuid4()),
            campaign_id=campaign_id,
            event_type=event_type,
            timestamp=timestamp,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._event_repository.create(event)
    
    def get_event(self, event_id: str) -> TimelineEvent | None:
        """Get event by ID."""
        return self._event_repository.get(event_id)
    
    def list_events(self) -> list[TimelineEvent]:
        """List all events."""
        return self._event_repository.list_all()
    
    def find_events_by_campaign(self, campaign_id: str) -> list[TimelineEvent]:
        """Find events by campaign."""
        return self._event_repository.search({"campaign_id": campaign_id})
    
    def create_milestone(
        self,
        campaign_id: str,
        name: str,
        target_date: str,
        description: str = "",
        author: str = "",
        **kwargs: Any,
    ) -> Milestone:
        """Create a new milestone."""
        milestone = Milestone(
            id=str(uuid4()),
            campaign_id=campaign_id,
            name=name,
            target_date=target_date,
            description=description,
            author=author,
            created_at=datetime.now(timezone.utc).isoformat(),
            modified_at=datetime.now(timezone.utc).isoformat(),
            version=1,
            **kwargs,
        )
        return self._milestone_repository.create(milestone)
    
    def get_milestone(self, milestone_id: str) -> Milestone | None:
        """Get milestone by ID."""
        return self._milestone_repository.get(milestone_id)
    
    def list_milestones(self) -> list[Milestone]:
        """List all milestones."""
        return self._milestone_repository.list_all()
    
    def find_milestones_by_campaign(self, campaign_id: str) -> list[Milestone]:
        """Find milestones by campaign."""
        return self._milestone_repository.search({"campaign_id": campaign_id})
