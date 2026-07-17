"""
workbench/events.py

Workbench Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class WorkbenchEventType(Enum):
    """Workbench event types."""
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    PRODUCT_REVIEW_STARTED = "product.review.started"
    PRODUCT_REVIEW_COMPLETED = "product.review.completed"
    PRODUCT_APPROVED = "product.approved"
    PRODUCT_REJECTED = "product.rejected"
    PRODUCT_PUBLISHED = "product.published"
    PRODUCT_ARCHIVED = "product.archived"
    PRODUCT_SUPERSEDED = "product.superseded"
    COLLECTION_CREATED = "collection.created"
    COLLECTION_UPDATED = "collection.updated"
    PUBLICATION_CREATED = "publication.created"
    PUBLICATION_PUBLISHED = "publication.published"
    APPROVAL_COMPLETED = "approval.completed"
    CONFIDENCE_REVIEWED = "confidence.reviewed"
    SOURCE_ASSESSED = "source.assessed"
    GOVERANCE_DECISION = "governance.decision"


@dataclass
class WorkbenchEvent:
    """Workbench event."""
    event_type: str
    entity_id: str
    entity_type: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    version: str = "1.0"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
            "version": self.version,
        }


class WorkbenchEventEmitter:
    """Emitter for workbench events."""
    
    def __init__(self) -> None:
        self._events: list[WorkbenchEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: WorkbenchEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_product_created(
        self,
        product_id: str,
        actor: str = "",
    ) -> None:
        """Emit product created event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_CREATED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_product_updated(
        self,
        product_id: str,
        actor: str = "",
    ) -> None:
        """Emit product updated event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_UPDATED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_product_review_started(
        self,
        product_id: str,
        review_id: str,
        actor: str = "",
    ) -> None:
        """Emit product review started event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_REVIEW_STARTED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"review_id": review_id},
            actor=actor,
        ))
    
    def emit_product_review_completed(
        self,
        product_id: str,
        review_id: str,
        actor: str = "",
    ) -> None:
        """Emit product review completed event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_REVIEW_COMPLETED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"review_id": review_id},
            actor=actor,
        ))
    
    def emit_product_approved(
        self,
        product_id: str,
        approval_id: str,
        actor: str = "",
    ) -> None:
        """Emit product approved event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_APPROVED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"approval_id": approval_id},
            actor=actor,
        ))
    
    def emit_product_rejected(
        self,
        product_id: str,
        approval_id: str,
        actor: str = "",
    ) -> None:
        """Emit product rejected event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_REJECTED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"approval_id": approval_id},
            actor=actor,
        ))
    
    def emit_product_published(
        self,
        product_id: str,
        publication_id: str,
        actor: str = "",
    ) -> None:
        """Emit product published event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_PUBLISHED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"publication_id": publication_id},
            actor=actor,
        ))
    
    def emit_product_archived(
        self,
        product_id: str,
        actor: str = "",
    ) -> None:
        """Emit product archived event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PRODUCT_ARCHIVED.value,
            entity_id=product_id,
            entity_type="product",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_collection_created(
        self,
        collection_id: str,
        actor: str = "",
    ) -> None:
        """Emit collection created event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.COLLECTION_CREATED.value,
            entity_id=collection_id,
            entity_type="collection",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={},
            actor=actor,
        ))
    
    def emit_publication_created(
        self,
        publication_id: str,
        product_id: str,
        actor: str = "",
    ) -> None:
        """Emit publication created event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.PUBLICATION_CREATED.value,
            entity_id=publication_id,
            entity_type="publication",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"product_id": product_id},
            actor=actor,
        ))
    
    def emit_approval_completed(
        self,
        approval_id: str,
        product_id: str,
        actor: str = "",
    ) -> None:
        """Emit approval completed event."""
        self.emit(WorkbenchEvent(
            event_type=WorkbenchEventType.APPROVAL_COMPLETED.value,
            entity_id=approval_id,
            entity_type="approval",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"product_id": product_id},
            actor=actor,
        ))
    
    def get_events(self) -> list[WorkbenchEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
