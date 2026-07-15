# ADR-0007: Python-First Platform Architecture

## Status

**Accepted**

## Context

The FOOL Platform Phase 1 established a solid foundation with JSON Schema contracts, TypeScript domain models, and declarative workflows. However, Phase 2 requires a platform kernel and runtime infrastructure that demands careful selection of the canonical implementation language.

The platform must:
- Support multiple agent implementations (research, extraction, discovery, investigation, reporting, monitoring)
- Enable workflow execution and orchestration
- Provide a clean extension model for future capabilities
- Maintain strong separation between business logic and infrastructure

Several factors drive the language selection decision:

1. **Agent Ecosystem**: The AI/agent ecosystem is increasingly Python-centric, with most LLM frameworks (LangChain, LlamaIndex, AutoGen), embedding models, and ML tooling in Python.

2. **Domain Purity**: The domain layer must remain free of infrastructure concerns. Python's strong typing and dataclasses provide excellent support for immutable domain models.

3. **Team Skills**: Python remains the most widely-used language for AI/ML work, making it the natural choice for a platform that will integrate AI capabilities.

4. **Interoperability**: JSON Schema contracts define the wire format, ensuring that TypeScript web UIs and Python backends can communicate seamlessly.

## Decision

The FOOL Platform adopts a **Python-first backend architecture**. The canonical implementation language for the following layers is Python:

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

**TypeScript is reserved for:**
- Web UI
- Admin UI
- Frontend tooling
- Optional client SDKs

## Architecture Principles

1. **Standards define semantics.** Vocabulary, concepts, and meanings are captured in `standards/`.

2. **Contracts define interoperability.** JSON Schema contracts in `contracts/` define wire formats and API shapes. They are the canonical source of truth for interoperability.

3. **Implementations conform to contracts.** Both Python and TypeScript implementations must validate against the same contract schemas.

4. **Domain owns business rules.** The `domain/` package contains pure, immutable domain models with no framework, database, HTTP, or AI SDK dependencies.

5. **Knowledge owns graph semantics.** The knowledge layer manages entity relationships, provenance chains, and ontological structures.

6. **Intelligence owns reasoning.** The intelligence layer handles inference, confidence scoring, and synthesis.

7. **Platform owns execution.** The platform layer provides runtime infrastructure including the kernel, lifecycle management, and dependency injection.

8. **Applications own presentation.** UI applications consume platform APIs and present data to users.

## Dependency Rules

The following dependency direction is mandatory:

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
- Domain MUST NOT import AI
- Domain MUST NOT import Infrastructure
- Domain MUST NOT import Applications
- Domain MUST NOT import Data
- Domain MUST NOT import Orchestration
- Cross-layer circular dependencies are forbidden

## Migration Requirements

For Phase 1 TypeScript domain implementations:

1. **Do not maintain duplicate domain implementations.** There must be exactly one canonical domain implementation.

2. **Do not create adapters between languages.** If a domain model exists in both Python and TypeScript, migrate the canonical source to Python.

3. **Frontend/client SDKs are acceptable.** TypeScript implementations that serve only as client-side types or UI components are permitted.

4. **Migration path:**
   - Extract domain semantics from TypeScript implementations
   - Implement canonical Python domain models conforming to contracts
   - TypeScript retains client types only (generated from contracts if possible)
   - Architecture tests verify no backend authority remains in TypeScript

## Consequences

### Positive

- Python agent ecosystem is accessible directly
- Domain models benefit from Python's strong typing and dataclasses
- Single implementation reduces maintenance burden
- Clear separation between frontend and backend responsibilities

### Negative

- TypeScript domain implementations must be migrated
- Two testing paradigms (vitest for TS, pytest for Python)
- Need to maintain TypeScript client types separately

### Neutral

- Contracts remain the interoperability boundary regardless of implementation language
- Web UI remains TypeScript, enabling modern frontend frameworks

## Validation Requirements

Before Phase 2 proceeds beyond 2A, the following must be verified:

1. ✅ Domain is implemented in Python
2. ✅ Domain conforms to Contracts (schema validation)
3. ✅ Contracts conform to Standards
4. ✅ No TypeScript Domain implementation remains as backend/domain authority
5. ✅ Domain has no forbidden imports
6. ✅ Architecture documentation reflects Python-first architecture

## Phase 2 Prerequisites Checklist

- [ ] Python domain modules created and validated against contracts
- [ ] Platform kernel foundation implemented (Phase 2A)
- [ ] Dependency injection container functional
- [ ] Configuration management operational
- [ ] Health check system operational
- [ ] Registry loaders for YAML files functional
- [ ] Architecture tests verify Python-first rules
- [ ] Documentation updated to reflect Python-first architecture

## Related Documents

- `contracts/` - JSON Schema definitions
- `standards/` - Concept definitions and data dictionaries
- `domain/` - Python domain implementations
- `platform/kernel/` - Platform kernel foundation

## Review History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-07-15 | 1.0 | FOOL Platform Team | Initial decision |
