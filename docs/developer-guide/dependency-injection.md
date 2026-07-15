# Dependency Injection Developer Guide

## Overview

The FOOL Platform kernel includes a full-featured dependency injection (DI) container that manages service creation, lifetime, and dependency resolution.

## Core Concepts

### Service Registration

Services are registered in the container with a specified lifetime:

```python
from platform.kernel.di import DIContainer, ServiceLifetime

container = DIContainer()

# Register a singleton
container.register_singleton(MyService, MyService)

# Register a transient
container.register_transient(MyTransientService, MyTransientService)

# Register a scoped service
container.register_scoped(MyScopedService, MyScopedService)
```

### Service Resolution

Resolve services by type:

```python
service = container.resolve(MyService)
```

## Lifetime Policies

### Singleton

One instance is created and shared across all resolutions:

```python
container.register_singleton(Cache, Cache)

cache1 = container.resolve(Cache)
cache2 = container.resolve(Cache)

assert cache1 is cache2  # Same instance
```

### Transient

A new instance is created each time:

```python
container.register_transient(RequestHandler, RequestHandler)

handler1 = container.resolve(RequestHandler)
handler2 = container.resolve(RequestHandler)

assert handler1 is not handler2  # Different instances
```

### Scoped

One instance per scope. Useful for request-scoped services:

```python
container.register_scoped(DbConnection, DbConnection)

container.begin_scope("request-1")
conn1 = container.resolve(DbConnection)
conn2 = container.resolve(DbConnection)
assert conn1 is conn2  # Same instance in scope
container.end_scope("request-1")

container.begin_scope("request-2")
conn3 = container.resolve(DbConnection)
assert conn1 is not conn3  # Different instance in different scope
container.end_scope("request-2")
```

## Fluent Registration

Use the builder pattern for fluent registration:

```python
container = DIContainer()

container.register(MyService) \
    .to(MyServiceImpl) \
    .singleton()
```

## Lifecycle Hooks

Register hooks for service lifecycle events:

```python
from platform.kernel.di import HookType

def on_resolved(container, instance, key):
    print(f"Resolved: {key}")

container.add_hook(HookType.AFTER_RESOLVE, on_resolved)
```

## Validation

Validate the container configuration:

```python
errors = container.validate()
if errors:
    for key, error_list in errors.items():
        print(f"{key}: {error_list}")
```

## Best Practices

1. **Prefer singleton for stateless services**: Reduces memory and initialization overhead

2. **Use scoped for request-scoped state**: Ensures proper isolation between requests

3. **Use transient for stateful services**: Prevents shared state issues

4. **Register dependencies in dependency order**: The container resolves dependencies automatically

5. **Use interfaces for registration**: Makes testing easier with mock implementations

## Testing with DI

The container makes testing straightforward:

```python
def test_service_logic():
    container = DIContainer()
    container.register_singleton(IDatabase, MockDatabase)
    container.register_singleton(UserService, UserService)
    
    service = container.resolve(UserService)
    # Test service logic with mock database
```

## Limitations

Phase 2A DI container:

- ✅ Constructor injection
- ✅ Factory-based resolution
- ✅ Circular dependency detection
- ✅ Lifecycle hooks
- ❌ Property injection (not implemented)
- ❌ Method injection (not implemented)
- ❌ Interception (not implemented)
