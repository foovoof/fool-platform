"""
intelligence/pipeline/pipeline.py

Intelligence Pipeline.

Provides pipeline execution for intelligence tasks.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


class StepStatus(Enum):
    """Pipeline step status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PipelineStep:
    """
    Represents a single step in a pipeline.
    
    Steps are executed sequentially in a deterministic order.
    """
    step_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    step_type: str = ""
    handler: Callable | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    status: StepStatus = StepStatus.PENDING
    order: int = 0
    required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def execute(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute the step."""
        self.status = StepStatus.RUNNING
        
        if self.handler:
            try:
                self.outputs = self.handler(self.inputs, context or {})
                self.status = StepStatus.COMPLETED
            except Exception as e:
                self.status = StepStatus.FAILED
                self.outputs = {"error": str(e)}
        else:
            self.status = StepStatus.COMPLETED
        
        return self.outputs
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step_id": self.step_id,
            "name": self.name,
            "description": self.description,
            "step_type": self.step_type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "status": self.status.value,
            "order": self.order,
            "required": self.required,
            "metadata": self.metadata,
        }


@dataclass
class ExecutionReport:
    """Report of pipeline execution."""
    pipeline_id: str
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: str | None = None
    steps_executed: int = 0
    steps_completed: int = 0
    steps_failed: int = 0
    steps_skipped: int = 0
    results: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    checkpoints: list[dict[str, Any]] = field(default_factory=list)
    
    def add_checkpoint(self, name: str, data: dict[str, Any]) -> None:
        """Add a checkpoint."""
        self.checkpoints.append({
            "name": name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        })
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pipeline_id": self.pipeline_id,
            "execution_id": self.execution_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps_executed": self.steps_executed,
            "steps_completed": self.steps_completed,
            "steps_failed": self.steps_failed,
            "steps_skipped": self.steps_skipped,
            "results": self.results,
            "errors": self.errors,
            "checkpoints": self.checkpoints,
        }


@dataclass
class Pipeline:
    """
    Represents an intelligence pipeline.
    
    Pipelines are sequences of steps executed deterministically.
    """
    pipeline_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    task_type: str = ""
    steps: list[PipelineStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_step(self, step: PipelineStep) -> None:
        """Add a step to the pipeline."""
        step.order = len(self.steps)
        self.steps.append(step)
    
    def get_step(self, step_id: str) -> PipelineStep | None:
        """Get step by ID."""
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validate the pipeline."""
        errors = []
        
        if not self.steps:
            errors.append("Pipeline has no steps")
        
        for i, step in enumerate(self.steps):
            if not step.name:
                errors.append(f"Step {i} has no name")
            
            if step.required and not step.handler:
                errors.append(f"Required step '{step.name}' has no handler")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "description": self.description,
            "task_type": self.task_type,
            "steps": [s.to_dict() for s in self.steps],
            "metadata": self.metadata,
        }


class PipelineExecutor:
    """
    Executes pipelines.
    
    Supports sequential execution with checkpoints.
    """
    
    def __init__(self) -> None:
        """Initialize the executor."""
        pass
    
    def validate(self, pipeline: Pipeline) -> ValidationResult:
        """Validate a pipeline."""
        is_valid, errors = pipeline.validate()
        
        result = ValidationResult(
            is_valid=is_valid,
            pipeline_id=pipeline.pipeline_id,
        )
        
        for error in errors:
            result.add_issue("validation_error", "error", error)
        
        return result
    
    def execute(
        self,
        pipeline: Pipeline,
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute a pipeline.
        
        Args:
            pipeline: Pipeline to execute
            context: Execution context
            
        Returns:
            List of step results
        """
        results: list[dict[str, Any]] = []
        
        sorted_steps = sorted(pipeline.steps, key=lambda s: s.order)
        
        for step in sorted_steps:
            try:
                output = step.execute(context)
                results.append({
                    "step_id": step.step_id,
                    "name": step.name,
                    "status": step.status.value,
                    "output": output,
                })
            except Exception as e:
                results.append({
                    "step_id": step.step_id,
                    "name": step.name,
                    "status": StepStatus.FAILED.value,
                    "error": str(e),
                })
                if step.required:
                    break
        
        return results


@dataclass
class ValidationIssue:
    """A validation issue."""
    issue_type: str
    severity: str
    message: str


@dataclass
class ValidationResult:
    """Result of validation."""
    is_valid: bool
    pipeline_id: str
    issues: list[ValidationIssue] = field(default_factory=list)
    
    def add_issue(
        self,
        issue_type: str,
        severity: str,
        message: str,
    ) -> None:
        """Add a validation issue."""
        self.issues.append(ValidationIssue(
            issue_type=issue_type,
            severity=severity,
            message=message,
        ))
        if severity == "error":
            self.is_valid = False


class PipelineRegistry:
    """
    Registry for managing pipelines.
    """
    
    def __init__(self) -> None:
        """Initialize the registry."""
        self._pipelines: dict[str, Pipeline] = {}
        self._by_task_type: dict[str, str] = {}
    
    def register_pipeline(self, pipeline: Pipeline) -> bool:
        """
        Register a pipeline.
        
        Args:
            pipeline: Pipeline to register
            
        Returns:
            True if registered successfully
        """
        is_valid, _ = pipeline.validate()
        if not is_valid:
            return False
        
        self._pipelines[pipeline.pipeline_id] = pipeline
        
        if pipeline.task_type:
            self._by_task_type[pipeline.task_type] = pipeline.pipeline_id
        
        return True
    
    def get_pipeline(self, task_type: str) -> Pipeline | None:
        """Get pipeline by task type."""
        pipeline_id = self._by_task_type.get(task_type)
        if pipeline_id:
            return self._pipelines.get(pipeline_id)
        return None
    
    def get_pipeline_by_id(self, pipeline_id: str) -> Pipeline | None:
        """Get pipeline by ID."""
        return self._pipelines.get(pipeline_id)
    
    def list_pipelines(self) -> list[Pipeline]:
        """List all pipelines."""
        return list(self._pipelines.values())
    
    def unregister_pipeline(self, pipeline_id: str) -> bool:
        """Unregister a pipeline."""
        if pipeline_id not in self._pipelines:
            return False
        
        pipeline = self._pipelines[pipeline_id]
        if pipeline.task_type in self._by_task_type:
            del self._by_task_type[pipeline.task_type]
        
        del self._pipelines[pipeline_id]
        return True
