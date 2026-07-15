"""
intelligence/services/pipeline_service.py

Pipeline Service.

Manages pipelines.
"""
from typing import Any

from intelligence.pipeline import Pipeline, PipelineStep, PipelineRegistry


class PipelineService:
    """
    Service for pipeline management.
    
    Coordinates:
    - Pipeline registration
    - Pipeline retrieval
    - Pipeline validation
    """
    
    def __init__(self, registry: PipelineRegistry | None = None) -> None:
        """Initialize the service."""
        self._registry = registry or PipelineRegistry()
    
    def register_pipeline(self, pipeline: Pipeline) -> dict[str, Any]:
        """
        Register a pipeline.
        
        Args:
            pipeline: Pipeline to register
            
        Returns:
            Registration result
        """
        success = self._registry.register_pipeline(pipeline)
        
        return {
            "success": success,
            "pipeline_id": pipeline.pipeline_id,
        }
    
    def get_pipeline(self, task_type: str) -> dict[str, Any] | None:
        """Get pipeline by task type."""
        pipeline = self._registry.get_pipeline(task_type)
        if pipeline:
            return pipeline.to_dict()
        return None
    
    def list_pipelines(self) -> list[dict[str, Any]]:
        """List all pipelines."""
        return [p.to_dict() for p in self._registry.list_pipelines()]
    
    def create_pipeline(
        self,
        name: str,
        task_type: str,
        steps: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new pipeline.
        
        Args:
            name: Pipeline name
            task_type: Task type
            steps: Optional step definitions
            
        Returns:
            Created pipeline
        """
        pipeline = Pipeline(
            name=name,
            task_type=task_type,
        )
        
        if steps:
            for step_data in steps:
                step = PipelineStep(
                    name=step_data.get("name", ""),
                    step_type=step_data.get("type", ""),
                )
                pipeline.add_step(step)
        
        self._registry.register_pipeline(pipeline)
        
        return pipeline.to_dict()
