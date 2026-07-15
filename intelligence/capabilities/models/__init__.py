"""
intelligence/capabilities/models/__init__.py

Intelligence Capability Models.

Defines core data structures for intelligence capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class CapabilityType(Enum):
    """Intelligence capability types."""
    RESEARCH = "research"
    DISCOVERY = "discovery"
    EXTRACTION = "extraction"
    CORRELATION = "correlation"
    INVESTIGATION = "investigation"
    ASSESSMENT = "assessment"
    REPORTING = "reporting"
    TIMELINE = "timeline"
    EVIDENCE_ANALYSIS = "evidence_analysis"


class CapabilityStatus(Enum):
    """Capability execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FindingType(Enum):
    """Finding types for capabilities."""
    OBSERVATION = "observation"
    PATTERN = "pattern"
    CORRELATION = "correlation"
    ANOMALY = "anomaly"
    INDICATOR = "indicator"
    CONCLUSION = "conclusion"
    RECOMMENDATION = "recommendation"


@dataclass
class CapabilityDefinition:
    """
    Defines an intelligence capability.
    
    A capability is a reusable unit of intelligence work.
    """
    capability_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    version: str = "1.0.0"
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    pipeline_id: str | None = None
    agent_type: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "description": self.description,
            "capability_type": self.capability_type.value,
            "version": self.version,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "parameters": self.parameters,
            "metadata": self.metadata,
            "pipeline_id": self.pipeline_id,
            "agent_type": self.agent_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityDefinition:
        """Create from dictionary."""
        if isinstance(data.get("capability_type"), str):
            data["capability_type"] = CapabilityType(data["capability_type"])
        return cls(**data)


@dataclass
class CapabilityTask:
    """
    Represents a task for a capability.
    
    Tasks are created when a capability is invoked.
    """
    task_id: str = field(default_factory=lambda: str(uuid4()))
    capability_id: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    objective: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    status: CapabilityStatus = CapabilityStatus.PENDING
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "capability_id": self.capability_id,
            "capability_type": self.capability_type.value,
            "objective": self.objective,
            "inputs": self.inputs,
            "parameters": self.parameters,
            "context": self.context,
            "status": self.status.value,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityTask:
        """Create from dictionary."""
        if isinstance(data.get("capability_type"), str):
            data["capability_type"] = CapabilityType(data["capability_type"])
        if isinstance(data.get("status"), str):
            data["status"] = CapabilityStatus(data["status"])
        return cls(**data)


@dataclass
class CapabilityArtifact:
    """
    Represents an artifact produced by a capability.
    
    Artifacts are structured outputs like reports, graphs, or data.
    """
    artifact_id: str = field(default_factory=lambda: str(uuid4()))
    artifact_type: str = ""
    name: str = ""
    content: Any = None
    task_id: str | None = None
    capability_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "name": self.name,
            "content": self.content,
            "task_id": self.task_id,
            "capability_id": self.capability_id,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityArtifact:
        """Create from dictionary."""
        return cls(**data)


@dataclass
class CapabilityFinding:
    """
    Represents a finding from a capability execution.
    
    Findings are insights derived from analysis.
    """
    finding_id: str = field(default_factory=lambda: str(uuid4()))
    finding_type: FindingType = FindingType.OBSERVATION
    title: str = ""
    description: str = ""
    confidence: float = 0.0
    evidence_refs: list[str] = field(default_factory=list)
    task_id: str | None = None
    capability_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "finding_id": self.finding_id,
            "finding_type": self.finding_type.value,
            "title": self.title,
            "description": self.description,
            "confidence": self.confidence,
            "evidence_refs": self.evidence_refs,
            "task_id": self.task_id,
            "capability_id": self.capability_id,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityFinding:
        """Create from dictionary."""
        if isinstance(data.get("finding_type"), str):
            data["finding_type"] = FindingType(data["finding_type"])
        return cls(**data)


@dataclass
class CapabilityResult:
    """
    Represents the result of a capability execution.
    
    Results contain findings, artifacts, and execution metadata.
    """
    result_id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    capability_id: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    status: CapabilityStatus = CapabilityStatus.COMPLETED
    findings: list[CapabilityFinding] = field(default_factory=list)
    artifacts: list[CapabilityArtifact] = field(default_factory=list)
    outputs: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    
    def is_successful(self) -> bool:
        """Check if result is successful."""
        return self.status == CapabilityStatus.COMPLETED and len(self.errors) == 0
    
    def add_finding(self, finding: CapabilityFinding) -> None:
        """Add a finding to the result."""
        self.findings.append(finding)
    
    def add_artifact(self, artifact: CapabilityArtifact) -> None:
        """Add an artifact to the result."""
        self.artifacts.append(artifact)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "result_id": self.result_id,
            "task_id": self.task_id,
            "capability_id": self.capability_id,
            "capability_type": self.capability_type.value,
            "status": self.status.value,
            "findings": [f.to_dict() for f in self.findings],
            "artifacts": [a.to_dict() for a in self.artifacts],
            "outputs": self.outputs,
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata,
            "execution_time_ms": self.execution_time_ms,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityResult:
        """Create from dictionary."""
        if isinstance(data.get("capability_type"), str):
            data["capability_type"] = CapabilityType(data["capability_type"])
        if isinstance(data.get("status"), str):
            data["status"] = CapabilityStatus(data["status"])
        if "findings" in data:
            data["findings"] = [
                CapabilityFinding.from_dict(f) for f in data["findings"]
            ]
        if "artifacts" in data:
            data["artifacts"] = [
                CapabilityArtifact.from_dict(a) for a in data["artifacts"]
            ]
        return cls(**data)


@dataclass
class CapabilityExecutionRecord:
    """
    Records the execution of a capability.
    
    Used for auditing and replay.
    """
    record_id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    capability_id: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    inputs: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    result_id: str | None = None
    status: CapabilityStatus = CapabilityStatus.PENDING
    agent_id: str | None = None
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "record_id": self.record_id,
            "task_id": self.task_id,
            "capability_id": self.capability_id,
            "capability_type": self.capability_type.value,
            "inputs": self.inputs,
            "parameters": self.parameters,
            "result_id": self.result_id,
            "status": self.status.value,
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityExecutionRecord:
        """Create from dictionary."""
        if isinstance(data.get("capability_type"), str):
            data["capability_type"] = CapabilityType(data["capability_type"])
        if isinstance(data.get("status"), str):
            data["status"] = CapabilityStatus(data["status"])
        return cls(**data)
