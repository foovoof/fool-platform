from __future__ import annotations

"""
knowledge/events/knowledge_events.py

Knowledge events for the Knowledge Layer.

Provides event emission for knowledge operations.
Uses platform/events interfaces.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class GraphEventType(Enum):
    """Graph event types."""
    NODE_CREATED = "knowledge.node.created"
    NODE_UPDATED = "knowledge.node.updated"
    NODE_REMOVED = "knowledge.node.removed"
    EDGE_CREATED = "knowledge.edge.created"
    EDGE_UPDATED = "knowledge.edge.updated"
    EDGE_REMOVED = "knowledge.edge.removed"
    GRAPH_VALIDATED = "knowledge.graph.validated"


class ResolutionEventType(Enum):
    """Resolution event types."""
    ENTITY_RESOLVED = "knowledge.entity.resolved"
    IDENTITY_MERGED = "knowledge.identity.merged"
    RELATIONSHIP_CREATED = "knowledge.relationship.created"
    RELATIONSHIP_VALIDATED = "knowledge.relationship.validated"


VALID_GRAPH_EVENTS = {
    GraphEventType.NODE_CREATED,
    GraphEventType.NODE_UPDATED,
    GraphEventType.NODE_REMOVED,
    GraphEventType.EDGE_CREATED,
    GraphEventType.EDGE_UPDATED,
    GraphEventType.EDGE_REMOVED,
    GraphEventType.GRAPH_VALIDATED,
}

VALID_RESOLUTION_EVENTS = {
    ResolutionEventType.ENTITY_RESOLVED,
    ResolutionEventType.IDENTITY_MERGED,
    ResolutionEventType.RELATIONSHIP_CREATED,
    ResolutionEventType.RELATIONSHIP_VALIDATED,
}


@dataclass
class KnowledgeEvent:
    """A knowledge event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = "fool_platform.knowledge"
    data: dict[str, Any] = field(default_factory=dict)


class KnowledgeEventEmitter:
    """
    Emits knowledge events through the Event Bus.
    
    Supports optional EventBus integration.
    Event failures do not fail operations.
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
        Emit a knowledge event.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            True if emitted successfully
        """
        self._event_count += 1

        event = KnowledgeEvent(
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

    def emit_node_created(self, node_id: str, node_type: str) -> bool:
        """Emit node.created event."""
        return self.emit(
            GraphEventType.NODE_CREATED.value,
            {"node_id": node_id, "node_type": node_type},
        )

    def emit_node_updated(self, node_id: str, changes: dict[str, Any]) -> bool:
        """Emit node.updated event."""
        return self.emit(
            GraphEventType.NODE_UPDATED.value,
            {"node_id": node_id, "changes": changes},
        )

    def emit_node_removed(self, node_id: str) -> bool:
        """Emit node.removed event."""
        return self.emit(
            GraphEventType.NODE_REMOVED.value,
            {"node_id": node_id},
        )

    def emit_edge_created(
        self,
        edge_id: str,
        source_id: str,
        target_id: str,
        relationship_type: str,
    ) -> bool:
        """Emit edge.created event."""
        return self.emit(
            GraphEventType.EDGE_CREATED.value,
            {
                "edge_id": edge_id,
                "source_node_id": source_id,
                "target_node_id": target_id,
                "relationship_type": relationship_type,
            },
        )

    def emit_edge_updated(self, edge_id: str, changes: dict[str, Any]) -> bool:
        """Emit edge.updated event."""
        return self.emit(
            GraphEventType.EDGE_UPDATED.value,
            {"edge_id": edge_id, "changes": changes},
        )

    def emit_edge_removed(self, edge_id: str) -> bool:
        """Emit edge.removed event."""
        return self.emit(
            GraphEventType.EDGE_REMOVED.value,
            {"edge_id": edge_id},
        )

    def emit_graph_validated(
        self,
        graph_id: str,
        is_valid: bool,
        error_count: int,
    ) -> bool:
        """Emit graph.validated event."""
        return self.emit(
            GraphEventType.GRAPH_VALIDATED.value,
            {
                "graph_id": graph_id,
                "is_valid": is_valid,
                "error_count": error_count,
            },
        )

    def emit_entity_resolved(
        self,
        source_id: str,
        target_id: str,
        match_type: str,
        confidence: float,
    ) -> bool:
        """Emit entity.resolved event."""
        return self.emit(
            ResolutionEventType.ENTITY_RESOLVED.value,
            {
                "source_entity_id": source_id,
                "target_entity_id": target_id,
                "match_type": match_type,
                "confidence": confidence,
            },
        )

    def emit_identity_merged(
        self,
        identity_ref: str,
        merged_node_ids: list[str],
    ) -> bool:
        """Emit identity.merged event."""
        return self.emit(
            ResolutionEventType.IDENTITY_MERGED.value,
            {
                "identity_ref": identity_ref,
                "merged_node_ids": merged_node_ids,
            },
        )

    def emit_relationship_created(
        self,
        relationship_id: str,
        source_id: str,
        target_id: str,
        relationship_type: str,
    ) -> bool:
        """Emit relationship.created event."""
        return self.emit(
            ResolutionEventType.RELATIONSHIP_CREATED.value,
            {
                "relationship_id": relationship_id,
                "source_entity_id": source_id,
                "target_entity_id": target_id,
                "relationship_type": relationship_type,
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
