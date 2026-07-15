"""
intelligence/models/__init__.py

Intelligence Models.

Defines core data structures for the Intelligence Runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskStatus(Enum):
    """Intelligence task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FindingType(Enum):
    """Intelligence finding types."""
    OBSERVATION = "observation"
    PATTERN = "pattern"
    CORRELATION = "correlation"
    ANOMALY = "anomaly"
    INDICATOR = "indicator"
    CONCLUSION = "conclusion"
    RECOMMENDATION = "recommendation"


class ArtifactType(Enum):
    """Intelligence artifact types."""
    REPORT = "report"
    SUMMARY = "summary"
    GRAPH = "graph"
    EVIDENCE = "evidence"
    DATA = "data"
    METADATA = "metadata"


class ResultStatus(Enum):
    """Intelligence result status."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    CANCELLED = "cancelled"


@dataclass
class IntelligenceTask:
    """
    Represents an intelligence task.
    
    Tasks are the primary unit of work for the Intelligence Runtime.
    """
    task_id: str = field(default_factory=lambda: str(uuid4()))
    task_type: str = ""
    objective: str = ""
    inputs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    trace_id: str | None = None
    correlation_id: str | None = None
    parent_task_id: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    status: TaskStatus = TaskStatus.PENDING
    
    def is_valid(self) -> bool:
        """Check if task is valid."""
        return bool(self.task_type) and bool(self.objective)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "objective": self.objective,
            "inputs": self.inputs,
            "metadata": self.metadata,
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "parent_task_id": self.parent_task_id,
            "created_at": self.created_at,
            "status": self.status.value,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntelligenceTask:
        """Create from dictionary."""
        if isinstance(data.get("status"), str):
            data["status"] = TaskStatus(data["status"])
        return cls(**data)


@dataclass
class IntelligenceFinding:
    """
    Represents an intelligence finding.
    
    Findings are the results of intelligence analysis.
    """
    finding_id: str = field(default_factory=lambda: str(uuid4()))
    finding_type: FindingType = FindingType.OBSERVATION
    title: str = ""
    description: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    confidence: float = 0.0
    source_task_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def is_valid(self) -> bool:
        """Check if finding is valid."""
        return (
            bool(self.title)
            and 0.0 <= self.confidence <= 1.0
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "finding_id": self.finding_id,
            "finding_type": self.finding_type.value,
            "title": self.title,
            "description": self.description,
            "evidence_refs": self.evidence_refs,
            "confidence": self.confidence,
            "source_task_id": self.source_task_id,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntelligenceFinding:
        """Create from dictionary."""
        if isinstance(data.get("finding_type"), str):
            data["finding_type"] = FindingType(data["finding_type"])
        return cls(**data)


@dataclass
class IntelligenceArtifact:
    """
    Represents an intelligence artifact.
    
    Artifacts are the outputs produced by intelligence processing.
    """
    artifact_id: str = field(default_factory=lambda: str(uuid4()))
    artifact_type: ArtifactType = ArtifactType.DATA
    content: Any = None
    name: str = ""
    source_task_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type.value,
            "content": self.content,
            "name": self.name,
            "source_task_id": self.source_task_id,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntelligenceArtifact:
        """Create from dictionary."""
        if isinstance(data.get("artifact_type"), str):
            data["artifact_type"] = ArtifactType(data["artifact_type"])
        return cls(**data)


@dataclass
class IntelligenceResult:
    """
    Represents the result of an intelligence task.
    
    Results contain outputs, findings, artifacts, and recommendations.
    """
    result_id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    status: ResultStatus = ResultStatus.SUCCESS
    outputs: dict[str, Any] = field(default_factory=dict)
    findings: list[IntelligenceFinding] = field(default_factory=list)
    artifacts: list[IntelligenceArtifact] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    
    def is_successful(self) -> bool:
        """Check if result is successful."""
        return self.status == ResultStatus.SUCCESS and len(self.errors) == 0
    
    def add_finding(self, finding: IntelligenceFinding) -> None:
        """Add a finding."""
        self.findings.append(finding)
    
    def add_artifact(self, artifact: IntelligenceArtifact) -> None:
        """Add an artifact."""
        self.artifacts.append(artifact)
    
    def add_recommendation(
        self,
        recommendation_type: str,
        action: str,
        rationale: str,
    ) -> None:
        """Add a recommendation."""
        self.recommendations.append({
            "type": recommendation_type,
            "action": action,
            "rationale": rationale,
        })
    
    def mark_completed(self) -> None:
        """Mark result as completed."""
        self.completed_at = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "result_id": self.result_id,
            "task_id": self.task_id,
            "status": self.status.value,
            "outputs": self.outputs,
            "findings": [f.to_dict() for f in self.findings],
            "artifacts": [a.to_dict() for a in self.artifacts],
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntelligenceResult:
        """Create from dictionary."""
        if isinstance(data.get("status"), str):
            data["status"] = ResultStatus(data["status"])
        if "findings" in data:
            data["findings"] = [
                IntelligenceFinding.from_dict(f)
                for f in data["findings"]
            ]
        if "artifacts" in data:
            data["artifacts"] = [
                IntelligenceArtifact.from_dict(a)
                for a in data["artifacts"]
            ]
        return cls(**data)
