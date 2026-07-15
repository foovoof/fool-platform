# Data Dictionary — Report

Source of truth for wire shape: `contracts/domain/report.schema.json`.
Source of truth for in-process shape: `domain/report.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `id` | uuid | yes | yes | no | Canonical identifier of the report. | `7a8b9c0d-1e2f-4a3b-9c0d-1e2f3a4b5c6d` |
| `version` | semver string | yes | no | no | Schema version. | `1.0.0` |
| `created_at` | timestamp | yes | no | no | Creation time. | `2026-07-15T10:00:00Z` |
| `updated_at` | timestamp | yes | no | yes | Last modification time. | `2026-07-15T10:00:00Z` |
| `status` | enum(status) | yes | no | yes | `draft` → `under_review` → `active`; `active` requires `reviewed_by`. | `under_review` |
| `classification` | enum(classificationLevel) | no | no | yes | Sensitivity classification. | `confidential` |
| `investigation_ref` | Reference | yes | no | no | Source investigation. | `{ref_id: ..., ref_type: "investigation"}` |
| `case_ref` | Reference | yes | no | no | Owning case. | `{ref_id: ..., ref_type: "case"}` |
| `title` | string | yes | no | yes | Report title. | `Identity resolution findings — Case-2026-0142` |
| `summary` | string | yes | no | yes | Publishable summary text. | `The reported email and phone...` |
| `finding_refs` | array<Reference> | no | no | yes | Findings synthesized into this report. | `[]` |
| `authored_by` | string | yes | no | no | Human author; must not be empty. | `analyst.jane@fool-platform.dev` |
| `reviewed_by` | string | no | no | yes | Human reviewer; required before `active`. | `analyst.lead@fool-platform.dev` |
| `published_at` | timestamp | no | no | yes | Set when status becomes `active`. | `2026-07-15T11:00:00Z` |
| `confidence` | ConfidenceRef | no | no | yes | Aggregate confidence across cited findings. | score 0.8, level `high` |
| `provenance` | Provenance | no | no | no | Origin/lineage. | `origin: "reporting-agent"` |
| `tags` | array<string> | no | yes (per item) | yes | Free-form labels. | `[]` |
| `metadata` | object | no | no | yes | Extension-owned attributes. | `{}` |
