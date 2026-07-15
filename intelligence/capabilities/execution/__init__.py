"""
intelligence/capabilities/execution/__init__.py

Capability Execution Components.

Handles capability execution and dispatching.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from intelligence.capabilities.models import (
    CapabilityTask,
    CapabilityResult,
    CapabilityDefinition,
    CapabilityType,
    CapabilityStatus,
    CapabilityExecutionRecord,
)
from intelligence.capabilities.agents import AgentFactory
from intelligence.capabilities.registry import CapabilityRegistry


class CapabilityExecutor:
    """
    Executes capability tasks.
    
    Responsibilities:
    - Validate task
    - Select agent
    - Execute through Agent Runtime
    - Collect results
    """
    
    def __init__(self) -> None:
        """Initialize executor."""
        self._agent_factory = AgentFactory()
    
    def execute(self, task: CapabilityTask) -> CapabilityResult:
        """
        Execute a capability task.
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        result = CapabilityResult(
            task_id=task.task_id,
            capability_id=task.capability_id,
            capability_type=task.capability_type,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        
        try:
            agent_type = task.capability_type.value
            agent = self._agent_factory.create(agent_type)
            
            if not agent:
                result.status = CapabilityStatus.FAILED
                result.errors.append(f"No agent found for type: {agent_type}")
                return result
            
            result = agent.execute(task)
            result.completed_at = datetime.now(timezone.utc).isoformat()
            
        except Exception as e:
            result.status = CapabilityStatus.FAILED
            result.errors.append(str(e))
        
        return result


class CapabilityDispatcher:
    """
    Dispatches capability tasks to appropriate executors.
    
    Responsibilities:
    - Resolve capability
    - Validate task
    - Select executor
    - Route execution
    """
    
    def __init__(
        self,
        registry: CapabilityRegistry | None = None,
    ) -> None:
        """Initialize dispatcher."""
        self._registry = registry
        self._executor = CapabilityExecutor()
        self._handlers: dict[CapabilityType, callable] = {}
    
    def register_handler(
        self,
        capability_type: CapabilityType,
        handler: callable,
    ) -> None:
        """Register a custom handler for a capability type."""
        self._handlers[capability_type] = handler
    
    def dispatch(self, task: CapabilityTask) -> CapabilityResult:
        """
        Dispatch a task for execution.
        
        Args:
            task: Task to dispatch
            
        Returns:
            Execution result
        """
        if not self._validate_task(task):
            return CapabilityResult(
                task_id=task.task_id,
                capability_id=task.capability_id,
                capability_type=task.capability_type,
                status=CapabilityStatus.FAILED,
                errors=["Task validation failed"],
            )
        
        handler = self._handlers.get(task.capability_type)
        if handler:
            return handler(task)
        
        return self._executor.execute(task)
    
    def _validate_task(self, task: CapabilityTask) -> bool:
        """Validate task before dispatch."""
        if not task.task_id:
            return False
        if not task.capability_type:
            return False
        return True


class CapabilityResolver:
    """
    Resolves capabilities and selects appropriate agents.
    
    Responsibilities:
    - Resolve capability by ID or type
    - Validate capability compatibility
    - Select appropriate agent
    """
    
    def __init__(
        self,
        registry: CapabilityRegistry | None = None,
    ) -> None:
        """Initialize resolver."""
        self._registry = registry
    
    def resolve_by_id(self, capability_id: str) -> CapabilityDefinition | None:
        """Resolve capability by ID."""
        if self._registry:
            return self._registry.get(capability_id)
        return None
    
    def resolve_by_type(
        self,
        capability_type: CapabilityType,
    ) -> CapabilityDefinition | None:
        """Resolve capability by type."""
        if self._registry:
            return self._registry.get_by_type(capability_type)
        return None
    
    def resolve_agent_type(self, capability_type: CapabilityType) -> str:
        """Resolve agent type for capability."""
        return capability_type.value


@dataclass
class ExecutionContext:
    """Context for capability execution."""
    context_id: str = field(default_factory=lambda: str(uuid4()))
    task: CapabilityTask | None = None
    capability: CapabilityDefinition | None = None
    agent_id: str | None = None
    session_id: str | None = None
    result: CapabilityResult | None = None
    record: CapabilityExecutionRecord | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ExecutionManager:
    """
    Manages capability execution lifecycle.
    
    Responsibilities:
    - Create execution context
    - Track execution records
    - Manage execution state
    """
    
    def __init__(self) -> None:
        """Initialize manager."""
        self._contexts: dict[str, ExecutionContext] = {}
        self._records: list[CapabilityExecutionRecord] = []
    
    def create_context(
        self,
        task: CapabilityTask,
        capability: CapabilityDefinition | None = None,
    ) -> ExecutionContext:
        """Create execution context."""
        context = ExecutionContext(
            task=task,
            capability=capability,
        )
        self._contexts[context.context_id] = context
        return context
    
    def create_record(self, task: CapabilityTask) -> CapabilityExecutionRecord:
        """Create execution record."""
        record = CapabilityExecutionRecord(
            task_id=task.task_id,
            capability_id=task.capability_id,
            capability_type=task.capability_type,
            inputs=task.inputs,
            parameters=task.parameters,
        )
        self._records.append(record)
        return record
    
    def update_record(
        self,
        record_id: str,
        result_id: str | None = None,
        status: CapabilityStatus | None = None,
    ) -> None:
        """Update execution record."""
        for record in self._records:
            if record.record_id == record_id:
                if result_id:
                    record.result_id = result_id
                if status:
                    record.status = status
                if status == CapabilityStatus.COMPLETED:
                    record.completed_at = datetime.now(timezone.utc).isoformat()
                break
    
    def get_records(self) -> list[CapabilityExecutionRecord]:
        """Get all execution records."""
        return self._records.copy()
    
    def get_record(self, record_id: str) -> CapabilityExecutionRecord | None:
        """Get execution record by ID."""
        for record in self._records:
            if record.record_id == record_id:
                return record
        return None
