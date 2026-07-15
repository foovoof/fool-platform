"""
connectors/base/validation.py

Connector Validators.

Validates connector structures, requests, and configurations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from connectors.base.models import (
    ConnectorDefinition,
    ConnectorRequest,
    ConnectorConfiguration,
    ConnectorArtifact,
    ConnectorStatus,
    ConnectorType,
)


@dataclass
class ValidationIssue:
    """Validation issue."""
    severity: str = "error"
    code: str = ""
    message: str = ""
    path: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass
class ValidationResult:
    """Validation result."""
    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, code: str, message: str, path: str = "") -> None:
        self.is_valid = False
        self.issues.append(ValidationIssue(
            severity="error",
            code=code,
            message=message,
            path=path,
        ))
    
    def add_warning(self, code: str, message: str, path: str = "") -> None:
        self.issues.append(ValidationIssue(
            severity="warning",
            code=code,
            message=message,
            path=path,
        ))
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [i.to_dict() for i in self.issues],
            "metadata": self.metadata,
        }


class ConfigurationValidator:
    """Validates connector configuration."""
    
    def validate(
        self,
        config: ConnectorConfiguration,
    ) -> ValidationResult:
        """
        Validate connector configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if config.timeout <= 0:
            result.add_error(
                "INVALID_TIMEOUT",
                "Timeout must be positive",
                "timeout",
            )
        
        if config.timeout > 300:
            result.add_warning(
                "LARGE_TIMEOUT",
                "Timeout > 300s may cause delays",
                "timeout",
            )
        
        if config.retry_count < 0:
            result.add_error(
                "INVALID_RETRY_COUNT",
                "Retry count must be non-negative",
                "retry_count",
            )
        
        if config.retry_delay < 0:
            result.add_error(
                "INVALID_RETRY_DELAY",
                "Retry delay must be non-negative",
                "retry_delay",
            )
        
        if config.max_size <= 0:
            result.add_error(
                "INVALID_MAX_SIZE",
                "Max size must be positive",
                "max_size",
            )
        
        return result


class RequestValidator:
    """Validates connector requests."""
    
    def validate(self, request: ConnectorRequest) -> ValidationResult:
        """
        Validate connector request.
        
        Args:
            request: Request to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not request.request_id:
            result.add_error(
                "MISSING_REQUEST_ID",
                "Request must have a request_id",
                "request_id",
            )
        
        if not request.connector_id:
            result.add_error(
                "MISSING_CONNECTOR_ID",
                "Request must have a connector_id",
                "connector_id",
            )
        
        if not request.source:
            result.add_error(
                "MISSING_SOURCE",
                "Request must have a source",
                "source",
            )
        
        if not request.operation:
            result.add_warning(
                "MISSING_OPERATION",
                "Request should have an operation",
                "operation",
            )
        
        return result


class LifecycleValidator:
    """Validates connector lifecycle."""
    
    def validate_state_transition(
        self,
        current: ConnectorStatus,
        target: ConnectorStatus,
    ) -> ValidationResult:
        """
        Validate state transition.
        
        Args:
            current: Current status
            target: Target status
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        valid_transitions = {
            ConnectorStatus.PENDING: [ConnectorStatus.INITIALIZED],
            ConnectorStatus.INITIALIZED: [ConnectorStatus.STARTING, ConnectorStatus.STOPPED],
            ConnectorStatus.STARTING: [ConnectorStatus.RUNNING, ConnectorStatus.FAILED],
            ConnectorStatus.RUNNING: [ConnectorStatus.STOPPING, ConnectorStatus.FAILED],
            ConnectorStatus.STOPPING: [ConnectorStatus.STOPPED, ConnectorStatus.FAILED],
            ConnectorStatus.STOPPED: [ConnectorStatus.INITIALIZED, ConnectorStatus.FAILED],
            ConnectorStatus.FAILED: [ConnectorStatus.INITIALIZED],
            ConnectorStatus.COMPLETED: [ConnectorStatus.PENDING],
        }
        
        allowed = valid_transitions.get(current, [])
        if target not in allowed:
            result.add_error(
                "INVALID_TRANSITION",
                f"Cannot transition from {current.value} to {target.value}",
                "status",
            )
        
        return result


class CapabilityValidator:
    """Validates connector capabilities."""
    
    def validate_definition(
        self,
        definition: ConnectorDefinition,
    ) -> ValidationResult:
        """
        Validate connector definition.
        
        Args:
            definition: Definition to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not definition.connector_id:
            result.add_error(
                "MISSING_CONNECTOR_ID",
                "Definition must have an connector_id",
                "connector_id",
            )
        
        if not definition.name:
            result.add_error(
                "MISSING_NAME",
                "Definition must have a name",
                "name",
            )
        
        if not definition.description:
            result.add_warning(
                "MISSING_DESCRIPTION",
                "Definition should have a description",
                "description",
            )
        
        if not definition.capabilities:
            result.add_warning(
                "NO_CAPABILITIES",
                "Definition should declare capabilities",
                "capabilities",
            )
        
        return result


class ArtifactValidator:
    """Validates connector artifacts."""
    
    def validate(self, artifact: ConnectorArtifact) -> ValidationResult:
        """
        Validate connector artifact.
        
        Args:
            artifact: Artifact to validate
            
        Returns:
            Validation result
        """
        result = ValidationResult()
        
        if not artifact.artifact_id:
            result.add_error(
                "MISSING_ARTIFACT_ID",
                "Artifact must have an artifact_id",
                "artifact_id",
            )
        
        if not artifact.name:
            result.add_warning(
                "MISSING_NAME",
                "Artifact should have a name",
                "name",
            )
        
        if artifact.content is None:
            result.add_warning(
                "NULL_CONTENT",
                "Artifact content is null",
                "content",
            )
        
        if artifact.size < 0:
            result.add_error(
                "INVALID_SIZE",
                "Artifact size must be non-negative",
                "size",
            )
        
        return result
