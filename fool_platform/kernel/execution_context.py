"""
platform/kernel/execution_context.py

Execution context for operation-scoped information.
"""
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ExecutionContext:
    """
    Immutable execution context for tracking operation execution.
    
    Execution contexts form a hierarchy, tracking the lineage of
    operations from initial request through completion.
    """
    context_id: str
    parent_id: str | None
    operation_name: str
    started_at: str
    correlation_id: str | None = None
    causality_id: str | None = None
    metadata: dict = field(default_factory=dict)
    
    @classmethod
    def create(
        cls,
        operation_name: str,
        parent_id: str | None = None,
        correlation_id: str | None = None,
        causality_id: str | None = None,
        metadata: dict | None = None,
    ) -> "ExecutionContext":
        """Factory method to create a new execution context."""
        return cls(
            context_id=str(uuid4()),
            parent_id=parent_id,
            operation_name=operation_name,
            started_at=datetime.now(timezone.utc).isoformat(),
            correlation_id=correlation_id,
            causality_id=causality_id,
            metadata=metadata or {},
        )
    
    def child(self, operation_name: str) -> "ExecutionContext":
        """Create a child execution context for a nested operation."""
        return ExecutionContext.create(
            operation_name=operation_name,
            parent_id=self.context_id,
            correlation_id=self.correlation_id,
            causality_id=self.context_id,
            metadata=self.metadata.copy(),
        )
    
    def with_correlation(self, correlation_id: str) -> "ExecutionContext":
        """Return a new context with correlation ID set."""
        return ExecutionContext(
            context_id=self.context_id,
            parent_id=self.parent_id,
            operation_name=self.operation_name,
            started_at=self.started_at,
            correlation_id=correlation_id,
            causality_id=self.causality_id,
            metadata=self.metadata,
        )


# Context variable for current execution context
_current_context: ContextVar[ExecutionContext | None] = ContextVar(
    "current_context", default=None
)


def get_current_context() -> ExecutionContext | None:
    """Get the current execution context from the context variable."""
    return _current_context.get()


def set_current_context(ctx: ExecutionContext | None) -> None:
    """Set the current execution context in the context variable."""
    _current_context.set(ctx)


class ExecutionContextManager:
    """
    Manages execution context with automatic cleanup.
    
    Use as a context manager to ensure proper cleanup of
    the current context.
    """
    
    def __init__(self, context: ExecutionContext) -> None:
        self._context = context
        self._previous: ExecutionContext | None = None
    
    def __enter__(self) -> ExecutionContext:
        self._previous = get_current_context()
        set_current_context(self._context)
        return self._context
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        set_current_context(self._previous)


__all__ = [
    "ExecutionContext",
    "ExecutionContextManager",
    "get_current_context",
    "set_current_context",
]
