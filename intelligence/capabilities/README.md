# Intelligence Capabilities Foundation

## Phase 4B

This is the **Intelligence Capabilities Foundation** - Phase 4B of the FOOL Platform architecture.

## IMPORTANT: What This Is NOT

This phase does **NOT** implement:

- ❌ Real Intelligence Collection
- ❌ Cyber Intelligence
- ❌ Threat Intelligence
- ❌ OSINT (Open Source Intelligence)
- ❌ AI/LLM Integration
- ❌ Planning
- ❌ Autonomous Decisions
- ❌ Connectors
- ❌ Databases
- ❌ External APIs

## What This IS

This phase implements the **Generic Intelligence Capabilities** that:

✅ Define reusable intelligence work units  
✅ Execute through Capability Runtime  
✅ Integrate with Knowledge Graph  
✅ Integrate with Deterministic Inference  
✅ Emit events for all operations  
✅ Remain deterministic and in-memory  

## Architecture

```
Standards
    ↓
Contracts
    ↓
Domain
    ↓
Knowledge
    ↓
Intelligence
    ↓
Platform
    ↓
Applications
```

## Capability Types

### Generic Capabilities

1. **Research** - Investigate topics
2. **Discovery** - Find entities
3. **Extraction** - Extract data
4. **Correlation** - Find relationships
5. **Investigation** - Deep analysis
6. **Assessment** - Evaluate subjects
7. **Reporting** - Generate reports
8. **Timeline** - Sequence events
9. **Evidence Analysis** - Analyze evidence

## Components

### Models (`intelligence/capabilities/models/`)
- `CapabilityDefinition` - Capability definition
- `CapabilityTask` - Task for capability
- `CapabilityResult` - Execution result
- `CapabilityFinding` - Analysis finding
- `CapabilityArtifact` - Processing output
- `CapabilityExecutionRecord` - Execution record

### Registry (`intelligence/capabilities/registry/`)
- `CapabilityRegistry` - Capability discovery
- `create_default_registry()` - Default capabilities

### Agents (`intelligence/capabilities/agents/`)
- `ResearchAgent` - Research capability agent
- `DiscoveryAgent` - Discovery capability agent
- `ExtractionAgent` - Extraction capability agent
- `CorrelationAgent` - Correlation capability agent
- `InvestigationAgent` - Investigation capability agent
- `AssessmentAgent` - Assessment capability agent
- `ReportingAgent` - Reporting capability agent
- `TimelineAgent` - Timeline capability agent
- `EvidenceAnalysisAgent` - Evidence analysis capability agent
- `AgentFactory` - Agent factory

### Execution (`intelligence/capabilities/execution/`)
- `CapabilityExecutor` - Execute capability tasks
- `CapabilityDispatcher` - Dispatch tasks
- `CapabilityResolver` - Resolve capabilities
- `ExecutionManager` - Manage execution lifecycle

### Pipelines (`intelligence/capabilities/pipelines/`)
- `CapabilityPipeline` - Pipeline definition
- `PipelineStep` - Pipeline step
- `PipelineExecutor` - Pipeline execution
- `create_default_pipeline()` - Default pipeline creation

### Validation (`intelligence/capabilities/validation/`)
- `CapabilityValidator` - Validate capabilities
- `TaskValidator` - Validate tasks
- `ResultValidator` - Validate results
- `PipelineValidator` - Validate pipelines
- `AgentValidator` - Validate agents
- `CompatibilityValidator` - Validate compatibility

### Events (`intelligence/capabilities/events/`)
- `CapabilityEventEmitter` - Event emission
- Event types for all capability operations

### Services (`intelligence/capabilities/services/`)
- `CapabilityService` - Main capability service
- `ResearchService` - Research capability service
- `DiscoveryService` - Discovery capability service
- `ExtractionService` - Extraction capability service
- `CorrelationService` - Correlation capability service
- `InvestigationService` - Investigation capability service
- `AssessmentService` - Assessment capability service
- `ReportingService` - Reporting capability service
- `TimelineService` - Timeline capability service
- `EvidenceAnalysisService` - Evidence analysis capability service

## Usage

```python
from intelligence.capabilities import CapabilityService
from intelligence.capabilities.models import CapabilityTask, CapabilityType

# Create service
service = CapabilityService()

# Create task
task = CapabilityTask(
    capability_id="research-capability",
    capability_type=CapabilityType.RESEARCH,
    objective="Research topic",
    inputs={"topic": "example"},
)

# Execute
result = service.execute_task(task)

# Check result
if result.is_successful():
    print(f"Findings: {result.findings}")
    print(f"Artifacts: {result.artifacts}")
```

## Key Principles

1. **Capabilities are Generic** - Not domain-specific
2. **Deterministic** - All execution is deterministic
3. **No External Dependencies** - In-memory only
4. **Event-Driven** - Events for all operations
5. **Validatable** - All components can be validated

## Next Phase

**Phase 5A — Connectors Foundation**

This will implement:
- Real data acquisition
- External integrations
- Network clients
- Database connectors
