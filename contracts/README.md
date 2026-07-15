# Contracts

This layer is the platform's single source of truth for wire shape. Every
domain object, agent message, workflow definition, and confidence
assessment that crosses a boundary (agent ↔ agent, agent ↔ workflow engine,
platform ↔ storage) is defined here first, as a JSON Schema (Draft
2020-12), before any code that produces or consumes it is written. This is
the Contracts First principle: no code changes a shape that isn't already
declared here.

## Structure

| Directory | Contents |
|---|---|
| `common/` | `common-defs.schema.json` — shared `$defs` (id, timestamp, semanticVersion, tags, metadata, reference, referenceList, confidenceScore, confidenceLevel, confidenceRef, provenance, classificationLevel, status) referenced by every other schema via relative `$ref`, so no definition is duplicated across files. |
| `domain/` | The eight core domain object schemas: `identity`, `entity`, `relationship`, `evidence`, `source`, `case`, `investigation`, `report`. |
| `agent/` | The agent protocol schemas: `agent-task`, `agent-context`, `agent-error`, `agent-capability`, `agent-manifest`, `agent-result`, `agent-event`. |
| `workflow/` | Declarative workflow schemas: `retry-policy`, `timeout-policy`, `failure-policy`, `termination-condition`, `checkpoint`, `workflow-step`, `workflow-transition`, `workflow-definition`, `workflow-state`, `workflow-execution`. |
| `confidence/` | Confidence-model schemas: the base `confidence-model` and `scoring-model`, plus one specialization per assessed object type (`source-reliability`, `evidence-confidence`, `entity-confidence`, `relationship-confidence`, `finding-confidence`, `investigation-confidence`). |

## Conventions

- Every schema uses `"$schema": "https://json-schema.org/draft/2020-12/schema"`
  and declares a stable `"$id"`.
- Every schema sets `"additionalProperties": false` and lists explicit
  `"required"` fields — nothing may silently pass through undeclared.
- Every schema carries at least one realistic `"examples"` entry, which
  `testing/architecture/schemas_valid.test.ts` validates against the schema
  itself on every test run.
- Shared concepts (ids, timestamps, provenance, confidence, references,
  classification, status) live only in `common/common-defs.schema.json` and
  are pulled in elsewhere via `"$ref"` — never redefined inline.
- Confidence specializations extend `confidence-model.schema.json` via
  `"allOf"` and add only the one field specific to what they assess (e.g.
  `evidence_ref`, `finding_ref`).

## Relationship to other layers

- `domain/` (TypeScript) implements the in-process behavior for these
  shapes; the two must be kept in lockstep — see each domain module's
  header comment for which schema it mirrors.
- `standards/data_dictionary/` documents each schema's fields in prose/table
  form for humans; `standards/concepts/` documents the *meaning* of each
  object, independent of its exact fields.
- `workflows/` and `platform/agents/registry/` reference these schemas by
  path for step input/output shapes and manifest validation.
