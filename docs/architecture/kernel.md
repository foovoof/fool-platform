# Kernel Architecture

## Overview

The kernel is the foundation layer of the FOOL Platform Phase 2. It provides core runtime services that all other platform components depend on.

## Architecture Principles

1. **Standards define semantics** - Vocabulary from `standards/`
2. **Contracts define interoperability** - JSON Schema from `contracts/`
3. **Implementations conform to contracts** - Python domain from `domain/`
4. **Domain owns business rules** - Pure domain logic
5. **Kernel owns execution** - Runtime infrastructure

## Dependency Flow

```
Standards
    ↓
Contracts
    ↓
Domain
    ↓
Kernel
    ↓
Applications
```

## Kernel Services

### Lifecycle Management

The kernel manages its own lifecycle through a state machine:

- **CREATED**: Initial state after construction
- **STARTING**: Transitioning to running
- **RUNNING**: Fully operational
- **STOPPING**: Transitioning to stopped
- **STOPPED**: Fully shut down
- **FAILED**: Error occurred during lifecycle

### Dependency Injection

The DI container provides:

- **Singleton lifetime**: One instance shared across all resolutions
- **Transient lifetime**: New instance each time
- **Scoped lifetime**: One instance per scope

Features:
- Constructor injection
- Factory-based resolution
- Circular dependency detection
- Lifecycle hooks

### Configuration

Layered configuration system:

1. Default values
2. Configuration files
3. Environment variables
4. Runtime overrides

Environment profiles:
- local
- development
- testing
- production

### Health System

Comprehensive health checking:

- **Liveness**: Is the kernel alive?
- **Readiness**: Is the kernel ready to receive work?
- **Startup**: Did startup complete successfully?
- **Shutdown**: Was cleanup performed correctly?

### Registry Access

Loaders for platform registries:

- Agent Registry (agents.yaml)
- Capability Registry (capabilities.yaml)
- Workflow Registry (workflows/*.yaml)
- Concept Registry (standards/concepts/*.md)
- Contract Registry (contracts/**/*.schema.json)

## Thread Safety

The kernel is designed for single-threaded initialization with:

- Sequential startup phases
- Ordered shutdown
- Scoped concurrency support via context variables

## Extension Points

The kernel can be extended through:

1. **Service Registration**: Register services in the DI container
2. **Health Checks**: Add custom health checks
3. **Lifecycle Hooks**: React to kernel lifecycle events
4. **Configuration Sources**: Add custom configuration loaders

## Future Phases

### Phase 2B: Event Bus Foundation
- In-process event bus
- Event publishing/subscription
- Async event processing

### Phase 2C: Workflow Engine
- Workflow execution
- Step orchestration
- State persistence

### Phase 2D: Agent Runtime
- Agent implementations
- Task execution
- Result handling
