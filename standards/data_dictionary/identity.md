# Data Dictionary — Identity

Source of truth for wire shape: `contracts/domain/identity.schema.json`.
Source of truth for in-process shape: `domain/identity.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the identity. | `b7e2b3d0-5c3f-4a9e-9b8b-2e7f1a6c9d10` |
| `version` | semver string | yes | no | no | Schema version this record conforms to. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | When the identity was first created. | `2026-07-15T09:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | When the identity was last modified. | `2026-07-15T09:00:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification. | `internal` |
| `display_label` | string | no | no | yes | Non-authoritative human-readable label. | `Identity-4471` |
| `identifiers` | array<Identifier> | yes | no | yes (append-only in practice) | Resolved observable identifiers; at least one required. | see schema example |
| `identifiers[].identifier_type` | enum | yes | no | no | Kind of identifier. | `email` |
| `identifiers[].value` | string | yes | no | no | The identifier's literal value. | `j.doe@example.com` |
| `identifiers[].confidence` | ConfidenceRef | yes | no | no | Confidence that this identifier belongs to the identity. | score 0.92, level `high` |
| `entity_refs` | array<Reference> | no | no | yes | Entities this identity points to. | `[{ref_id: ..., ref_type: "entity"}]` |
| `evidence_refs` | array<Reference> | no | no | yes | Evidence supporting the identity as a whole. | `[]` |
| `confidence` | ConfidenceRef | no | no | yes | Aggregate confidence in the identity resolution. | score 0.85, level `high` |
| `provenance` | Provenance | no | no | no | Origin/lineage of the identity record. | `origin: "investigation-workflow"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `["priority"]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
