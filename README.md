# FOOL Platform

**FOOL** is a Cognitive Operating System for open-source, evidence-driven
investigation. Phase 1 of this repository builds the **Core Foundation
Layer**: the contracts, domain models, standards, agent/capability
registries, and declarative workflow definitions that every later phase
builds on. There is intentionally no runtime, no orchestrator, and no UI
in Phase 1 — those are Phase 2 concerns layered on top of a foundation that
must be correct first.

This repository is the successor to, and absorbs, the
[`Goy`](https://github.com/foovoof/Goy) OSINT link-aggregator: Goy's
`contracts/` folder was an early sketch of the shape FOOL now implements in
full.

## The eight layers

| # | Layer | Directory | What it is |
|---|---|---|---|
| 1 | Contracts | `contracts/` | JSON Schema (Draft 2020-12) definitions of every wire shape: domain objects, agent messages, workflow definitions, confidence models. The single source of truth for shape. |
| 2 | Domain | `domain/` | Pure, immutable TypeScript implementations of the behavior behind each contract — no framework, database, HTTP, or AI SDK imports anywhere in this layer. |
| 3 | Standards | `standards/` | Human-facing vocabulary: `concepts/` (what each thing means and how it differs from things it's commonly confused with) and `data_dictionary/` (exact field-by-field reference). |
| 4 | Agent registry | `platform/agents/registry/` | Data-only registry of agent types (`agents.yaml`) and the capabilities they implement (`capabilities.yaml`). No agent runtime code lives here. |
| 5 | Workflows | `workflows/` | Declarative `WorkflowDefinition` documents (research, extraction, discovery, investigation, reporting, monitoring) — steps, transitions, retry/timeout/failure policy, termination conditions. No execution engine. |
| 6 | Testing / architecture | `testing/architecture/` | Automated checks that the other seven layers stay internally consistent: schemas compile and their own examples validate, every required Phase 1 file exists, every workflow's required agents/capabilities resolve in the registry, and no placeholder markers exist anywhere in the deliverable. |
| 7 | Domain tests | `domain/tests/` | Unit tests for every domain module's construction rules, invariants, immutability, and purity. |
| 8 | Documentation | this file + per-layer `README.md` | Vision, structure, build order, and status, kept next to the code it documents. |

## Core principles

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
3. `domain/` (implements the behavior behind `contracts/domain/`, plus
   `Finding`/`Event`/`Timeline`/`Annotation`/`ChainOfCustody`/
   `ConfidenceScore`/`ClassificationLevel`) →
4. `standards/` (documents the concepts and fields the previous two layers
   just fixed) →
5. `platform/agents/registry/` (declares which agent types/capabilities
   exist, referencing contract schemas for input/output shape) →
6. `workflows/` (declares how work gets done, referencing the registry) →
7. `testing/architecture/` + `domain/tests/` (validate 1–6 stay consistent).

## Running the checks

```bash
pnpm install
pnpm typecheck          # tsc --noEmit across domain/ and testing/
pnpm test                # domain/tests + testing/architecture, via vitest
pnpm test:domain         # domain/tests only
pnpm test:architecture   # testing/architecture only
```

## Current status (Phase 1)

Complete: all eight layers above have real, non-placeholder content —
33 contract schemas, 16 domain modules with 10 accompanying test files,
11 concept files, 11 data dictionary files, the agent/capability registry,
6 workflow definitions, and 4 architecture-level consistency tests, plus
this documentation set.

Not yet built (explicitly out of scope for Phase 1): any workflow
execution engine, any agent runtime, any persistence layer, any API server,
and any user interface. `domain/` objects are constructed and returned by
callers; nothing in this repository writes to storage or calls an external
service.

## Phase 2 roadmap

- A workflow execution engine that consumes `workflows/*.yaml` and drives
  `AgentTask`/`AgentResult`/`AgentEvent` exchanges against real agent
  implementations.
- Concrete agent implementations for each `agent_type` in
  `platform/agents/registry/agents.yaml` (research, extraction, discovery,
  investigation, reporting, monitoring).
- A persistence layer mapping `domain/` objects to storage, respecting the
  `classification` field on every object for access control.
- An API and/or UI layer for case intake, investigation review, and report
  publication — always requiring the human `reviewed_by` step `report.ts`
  already enforces at the domain level.
