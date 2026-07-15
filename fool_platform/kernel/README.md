# Platform Kernel

The kernel is the central runtime component of the FOOL Platform.

## Purpose

The kernel provides the foundation services that all platform components depend on:

1. **Lifecycle Management**: Startup, running, shutdown coordination
2. **Dependency Injection**: Service registration and resolution with singleton, transient, and scoped lifetimes
3. **Configuration**: Environment-based configuration with layered overrides
4. **Health Checks**: Liveness, readiness, startup, and shutdown validation
5. **Event Bus**: Publish-subscribe for kernel lifecycle events
6. **Registry Access**: Load and access platform registries

## Key Components

### Kernel (`runtime.py`)

The main kernel class that coordinates all kernel services.

```python
from platform.kernel import Kernel, KernelConfig

config = KernelConfig.for_development()
kernel = Kernel(config)
kernel.start()
```

### Lifecycle (`lifecycle.py`, `kernel_state.py`)

State machine for kernel lifecycle:

```
CREATED → STARTING → RUNNING → STOPPING → STOPPED
                    ↓           ↓
                 FAILED      FAILED
```

### Dependency Injection (`di/`)

Full-featured DI container with:

- **Singleton**: One instance shared across all resolutions
- **Transient**: New instance each time
- **Scoped**: One instance per scope

```python
from platform.kernel.di import DIContainer, ServiceLifetime

container = DIContainer()
container.register_singleton(MyService, MyService)
service = container.resolve(MyService)
```

### Configuration (`config/`)

Layered configuration with:

- Environment profiles (local, development, testing, production)
- Environment variable overrides
- Runtime overrides
- Typed configuration access

```python
from platform.kernel.config import ConfigLoader, EnvironmentProfile

loader = ConfigLoader(EnvironmentProfile.DEVELOPMENT)
result = loader.load()
```

### Health (`health/`)

Comprehensive health check system:

- Liveness checks
- Readiness checks
- Startup validation
- Shutdown validation
- Diagnostics and reporting

### Registries (`registries/`)

Loaders for platform registries:

- Agent Registry
- Capability Registry
- Workflow Registry
- Concept Registry
- Contract Registry

## What Is Not In Phase 2A

Phase 2A intentionally does not include:

- ❌ Event Bus implementation
- ❌ Workflow execution engine
- ❌ Real orchestration
- ❌ Real agents
- ❌ Plugin runtime
- ❌ AI/LLM integration
- ❌ External connectors
- ❌ APIs
- ❌ Database/persistence
- ❌ Message brokers

These will be added in later phases.

## Phase 2B Scope Recommendation

The recommended next phase (Phase 2B) is **Event Bus Foundation**:

- In-process event bus for domain events
- Event publishing and subscription
- Event handlers
- Async event processing support

This sets the foundation for workflow execution in Phase 2C.
