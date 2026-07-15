"""
fool_platform/orchestration/__init__.py

Orchestration layer for FOOL Platform.

Provides workflow coordination without real agent execution.
"""

from fool_platform.orchestration.execution_context import ExecutionContext
from fool_platform.orchestration.models import (
    ExecutionSummary,
    OrchestrationDecision,
    StepStatus,
    WorkflowExecution,
    WorkflowExecutionStatus,
    WorkflowStepExecution,
)
from fool_platform.orchestration.orchestration_exceptions import (
    AgentRegistryError,
    CapabilityRegistryError,
    CheckpointError,
    ExecutionContextError,
    OrchestrationError,
    PolicyEvaluationError,
    WorkflowNotFoundError,
    WorkflowPlanningError,
    WorkflowStateError,
    WorkflowTransitionError,
    WorkflowValidationError,
)

__all__ = [
    "ExecutionContext",
    "ExecutionSummary",
    "OrchestrationDecision",
    "OrchestrationError",
    "AgentRegistryError",
    "CapabilityRegistryError",
    "CheckpointError",
    "ExecutionContextError",
    "PolicyEvaluationError",
    "StepStatus",
    "WorkflowExecution",
    "WorkflowExecutionStatus",
    "WorkflowNotFoundError",
    "WorkflowPlanningError",
    "WorkflowStateError",
    "WorkflowStepExecution",
    "WorkflowTransitionError",
    "WorkflowValidationError",
]
