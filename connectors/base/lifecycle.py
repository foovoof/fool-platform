"""
connectors/base/lifecycle.py

Connector Lifecycle Management.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from connectors.base.models import ConnectorStatus

if TYPE_CHECKING:
    from connectors.base.connector import BaseConnector


class ConnectorLifecycleManager:
    """
    Manages connector lifecycle.
    
    Responsibilities:
    - Track lifecycle state
    - Enforce state transitions
    - Record lifecycle events
    """
    
    VALID_TRANSITIONS: dict[ConnectorStatus, list[ConnectorStatus]] = {
        ConnectorStatus.PENDING: [ConnectorStatus.INITIALIZED],
        ConnectorStatus.INITIALIZED: [ConnectorStatus.STARTING, ConnectorStatus.STOPPED],
        ConnectorStatus.STARTING: [ConnectorStatus.RUNNING, ConnectorStatus.FAILED],
        ConnectorStatus.RUNNING: [ConnectorStatus.STOPPING, ConnectorStatus.FAILED],
        ConnectorStatus.STOPPING: [ConnectorStatus.STOPPED, ConnectorStatus.FAILED],
        ConnectorStatus.STOPPED: [ConnectorStatus.INITIALIZED, ConnectorStatus.FAILED],
        ConnectorStatus.FAILED: [ConnectorStatus.INITIALIZED],
        ConnectorStatus.COMPLETED: [ConnectorStatus.PENDING],
    }
    
    def __init__(self, connector: BaseConnector) -> None:
        """Initialize lifecycle manager."""
        self._connector = connector
        self._status = ConnectorStatus.PENDING
        self._lifecycle_events: list[dict] = []
    
    @property
    def status(self) -> ConnectorStatus:
        """Get current status."""
        return self._status
    
    def can_transition(self, new_status: ConnectorStatus) -> bool:
        """Check if transition is valid."""
        valid = self.VALID_TRANSITIONS.get(self._status, [])
        return new_status in valid
    
    def transition(self, new_status: ConnectorStatus) -> bool:
        """
        Transition to new status.
        
        Args:
            new_status: Target status
            
        Returns:
            True if transition succeeded
        """
        if not self.can_transition(new_status):
            return False
        
        old_status = self._status
        self._status = new_status
        
        self._record_event(
            "transition",
            {"from": old_status.value, "to": new_status.value}
        )
        
        return True
    
    def initialize(self) -> None:
        """Mark as initialized."""
        self.transition(ConnectorStatus.INITIALIZED)
        self._record_event("initialized", {})
    
    def start(self) -> None:
        """Mark as starting."""
        if self.transition(ConnectorStatus.STARTING):
            self._record_event("started", {})
    
    def running(self) -> None:
        """Mark as running."""
        if self.transition(ConnectorStatus.RUNNING):
            self._record_event("running", {})
    
    def stop(self) -> None:
        """Mark as stopping."""
        if self.transition(ConnectorStatus.STOPPING):
            self._record_event("stopping", {})
    
    def stopped(self) -> None:
        """Mark as stopped."""
        if self.transition(ConnectorStatus.STOPPED):
            self._record_event("stopped", {})
    
    def complete(self) -> None:
        """Mark as completed."""
        if self.transition(ConnectorStatus.COMPLETED):
            self._record_event("completed", {})
    
    def fail(self, error: str | None = None) -> None:
        """Mark as failed."""
        self.transition(ConnectorStatus.FAILED)
        self._record_event("failed", {"error": error})
    
    def _record_event(self, event: str, data: dict) -> None:
        """Record lifecycle event."""
        self._lifecycle_events.append({
            "event": event,
            "status": self._status.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data,
        })
    
    def get_events(self) -> list[dict]:
        """Get lifecycle events."""
        return self._lifecycle_events.copy()
    
    def reset(self) -> None:
        """Reset to pending state."""
        self._status = ConnectorStatus.PENDING
        self._lifecycle_events.clear()
        self._record_event("reset", {})
