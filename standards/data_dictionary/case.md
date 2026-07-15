# Data Dictionary — Case

Source of truth for wire shape: `contracts/domain/case.schema.json`.
Source of truth for in-process shape: `domain/case.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the case. | `5e6f7a8b-9c0d-4e1f-9a0b-1c2d3e4f5a6b` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T07:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T07:00:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification; defaults to `confidential`. | `confidential` |
| `title` | string | yes | no | yes | Case title; must not be empty. | `Case-2026-0142` |
| `description` | string | no | no | yes | Free-text description. | `Fraud-pattern investigation...` |
| `priority` | enum | no | no | yes | `low`\|`normal`\|`high`\|`critical`. | `high` |
| `owner` | string | yes | no | yes | Accountable human owner; must not be empty. | `analyst.lead@fool-platform.dev` |
| `opened_at` | timestamp | yes | no | no | When the case was opened. | `2026-07-15T07:00:00Z` |
| `closed_at` | timestamp | no | no | yes | Set when the case is closed. | `null` |
| `identity_refs` | array<Reference> | no | no | yes | Identities in scope. | `[]` |
| `investigation_refs` | array<Reference> | no | no | yes | Investigations under this case. | `[]` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "case-intake"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `["fraud"]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
