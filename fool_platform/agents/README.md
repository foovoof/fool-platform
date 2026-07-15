# Agent Runtime Framework

The Agent Runtime Framework provides the foundational execution layer for FOOL Platform agents.

## Purpose

Agent Runtime is part of the **Platform** layer, not a separate architectural layer.

```
FOOL Platform Architecture:

Standards ──► Contracts ──► Domain ──► Knowledge ──► Intelligence
    ↓
Platform (Kernel + Events + Orchestration + Agent Runtime)
    ↓
Applications
```

## What Agent Runtime Does

- **Agent Lifecycle Management**: Initialize, start, stop, and monitor agents
- **Task Execution**: Execute tasks through agents with validation
- **Capability Resolution**: Match tasks to agents by capability
- **Event Integration**: Emit events for observability
- **Policy Evaluation**: Enforce agent policies
- **Memory Management**: Provide in-memory context storage

## What Agent Runtime Does NOT Do

- ❌ **No Real Agents**: Phase 2D creates the framework only
- ❌ **No AI Execution**: No LLM calls or intelligence
- ❌ **No Tool Execution**: No external tools or connectors
- ❌ **No OSINT Logic**: No domain-specific agent behavior
- ❌ **No Business Logic**: Only framework code

## Dependency Direction

```
Platform Kernel
    ↓
Event Bus
    ↓
Orchestration
    ↓
Agent Runtime
```

**Important**: BaseAgent MUST NOT depend on:
- Orchestration
- Workflow Engine
- Planner
- Workflow State
- Workflow Registry

**Allowed**: Workflow Engine MAY use Agent Executor

## Architecture

```
fool_platform/agents/
├── __init__.py                    # Module exports
├── base/                          # Core abstractions
│   ├── __init__.py
│   ├── agent.py                   # BaseAgent abstract class
│   ├── agent_exceptions.py        # Exception hierarchy
│   ├── context.py                 # AgentContext
│   ├── lifecycle.py                # AgentLifecycleManager
│   ├── memory.py                  # AgentMemory interface
│   ├── models.py                  # Data models
│   ├── policies.py                # AgentPolicy
│   ├── validation.py              # Validators
│   ├── events.py                  # AgentEventEmitter
│   └── example_agent.py           # ExampleAgent (validation only)
├── runtime/                       # Execution runtime
│   ├── __init__.py
│   └── executor.py                # AgentExecutor
├── registry/                      # Registry definitions
│   ├── __init__.py
│   ├── registry_adapter.py        # Registry adapter
│   ├── agents.yaml                # Agent definitions
│   └── capabilities.yaml          # Capability definitions
└── tests/                         # Tests
    ├── __init__.py
    └── test_agents.py
```

## Core Concepts

### AgentTask

Input to agent execution.

```python
from fool_platform.agents.base import AgentTask

task = AgentTask(
    task_id="task-123",
    task_type="example.echo",
    objective="Process this data",
    inputs={"data": "value"},
)
```

### AgentResult

Output from agent execution.

```python
from fool_platform.agents.base import AgentResult

result = AgentResult(
    task_id="task-123",
    agent_id="agent-456",
    status=AgentResultStatus.SUCCESS,
    outputs={"processed": True},
)
```

### AgentContext

Execution context for isolation and traceability.

```python
from fool_platform.agents.base import AgentContext

context = AgentContext.create(
    agent_id="agent-456",
    task_id="task-123",
)
```

### BaseAgent

Abstract base class for all agents.

```python
from fool_platform.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def _execute(self, task, context):
        # Implement agent logic
        return {"result": "output"}
```

### AgentExecutor

Executes tasks through registered agents.

```python
from fool_platform.agents.runtime import AgentExecutor
from fool_platform.agents.base import ExampleAgent

executor = AgentExecutor()
executor.register_agent(ExampleAgent())

result = executor.execute(task, "example.echo.agent")
```

## ExampleAgent

ExampleAgent exists **only** to validate runtime integrity.

- No AI
- No business logic
- No external calls
- Echoes task data in outputs

## Phase 2D Scope

Phase 2D implements only the generic execution runtime:

- ✅ BaseAgent abstraction
- ✅ Agent lifecycle
- ✅ Agent task model
- ✅ Agent result model
- ✅ Agent context
- ✅ Agent capability model
- ✅ Agent validation
- ✅ Agent executor
- ✅ Agent memory interface
- ✅ Agent policy hooks
- ✅ Agent event integration
- ✅ Registry adapter
- ✅ ExampleAgent

Not implemented in Phase 2D:

- ❌ Research Agent
- ❌ Extraction Agent
- ❌ Investigation Agent
- ❌ Reporting Agent
- ❌ AI/LLM integration
- ❌ Tool execution
- ❌ Connectors
- ❌ OSINT logic

## Testing

Run tests:

```bash
pytest fool_platform/agents/tests/
```

Test coverage:

1. AgentTask creation
2. AgentResult creation
3. AgentCapability creation
4. AgentContext creation
5. Child context creation
6. BaseAgent abstract behavior
7. ExampleAgent initialization
8. ExampleAgent start
9. ExampleAgent execution
10. ExampleAgent result
11. Lifecycle valid transitions
12. Lifecycle invalid transitions
13. Task validation success
14. Task validation failure
15. Result validation success
16. Memory set/get/delete/clear
17. Policy allow
18. Policy deny
19. Event emitter without Event Bus
20. Event emitter with Event Bus
21. Executor register agent
22. Executor execute by id
23. Executor execute by capability
24. Executor handles failures
25. Registry adapter loads agents
26. Registry adapter loads capabilities
27. No tool execution
28. No connector execution
29. No AI imports
30. Architecture rules enforced

## Next Phase

**Phase 2D is complete.**

Next: **Phase 3 — Knowledge Foundation**

Phase 3 will implement the Knowledge layer for entity/relationship management.
