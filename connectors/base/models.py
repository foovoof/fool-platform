"""
connectors/base/models.py

Connector Contracts.

All connector data structures using dataclasses only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ConnectorStatus(Enum):
    """Connector status."""
    PENDING = "pending"
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    COMPLETED = "completed"


class ConnectorType(Enum):
    """Connector type."""
    FILE = "file"
    DIRECTORY = "directory"
    HTTP = "http"
    REST = "rest"
    JSON = "json"
    CSV = "csv"
    TEXT = "text"
    BINARY = "binary"
    ZIP = "zip"
    TAR = "tar"
    GENERIC = "generic"


class ConnectorCapability(Enum):
    """Connector capability."""
    READ = "read"
    WRITE = "write"
    APPEND = "append"
    DELETE = "delete"
    LIST = "list"
    SEARCH = "search"
    STREAM = "stream"


class PolicyAction(Enum):
    """Policy action."""
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"


@dataclass
class ConnectorConfiguration:
    """Connector configuration."""
    connector_id: str = ""
    name: str = ""
    description: str = ""
    connector_type: ConnectorType = ConnectorType.GENERIC
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0
    max_size: int = 10485760  # 10MB default
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "name": self.name,
            "description": self.description,
            "connector_type": self.connector_type.value,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "retry_delay": self.retry_delay,
            "max_size": self.max_size,
            "metadata": self.metadata,
        }


@dataclass
class ConnectorRequest:
    """Connector request."""
    request_id: str = field(default_factory=lambda: str(uuid4()))
    connector_id: str = ""
    connector_type: ConnectorType = ConnectorType.GENERIC
    operation: str = "read"
    source: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "connector_id": self.connector_id,
            "connector_type": self.connector_type.value,
            "operation": self.operation,
            "source": self.source,
            "inputs": self.inputs,
            "parameters": self.parameters,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


@dataclass
class ConnectorArtifact:
    """Connector artifact - raw data retrieved."""
    artifact_id: str = field(default_factory=lambda: str(uuid4()))
    artifact_type: str = "data"
    name: str = ""
    content: Any = None
    content_type: str = "application/octet-stream"
    size: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "name": self.name,
            "content_type": self.content_type,
            "size": self.size,
            "metadata": self.metadata,
        }


@dataclass
class ConnectorResult:
    """Connector execution result."""
    result_id: str = field(default_factory=lambda: str(uuid4()))
    request_id: str = ""
    connector_id: str = ""
    connector_type: ConnectorType = ConnectorType.GENERIC
    status: ConnectorStatus = ConnectorStatus.PENDING
    artifacts: list[ConnectorArtifact] = field(default_factory=list)
    outputs: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""
    execution_time_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def is_successful(self) -> bool:
        return self.status == ConnectorStatus.COMPLETED
    
    def add_artifact(self, artifact: ConnectorArtifact) -> None:
        self.artifacts.append(artifact)
    
    def add_error(self, error: str) -> None:
        self.errors.append(error)
        self.status = ConnectorStatus.FAILED
    
    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "connector_id": self.connector_id,
            "connector_type": self.connector_type.value,
            "status": self.status.value,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "outputs": self.outputs,
            "errors": self.errors,
            "warnings": self.warnings,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "execution_time_ms": self.execution_time_ms,
            "metadata": self.metadata,
        }


@dataclass
class ConnectorDefinition:
    """Connector definition."""
    connector_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    connector_type: ConnectorType = ConnectorType.GENERIC
    version: str = "1.0.0"
    capabilities: list[ConnectorCapability] = field(default_factory=list)
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    configuration: ConnectorConfiguration | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "name": self.name,
            "description": self.description,
            "connector_type": self.connector_type.value,
            "version": self.version,
            "capabilities": [c.value for c in self.capabilities],
            "inputs": self.inputs,
            "outputs": self.outputs,
            "metadata": self.metadata,
        }


@dataclass
class ConnectorExecutionRecord:
    """Execution record for audit/replay."""
    record_id: str = field(default_factory=lambda: str(uuid4()))
    request_id: str = ""
    connector_id: str = ""
    connector_type: ConnectorType = ConnectorType.GENERIC
    operation: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    result_id: str | None = None
    status: ConnectorStatus = ConnectorStatus.PENDING
    started_at: str = ""
    completed_at: str = ""
    execution_time_ms: float = 0.0
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "request_id": self.request_id,
            "connector_id": self.connector_id,
            "connector_type": self.connector_type.value,
            "operation": self.operation,
            "inputs": self.inputs,
            "parameters": self.parameters,
            "result_id": self.result_id,
            "status": self.status.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "execution_time_ms": self.execution_time_ms,
        }
