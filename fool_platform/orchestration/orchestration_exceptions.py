"""
fool_platform/orchestration/orchestration_exceptions.py

Dedicated exceptions for the Orchestration layer.
"""


class OrchestrationError(Exception):
    """Base exception for all orchestration errors."""
    pass


class WorkflowNotFoundError(OrchestrationError):
    """Raised when a workflow is not found in the registry."""

    def __init__(
        self,
        workflow_id: str,
        message: str | None = None,
    ) -> None:
        self.workflow_id = workflow_id
        msg = message or f"Workflow not found: {workflow_id}"
        super().__init__(msg)


class WorkflowValidationError(OrchestrationError):
    """Raised when workflow validation fails."""

    def __init__(
        self,
        workflow_id: str,
        errors: list[str],
        message: str | None = None,
    ) -> None:
        self.workflow_id = workflow_id
        self.errors = errors
        msg = message or f"Workflow validation failed for {workflow_id}: {errors}"
        super().__init__(msg)


class WorkflowStateError(OrchestrationError):
    """Raised when workflow state is invalid or unexpected."""

    def __init__(
        self,
        execution_id: str,
        message: str,
        current_state: str | None = None,
    ) -> None:
        self.execution_id = execution_id
        self.current_state = current_state
        super().__init__(f"Workflow state error for {execution_id}: {message}")


class WorkflowTransitionError(WorkflowStateError):
    """Raised when a workflow state transition is invalid."""

    def __init__(
        self,
        execution_id: str,
        current_status: str,
        target_status: str,
    ) -> None:
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(
            execution_id=execution_id,
            message=f"Invalid transition from {current_status} to {target_status}",
            current_state=current_status,
        )


class WorkflowPlanningError(OrchestrationError):
    """Raised when workflow planning fails."""

    def __init__(
        self,
        workflow_id: str,
        reason: str,
        details: list[str] | None = None,
    ) -> None:
        self.workflow_id = workflow_id
        self.reason = reason
        self.details = details or []
        super().__init__(f"Workflow planning failed for {workflow_id}: {reason}")


class AgentRegistryError(OrchestrationError):
    """Raised when agent registry operations fail."""

    def __init__(
        self,
        message: str,
        agent_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        self.agent_id = agent_id
        self.cause = cause
        super().__init__(message)


class CapabilityRegistryError(OrchestrationError):
    """Raised when capability registry operations fail."""

    def __init__(
        self,
        message: str,
        capability_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        self.capability_id = capability_id
        self.cause = cause
        super().__init__(message)


class PolicyEvaluationError(OrchestrationError):
    """Raised when policy evaluation fails."""

    def __init__(
        self,
        policy_type: str,
        reason: str,
        execution_id: str | None = None,
    ) -> None:
        self.policy_type = policy_type
        self.reason = reason
        self.execution_id = execution_id
        super().__init__(f"Policy evaluation failed ({policy_type}): {reason}")


class CheckpointError(OrchestrationError):
    """Raised when checkpoint operations fail."""

    def __init__(
        self,
        message: str,
        checkpoint_id: str | None = None,
        execution_id: str | None = None,
    ) -> None:
        self.checkpoint_id = checkpoint_id
        self.execution_id = execution_id
        super().__init__(message)


class ExecutionContextError(OrchestrationError):
    """Raised when execution context operations fail."""

    def __init__(
        self,
        message: str,
        execution_id: str | None = None,
    ) -> None:
        self.execution_id = execution_id
        super().__init__(message)
