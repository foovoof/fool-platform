# Data Dictionary — Event

Source of truth for wire shape: `contracts/agent/agent-event.schema.json`.
Source of truth for in-process shape: `domain/event.ts`.

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `event_id` / `id` | uuid | yes | yes | no | Canonical identifier of the event. | `d4e5f6a7-b8c9-4d1e-9f0a-1b2c3d4e5f6a` |
| `event_type` | dotted string | yes | no | no | Namespaced, versionable event name. | `agent.task.completed` |
| `version` | semver string | yes | no | no | Event schema version. | `1.0.0` |
| `subject_ref` / `task_id` | Reference | yes | no | no | The object the event happened to. | `{ref_id: ..., ref_type: "agent-task"}` |
| `trace_id` | uuid | no | no | no | Correlates events across one causal chain. | `9c0d1e2f-3a4b-4c5d-9e0f-1a2b3c4d5e6f` |
| `payload` | object | no | no | no | Event-type-specific data. | `{result_id: ...}` |
| `occurred_at` | timestamp | yes | no | no | When the event happened; events are never updated after creation. | `2026-07-15T09:12:00Z` |
| `metadata` | object | no | no | no | Extension-owned attributes. | `{}` |
