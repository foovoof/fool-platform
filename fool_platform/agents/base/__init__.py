"""
fool_platform/agents/base/__init__.py

Agent Base Module for FOOL Platform.

Provides core abstractions for agent implementation.
"""
from fool_platform.agents.base.agent import BaseAgent
from fool_platform.agents.base.agent_exceptions import (
    AgentCapabilityError,
    AgentContextError,
    AgentError,
    AgentExecutionError,
    AgentInitializationError,
    AgentLifecycleError,
    AgentMemoryError,
    AgentPolicyError,
    AgentResultError,
    AgentValidationError,
)
from fool_platform.agents.base.context import AgentContext
from fool_platform.agents.base.example_agent import ExampleAgent
from fool_platform.agents.base.lifecycle import AgentLifecycleManager
from fool_platform.agents.base.memory import AgentMemory, InMemoryAgentMemory
from fool_platform.agents.base.models import (
    AgentCapability,
    AgentExecutionRecord,
    AgentResult,
    AgentResultStatus,
    AgentStatus,
    AgentTask,
    AgentTaskStatus,
)
from fool_platform.agents.base.policies import (
    AgentPolicy,
    AgentPolicyDecision,
    AgentPolicyDecisionResult,
    AgentPolicyEvaluator,
)
from fool_platform.agents.base.validation import (
    AgentCapabilityValidator,
    AgentResultValidator,
    AgentTaskValidator,
    ValidationResult,
)
from fool_platform.agents.base.events import AgentEventEmitter

__all__ = [
    # Core
    "BaseAgent",
    # Exceptions
    "AgentError",
    "AgentInitializationError",
    "AgentValidationError",
    "AgentExecutionError",
    "AgentCapabilityError",
    "AgentLifecycleError",
    "AgentContextError",
    "AgentPolicyError",
    "AgentMemoryError",
    "AgentResultError",
    # Models
    "AgentTask",
    "AgentResult",
    "AgentCapability",
    "AgentExecutionRecord",
    "AgentStatus",
    "AgentTaskStatus",
    "AgentResultStatus",
    # Context
    "AgentContext",
    # Lifecycle
    "AgentLifecycleManager",
    # Memory
    "AgentMemory",
    "InMemoryAgentMemory",
    # Policies
    "AgentPolicy",
    "AgentPolicyDecision",
    "AgentPolicyDecisionResult",
    "AgentPolicyEvaluator",
    # Validation
    "AgentTaskValidator",
    "AgentResultValidator",
    "AgentCapabilityValidator",
    "ValidationResult",
    # Events
    "AgentEventEmitter",
    # Example
    "ExampleAgent",
]
