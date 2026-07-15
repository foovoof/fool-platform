"""
intelligence/services/execution_service.py

Execution Service.

Manages task execution.
"""
from typing import Any

from intelligence.models import IntelligenceTask, IntelligenceResult
from intelligence.context import IntelligenceContext
from intelligence.session import IntelligenceSession
from intelligence.runtime import IntelligenceRuntime


class ExecutionService:
    """
    Service for task execution management.
    
    Coordinates:
    - Task submission
    - Execution monitoring
    - Result retrieval
    """
    
    def __init__(self, runtime: IntelligenceRuntime | None = None) -> None:
        """Initialize the service."""
        self._runtime = runtime or IntelligenceRuntime()
    
    def submit_task(
        self,
        task: IntelligenceTask,
        context: IntelligenceContext | None = None,
    ) -> dict[str, Any]:
        """
        Submit a task for execution.
        
        Args:
            task: Task to execute
            context: Optional context
            
        Returns:
            Execution result
        """
        result = self._runtime.execute_task(task, context)
        
        return {
            "result_id": result.result_id,
            "task_id": result.task_id,
            "status": result.status.value,
            "success": result.is_successful(),
        }
    
    def get_result(self, result_id: str) -> dict[str, Any] | None:
        """Get result by ID."""
        for session in self._runtime._active_sessions.values():
            result = session.get_result(result_id)
            if result:
                return result.to_dict()
        return None
    
    def get_session_results(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        """Get all results for a session."""
        session = self._runtime.get_session(session_id)
        if session:
            return [r.to_dict() for r in session.results]
        return []
    
    def monitor_execution(
        self,
        task_id: str,
    ) -> dict[str, Any]:
        """
        Monitor task execution.
        
        Args:
            task_id: Task ID to monitor
            
        Returns:
            Execution status
        """
        for session in self._runtime._active_sessions.values():
            task = session.get_task(task_id)
            if task:
                return {
                    "task_id": task.task_id,
                    "status": task.status.value,
                    "created_at": task.created_at,
                }
        
        return {
            "task_id": task_id,
            "status": "not_found",
        }
