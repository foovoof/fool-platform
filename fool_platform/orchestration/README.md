# Orchestration Layer

The Orchestration layer coordinates workflow execution in FOOL Platform without executing real agents.

## Purpose

Orchestration is the deterministic coordination brain of FOOL Platform. It:

- Coordinates workflows declaratively
- Validates dependencies
- Evaluates policies
- Tracks state
- Emits events
- Explains decisions

## What Orchestration Does NOT Do

- Execute real agents
- Perform AI/LLM calls
- Execute tools
- Access external APIs
- Persist data
- Run background schedulers

## Architecture

```
fool_platform/orchestration/
├── __init__.py
├── orchestration_exceptions.py    # Dedicated exceptions
├── models.py                     # Workflow/Step execution models
├── execution_context.py           # Execution context
├── registry/                     # Registries
│   ├── __init__.py
│   ├── agent_registry.py         # Agent definitions
│   ├── capability_registry.py    # Capability definitions
│   ├── workflow_registry.py      # Workflow definitions
│   └── policy_registry.py         # Policy extraction
├── state/                        # State management
│   ├── __init__.py
│   ├── workflow_state_store.py   # In-memory state store
│   ├── checkpoint.py             # Checkpoint management
│   └── state_transitions.py      # Transition validation
├── policies/                      # Policy evaluation
│   ├── __init__.py
│   ├── retry_policy.py           # Retry evaluation
│   ├── timeout_policy.py         # Timeout evaluation
│   ├── failure_policy.py         # Failure evaluation
│   └── termination_policy.py     # Termination evaluation
├── planner/                       # Workflow planning
│   ├── __init__.py
│   ├── workflow_planner.py       # Dependency analysis
│   └── agent_selector.py         # Agent selection
├── engine/                        # Workflow engine
│   ├── __init__.py
│   ├── workflow_engine.py        # Main engine
│   ├── step_runner.py            # Step state management
│   └── transition_evaluator.py   # Transition evaluation
└── tests/
    └── test_orchestration.py     # Comprehensive tests
```

## Key Concepts

### Workflow Execution Status

- `CREATED` → `INITIALIZED` → `PLANNED` → `RUNNING` → `COMPLETED/FAILED/CANCELLED/TERMINATED`

### Step Status

- `PENDING` → `READY` → `RUNNING` → `COMPLETED/FAILED/SKIPPED/BLOCKED`

### Event Bus Integration

Events are emitted for:
- `workflow.initialized`
- `workflow.planned`
- `workflow.step.ready`
- `workflow.step.running`
- `workflow.step.completed`
- `workflow.step.failed`
- `workflow.completed`
- `workflow.failed`
- `workflow.cancelled`
- `workflow.terminated`

## Usage Example

```python
from fool_platform.orchestration.engine import WorkflowEngine
from fool_platform.orchestration.registry import WorkflowRegistry

# Create registry and engine
workflow_registry = WorkflowRegistry(Path("workflows"))
engine = WorkflowEngine(workflow_registry=workflow_registry)

# Initialize workflow
execution = engine.initialize_workflow(
    workflow_id="wf.investigation.v1",
    input_payload={"case_id": "case123"},
)

# Plan and execute
execution = engine.plan_workflow(execution.execution_id)
runnable_steps = engine.get_runnable_steps(execution.execution_id)

# Mark steps complete
for step_id in runnable_steps:
    engine.mark_step_completed(execution.execution_id, step_id)

# Get summary
summary = engine.get_execution_summary(execution.execution_id)
```

## Testing

52 comprehensive tests covering:
- Models and exceptions
- Registries
- State management
- Policy evaluation
- Workflow planning
- Step runner
- Workflow engine

## Phase 2D: Agent Runtime Framework

Phase 2D will implement actual agent execution using this orchestration layer.
