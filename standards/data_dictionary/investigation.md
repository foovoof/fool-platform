# Data Dictionary — Investigation

Source of truth for wire shape: `contracts/domain/investigation.schema.json`.
Source of truth for in-process shape: `domain/investigation.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier. | `6f7a8b9c-0d1e-4f2a-9b0c-1d2e3f4a5b6c` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T07:15:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T07:15:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification. | `confidential` |
| `case_ref` | Reference | yes | no | no | Owning Case. | `{ref_id: ..., ref_type: "case"}` |
| `title` | string | yes | no | yes | Investigation title. | `Resolve subject identity` |
| `objective` | string | yes | no | no | Falsifiable objective; must not be empty. | `Confirm whether identifiers resolve to one person.` |
| `identity_refs` | array<Reference> | no | no | yes | Identities in scope. | `[]` |
| `entity_refs` | array<Reference> | no | no | yes | Entities in scope. | `[]` |
| `evidence_refs` | array<Reference> | no | no | yes | Evidence collected. | `[]` |
| `finding_refs` | array<Reference> | no | no | yes | Findings produced. | `[]` |
| `workflow_refs` | array<Reference> | no | no | yes | WorkflowExecutions that carried out the work. | `[]` |
| `confidence` | ConfidenceRef | no | no | yes | Confidence that the objective is satisfied. | score 0.5, level `moderate` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "case-intake"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `[]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
