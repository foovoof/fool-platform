"""
fool_platform/agents/__init__.py

Agent Runtime Framework for FOOL Platform.

This module provides the foundational Agent Runtime Framework for FOOL Platform.
Phase 2D creates the generic execution framework used by future agents.

This phase does NOT implement intelligence.
This phase implements:
- BaseAgent abstraction
- Agent lifecycle
- Agent task model
- Agent result model
- Agent context
- Agent capability model
- Agent validation
- Agent executor
- Agent memory interface
- Agent policy hooks
- Agent event integration
- Registry adapter
- ExampleAgent
"""
from fool_platform.agents.base import (
    BaseAgent,
    ExampleAgent,
    AgentContext,
    AgentTask,
    AgentResult,
    AgentCapability,
    AgentEventEmitter,
)
from fool_platform.agents.runtime import AgentExecutor

__all__ = [
    "BaseAgent",
    "ExampleAgent",
    "AgentExecutor",
    "AgentContext",
    "AgentTask",
    "AgentResult",
    "AgentCapability",
    "AgentEventEmitter",
]
