"""
intelligence/events/emitter.py

Intelligence Event Emitter.

Emits events for the Intelligence Runtime.
Uses platform/events interfaces.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class IntelligenceEventType(Enum):
    """Intelligence event types."""
    SESSION_STARTED = "intelligence.session.started"
    SESSION_COMPLETED = "intelligence.session.completed"
    SESSION_FAILED = "intelligence.session.failed"
    TASK_STARTED = "intelligence.task.started"
    TASK_COMPLETED = "intelligence.task.completed"
    TASK_FAILED = "intelligence.task.failed"
    PIPELINE_STARTED = "intelligence.pipeline.started"
    PIPELINE_COMPLETED = "intelligence.pipeline.completed"
    PIPELINE_STEP_EXECUTED = "intelligence.pipeline.step_executed"
    FINDING_GENERATED = "intelligence.finding.generated"
    ARTIFACT_CREATED = "intelligence.artifact.created"
    CONTEXT_CREATED = "intelligence.context.created"


VALID_EVENT_TYPES = {
    IntelligenceEventType.SESSION_STARTED,
    IntelligenceEventType.SESSION_COMPLETED,
    IntelligenceEventType.SESSION_FAILED,
    IntelligenceEventType.TASK_STARTED,
    IntelligenceEventType.TASK_COMPLETED,
    IntelligenceEventType.TASK_FAILED,
    IntelligenceEventType.PIPELINE_STARTED,
    IntelligenceEventType.PIPELINE_COMPLETED,
    IntelligenceEventType.PIPELINE_STEP_EXECUTED,
    IntelligenceEventType.FINDING_GENERATED,
    IntelligenceEventType.ARTIFACT_CREATED,
    IntelligenceEventType.CONTEXT_CREATED,
}


@dataclass
class IntelligenceEvent:
    """An intelligence event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = "fool_platform.intelligence"
    data: dict[str, Any] = field(default_factory=dict)


class IntelligenceEventEmitter:
    """
    Emits intelligence events through the Event Bus.
    
    Supports optional EventBus integration.
    Event failures do not fail intelligence operations.
    """
    
    def __init__(self, event_bus: Any = None) -> None:
        """
        Initialize the event emitter.
        
        Args:
            event_bus: Optional EventBus instance
        """
        self._event_bus = event_bus
        self._event_count = 0
        self._failed_events: list[dict[str, Any]] = []
    
    @property
    def has_event_bus(self) -> bool:
        """Check if an event bus is configured."""
        return self._event_bus is not None
    
    def emit(self, event_type: str, data: dict[str, Any]) -> bool:
        """
        Emit an intelligence event.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            True if emitted successfully
        """
        self._event_count += 1
        
        event = IntelligenceEvent(
            event_type=event_type,
            data=data,
        )
        
        if self._event_bus is None:
            return False
        
        try:
            if hasattr(self._event_bus, "publish"):
                self._event_bus.publish(event_type, event)
            elif hasattr(self._event_bus, "emit"):
                self._event_bus.emit(event)
            else:
                self._failed_events.append({
                    "event_type": event_type,
                    "data": data,
                    "error": "Event bus has no publish or emit method",
                })
                return False
            return True
        except Exception as e:
            self._failed_events.append({
                "event_type": event_type,
                "data": data,
                "error": str(e),
            })
            return False
    
    def emit_session_started(
        self,
        session_id: str,
        task_id: str,
    ) -> bool:
        """Emit session.started event."""
        return self.emit(
            IntelligenceEventType.SESSION_STARTED.value,
            {
                "session_id": session_id,
                "task_id": task_id,
            },
        )
    
    def emit_session_completed(
        self,
        session_id: str,
        result_id: str,
    ) -> bool:
        """Emit session.completed event."""
        return self.emit(
            IntelligenceEventType.SESSION_COMPLETED.value,
            {
                "session_id": session_id,
                "result_id": result_id,
            },
        )
    
    def emit_task_started(
        self,
        task_id: str,
        session_id: str,
    ) -> bool:
        """Emit task.started event."""
        return self.emit(
            IntelligenceEventType.TASK_STARTED.value,
            {
                "task_id": task_id,
                "session_id": session_id,
            },
        )
    
    def emit_task_completed(
        self,
        task_id: str,
        result_id: str,
        status: str,
    ) -> bool:
        """Emit task.completed event."""
        return self.emit(
            IntelligenceEventType.TASK_COMPLETED.value,
            {
                "task_id": task_id,
                "result_id": result_id,
                "status": status,
            },
        )
    
    def emit_pipeline_started(
        self,
        task_id: str,
        pipeline_id: str,
    ) -> bool:
        """Emit pipeline.started event."""
        return self.emit(
            IntelligenceEventType.PIPELINE_STARTED.value,
            {
                "task_id": task_id,
                "pipeline_id": pipeline_id,
            },
        )
    
    def emit_pipeline_completed(
        self,
        task_id: str,
        pipeline_id: str,
    ) -> bool:
        """Emit pipeline.completed event."""
        return self.emit(
            IntelligenceEventType.PIPELINE_COMPLETED.value,
            {
                "task_id": task_id,
                "pipeline_id": pipeline_id,
            },
        )
    
    def emit_finding_generated(
        self,
        finding_id: str,
        task_id: str,
    ) -> bool:
        """Emit finding.generated event."""
        return self.emit(
            IntelligenceEventType.FINDING_GENERATED.value,
            {
                "finding_id": finding_id,
                "task_id": task_id,
            },
        )
    
    def get_event_count(self) -> int:
        """Get total events emitted."""
        return self._event_count
    
    def get_failed_events(self) -> list[dict[str, Any]]:
        """Get failed events."""
        return self._failed_events.copy()
    
    def clear_failed_events(self) -> None:
        """Clear failed events list."""
        self._failed_events.clear()
