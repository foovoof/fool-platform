"""
connectors/base/__init__.py

Connector Base Components.

Base classes and utilities for connectors.
"""
from connectors.base.models import (
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
)
from connectors.base.connector import BaseConnector
from connectors.base.lifecycle import ConnectorLifecycleManager
from connectors.base.runtime import (
    ConnectorRuntime,
    ConnectorExecutor,
    ConnectorDispatcher,
)
from connectors.base.policies import (
    ConnectorPolicyEngine,
    PolicyRule,
    PolicyResult,
    PolicyType,
)
from connectors.base.events import (
    ConnectorEventEmitter,
    ConnectorEventType,
    ConnectorEvent,
)
from connectors.base.validation import (
    ConfigurationValidator,
    RequestValidator,
    LifecycleValidator,
    CapabilityValidator,
    ArtifactValidator,
    ValidationResult,
    ValidationIssue,
)
from connectors.base.exceptions import (
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
