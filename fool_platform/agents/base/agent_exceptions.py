"""
fool_platform/agents/base/agent_exceptions.py

Agent Runtime exceptions for FOOL Platform.

This module provides the exception hierarchy for the Agent Runtime Framework.
All agent-related errors inherit from AgentError.
"""


class AgentError(Exception):
    """Base exception for all agent-related errors."""

    def __init__(self, message: str, agent_id: str | None = None) -> None:
        super().__init__(message)
        self.agent_id = agent_id


class AgentInitializationError(AgentError):
    """Raised when agent initialization fails."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.cause = cause


class AgentValidationError(AgentError):
    """Raised when agent validation fails."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        validation_errors: list[str] | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.validation_errors = validation_errors or []


class AgentExecutionError(AgentError):
    """Raised when agent execution fails."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        task_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.task_id = task_id
        self.cause = cause


class AgentCapabilityError(AgentError):
    """Raised when capability validation or execution fails."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        capability_id: str | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.capability_id = capability_id


class AgentLifecycleError(AgentError):
    """Raised when agent lifecycle operation is invalid."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        current_status: str | None = None,
        target_status: str | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.current_status = current_status
        self.target_status = target_status


class AgentContextError(AgentError):
    """Raised when agent context operation fails."""

    def __init__(
        self,
        message: str,
        context_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.context_id = context_id


class AgentPolicyError(AgentError):
    """Raised when agent policy evaluation fails."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        policy_name: str | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.policy_name = policy_name


class AgentMemoryError(AgentError):
    """Raised when agent memory operation fails."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        key: str | None = None,
    ) -> None:
        super().__init__(message, agent_id)
        self.key = key


class AgentResultError(AgentError):
    """Raised when agent result validation fails."""

    def __init__(
        self,
        message: str,
        result_id: str | None = None,
        task_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.result_id = result_id
        self.task_id = task_id
