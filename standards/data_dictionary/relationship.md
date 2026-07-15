# Data Dictionary — Relationship

Source of truth for wire shape: `contracts/domain/relationship.schema.json`.
Source of truth for in-process shape: `domain/relationship.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the relationship. | `2b3c4d5e-6f7a-4b1c-9d0e-1f2a3b4c5d6e` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T09:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T09:00:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification. | `internal` |
| `relationship_type` | enum | yes | no | no | Kind of edge. | `employed_by` |
| `source_entity_ref` | Reference | yes | no | no | Origin endpoint entity. | `{ref_id: ..., ref_type: "entity"}` |
| `target_entity_ref` | Reference | yes | no | no | Destination endpoint entity; must differ from source. | `{ref_id: ..., ref_type: "entity"}` |
| `directional` | boolean | no | no | no | Whether the edge is directional. | `true` |
| `valid_from` | timestamp | no | no | yes | Start of temporal validity. | `2024-01-01T00:00:00Z` |
| `valid_to` | timestamp | no | no | yes | End of temporal validity; must not precede `valid_from`. | `null` |
| `evidence_refs` | array<Reference> | no | no | yes | Supporting evidence. | `[]` |
| `source_refs` | array<Reference> | no | no | yes | Contributing sources. | `[]` |
| `confidence` | ConfidenceRef | no | no | yes | Confidence in this specific edge. | score 0.6, level `moderate` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "investigation-agent"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `[]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
