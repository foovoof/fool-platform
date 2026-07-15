# Agent Runtime Architecture

## Overview

Agent Runtime is the execution framework for FOOL Platform agents. It provides the foundational abstractions for agent lifecycle, task execution, and capability management.

**Important**: Agent Runtime belongs to the **Platform** layer, not a separate architectural layer.

## Architecture Position

```
FOOL Platform Architecture:

Standards ──► Contracts ──► Domain ──► Knowledge ──► Intelligence
    ↓
┌─────────────────────────────────────────────────────┐
│                     Platform                          │
│  ┌───────────┐ ┌───────────┐ ┌───────────────────┐  │
│  │  Kernel   │ │  Events   │ │  Orchestration    │  │
│  └───────────┘ └───────────┘ └───────────────────┘  │
│  ┌─────────────────────────────────────────────────┤
│  │              Agent Runtime                       │
│  └─────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────┘
    ↓
Applications
```

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

## Architectural Rules

### Allowed Dependencies

✅ Agent Runtime → Platform Kernel
✅ Agent Runtime → Event Bus
✅ Agent Runtime → Contracts
✅ Workflow Engine → Agent Executor

### Forbidden Dependencies

❌ BaseAgent → Orchestration
❌ BaseAgent → Workflow Engine
❌ BaseAgent → Planner
❌ BaseAgent → Workflow State
❌ BaseAgent → Workflow Registry

### Core Principle

**Agent Runtime must remain orchestration-agnostic.**

Agents should be reusable outside orchestration contexts.

## Components

### Registries

| Registry | Purpose | Source |
|----------|---------|--------|
| AgentRegistry | Agent type definitions | `agents.yaml` |
| CapabilityRegistry | Capability definitions | `capabilities.yaml` |

### Core Abstractions

| Component | Purpose |
|-----------|---------|
| BaseAgent | Abstract base for all agents |
| AgentContext | Execution context for isolation |
| AgentTask | Task input model |
| AgentResult | Task output model |
| AgentCapability | Capability definition |
| AgentLifecycleManager | State machine management |

### Execution

| Component | Purpose |
|-----------|---------|
| AgentExecutor | Task execution engine |
| AgentTaskValidator | Task validation |
| AgentResultValidator | Result validation |

### Support

| Component | Purpose |
|-----------|---------|
| AgentMemory | In-memory storage |
| AgentPolicy | Behavior control rules |
| AgentPolicyEvaluator | Policy decision engine |
| AgentEventEmitter | Event emission |

## State Machines

### Agent Lifecycle

```
CREATED
    ↓
INITIALIZED
    ↓
RUNNING
 ↙    ↘
STOPPED  FAILED
```

### Agent Task Status

```
PENDING
    ↓
RUNNING
    ↓
COMPLETED / FAILED / CANCELLED
```

## Event Types

Events emitted through Event Bus:

| Event | Trigger |
|-------|---------|
| `agent.initialized` | Agent initialized |
| `agent.started` | Agent started |
| `agent.stopped` | Agent stopped |
| `agent.task.started` | Task execution started |
| `agent.task.completed` | Task execution completed |
| `agent.task.failed` | Task execution failed |

## Phase 2D Scope

Phase 2D implements the generic execution runtime framework only.

### Implemented

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

### NOT Implemented

- ❌ Research Agent
- ❌ Extraction Agent
- ❌ Investigation Agent
- ❌ Reporting Agent
- ❌ AI/LLM integration
- ❌ Tool execution
- ❌ Connectors
- ❌ OSINT logic

## ExampleAgent

ExampleAgent exists **only** to validate runtime integrity.

It:
- Accepts AgentTask
- Returns AgentResult
- Echoes objective and inputs into outputs
- **No AI**
- **No business logic**
- **No external calls**

## Testing

Architecture tests verify:

1. `fool_platform/agents` must not import `ai`
2. `fool_platform/agents` must not import `connectors`
3. `fool_platform/agents` must not import `infrastructure`
4. `fool_platform/agents` must not import `applications`
5. `fool_platform/domain` must not import `fool_platform/agents`

## Dependencies

```
fool_platform/agents
├── fool_platform/kernel ✓
├── fool_platform/events ✓
├── contracts/ ✓
├── standards/ ✓
└── Python stdlib ✓
```

## Not Dependencies

```
fool_platform/agents
├── fool_platform/orchestration ✗
├── fool_platform/intelligence ✗
├── fool_platform/ai ✗
├── fool_platform/apps ✗
├── fool_platform/connectors ✗
├── infrastructure/ ✗
└── databases/ ✗
```

## Next Phase

Phase 3: Knowledge Foundation
