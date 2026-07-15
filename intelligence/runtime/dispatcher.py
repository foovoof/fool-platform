"""
intelligence/runtime/dispatcher.py

Runtime Dispatcher.

Dispatches tasks to appropriate handlers.
"""
from __future__ import annotations

from typing import Any, Callable

from intelligence.models import IntelligenceTask


class RuntimeDispatcher:
    """
    Dispatches tasks to appropriate handlers.
    
    The dispatcher does NOT process intelligence.
    It ONLY routes tasks to registered handlers.
    """
    
    def __init__(self) -> None:
        """Initialize the dispatcher."""
        self._handlers: dict[str, Callable] = {}
        self._default_handler: Callable | None = None
    
    def register_handler(
        self,
        task_type: str,
        handler: Callable,
    ) -> None:
        """
        Register a handler for a task type.
        
        Args:
            task_type: Task type to handle
            handler: Handler function
        """
        self._handlers[task_type] = handler
    
    def set_default_handler(self, handler: Callable) -> None:
        """
        Set the default handler.
        
        Args:
            handler: Default handler function
        """
        self._default_handler = handler
    
    def dispatch(
        self,
        task: IntelligenceTask,
        context: dict[str, Any] | None = None,
    ) -> Any:
        """
        Dispatch a task to its handler.
        
        Args:
            task: Task to dispatch
            context: Optional dispatch context
            
        Returns:
            Handler result
        """
        handler = self._handlers.get(task.task_type, self._default_handler)
        
        if handler is None:
            return {
                "error": f"No handler for task type: {task.task_type}",
                "task_id": task.task_id,
            }
        
        return handler(task, context)
    
    def get_handler(self, task_type: str) -> Callable | None:
        """Get handler for task type."""
        return self._handlers.get(task_type)
    
    def list_handlers(self) -> list[str]:
        """List registered task types."""
        return list(self._handlers.keys())
