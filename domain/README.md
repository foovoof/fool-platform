# Domain

This layer is the platform's pure business logic: immutable TypeScript
value objects and aggregates implementing the behavior of every object
declared in `contracts/domain/` (plus the supporting concepts `Finding`,
`Event`, `Timeline`, `Annotation`, `ChainOfCustody`, `ConfidenceScore`, and
`ClassificationLevel`).

## Domain Purity

Every file in this directory (excluding `tests/`) may import only:

- the TypeScript/JavaScript standard runtime (`crypto`, `Date`, etc.), and
- sibling modules within `domain/`.

It must never import from `platform/`, `intelligence/`, `ai/`, `data/`,
`infrastructure/`, `security/`, `apps/`, `connectors/`, or `tools/` — no
database client, no HTTP client, no AI SDK, no framework. This is enforced
mechanically by `domain/tests/domain_purity.test.ts` and again at the whole
repository level by `testing/architecture/`.

## Design conventions

- Every object is an immutable class: `Object.freeze(this)` at the end of
  the constructor, `readonly` fields throughout, and mutation-shaped
  operations (e.g. `withEntityRef`) return a *new* instance rather than
  mutating in place.
- Construction is always through a static factory (`create`, `open`,
  `draft`, `record`, `write`) rather than a public constructor, so that
  domain invariants (e.g. "a Case must have a non-empty owner", "a Finding's
  confidence must carry a rationale") are enforced at the single point of
  construction and cannot be bypassed.
- Confidence is never a bare boolean or bare number: every assessed field
  uses `ConfidenceScore`, which always pairs a `[0, 1]` score with a derived
  `ConfidenceLevel`, a named `method`, a timestamp, and optional evidence/
  source references.
- Every object that asserts something about the world carries a
  `Provenance` (origin, recording time, lineage, custody/source references)
  from `common.ts`; objects that are pure organizational containers (e.g.
  `Timeline`, `Annotation`) do not, since they assert nothing themselves.

## Files

| File | Mirrors |
|---|---|
| `common.ts` | `contracts/common/common-defs.schema.json` |
| `identity.ts` | `contracts/domain/identity.schema.json` |
| `entity.ts` | `contracts/domain/entity.schema.json` |
| `relationship.ts` | `contracts/domain/relationship.schema.json` |
| `evidence.ts` | `contracts/domain/evidence.schema.json` |
| `source.ts` | `contracts/domain/source.schema.json` |
| `case.ts` | `contracts/domain/case.schema.json` |
| `investigation.ts` | `contracts/domain/investigation.schema.json` |
| `report.ts` | `contracts/domain/report.schema.json` |
| `finding.ts` | (see `standards/concepts/finding.yaml`) |
| `event.ts` | `contracts/agent/agent-event.schema.json` (domain-level events) |
| `timeline.ts` | ordered view over `event.ts` references |
| `annotation.ts` | human commentary, distinct from `finding.ts` |
| `chain_of_custody.ts` | evidentiary custody trail for `evidence.ts` |
| `confidence_score.ts` | `contracts/confidence/confidence-model.schema.json` |
| `classification_level.ts` | `classificationLevel` in `common-defs.schema.json` |

## Tests

`domain/tests/*.test.ts` covers construction, invariant enforcement,
immutability, and the purity rule above for every module in this directory.
Run with `pnpm test:domain`.
