"""
intelligence/runtime/runtime.py

Intelligence Runtime.

Core runtime for intelligence task execution.

IMPORTANT: The runtime does NOT perform intelligence logic.
The runtime ONLY orchestrates execution.
"""
from __future__ import annotations

from typing import Any

from intelligence.models import (
    IntelligenceTask,
    IntelligenceResult,
    TaskStatus,
    ResultStatus,
)
from intelligence.context import IntelligenceContext
from intelligence.session import IntelligenceSession
from intelligence.runtime.executor import RuntimeExecutor
from intelligence.runtime.dispatcher import RuntimeDispatcher
from intelligence.pipeline import PipelineRegistry, Pipeline
from intelligence.validation import RuntimeValidator, ValidationResult


class IntelligenceRuntime:
    """
    Core Intelligence Runtime.
    
    Responsibilities:
    - Receive intelligence task
    - Validate task
    - Create session
    - Execute runtime pipeline
    - Invoke Agent Runtime (delegation)
    - Consume Knowledge Services (delegation)
    - Consume Inference Services (delegation)
    - Aggregate results
    - Return IntelligenceResult
    
    IMPORTANT: Runtime MUST NOT perform intelligence logic.
    Runtime ONLY orchestrates execution.
    """
    
    def __init__(
        self,
        executor: RuntimeExecutor | None = None,
        dispatcher: RuntimeDispatcher | None = None,
        validator: RuntimeValidator | None = None,
        pipeline_registry: PipelineRegistry | None = None,
        event_emitter: Any = None,
    ) -> None:
        """
        Initialize the Intelligence Runtime.
        
        Args:
            executor: Runtime executor
            dispatcher: Runtime dispatcher
            validator: Runtime validator
            pipeline_registry: Pipeline registry
            event_emitter: Optional event emitter
        """
        self._executor = executor or RuntimeExecutor()
        self._dispatcher = dispatcher or RuntimeDispatcher()
        self._validator = validator or RuntimeValidator()
        self._pipeline_registry = pipeline_registry or PipelineRegistry()
        self._event_emitter = event_emitter
        self._active_sessions: dict[str, IntelligenceSession] = {}
    
    def execute_task(
        self,
        task: IntelligenceTask,
        context: IntelligenceContext | None = None,
    ) -> IntelligenceResult:
        """
        Execute an intelligence task.
        
        Args:
            task: The task to execute
            context: Optional execution context
            
        Returns:
            Intelligence result
        """
        result = IntelligenceResult(task_id=task.task_id)
        
        validation = self._validator.validate_task(task)
        if not validation.is_valid:
            result.status = ResultStatus.FAILURE
            result.errors.extend([i.message for i in validation.issues])
            return result
        
        session = self._create_session(task, context)
        task.status = TaskStatus.RUNNING
        
        self._emit_event("intelligence.task.started", {
            "task_id": task.task_id,
            "session_id": session.session_id,
        })
        
        try:
            result = self._execute_pipeline(task, session, context)
            
            if result.is_successful():
                task.status = TaskStatus.COMPLETED
            else:
                task.status = TaskStatus.FAILED
            
            result.mark_completed()
            
            self._emit_event("intelligence.task.completed", {
                "task_id": task.task_id,
                "result_id": result.result_id,
                "status": result.status.value,
            })
            
        except Exception as e:
            result.status = ResultStatus.FAILURE
            result.errors.append(str(e))
            task.status = TaskStatus.FAILED
            result.mark_completed()
        
        return result
    
    def _create_session(
        self,
        task: IntelligenceTask,
        context: IntelligenceContext | None = None,
    ) -> IntelligenceSession:
        """Create a new session for task execution."""
        session = IntelligenceSession(
            context_id=context.context_id if context else None,
            graph_id=context.graph_id if context else None,
            inference_session_id=context.inference_session_id if context else None,
            metadata=task.metadata.copy(),
        )
        session.add_task(task)
        
        self._active_sessions[session.session_id] = session
        
        self._emit_event("intelligence.session.started", {
            "session_id": session.session_id,
            "task_id": task.task_id,
        })
        
        return session
    
    def _execute_pipeline(
        self,
        task: IntelligenceTask,
        session: IntelligenceSession,
        context: IntelligenceContext | None = None,
    ) -> IntelligenceResult:
        """Execute the runtime pipeline."""
        pipeline = self._get_pipeline(task.task_type)
        
        if pipeline is None:
            return self._execute_default(task, session)
        
        self._emit_event("intelligence.pipeline.started", {
            "task_id": task.task_id,
            "pipeline_id": pipeline.pipeline_id,
        })
        
        result = self._executor.execute(
            task=task,
            pipeline=pipeline,
            session=session,
            context=context,
        )
        
        self._emit_event("intelligence.pipeline.completed", {
            "task_id": task.task_id,
            "pipeline_id": pipeline.pipeline_id,
        })
        
        return result
    
    def _execute_default(
        self,
        task: IntelligenceTask,
        session: IntelligenceSession,
    ) -> IntelligenceResult:
        """Execute task with default behavior."""
        result = IntelligenceResult(task_id=task.task_id)
        
        result.outputs = {
            "task_type": task.task_type,
            "objective": task.objective,
            "inputs_received": True,
        }
        
        return result
    
    def _get_pipeline(self, task_type: str) -> Pipeline | None:
        """Get pipeline for task type."""
        return self._pipeline_registry.get_pipeline(task_type)
    
    def register_pipeline(self, pipeline: Pipeline) -> bool:
        """
        Register a pipeline.
        
        Args:
            pipeline: Pipeline to register
            
        Returns:
            True if registered successfully
        """
        return self._pipeline_registry.register_pipeline(pipeline)
    
    def get_session(self, session_id: str) -> IntelligenceSession | None:
        """Get session by ID."""
        return self._active_sessions.get(session_id)
    
    def _emit_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Emit an event."""
        if self._event_emitter is None:
            return
        
        try:
            if hasattr(self._event_emitter, "emit"):
                self._event_emitter.emit(event_type, data)
        except Exception:
            pass
