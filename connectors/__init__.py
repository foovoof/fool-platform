"""
connectors/__init__.py

FOOL Platform Data Connectors.

IMPORTANT: Connectors only retrieve data.
No intelligence, parsing, or processing.
"""

from connectors.base import (
    # Models
    ConnectorStatus,
    ConnectorType,
    ConnectorCapability,
    ConnectorConfiguration,
    ConnectorRequest,
    ConnectorResult,
    ConnectorArtifact,
    ConnectorDefinition,
    ConnectorExecutionRecord,
    PolicyAction,
    # Connector
    BaseConnector,
    # Lifecycle
    ConnectorLifecycleManager,
    # Runtime
    ConnectorRuntime,
    ConnectorExecutor,
    ConnectorDispatcher,
    # Policies
    ConnectorPolicyEngine,
    PolicyRule,
    PolicyResult,
    PolicyType,
    # Events
    ConnectorEventEmitter,
    ConnectorEventType,
    ConnectorEvent,
    # Validation
    ConfigurationValidator,
    RequestValidator,
    LifecycleValidator,
    CapabilityValidator,
    ArtifactValidator,
    ValidationResult,
    ValidationIssue,
    # Exceptions
    ConnectorError,
    ConnectorInitializationError,
    ConnectorStartError,
    ConnectorStopError,
    ConnectorValidationError,
    ConnectorExecutionError,
    ConnectorTimeoutError,
    ConnectorNotFoundError,
    ConnectorConfigurationError,
    ConnectorPolicyError,
    ConnectorHealthCheckError,
    ConnectorArtifactError,
)


__all__ = [
    # Models
    "ConnectorStatus",
    "ConnectorType",
    "ConnectorCapability",
    "ConnectorConfiguration",
    "ConnectorRequest",
    "ConnectorResult",
    "ConnectorArtifact",
    "ConnectorDefinition",
    "ConnectorExecutionRecord",
    "PolicyAction",
    # Connector
    "BaseConnector",
    # Lifecycle
    "ConnectorLifecycleManager",
    # Runtime
    "ConnectorRuntime",
    "ConnectorExecutor",
    "ConnectorDispatcher",
    # Policies
    "ConnectorPolicyEngine",
    "PolicyRule",
    "PolicyResult",
    "PolicyType",
    # Events
    "ConnectorEventEmitter",
    "ConnectorEventType",
    "ConnectorEvent",
    # Validation
    "ConfigurationValidator",
    "RequestValidator",
    "LifecycleValidator",
    "CapabilityValidator",
    "ArtifactValidator",
    "ValidationResult",
    "ValidationIssue",
    # Exceptions
    "ConnectorError",
    "ConnectorInitializationError",
    "ConnectorStartError",
    "ConnectorStopError",
    "ConnectorValidationError",
    "ConnectorExecutionError",
    "ConnectorTimeoutError",
    "ConnectorNotFoundError",
    "ConnectorConfigurationError",
    "ConnectorPolicyError",
    "ConnectorHealthCheckError",
    "ConnectorArtifactError",
]
