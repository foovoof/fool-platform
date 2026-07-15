"""
intelligence/runtime/executor.py

Runtime Executor.

Executes pipelines and tasks.
"""
from __future__ import annotations

from typing import Any

from intelligence.models import (
    IntelligenceTask,
    IntelligenceResult,
    IntelligenceFinding,
    IntelligenceArtifact,
    ResultStatus,
)
from intelligence.context import IntelligenceContext
from intelligence.session import IntelligenceSession
from intelligence.pipeline import Pipeline, PipelineStep, PipelineExecutor


class RuntimeExecutor:
    """
    Executes intelligence tasks through pipelines.
    
    Responsibilities:
    - Execute pipeline steps
    - Coordinate step execution
    - Aggregate results
    - Handle errors
    
    NOTE: This is a coordinator, not an intelligence processor.
    """
    
    def __init__(self) -> None:
        """Initialize the executor."""
        self._pipeline_executor = PipelineExecutor()
    
    def execute(
        self,
        task: IntelligenceTask,
        pipeline: Pipeline,
        session: IntelligenceSession,
        context: IntelligenceContext | None = None,
    ) -> IntelligenceResult:
        """
        Execute a task through a pipeline.
        
        Args:
            task: Task to execute
            pipeline: Pipeline to execute
            session: Execution session
            context: Optional context
            
        Returns:
            Task result
        """
        result = IntelligenceResult(task_id=task.task_id)
        
        validation = self._pipeline_executor.validate(pipeline)
        if not validation.is_valid:
            result.status = ResultStatus.FAILURE
            result.errors.extend([i.message for i in validation.issues])
            return result
        
        step_results = self._pipeline_executor.execute(pipeline)
        
        result.outputs = {
            "pipeline_id": pipeline.pipeline_id,
            "steps_executed": len(step_results),
            "step_results": step_results,
        }
        
        for finding_data in pipeline.metadata.get("findings", []):
            finding = IntelligenceFinding(
                finding_type=finding_data.get("type", "observation"),
                title=finding_data.get("title", ""),
                description=finding_data.get("description", ""),
                confidence=finding_data.get("confidence", 0.5),
                source_task_id=task.task_id,
            )
            result.add_finding(finding)
        
        for artifact_data in pipeline.metadata.get("artifacts", []):
            artifact = IntelligenceArtifact(
                artifact_type=artifact_data.get("type", "data"),
                name=artifact_data.get("name", ""),
                content=artifact_data.get("content"),
                source_task_id=task.task_id,
            )
            result.add_artifact(artifact)
        
        for rec_data in pipeline.metadata.get("recommendations", []):
            result.add_recommendation(
                recommendation_type=rec_data.get("type", "general"),
                action=rec_data.get("action", ""),
                rationale=rec_data.get("rationale", ""),
            )
        
        result.status = ResultStatus.SUCCESS
        
        session.add_result(result)
        
        return result
    
    def execute_step(
        self,
        step: PipelineStep,
        task: IntelligenceTask,
        context: IntelligenceContext | None = None,
    ) -> dict[str, Any]:
        """
        Execute a single step.
        
        Args:
            step: Step to execute
            task: Parent task
            context: Optional context
            
        Returns:
            Step result
        """
        return {
            "step_id": step.step_id,
            "step_name": step.name,
            "executed": True,
            "output": {},
        }
