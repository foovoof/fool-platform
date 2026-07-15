# FOOL Platform

**FOOL** is a Cognitive Operating System for open-source, evidence-driven
investigation. This repository contains the **Core Foundation Layer** (Phase 1)
and the **Platform Kernel** (Phase 2A): the contracts, domain models, standards,
agent/capability registries, declarative workflow definitions, and Python-first
platform kernel that every later phase builds on.

## Phase Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Core Foundation Layer (contracts, domain, standards, registries) |
| Phase 2A | ✅ Complete | Python-first platform kernel foundation |
| Phase 2B | 🔜 Next | Event Bus Foundation |
| Phase 2C | 📋 Future | Workflow Engine Foundation |
| Phase 2D | 📋 Future | Agent Runtime Foundation |

## The eight layers

| # | Layer | Directory | What it is |
|---|---|---|---|
| 1 | Contracts | `contracts/` | JSON Schema (Draft 2020-12) definitions of every wire shape: domain objects, agent messages, workflow definitions, confidence models. The single source of truth for shape. |
| 2 | Domain | `domain/` | Pure, immutable Python implementations of the behavior behind each contract — no framework, database, HTTP, or AI SDK imports anywhere in this layer. |
| 3 | Standards | `standards/` | Human-facing vocabulary: `concepts/` (what each thing means and how it differs from things it's commonly confused with) and `data_dictionary/` (exact field-by-field reference). |
| 4 | Agent registry | `platform/agents/registry/` | Data-only registry of agent types (`agents.yaml`) and the capabilities they implement (`capabilities.yaml`). No agent runtime code lives here. |
| 5 | Workflows | `workflows/` | Declarative `WorkflowDefinition` documents (research, extraction, discovery, investigation, reporting, monitoring) — steps, transitions, retry/timeout/failure policy, termination conditions. No execution engine. |
| 6 | Platform | `platform/` | Python-first platform kernel with dependency injection, configuration, health checks, and registry loaders. |
| 7 | Testing / architecture | `testing/architecture/` | Automated checks that the other layers stay internally consistent: schemas compile and their own examples validate, Python-first rules enforced, and no placeholder markers exist anywhere in the deliverable. |
| 8 | Documentation | this file + per-layer `README.md` | Vision, structure, build order, and status, kept next to the code it documents. |

## Core principles

- **Python-First** — the platform adopts Python as the canonical implementation
  language for domain, platform, intelligence, orchestration, and agents.
  TypeScript is reserved for web UI and optional client SDKs.
- **Contracts First** — no domain, agent, or workflow shape exists in code
  before it exists as a schema in `contracts/`.
- **Domain Purity** — `domain/` never imports a database, HTTP client, AI
  SDK, or framework; it is pure, testable business logic.
- **Identity-Centric** — `Identity` is the aggregation anchor every Entity,
  piece of Evidence, and Finding ultimately traces back to.
- **Event-Driven Language** — state changes are described as dotted,
  namespaced, versioned `Event`s, never ad hoc strings.
- **Workflow-Driven Execution** — "how work gets done" is declarative data
  in `workflows/`, not hardcoded control flow in agent logic.
- **Confidence Everywhere** — no claim is a bare boolean; every assessed
  field carries a `ConfidenceScore` with a score, a derived level, a named
  method, and (ideally) evidence/source references.
- **Provenance Everywhere** — no domain object asserting something about
  the world exists without a recorded origin, and Evidence specifically
  carries a `ChainOfCustody`.
- **Human Accountability** — every `Case` has a named human `owner`, and
  every `Report` requires a recorded human `reviewed_by` before it can
  reach `active` (published) status. The platform assists; it never
  publishes or closes a case on its own authority.
- **No placeholders** — enforced mechanically by
  `testing/architecture/no_placeholders.test.ts`; nothing in this
  repository is a stub, a mock, or "coming soon."

## Build order

The layers above were built and must continue to be extended in this
order, because each depends on the one before it:

1. `contracts/common/` (shared `$defs`) →
2. `contracts/domain/`, `contracts/agent/`, `contracts/confidence/`,
   `contracts/workflow/` (all reference `common/`) →
3. `domain/` (implements the behavior behind `contracts/domain/` in Python, plus
   `Finding`/`Event`/`Timeline`/`Annotation`/`ChainOfCustody`/
   `ConfidenceScore`/`ClassificationLevel`) →
4. `standards/` (documents the concepts and fields the previous two layers
   just fixed) →
5. `platform/agents/registry/` (declares which agent types/capabilities
   exist, referencing contract schemas for input/output shape) →
6. `workflows/` (declares how work gets done, referencing the registry) →
7. `fool_platform/kernel/` (Python-first platform kernel with DI, config, health, registries) →
8. `testing/architecture/` + `domain/tests/` (validate 1–7 stay consistent).

## Running the checks

```bash
# Python checks
python -m compileall domain fool_platform/kernel
pytest fool_platform/kernel/tests/ testing/architecture/

# TypeScript checks (legacy domain)
pnpm install
pnpm typecheck
pnpm test
```

## Current status

**Phase 1**: Complete — 33 contract schemas, Python domain modules with tests,
11 concept files, 11 data dictionary files, the agent/capability registry,
6 workflow definitions.

**Phase 2A**: Complete — Python-first platform kernel with 12 kernel modules,
6 DI modules, 7 config modules, 8 health modules, 5 registry loaders,
and comprehensive architecture tests.

Not yet built (explicitly out of scope for Phase 2A): any workflow
execution engine, any agent runtime, any persistence layer, any API server,
and any user interface. `domain/` objects are constructed and returned by
callers; nothing in this repository writes to storage or calls an external
service.

## Phase 2 roadmap

### Phase 2A (✅ Complete)
- Python-first domain verification
- Platform Kernel Foundation
- Dependency Injection Foundation
- Configuration Foundation
- Health Foundation
- Registry Foundation

### Phase 2B (🔜 Next: Event Bus Foundation)
- In-process event bus for domain events
- Event publishing and subscription
- Event handlers
- Async event processing support

### Phase 2C (📋 Future: Workflow Engine)
- Workflow execution engine that consumes `workflows/*.yaml`
- `AgentTask`/`AgentResult`/`AgentEvent` exchanges
- Step orchestration and state management

### Phase 2D (📋 Future: Agent Runtime)
- Concrete agent implementations for each `agent_type` in
  `platform/agents/registry/agents.yaml` (research, extraction, discovery,
  investigation, reporting, monitoring).
- Task execution and result handling

### Phase 2E (📋 Future: Persistence & API)
- Persistence layer mapping `domain/` objects to storage, respecting the
  `classification` field on every object for access control.
- API and/or UI layer for case intake, investigation review, and report
  publication — always requiring the human `reviewed_by` step `report.ts`
  already enforces at the domain level.
