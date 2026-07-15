"""
intelligence/session.py

Intelligence Session.

Manages the lifecycle of an intelligence execution session.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from intelligence.models import (
    IntelligenceTask,
    IntelligenceResult,
    IntelligenceFinding,
    IntelligenceArtifact,
)


@dataclass
class IntelligenceSession:
    """
    Manages the lifecycle of intelligence execution.
    
    Tracks:
    - Task tracking
    - Execution history
    - Findings collection
    - Artifacts collection
    - Metadata
    """
    session_id: str = field(default_factory=lambda: str(uuid4()))
    context_id: str | None = None
    graph_id: str | None = None
    inference_session_id: str | None = None
    tasks: list[IntelligenceTask] = field(default_factory=list)
    results: list[IntelligenceResult] = field(default_factory=list)
    findings: list[IntelligenceFinding] = field(default_factory=list)
    artifacts: list[IntelligenceArtifact] = field(default_factory=list)
    execution_history: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    status: str = "active"
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    
    def add_task(self, task: IntelligenceTask) -> None:
        """Add a task to the session."""
        self.tasks.append(task)
        self._record_event("task_added", {"task_id": task.task_id})
    
    def add_result(self, result: IntelligenceResult) -> None:
        """Add a result to the session."""
        self.results.append(result)
        
        for finding in result.findings:
            self.add_finding(finding)
        
        for artifact in result.artifacts:
            self.add_artifact(artifact)
        
        self._record_event("result_added", {
            "result_id": result.result_id,
            "task_id": result.task_id,
        })
    
    def add_finding(self, finding: IntelligenceFinding) -> None:
        """Add a finding to the session."""
        if finding not in self.findings:
            self.findings.append(finding)
    
    def add_artifact(self, artifact: IntelligenceArtifact) -> None:
        """Add an artifact to the session."""
        if artifact not in self.artifacts:
            self.artifacts.append(artifact)
    
    def get_task(self, task_id: str) -> IntelligenceTask | None:
        """Get a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_result(self, result_id: str) -> IntelligenceResult | None:
        """Get a result by ID."""
        for result in self.results:
            if result.result_id == result_id:
                return result
        return None
    
    def mark_completed(self) -> None:
        """Mark the session as completed."""
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.status = "completed"
    
    def mark_failed(self, reason: str) -> None:
        """Mark the session as failed."""
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.status = "failed"
        self.metadata["failure_reason"] = reason
    
    def _record_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Record an event in execution history."""
        self.execution_history.append({
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        })
    
    def get_summary(self) -> dict[str, Any]:
        """Get session summary."""
        return {
            "session_id": self.session_id,
            "status": self.status,
            "task_count": len(self.tasks),
            "result_count": len(self.results),
            "finding_count": len(self.findings),
            "artifact_count": len(self.artifacts),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "session_id": self.session_id,
            "context_id": self.context_id,
            "graph_id": self.graph_id,
            "inference_session_id": self.inference_session_id,
            "tasks": [t.to_dict() for t in self.tasks],
            "results": [r.to_dict() for r in self.results],
            "findings": [f.to_dict() for f in self.findings],
            "artifacts": [a.to_dict() for a in self.artifacts],
            "execution_history": self.execution_history,
            "metadata": self.metadata,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IntelligenceSession:
        """Create from dictionary."""
        if "tasks" in data:
            data["tasks"] = [
                IntelligenceTask.from_dict(t)
                for t in data["tasks"]
            ]
        if "results" in data:
            data["results"] = [
                IntelligenceResult.from_dict(r)
                for r in data["results"]
            ]
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
