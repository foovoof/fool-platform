# Data Dictionary — Entity

Source of truth for wire shape: `contracts/domain/entity.schema.json`.
Source of truth for in-process shape: `domain/entity.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the entity. | `1a2b3c4d-5e6f-4a1b-8c9d-0e1f2a3b4c5d` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T09:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T09:00:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification. | `internal` |
| `entity_type` | enum | yes | no | no | Kind of entity node. | `person` |
| `name` | string | no | no | yes | Human-readable name. | `J. Doe` |
| `identity_ref` | Reference | no | no | yes | Optional back-reference to an Identity. | `{ref_id: ..., ref_type: "identity"}` |
| `attributes` | object | no | no | yes | Typed, entity_type-specific attributes. | `{nationality: "unknown"}` |
| `relationship_refs` | array<Reference> | no | no | yes | Relationships this entity participates in. | `[]` |
| `evidence_refs` | array<Reference> | no | no | yes | Evidence about this entity. | `[]` |
| `source_refs` | array<Reference> | no | no | yes | Sources that produced this entity. | `[]` |
| `confidence` | ConfidenceRef | no | no | yes | Confidence in this entity's existence/attributes. | score 0.7, level `moderate` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "extraction-agent"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `[]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
