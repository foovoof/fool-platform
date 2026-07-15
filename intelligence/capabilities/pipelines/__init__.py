"""
intelligence/capabilities/pipelines/__init__.py

Capability Pipelines.

Defines execution pipelines for capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityType,
    CapabilityStatus,
)


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PipelineStep:
    """A step in a capability pipeline."""
    step_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    step_type: str = ""
    handler: Callable | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    order: int = 0
    required: bool = True
    
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the step."""
        if self.handler:
            return self.handler(context)
        return {"step": self.name, "status": "executed"}


@dataclass
class CapabilityPipeline:
    """Pipeline for capability execution."""
    pipeline_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    capability_type: CapabilityType = CapabilityType.RESEARCH
    steps: list[PipelineStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def add_step(self, step: PipelineStep) -> None:
        """Add a step to the pipeline."""
        step.order = len(self.steps)
        self.steps.append(step)
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validate the pipeline."""
        errors = []
        
        if not self.name:
            errors.append("Pipeline must have a name")
        
        if not self.steps:
            errors.append("Pipeline must have at least one step")
        
        for step in self.steps:
            if not step.name:
                errors.append(f"Step {step.order} must have a name")
        
        return len(errors) == 0, errors
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        """Execute the pipeline."""
        result = CapabilityResult(
            task_id=task.task_id,
            capability_id=task.capability_id,
            capability_type=self.capability_type,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        
        context = {
            "task": task,
            "result": result,
            "pipeline": self,
        }
        
        try:
            for step in self.steps:
                step_result = step.execute(context)
                context[f"step_{step.order}_result"] = step_result
                
                if step_result.get("status") == "failed" and step.required:
                    result.status = CapabilityStatus.FAILED
                    result.errors.append(f"Required step '{step.name}' failed")
                    break
            
            if result.status != CapabilityStatus.FAILED:
                result.status = CapabilityStatus.COMPLETED
            
        except Exception as e:
            result.status = CapabilityStatus.FAILED
            result.errors.append(str(e))
        
        result.completed_at = datetime.now(timezone.utc).isoformat()
        return result


def create_default_pipeline(
    capability_type: CapabilityType,
) -> CapabilityPipeline:
    """Create default pipeline for a capability type."""
    pipeline = CapabilityPipeline(
        name=f"Default {capability_type.value.title()} Pipeline",
        description=f"Default pipeline for {capability_type.value} capability",
        capability_type=capability_type,
    )
    
    pipeline.add_step(PipelineStep(
        name="Validate",
        step_type="validation",
        handler=lambda ctx: {"status": "passed"},
    ))
    
    pipeline.add_step(PipelineStep(
        name="Execute",
        step_type="execution",
        handler=lambda ctx: {"status": "completed"},
    ))
    
    pipeline.add_step(PipelineStep(
        name="Aggregate",
        step_type="aggregation",
        handler=lambda ctx: {"status": "completed"},
    ))
    
    return pipeline


class PipelineRegistry:
    """Registry for capability pipelines."""
    
    def __init__(self) -> None:
        """Initialize registry."""
        self._pipelines: dict[CapabilityType, CapabilityPipeline] = {}
        self._by_id: dict[str, CapabilityPipeline] = {}
    
    def register(self, pipeline: CapabilityPipeline) -> bool:
        """Register a pipeline."""
        is_valid, errors = pipeline.validate()
        if not is_valid:
            return False
        
        self._pipelines[pipeline.capability_type] = pipeline
        self._by_id[pipeline.pipeline_id] = pipeline
        return True
    
    def get(self, capability_type: CapabilityType) -> CapabilityPipeline | None:
        """Get pipeline by capability type."""
        return self._pipelines.get(capability_type)
    
    def get_by_id(self, pipeline_id: str) -> CapabilityPipeline | None:
        """Get pipeline by ID."""
        return self._by_id.get(pipeline_id)
    
    def get_or_create(self, capability_type: CapabilityType) -> CapabilityPipeline:
        """Get pipeline or create default."""
        pipeline = self.get(capability_type)
        if not pipeline:
            pipeline = create_default_pipeline(capability_type)
            self.register(pipeline)
        return pipeline


class PipelineExecutor:
    """Executes capability pipelines."""
    
    def __init__(self) -> None:
        """Initialize executor."""
        self._registry = PipelineRegistry()
    
    def execute(
        self,
        capability_type: CapabilityType,
        task: CapabilityTask,
    ) -> CapabilityResult:
        """Execute pipeline for capability type."""
        pipeline = self._registry.get_or_create(capability_type)
        return pipeline.execute(task)
