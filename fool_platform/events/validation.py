"""
fool_platform/events/validation.py

Event validation logic for the Event Bus.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fool_platform.events.envelope import EventEnvelope, ValidationStatus
from fool_platform.events.exceptions import EventValidationError
from fool_platform.events.metadata import EventMetadata

if TYPE_CHECKING:
    from fool_platform.events.event_registry import EventRegistry


@dataclass
class ValidationError:
    """A single validation error."""
    field: str
    message: str
    code: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message} ({self.code})"


@dataclass
class ValidationResult:
    """Result of event validation."""
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def success(cls) -> "ValidationResult":
        """Create a successful validation result."""
        return cls(valid=True, errors=[], warnings=[])

    @classmethod
    def failure(cls, errors: list[ValidationError]) -> "ValidationResult":
        """Create a failed validation result."""
        return cls(valid=False, errors=errors, warnings=[])

    def add_error(self, field: str, message: str, code: str) -> None:
        """Add an error to the result."""
        self.errors.append(ValidationError(field=field, message=message, code=code))
        self.valid = False

    def add_warning(self, warning: str) -> None:
        """Add a warning to the result."""
        self.warnings.append(warning)

    def __str__(self) -> str:
        if self.valid:
            return "ValidationResult(valid=True)"
        return f"ValidationResult(valid=False, errors={len(self.errors)})"


@dataclass
class EventValidator:
    """
    Validates events against structural requirements and registry constraints.
    
    Does not implement full JSON Schema validation unless registry provides it.
    """
    _registry: "EventRegistry | None" = field(default=None, repr=False)
    _require_idempotency_key: bool = False
    _strict_version_checking: bool = True

    def validate_envelope(self, event: EventEnvelope) -> ValidationResult:
        """
        Validate an event envelope.
        
        Args:
            event: The event envelope to validate
            
        Returns:
            A ValidationResult indicating success or failure
        """
        result = ValidationResult.success()

        if event.metadata is None:
            result.add_error("metadata", "Event metadata is required", "MISSING_METADATA")
            return result

        metadata_result = self.validate_metadata(event.metadata)
        if not metadata_result.valid:
            result.valid = False
            result.errors.extend(metadata_result.errors)
            result.warnings.extend(metadata_result.warnings)

        payload_result = self.validate_payload(event.payload)
        if not payload_result.valid:
            result.valid = False
            result.errors.extend(payload_result.errors)

        if self._registry and self._registry.is_loaded():
            registry_result = self.validate_against_registry(event)
            if not registry_result.valid:
                result.valid = False
                result.errors.extend(registry_result.errors)

        return result

    def validate_metadata(self, metadata: EventMetadata) -> ValidationResult:
        """
        Validate event metadata.
        
        Args:
            metadata: The metadata to validate
            
        Returns:
            A ValidationResult indicating success or failure
        """
        result = ValidationResult.success()

        if not metadata.event_id or not metadata.event_id.strip():
            result.add_error("event_id", "Event ID is required", "MISSING_EVENT_ID")

        if not metadata.event_type or not metadata.event_type.strip():
            result.add_error("event_type", "Event type is required", "MISSING_EVENT_TYPE")

        if not metadata.event_version or not metadata.event_version.strip():
            result.add_error(
                "event_version",
                "Event version is required",
                "MISSING_EVENT_VERSION",
            )

        if not metadata.occurred_at or not metadata.occurred_at.strip():
            result.add_error(
                "occurred_at",
                "Occurred at timestamp is required",
                "MISSING_OCCURRED_AT",
            )

        if metadata.idempotency_key is not None:
            if not isinstance(metadata.idempotency_key, str):
                result.add_error(
                    "idempotency_key",
                    "Idempotency key must be a string",
                    "INVALID_IDEMPOTENCY_KEY_TYPE",
                )
            elif not metadata.idempotency_key.strip():
                result.add_error(
                    "idempotency_key",
                    "Idempotency key cannot be empty",
                    "EMPTY_IDEMPOTENCY_KEY",
                )

        if metadata.tags and not isinstance(metadata.tags, frozenset):
            result.add_warning("Tags should be a frozenset for immutability")

        return result

    def validate_payload(self, payload: dict) -> ValidationResult:
        """
        Validate event payload structure.
        
        Args:
            payload: The payload to validate
            
        Returns:
            A ValidationResult indicating success or failure
        """
        result = ValidationResult.success()

        if payload is None:
            result.add_error("payload", "Event payload is required", "MISSING_PAYLOAD")
            return result

        if not isinstance(payload, dict):
            result.add_error(
                "payload",
                "Event payload must be a dictionary",
                "INVALID_PAYLOAD_TYPE",
            )

        return result

    def validate_event_type(
        self,
        event_type: str,
        event_version: str | None = None,
    ) -> ValidationResult:
        """
        Validate an event type against the registry.
        
        Args:
            event_type: The event type to validate
            event_version: The event version to validate
            
        Returns:
            A ValidationResult indicating success or failure
        """
        result = ValidationResult.success()

        if self._registry is None or not self._registry.is_loaded():
            return result

        if not self._registry.has_event_type(event_type):
            result.add_error(
                "event_type",
                f"Unknown event type: {event_type}",
                "UNKNOWN_EVENT_TYPE",
            )

        elif event_version and not self._registry.has_event_version(event_type, event_version):
            result.add_error(
                "event_version",
                f"Unknown event version {event_version} for event type {event_type}",
                "UNKNOWN_EVENT_VERSION",
            )

        return result

    def validate_against_registry(self, event: EventEnvelope) -> ValidationResult:
        """
        Validate an event against the registry.
        
        Args:
            event: The event to validate
            
        Returns:
            A ValidationResult indicating success or failure
        """
        return self.validate_event_type(event.event_type, event.event_version)

    def set_registry(self, registry: "EventRegistry | None") -> None:
        """Set or update the registry."""
        self._registry = registry

    def set_require_idempotency_key(self, required: bool) -> None:
        """Set whether idempotency keys are required."""
        self._require_idempotency_key = required

    def set_strict_version_checking(self, strict: bool) -> None:
        """Set whether to strictly check event versions."""
        self._strict_version_checking = strict
