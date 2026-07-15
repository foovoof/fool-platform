# Data Dictionary — Source

Source of truth for wire shape: `contracts/domain/source.schema.json`.
Source of truth for in-process shape: `domain/source.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the source. | `0c9b6f2a-4e6a-4a1a-9a8a-8f6c2b1d3e44` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T08:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T08:00:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification; defaults to `public`. | `public` |
| `source_type` | enum | yes | no | no | Kind of channel. | `public_registry` |
| `name` | string | yes | no | no | Human-readable name; must not be empty. | `National Business Registry` |
| `uri` | uri | no | no | yes | Canonical URI of the source. | `https://registry.example.gov` |
| `reliability` | ConfidenceRef | no | no | yes | Independent reliability assessment of this channel. | score 0.9, level `very_high` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "research-agent"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `["government"]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
