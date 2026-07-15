# Data Dictionary — Evidence

Source of truth for wire shape: `contracts/domain/evidence.schema.json`.
Source of truth for in-process shape: `domain/evidence.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the evidence item. | `4d5e6f7a-8b9c-4d1e-9f0a-1b2c3d4e5f6a` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Record creation time. | `2026-07-15T09:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T09:00:00Z` |
| `status` | enum(status) | yes | no | yes | Lifecycle status. | `active` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification; defaults to `restricted`. | `restricted` |
| `evidence_type` | enum | yes | no | no | Kind of artifact. | `document` |
| `description` | string | no | no | yes | Human-readable description. | `Public business registry extract` |
| `content_ref` | uri | no | no | yes | Pointer to the stored artifact (no storage engine in this phase). | `https://evidence.fool-platform.dev/...` |
| `content_hash` | string | no | no | no | Integrity hash of the content. | `sha256:9f86d0...` |
| `collected_at` | timestamp | yes | no | no | When the evidence was collected; must not be in the future. | `2026-07-15T08:30:00Z` |
| `source_ref` | Reference | yes | no | no | The single Source this evidence was collected from. | `{ref_id: ..., ref_type: "source"}` |
| `identity_refs` | array<Reference> | no | no | yes | Identities this evidence supports. | `[]` |
| `entity_refs` | array<Reference> | no | no | yes | Entities this evidence supports. | `[]` |
| `chain_of_custody_refs` | array<Reference> | no | no | yes | Linked ChainOfCustody records. | `[]` |
| `confidence` | ConfidenceRef | no | no | yes | Confidence in the evidence's content. | score 0.95, level `very_high` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "research-agent"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `["registry"]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
