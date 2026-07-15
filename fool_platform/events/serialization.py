"""
fool_platform/events/serialization.py

Event serialization and deserialization using JSON.
"""
import json
from datetime import datetime, timezone
from typing import Any

from fool_platform.events.envelope import EventEnvelope, ValidationStatus
from fool_platform.events.exceptions import EventSerializationError
from fool_platform.events.metadata import EventMetadata


class EventSerializer:
    """
    Serializes and deserializes events to/from JSON.
    
    Preserves UUIDs as strings and datetimes as ISO 8601 strings.
    """
    
    def serialize_event(self, event: EventEnvelope) -> str:
        """
        Serialize an event envelope to JSON string.
        
        Args:
            event: The event envelope to serialize
            
        Returns:
            JSON string representation of the event
            
        Raises:
            EventSerializationError: If serialization fails
        """
        try:
            data = self._event_to_dict(event)
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        except Exception as e:
            raise EventSerializationError(
                f"Failed to serialize event {event.event_id}: {e}",
                event_id=event.event_id,
                cause=e,
            )

    def deserialize_event(self, raw: str) -> EventEnvelope:
        """
        Deserialize a JSON string to an event envelope.
        
        Args:
            raw: JSON string to deserialize
            
        Returns:
            The deserialized EventEnvelope
            
        Raises:
            EventSerializationError: If deserialization fails
        """
        try:
            data = json.loads(raw)
            return self._dict_to_event(data)
        except json.JSONDecodeError as e:
            raise EventSerializationError(
                f"Failed to parse JSON: {e}",
                cause=e,
            )
        except Exception as e:
            raise EventSerializationError(
                f"Failed to deserialize event: {e}",
                cause=e,
            )

    def serialize_metadata(self, metadata: EventMetadata) -> str:
        """
        Serialize metadata to JSON string.
        
        Args:
            metadata: The metadata to serialize
            
        Returns:
            JSON string representation of the metadata
        """
        try:
            data = self._metadata_to_dict(metadata)
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        except Exception as e:
            raise EventSerializationError(
                f"Failed to serialize metadata: {e}",
                cause=e,
            )

    def deserialize_metadata(self, raw: str) -> EventMetadata:
        """
        Deserialize JSON string to metadata.
        
        Args:
            raw: JSON string to deserialize
            
        Returns:
            The deserialized EventMetadata
        """
        try:
            data = json.loads(raw)
            return self._dict_to_metadata(data)
        except Exception as e:
            raise EventSerializationError(
                f"Failed to deserialize metadata: {e}",
                cause=e,
            )

    def _event_to_dict(self, event: EventEnvelope) -> dict[str, Any]:
        """Convert an event envelope to a dictionary."""
        return {
            "metadata": self._metadata_to_dict(event.metadata),
            "payload": event.payload,
            "schema_ref": event.schema_ref,
            "validation_status": event.validation_status.value,
            "created_at": event.created_at,
        }

    def _dict_to_event(self, data: dict[str, Any]) -> EventEnvelope:
        """Convert a dictionary to an event envelope."""
        metadata = self._dict_to_metadata(data["metadata"])
        
        return EventEnvelope.create(
            metadata=metadata,
            payload=data.get("payload", {}),
            schema_ref=data.get("schema_ref"),
            validation_status=ValidationStatus(data.get("validation_status", "pending")),
        )

    def _metadata_to_dict(self, metadata: EventMetadata) -> dict[str, Any]:
        """Convert metadata to a dictionary."""
        return {
            "event_id": metadata.event_id,
            "event_type": metadata.event_type,
            "event_version": metadata.event_version,
            "occurred_at": metadata.occurred_at,
            "correlation_id": metadata.correlation_id,
            "causation_id": metadata.causation_id,
            "trace_id": metadata.trace_id,
            "producer": metadata.producer,
            "source": metadata.source,
            "subject": metadata.subject,
            "case_id": metadata.case_id,
            "workflow_id": metadata.workflow_id,
            "agent_id": metadata.agent_id,
            "idempotency_key": metadata.idempotency_key,
            "tags": list(metadata.tags),
            "attributes": metadata.attributes,
        }

    def _dict_to_metadata(self, data: dict[str, Any]) -> EventMetadata:
        """Convert a dictionary to metadata."""
        return EventMetadata(
            event_id=data["event_id"],
            event_type=data["event_type"],
            event_version=data["event_version"],
            occurred_at=data["occurred_at"],
            correlation_id=data.get("correlation_id"),
            causation_id=data.get("causation_id"),
            trace_id=data.get("trace_id"),
            producer=data.get("producer"),
            source=data.get("source"),
            subject=data.get("subject"),
            case_id=data.get("case_id"),
            workflow_id=data.get("workflow_id"),
            agent_id=data.get("agent_id"),
            idempotency_key=data.get("idempotency_key"),
            tags=frozenset(data.get("tags", [])),
            attributes=data.get("attributes", {}),
        )

    def can_serialize(self, obj: Any) -> bool:
        """
        Check if an object can be serialized by this serializer.
        
        Args:
            obj: The object to check
            
        Returns:
            True if the object can be serialized
        """
        if isinstance(obj, EventEnvelope):
            return True
        if isinstance(obj, EventMetadata):
            return True
        return False
