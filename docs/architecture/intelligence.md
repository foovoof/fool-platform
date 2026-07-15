# Intelligence Runtime Architecture

## Overview

The Intelligence Runtime Foundation (Phase 4A) provides the execution layer that transforms validated Knowledge and Deterministic Inference into structured Intelligence workflows.

**IMPORTANT**: This phase implements only the runtime. No Intelligence capabilities exist yet.

## Position in Architecture

```
Canonical Architecture:
    Standards
        ↓
    Contracts
        ↓
    Domain
        ↓
    Knowledge
        ↓
    Intelligence (THIS PHASE)
        ↓
    Platform
        ↓
    Applications

Completed Phases:
    ✅ Phase 1 — Core Foundation
    ✅ Phase 2A — Platform Kernel
    ✅ Phase 2B — Event Bus
    ✅ Phase 2C — Orchestration
    ✅ Phase 2D — Agent Runtime
    ✅ Phase 3A — Knowledge Graph
    ✅ Phase 3B — Deterministic Inference
    
Current Phase:
    PHASE 4A — Intelligence Runtime Foundation
    
Next Phase:
    Phase 4B — Intelligence Capabilities Foundation
```

## Architectural Principles

### Allowed Dependencies

The Intelligence layer MAY depend on:

- ✅ Standards
- ✅ Contracts
- ✅ Domain
- ✅ Knowledge
- ✅ Knowledge/Inference
- ✅ Agents
- ✅ Platform/Events
- ✅ Platform/Orchestration Interfaces
- ✅ Platform/Kernel
- ✅ Python Standard Library

### Forbidden Dependencies

The Intelligence layer MUST NOT depend on:

- ❌ Applications
- ❌ Web/UI
- ❌ Connectors
- ❌ Databases
- ❌ External APIs
- ❌ AI/LLM
- ❌ Embeddings
- ❌ Vector Search
- ❌ Cyber Intelligence
- ❌ Threat Intelligence
- ❌ Infrastructure

## Core Components

### 1. Intelligence Models

**Location**: `intelligence/models/`

**Purpose**: Define core data structures

```python
# IntelligenceTask - Primary unit of work
@dataclass
class IntelligenceTask:
    task_id: str
    task_type: str
    objective: str
    inputs: dict[str, Any]
    metadata: dict[str, Any]
    trace_id: str | None
    correlation_id: str | None
    created_at: str
    status: TaskStatus

# IntelligenceResult - Task execution result
@dataclass
class IntelligenceResult:
    result_id: str
    task_id: str
    status: ResultStatus
    outputs: dict[str, Any]
    findings: list[IntelligenceFinding]
    artifacts: list[IntelligenceArtifact]
    evidence: list[str]
    recommendations: list[dict]
    warnings: list[str]
    errors: list[str]

# IntelligenceFinding - Analysis finding
@dataclass
class IntelligenceFinding:
    finding_id: str
    finding_type: FindingType
    title: str
    description: str
    evidence_refs: list[str]
    confidence: float
    source_task_id: str | None

# IntelligenceArtifact - Processing output
@dataclass
class IntelligenceArtifact:
    artifact_id: str
    artifact_type: ArtifactType
    content: Any
    name: str
    source_task_id: str | None
```

### 2. Intelligence Context

**Location**: `intelligence/context.py`

**Purpose**: Provide execution context

```python
@dataclass
class IntelligenceContext:
    context_id: str
    workflow_id: str | None
    execution_id: str | None
    session_id: str | None
    graph_id: str | None
    inference_session_id: str | None
    agent_execution_id: str | None
    parent_context_id: str | None
    metadata: dict[str, Any]
```

**Features**:
- Child context creation
- Event context conversion
- Hierarchical context support

### 3. Intelligence Session

**Location**: `intelligence/session.py`

**Purpose**: Manage execution lifecycle

```python
@dataclass
class IntelligenceSession:
    session_id: str
    context_id: str | None
    tasks: list[IntelligenceTask]
    results: list[IntelligenceResult]
    findings: list[IntelligenceFinding]
    artifacts: list[IntelligenceArtifact]
    execution_history: list[dict]
    status: str
```

**Features**:
- Task tracking
- Result aggregation
- Finding collection
- Execution history

### 4. Intelligence Runtime

**Location**: `intelligence/runtime/`

**Purpose**: Orchestrate execution

```python
class IntelligenceRuntime:
    def execute_task(
        self,
        task: IntelligenceTask,
        context: IntelligenceContext | None = None,
    ) -> IntelligenceResult
```

**Responsibilities**:
- Receive intelligence task
- Validate task
- Create session
- Execute runtime pipeline
- Invoke Agent Runtime (delegation)
- Consume Knowledge Services (delegation)
- Consume Inference Services (delegation)
- Aggregate results
- Return IntelligenceResult

**Runtime MUST NOT**:
- Perform intelligence logic
- Make autonomous decisions
- Access external resources

### 5. Pipeline Model

**Location**: `intelligence/pipeline/`

**Purpose**: Define execution workflows

