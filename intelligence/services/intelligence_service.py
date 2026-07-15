"""
intelligence/services/intelligence_service.py

Intelligence Runtime Service.

Main service for intelligence operations.
"""
from typing import Any

from intelligence.models import IntelligenceTask, IntelligenceResult
from intelligence.context import IntelligenceContext
from intelligence.session import IntelligenceSession
from intelligence.runtime import IntelligenceRuntime
from intelligence.events import IntelligenceEventEmitter


class IntelligenceRuntimeService:
    """
    Main service for intelligence operations.
    
    Coordinates:
    - Task execution
    - Session management
    - Event emission
    
    NOTE: This is a coordinator, not an intelligence processor.
    No business logic here.
    """
    
    def __init__(
        self,
        runtime: IntelligenceRuntime | None = None,
        event_emitter: IntelligenceEventEmitter | None = None,
    ) -> None:
        """
        Initialize the service.
        
        Args:
            runtime: Optional intelligence runtime
            event_emitter: Optional event emitter
        """
        self._runtime = runtime or IntelligenceRuntime()
        self._event_emitter = event_emitter or IntelligenceEventEmitter()
    
    def execute(
        self,
        task: IntelligenceTask,
        context: IntelligenceContext | None = None,
    ) -> dict[str, Any]:
        """
        Execute an intelligence task.
        
        Args:
            task: Task to execute
            context: Optional context
            
        Returns:
            Execution result
        """
        result = self._runtime.execute_task(task, context)
        
        return {
            "success": result.is_successful(),
            "result_id": result.result_id,
            "task_id": result.task_id,
            "status": result.status.value,
            "outputs": result.outputs,
            "finding_count": len(result.findings),
            "artifact_count": len(result.artifacts),
            "recommendation_count": len(result.recommendations),
            "errors": result.errors,
        }
    
    def create_context(
        self,
        workflow_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> IntelligenceContext:
        """Create a new context."""
        return IntelligenceContext(
            workflow_id=workflow_id,
            metadata=metadata or {},
        )
    
    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get session by ID."""
        session = self._runtime.get_session(session_id)
        if session:
            return session.to_dict()
        return None
