"""
product_suite/events.py

Unified Product Suite Events.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class SuiteEventType(Enum):
    """Unified suite event types."""
    # Product Lifecycle
    PRODUCT_REGISTERED = "suite.product.registered"
    PRODUCT_CERTIFIED = "suite.product.certified"
    PRODUCT_ACTIVATED = "suite.product.activated"
    PRODUCT_DEPRECATED = "suite.product.deprecated"
    
    # Integration
    CONTRACT_ESTABLISHED = "suite.contract.established"
    CONTRACT_VIOLATED = "suite.contract.violated"
    BOUNDARY_VIOLATED = "suite.boundary.violated"
    
    # Navigation
    NAVIGATION_FEDERATED = "suite.navigation.federated"
    CONTEXT_PROPAGATED = "suite.context.propagated"
    
    # Traceability
    ENTITY_TRACED = "suite.entity.traced"
    TRACEABILITY_VERIFIED = "suite.traceability.verified"
    
    # Replay
    REPLAY_VERIFIED = "suite.replay.verified"
    REPLAY_FAILED = "suite.replay.failed"
    
    # Certification
    CERTIFICATION_STARTED = "suite.certification.started"
    CERTIFICATION_COMPLETED = "suite.certification.completed"
    CERTIFICATION_FAILED = "suite.certification.failed"


@dataclass
class SuiteEvent:
    """Unified suite event."""
    event_type: str
    source_product: str
    timestamp: str
    data: dict[str, Any]
    actor: str = ""
    version: str = "1.0"
    trace_id: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source_product": self.source_product,
            "timestamp": self.timestamp,
            "data": self.data,
            "actor": self.actor,
            "version": self.version,
            "trace_id": self.trace_id,
        }


class SuiteEventEmitter:
    """Emitter for suite events."""
    
    def __init__(self) -> None:
        self._events: list[SuiteEvent] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable event emission."""
        self._enabled = False
    
    def emit(self, event: SuiteEvent) -> None:
        """Emit an event."""
        if self._enabled:
            self._events.append(event)
    
    def emit_product_certified(
        self,
        product_type: str,
        status: str = "certified",
    ) -> None:
        """Emit product certified event."""
        self.emit(SuiteEvent(
            event_type=SuiteEventType.PRODUCT_CERTIFIED.value,
            source_product=product_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"status": status},
        ))
    
    def emit_contract_established(
        self,
        contract_name: str,
        source: str,
        target: str,
    ) -> None:
        """Emit contract established event."""
        self.emit(SuiteEvent(
            event_type=SuiteEventType.CONTRACT_ESTABLISHED.value,
            source_product=source,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"contract_name": contract_name, "target": target},
        ))
    
    def emit_certification_completed(
        self,
        products: list[str],
        status: str = "pass",
    ) -> None:
        """Emit certification completed event."""
        self.emit(SuiteEvent(
            event_type=SuiteEventType.CERTIFICATION_COMPLETED.value,
            source_product="product_suite",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"products": products, "status": status},
        ))
    
    def emit_traceability_verified(
        self,
        entity_type: str,
        trace_path: list[str],
    ) -> None:
        """Emit traceability verified event."""
        self.emit(SuiteEvent(
            event_type=SuiteEventType.TRACEABILITY_VERIFIED.value,
            source_product="product_suite",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"entity_type": entity_type, "trace_path": trace_path},
        ))
    
    def get_events(self) -> list[SuiteEvent]:
        """Get all events."""
        return list(self._events)
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