```python
@dataclass
class Pipeline:
    pipeline_id: str
    name: str
    task_type: str
    steps: list[PipelineStep]
    metadata: dict[str, Any]

@dataclass
class PipelineStep:
    step_id: str
    name: str
    step_type: str
    handler: Callable | None
    inputs: dict[str, Any]
    order: int
    required: bool
```

**Features**:
- Sequential execution
- Deterministic execution
- Validation
- Checkpoints
- Execution reports

### 6. Validation

**Location**: `intelligence/validation/`

**Purpose**: Validate runtime components

```python
class RuntimeValidator:
    def validate_task(self, task: IntelligenceTask) -> ValidationResult
    def validate_context(self, context: IntelligenceContext) -> ValidationResult
    def validate_session(self, session: IntelligenceSession) -> ValidationResult
    def validate_pipeline(self, pipeline: Pipeline) -> ValidationResult
    def validate_contract_compatibility(self, task, contract) -> ValidationResult
```

### 7. Events

**Location**: `intelligence/events/`

**Purpose**: Emit runtime events

```python
class IntelligenceEventEmitter:
    def emit_session_started(self, session_id, task_id) -> bool
    def emit_session_completed(self, session_id, result_id) -> bool
    def emit_task_started(self, task_id, session_id) -> bool
    def emit_task_completed(self, task_id, result_id, status) -> bool
    def emit_pipeline_started(self, task_id, pipeline_id) -> bool
    def emit_pipeline_completed(self, task_id, pipeline_id) -> bool
    def emit_finding_generated(self, finding_id, task_id) -> bool
```

**Event Types**:
- `intelligence.session.started`
- `intelligence.session.completed`
- `intelligence.task.started`
- `intelligence.task.completed`
- `intelligence.pipeline.started`
- `intelligence.pipeline.completed`
- `intelligence.finding.generated`

**Note**: Event Bus integration is optional.

### 8. Services

**Location**: `intelligence/services/`

**Purpose**: Coordinate runtime components

```
IntelligenceRuntimeService  → Main service
PipelineService              → Pipeline management
SessionService              → Session management
FindingService              → Finding management
ArtifactService             → Artifact management
ExecutionService            → Execution management
```

**Note**: Services coordinate but do not implement business logic.

### 9. Registry Integration

**Location**: `intelligence/registry/`

**Purpose**: Integrate with existing registries

```python
class RegistryIntegration:
    def get_agent(self, agent_id: str) -> dict | None
    def list_agents(self) -> list[dict]
    def get_capability(self, capability_id: str) -> dict | None
    def list_capabilities(self) -> list[dict]
    def get_workflow(self, workflow_id: str) -> dict | None
    def list_workflows(self) -> list[dict]
```

**Note**: This is integration only. No duplicate registry implementation.

## Runtime Lifecycle

```
1. Task Submission
   └── Validate Task
2. Session Creation
   └── Initialize Context
3. Pipeline Selection
   └── Validate Pipeline
4. Pipeline Execution
   ├── Execute Steps (Sequential)
   └── Aggregate Results
5. Result Return
   └── Validate Result
6. Event Emission
```

## Session Lifecycle

```
1. Create Session
   └── Initialize empty
2. Add Task
   └── Track task
3. Execute Task
   └── Add result
4. Collect Findings
   └── Aggregate
5. Complete Session
   └── Mark complete
```

## Pipeline Model

```
Pipeline
├── Step 1 (order=0)
├── Step 2 (order=1)
│   ├── Substep A
│   └── Substep B
├── Step 3 (order=2)
└── ...
```

## What Phase 4A Does NOT Include

- ❌ Research Agent
- ❌ Investigation Agent
- ❌ Threat Intelligence
- ❌ Cyber Intelligence
- ❌ OSINT
- ❌ Extraction Logic
- ❌ Discovery Logic
- ❌ LLM Integration
- ❌ AI Integration
- ❌ Planning
- ❌ Goal Selection
- ❌ Autonomous Decisions
- ❌ Connectors
- ❌ Network Calls
- ❌ Databases
- ❌ Applications
- ❌ Web UI
- ❌ CLI
- ❌ REST API

## What Phase 4B Will Include

Phase 4B (Intelligence Capabilities Foundation) will implement:

- Real intelligence processing
- Knowledge synthesis
- Pattern analysis
- Correlation engines
- Indicator generation
- Threat intelligence (separate module)
- Cyber intelligence (separate module)
- OSINT collection (separate module)

## Testing

All components are fully tested:

```bash
pytest intelligence/tests/ -v
```

## Architecture Enforcement

The architecture tests verify:

```python
# No AI imports
assert "openai" not in code
assert "anthropic" not in code
assert "langchain" not in code

# No connector imports
assert "from connectors" not in code

# No application imports
assert "from applications" not in code

# No planning imports
assert "from planning" not in code
```

## Summary

Phase 4A establishes the **Intelligence Runtime Foundation** - the execution layer that coordinates but does not process intelligence.

The runtime:
- ✅ Coordinates execution
- ✅ Orchestrates workflows
- ✅ Validates inputs
- ✅ Records outputs
- ✅ Delegates to other layers

Real intelligence capabilities begin only in Phase 4B.
