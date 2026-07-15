# Orchestration Architecture

## Overview

The Orchestration layer is the deterministic coordination brain of FOOL Platform. It coordinates workflow execution without executing real agents, allowing the system to remain testable and predictable.

## Position in Architecture

```
FOOL Platform Architecture:

Standards ──► Contracts ──► Domain ──► Knowledge ──► Intelligence
                                                  ↓
                      ┌──────────────────────────┴────────────────────┐
                      │                                                   │
                  Platform                                             │
                      ↓                                                   │
         ┌────────────┴────────────┐                                    │
         │                         │                                    │
     Kernel                    Orchestration ◄──── Event Bus ◄──── Intelligence
         │                         │                      │
         └─────────────────────────┼──────────────────────┘
                                   ↓
                            Applications
```

## Core Principles

1. **Workflows are declarative** - Defined in YAML, not hardcoded
2. **Orchestration coordinates** - Does not perform intelligence
3. **Agents are referenced** - Not executed by orchestration
4. **Capabilities are validated** - Not implemented
5. **Policies are evaluated** - From workflow definitions
6. **State transitions are explicit** - Validated before application
7. **Every execution has an ID** - For traceability
8. **Decisions are explainable** - Rationale is recorded
9. **Events are emitted** - Through Event Bus when configured
10. **No business logic hardcoding** - Everything from contracts/workflows

## Components

### Registries

| Registry | Purpose | Source |
|----------|---------|--------|
| AgentRegistry | Agent type definitions | `agents.yaml` |
| CapabilityRegistry | Capability definitions | `capabilities.yaml` |
| WorkflowRegistry | Workflow definitions | `workflows/*.yaml` |
| PolicyRegistry | Policy extraction | From workflow definitions |

### State Management

- **WorkflowStateStore**: In-memory execution state
- **CheckpointStore**: State snapshots for recovery
- **StateTransitions**: Validated state transitions

### Policy Evaluation

| Evaluator | Purpose |
|-----------|---------|
| RetryPolicyEvaluator | Determines if step should retry |
| TimeoutPolicyEvaluator | Checks if step has timed out |
| FailurePolicyEvaluator | Decides workflow action on failure |
| TerminationPolicyEvaluator | Checks if workflow should terminate |

### Workflow Planner

- **Dependency Analysis**: Topological sorting
- **Cycle Detection**: Fails on cyclic dependencies
- **Agent Selection**: Chooses agents by explicit assignment or capability

### Workflow Engine

Coordinates:
- Workflow initialization
- Planning
- Step execution tracking
- State transitions
- Policy evaluation
- Event emission

## Event Types

Events emitted through Event Bus:

| Event | Trigger |
|-------|---------|
| `workflow.initialized` | Workflow execution created |
| `workflow.planned` | Steps analyzed and ordered |
| `workflow.step.ready` | Step ready to execute |
| `workflow.step.running` | Step execution started |
| `workflow.step.completed` | Step execution succeeded |
| `workflow.step.failed` | Step execution failed |
| `workflow.completed` | All steps completed |
| `workflow.failed` | Workflow failed |
| `workflow.cancelled` | Workflow cancelled |
| `workflow.terminated` | Workflow terminated |

## State Machines

### Workflow Execution Status

```
    CREATED
        ↓
    INITIALIZED
        ↓
      PLANNED
        ↓
      RUNNING
    ↙  ↓  ↘  ↓
WAITING  │  COMPLETED/FAILED
    ↘  ↓  ↙  CANCELLED/TERMINATED
      RUNNING
```

### Step Status

```
   PENDING
    ↙   ↘
BLOCKED  READY
    ↘   ↙
      RUNNING
   ↙  ↓  ↘
COMPLETED  FAILED
     SKIPPED
```

## Phase 2D: Agent Runtime Framework

Phase 2D will extend this orchestration layer with:

- Real agent instantiation
- Agent execution runtime
- Tool execution
- AI/LLM integration
- External API calls

Orchestration provides the skeleton; Phase 2D provides the muscles.

## Dependencies

```
fool_platform/orchestration
├── fool_platform/kernel       ✓
├── fool_platform/events      ✓
├── contracts/                ✓
├── standards/                ✓
├── domain/                   ✓
└── Python stdlib             ✓
```

## Not Dependencies

```
fool_platform/orchestration
├── fool_platform/intelligence  ✗
├── fool_platform/ai           ✗
├── fool_platform/apps         ✗
├── fool_platform/connectors   ✗
├── infrastructure/            ✗
└── databases/                 ✗
```

## Testing

- 52 orchestration tests
- Full test suite: 145 tests
- Deterministic behavior
- In-memory only
- Event Bus is optional
