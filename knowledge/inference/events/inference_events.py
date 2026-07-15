from __future__ import annotations

"""
knowledge/inference/events/inference_events.py

Inference Events for the Knowledge Layer.

Provides event emission for inference operations.
Uses platform/events interfaces.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class InferenceEventType(Enum):
    """Inference event types."""
    SESSION_STARTED = "knowledge.inference.session.started"
    SESSION_COMPLETED = "knowledge.inference.session.completed"
    SESSION_FAILED = "knowledge.inference.session.failed"
    RULE_EVALUATED = "knowledge.rule.evaluated"
    RULE_TRIGGERED = "knowledge.rule.triggered"
    CONCLUSION_GENERATED = "knowledge.conclusion.generated"
    CONFIDENCE_UPDATED = "knowledge.confidence.updated"
    EXPLANATION_GENERATED = "knowledge.explanation.generated"
    EVIDENCE_REGISTERED = "knowledge.evidence.registered"
    EVIDENCE_PROPAGATED = "knowledge.evidence.propagated"


VALID_INFERENCE_EVENTS = {
    InferenceEventType.SESSION_STARTED,
    InferenceEventType.SESSION_COMPLETED,
    InferenceEventType.SESSION_FAILED,
    InferenceEventType.RULE_EVALUATED,
    InferenceEventType.RULE_TRIGGERED,
    InferenceEventType.CONCLUSION_GENERATED,
    InferenceEventType.CONFIDENCE_UPDATED,
    InferenceEventType.EXPLANATION_GENERATED,
    InferenceEventType.EVIDENCE_REGISTERED,
    InferenceEventType.EVIDENCE_PROPAGATED,
}


@dataclass
class InferenceEvent:
    """An inference event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = "fool_platform.knowledge.inference"
    data: dict[str, Any] = field(default_factory=dict)


class InferenceEventEmitter:
    """
    Emits inference events through the Event Bus.
    
    Supports optional EventBus integration.
    Event failures do not fail inference operations.
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
        Emit an inference event.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            True if emitted successfully
        """
        self._event_count += 1
        
        event = InferenceEvent(
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
        graph_id: str,
    ) -> bool:
        """Emit session.started event."""
        return self.emit(
            InferenceEventType.SESSION_STARTED.value,
            {
                "session_id": session_id,
                "graph_id": graph_id,
            },
        )
    
    def emit_session_completed(
        self,
        session_id: str,
        conclusions: int,
        recommendations: int,
    ) -> bool:
        """Emit session.completed event."""
        return self.emit(
            InferenceEventType.SESSION_COMPLETED.value,
            {
                "session_id": session_id,
                "conclusions": conclusions,
                "recommendations": recommendations,
            },
        )
    
    def emit_rule_evaluated(
        self,
        session_id: str,
        rule_id: str,
        rule_name: str,
    ) -> bool:
        """Emit rule.evaluated event."""
        return self.emit(
            InferenceEventType.RULE_EVALUATED.value,
            {
                "session_id": session_id,
                "rule_id": rule_id,
                "rule_name": rule_name,
            },
        )
    
    def emit_rule_triggered(
        self,
        session_id: str,
        rule_id: str,
    ) -> bool:
        """Emit rule.triggered event."""
        return self.emit(
            InferenceEventType.RULE_TRIGGERED.value,
            {
                "session_id": session_id,
                "rule_id": rule_id,
            },
        )
    
    def emit_conclusion_generated(
        self,
        session_id: str,
        conclusion_id: str,
        rule_id: str,
        confidence: float,
    ) -> bool:
        """Emit conclusion.generated event."""
        return self.emit(
            InferenceEventType.CONCLUSION_GENERATED.value,
            {
                "session_id": session_id,
                "conclusion_id": conclusion_id,
                "rule_id": rule_id,
                "confidence": confidence,
            },
        )
    
    def emit_confidence_updated(
        self,
        entity_id: str,
        old_confidence: float,
        new_confidence: float,
        rule_id: str,
    ) -> bool:
        """Emit confidence.updated event."""
        return self.emit(
            InferenceEventType.CONFIDENCE_UPDATED.value,
            {
                "entity_id": entity_id,
                "old_confidence": old_confidence,
                "new_confidence": new_confidence,
                "rule_id": rule_id,
            },
        )
    
    def emit_explanation_generated(
        self,
        explanation_id: str,
        rule_id: str,
    ) -> bool:
        """Emit explanation.generated event."""
        return self.emit(
            InferenceEventType.EXPLANATION_GENERATED.value,
            {
                "explanation_id": explanation_id,
                "rule_id": rule_id,
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
