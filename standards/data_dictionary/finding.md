# Data Dictionary — Finding

Source of truth for in-process shape: `domain/finding.ts`.
Wire shape is expressed via the domain contracts referenced from a Finding
(`evidence_refs`, `entity_refs`, `relationship_refs`) plus
`contracts/confidence/finding-confidence.schema.json` for its confidence.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the finding. | `8c9d0e1f-2a3b-4c4d-9e0f-1a2b3c4d5e6f` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T09:30:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T09:30:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification; defaults to `confidential`. | `confidential` |
| `investigation_ref` | Reference | yes | no | no | The Investigation this finding belongs to. | `{ref_id: ..., ref_type: "investigation"}` |
| `statement` | string | yes | no | no | The conclusion in prose; must not be empty. | `Emails and phone resolve to one person.` |
| `confidence` | ConfidenceModel | yes | no | yes | Confidence assessment; `rationale` is mandatory for findings. | score 0.75, level `high` |
| `evidence_refs` | array<Reference> | no | no | yes | Supporting evidence. | `[]` |
| `entity_refs` | array<Reference> | no | no | yes | Supporting entities. | `[]` |
| `relationship_refs` | array<Reference> | no | no | yes | Supporting relationships. | `[]` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "investigation-agent"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `[]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
