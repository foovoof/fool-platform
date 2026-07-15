# Agent Base Module

Core abstractions for agent implementation.

## Components

### BaseAgent (`agent.py`)

Abstract base class that all agents must extend.

```python
from fool_platform.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def _execute(self, task, context):
        return {"result": "output"}
```

### Agent Exceptions (`agent_exceptions.py`)

Exception hierarchy for agent operations.

- `AgentError` - Base exception
- `AgentInitializationError` - Initialization failures
- `AgentValidationError` - Validation failures
- `AgentExecutionError` - Execution failures
- `AgentCapabilityError` - Capability issues
- `AgentLifecycleError` - Lifecycle violations
- `AgentContextError` - Context issues
- `AgentPolicyError` - Policy violations
- `AgentMemoryError` - Memory failures
- `AgentResultError` - Result validation failures

### Agent Context (`context.py`)

Execution context for task isolation.

```python
from fool_platform.agents.base import AgentContext

context = AgentContext.create(
    agent_id="agent-123",
    task_id="task-456",
)
```

### Agent Lifecycle (`lifecycle.py`)

State machine for agent lifecycle.

Valid states: CREATED → INITIALIZED → RUNNING → STOPPED/FAILED

### Agent Memory (`memory.py`)

In-memory storage for execution context.

```python
from fool_platform.agents.base import InMemoryAgentMemory

memory = InMemoryAgentMemory()
memory.set("key", "value")
```

### Agent Policies (`policies.py`)

Policy framework for agent behavior control.

```python
from fool_platform.agents.base import AgentPolicy, AgentPolicyEvaluator

policy = AgentPolicy(
    policy_name="restrictions",
    capability_restrictions=["restricted.cap"],
)
evaluator = AgentPolicyEvaluator([policy])
```

### Agent Events (`events.py`)

Event emission for observability.

Supported events:
- `agent.initialized`
- `agent.started`
- `agent.stopped`
- `agent.task.started`
- `agent.task.completed`
- `agent.task.failed`

### Validators (`validation.py`)

Task, result, and capability validation.

```python
from fool_platform.agents.base import AgentTaskValidator

result = AgentTaskValidator.validate(task)
if not result.is_valid:
    print(result.errors)
```

### ExampleAgent (`example_agent.py`)

Validates runtime integrity only.

- No AI
- No business logic
- Echoes task data in outputs

## Usage

```python
from fool_platform.agents.base import ExampleAgent, AgentTask

agent = ExampleAgent()
agent.initialize()
agent.start()

task = AgentTask(
    task_type="example.echo",
    objective="Test",
    inputs={"data": "value"},
)

result = agent.execute(task)
print(result.outputs)
```
