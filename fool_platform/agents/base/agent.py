"""
fool_platform/agents/base/agent.py

Base Agent abstraction for FOOL Platform.

This module provides the abstract BaseAgent class that all agents
must extend. BaseAgent contains no intelligence logic.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from fool_platform.agents.base.agent_exceptions import (
    AgentCapabilityError,
    AgentError,
    AgentExecutionError,
    AgentInitializationError,
    AgentLifecycleError,
    AgentValidationError,
)
from fool_platform.agents.base.context import AgentContext
from fool_platform.agents.base.lifecycle import AgentLifecycleManager
from fool_platform.agents.base.memory import AgentMemory
from fool_platform.agents.base.models import (
    AgentCapability,
    AgentResult,
    AgentStatus,
    AgentTask,
)

if TYPE_CHECKING:
    from fool_platform.agents.base.events import AgentEventEmitter
    from fool_platform.agents.base.policies import AgentPolicyEvaluator


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    This class provides the common interface and lifecycle management.
    Subclasses MUST implement _execute() with specific logic.
    
    IMPORTANT: BaseAgent does NOT contain intelligence logic.
    It provides the execution framework only.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        version: str = "1.0.0",
        description: str = "",
        capabilities: list[AgentCapability] | None = None,
        event_emitter: "AgentEventEmitter | None" = None,
        policy_evaluator: "AgentPolicyEvaluator | None" = None,
    ) -> None:
        """
        Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for this agent
            name: Human-readable name
            version: Agent version
            description: Agent description
            capabilities: List of capabilities this agent provides
            event_emitter: Optional event emitter
            policy_evaluator: Optional policy evaluator
        """
        self._agent_id = agent_id
        self._name = name
        self._version = version
        self._description = description
        self._capabilities = capabilities or []
        self._status = AgentStatus.CREATED
        self._metadata: dict[str, Any] = {}
        self._memory: AgentMemory | None = None
        self._event_emitter = event_emitter
        self._policy_evaluator = policy_evaluator
        self._lifecycle = AgentLifecycleManager()

    @property
    def agent_id(self) -> str:
        """Get the agent ID."""
        return self._agent_id

    @property
    def name(self) -> str:
        """Get the agent name."""
        return self._name

    @property
    def version(self) -> str:
        """Get the agent version."""
        return self._version

    @property
    def description(self) -> str:
        """Get the agent description."""
        return self._description

    @property
    def capabilities(self) -> list[AgentCapability]:
        """Get the agent capabilities."""
        return self._capabilities.copy()

    @property
    def status(self) -> AgentStatus:
        """Get the current agent status."""
        return self._status

    @property
    def metadata(self) -> dict[str, Any]:
        """Get the agent metadata."""
        return self._metadata.copy()

    @property
    def memory(self) -> AgentMemory | None:
        """Get the agent memory."""
        return self._memory

    def initialize(self) -> None:
        """
        Initialize the agent.
        
        Sets up the agent for operation.
        
        Raises:
            AgentInitializationError: If initialization fails
        """
        if self._status != AgentStatus.CREATED:
            raise AgentInitializationError(
                f"Agent {self._agent_id} cannot be initialized from status {self._status.value}",
                agent_id=self._agent_id,
            )

        try:
            self._lifecycle.validate_transition(
                self._status, AgentStatus.INITIALIZED
            )
            self._do_initialize()
            self._status = AgentStatus.INITIALIZED
            self._emit_event("agent.initialized", {"agent_id": self._agent_id})
        except AgentLifecycleError as e:
            raise AgentInitializationError(
                str(e),
                agent_id=self._agent_id,
                cause=e,
            )

    def start(self) -> None:
        """
        Start the agent.
        
        Transitions the agent to running state.
        
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        if self._status == AgentStatus.CREATED:
            self.initialize()

        self._lifecycle.validate_transition(self._status, AgentStatus.RUNNING)
        self._status = AgentStatus.RUNNING
        self._emit_event("agent.started", {"agent_id": self._agent_id})

    def stop(self) -> None:
        """
        Stop the agent.
        
        Transitions the agent to stopped state.
        
        Raises:
            AgentLifecycleError: If transition is invalid
        """
        self._lifecycle.validate_transition(self._status, AgentStatus.STOPPED)
        self._status = AgentStatus.STOPPED
        self._emit_event("agent.stopped", {"agent_id": self._agent_id})

    def validate_task(self, task: AgentTask) -> list[str]:
        """
        Validate a task before execution.
        
        Args:
            task: The task to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors: list[str] = []

        if not task.task_id:
            errors.append("Task must have a task_id")

        if not task.objective:
            errors.append("Task must have an objective")

        if not task.task_type:
            errors.append("Task must have a task_type")

        return errors

    def can_handle(self, task: AgentTask) -> bool:
        """
        Check if this agent can handle the given task.
        
        Default implementation checks capability match.
        
        Args:
            task: The task to check
            
        Returns:
            True if agent can handle the task
        """
        if not self._capabilities:
            return True

        return any(
            cap.capability_id == task.task_type
            for cap in self._capabilities
        )

    def execute(self, task: AgentTask, context: AgentContext | None = None) -> AgentResult:
        """
        Execute a task.
        
        Manages lifecycle and delegates to _execute().
        
        Args:
            task: The task to execute
            context: Optional execution context
            
        Returns:
            AgentResult from execution
            
        Raises:
            AgentValidationError: If task is invalid
            AgentExecutionError: If execution fails
        """
        validation_errors = self.validate_task(task)
        if validation_errors:
            raise AgentValidationError(
                f"Task validation failed: {validation_errors}",
                agent_id=self._agent_id,
                validation_errors=validation_errors,
            )

        if not self.can_handle(task):
            raise AgentCapabilityError(
                f"Agent {self._agent_id} cannot handle task type {task.task_type}",
                agent_id=self._agent_id,
                capability_id=task.task_type,
            )

        if self._status not in (AgentStatus.INITIALIZED, AgentStatus.RUNNING):
            raise AgentLifecycleError(
                f"Agent must be initialized or running to execute tasks",
                agent_id=self._agent_id,
                current_status=self._status.value,
            )

        ctx = context or AgentContext.create(agent_id=self._agent_id)
        if task.task_id:
            ctx = ctx.with_task(task.task_id)

        self._emit_event(
            "agent.task.started",
            {"task_id": task.task_id, "agent_id": self._agent_id},
        )

        result = AgentResult(
            task_id=task.task_id,
            agent_id=self._agent_id,
            started_at=datetime.now(timezone.utc).isoformat(),
        )

        try:
            output = self._execute(task, ctx)

            result = AgentResult(
                result_id=result.result_id,
                task_id=task.task_id,
                agent_id=self._agent_id,
                status=result.status,
                outputs=output or {},
                started_at=result.started_at,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )

            self._emit_event(
                "agent.task.completed",
                {"task_id": task.task_id, "agent_id": self._agent_id},
            )

            return result

        except Exception as e:
            result = AgentResult(
                result_id=result.result_id,
                task_id=task.task_id,
                agent_id=self._agent_id,
                status=result.status,
                outputs={},
                errors=[str(e)],
                started_at=result.started_at,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )

            self._emit_event(
                "agent.task.failed",
                {"task_id": task.task_id, "agent_id": self._agent_id, "error": str(e)},
            )

            raise AgentExecutionError(
                str(e),
                agent_id=self._agent_id,
                task_id=task.task_id,
                cause=e,
            )

    @abstractmethod
    def _execute(self, task: AgentTask, context: AgentContext) -> dict[str, Any]:
        """
        Execute the task logic.
        
        MUST be implemented by subclasses.
        
        Args:
            task: The task to execute
            context: The execution context
            
        Returns:
            Task outputs as dictionary
        """
        raise NotImplementedError

    def get_capabilities(self) -> list[AgentCapability]:
        """
        Get the agent's capabilities.
        
        Returns:
            List of capabilities
        """
        return self.capabilities

    def get_status(self) -> AgentStatus:
        """
        Get the current agent status.
        
        Returns:
            Current status
        """
        return self.status

    def health_check(self) -> bool:
        """
        Check if the agent is healthy.
        
        Returns:
            True if agent is healthy
        """
        return self._status in (AgentStatus.INITIALIZED, AgentStatus.RUNNING)

    def _do_initialize(self) -> None:
        """
        Perform agent-specific initialization.
        
        Override in subclasses for custom initialization.
        """
        pass

    def _emit_event(self, event_type: str, data: dict[str, Any]) -> None:
        """
        Emit an event through the event emitter.
        
        Args:
            event_type: Type of event
            data: Event data
        """
        if self._event_emitter:
            try:
                self._event_emitter.emit(event_type, data)
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(agent_id={self._agent_id}, status={self._status.value})"
