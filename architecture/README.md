# Architecture

This directory contains architecture documentation and decisions for the FOOL Platform.

## Architecture Decision Records (ADRs)

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0007 | Python-First Platform Architecture | Accepted |

## Directory Structure

```
architecture/
├── README.md           # This file
└── adr/                # Architecture Decision Records
    └── ADR-0007-python-first-platform.md
```

## Architecture Principles

1. **Standards define semantics** - Vocabulary, concepts, meanings
2. **Contracts define interoperability** - JSON Schema for wire formats
3. **Implementations conform to contracts** - Language implementations
4. **Domain owns business rules** - Pure, immutable domain models
5. **Platform owns execution** - Runtime infrastructure
6. **Applications own presentation** - UI layers

## Dependency Rules

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

### Forbidden Dependencies

- Domain MUST NOT import Platform
- Domain MUST NOT import AI/Infrastructure/Applications/Data/Orchestration
- Cross-layer circular dependencies are forbidden

## Python-First Decision

Per ADR-0007, the FOOL Platform adopts Python as the canonical implementation language for:

- Domain
- Knowledge
- Intelligence
- Platform
- Kernel
- Orchestration
- Agents
- Architecture tests
- Contract validation
- Backend services

TypeScript is reserved for:
- Web UI
- Admin UI
- Frontend tooling
- Optional client SDKs

## Phase 2 Architecture

Phase 2 introduces the Platform layer with:

```
platform/
├── kernel/           # Kernel runtime
│   ├── di/          # Dependency injection
│   ├── config/      # Configuration
│   ├── health/       # Health checks
│   └── registries/  # Registry loaders
└── agents/          # Agent registry
```

### Phase 2A (Completed)
- Platform Kernel Foundation
- Dependency Injection Foundation
- Configuration Foundation
- Health Foundation
- Registry Foundation

### Phase 2B (Next)
- Event Bus Foundation

### Phase 2C (Future)
- Workflow Engine Foundation
- Agent Runtime Foundation

## Validation

Architecture rules are enforced through tests in `testing/architecture/`:

```bash
pytest testing/architecture/
```
