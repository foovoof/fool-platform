# Platform

The FOOL Platform Phase 2 introduces the Python-first platform kernel and runtime.

## Architecture

The platform follows the canonical architecture:

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

## Kernel

The kernel (`platform/kernel/`) provides:

- **Runtime**: Lifecycle management, startup/shutdown coordination
- **Dependency Injection**: Service registration and resolution
- **Configuration**: Environment-based configuration with validation
- **Health**: Health checks for liveness, readiness, startup, shutdown
- **Registries**: Loaders for agents, capabilities, workflows, concepts, contracts

### Directory Structure

```
platform/
├── kernel/
│   ├── __init__.py           # Kernel exports
│   ├── runtime.py            # Kernel runtime
│   ├── lifecycle.py           # Lifecycle management
│   ├── kernel_state.py       # State machine
│   ├── kernel_config.py      # Configuration model
│   ├── kernel_events.py      # Event bus
│   ├── kernel_exceptions.py  # Exception hierarchy
│   ├── kernel_interfaces.py  # Abstract interfaces
│   ├── app_context.py        # Application context
│   ├── execution_context.py  # Execution context
│   ├── bootstrapper.py       # Bootstrap coordination
│   ├── health_manager.py     # Health management
│   ├── registry_manager.py   # Registry management
│   ├── di/                   # Dependency injection
│   │   ├── container.py
│   │   ├── lifetime.py
│   │   ├── registration.py
│   │   ├── resolution.py
│   │   ├── validation.py
│   │   └── hooks.py
│   ├── config/               # Configuration
│   │   ├── environment.py
│   │   ├── loader.py
│   │   ├── validator.py
│   │   ├── typed_config.py
│   │   ├── registry.py
│   │   ├── override.py
│   │   └── secrets.py
│   ├── health/               # Health system
│   │   ├── checks.py
│   │   ├── status.py
│   │   ├── readiness.py
│   │   ├── liveness.py
│   │   ├── startup.py
│   │   ├── shutdown.py
│   │   ├── registry.py
│   │   └── diagnostics.py
│   ├── registries/           # Registry loaders
│   │   ├── agent_registry.py
│   │   ├── capability_registry.py
│   │   ├── workflow_registry.py
│   │   ├── concept_registry.py
│   │   └── contract_registry.py
│   └── tests/                # Kernel tests
└── agents/                   # Agent registry
    └── registry/
        ├── agents.yaml
        └── capabilities.yaml
```

## Phase 2 Scope

### Phase 2A - Completed
- ✅ Python-first domain verification
- ✅ Architecture Decision Record (ADR-0007)
- ✅ Platform Kernel Foundation
- ✅ Dependency Injection Foundation
- ✅ Configuration Foundation
- ✅ Health Foundation
- ✅ Registry Foundation
- ✅ Tests
- ✅ Documentation

### Phase 2B - Next
- Event Bus Foundation
- Workflow Engine Foundation

### Phase 2C - Future
- Orchestration Foundation
- Agent Runtime Foundation

## Usage

```python
from platform.kernel import Kernel, KernelConfig

# Create kernel configuration
config = KernelConfig.for_development()

# Create and start kernel
kernel = Kernel(config)
kernel.start()

# Use kernel services
# ...

# Stop kernel
kernel.stop()
```

## Testing

```bash
# Run kernel tests
pytest platform/kernel/tests/

# Run architecture tests
pytest testing/architecture/
```
