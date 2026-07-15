# Data Dictionary — Workflow

Source of truth: `contracts/workflow/workflow-definition.schema.json`,
`contracts/workflow/workflow-execution.schema.json`,
`contracts/workflow/workflow-state.schema.json`.

## WorkflowDefinition

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `workflow_id` | string | yes | yes | no | Canonical dotted identifier. | `wf.research.v1` |
| `name` | string | yes | no | yes | Human-readable name. | `Research Workflow` |
| `version` | semver string | yes | no | no | Definition version. | `1.0.0` |
| `description` | string | yes | no | yes | What the workflow accomplishes. | `Enumerates candidate public sources.` |
| `steps` | array<WorkflowStep> | yes | no | yes (new version on change) | Ordered/graph-connected units of work. | see `workflows/research.yaml` |
| `transitions` | array<WorkflowTransition> | no | no | yes | Edges between steps. | `[]` |
| `retry_policy` | RetryPolicy | no | no | yes | Default retry behavior. | `max_attempts: 3` |
| `timeout_policy` | TimeoutPolicy | no | no | yes | Default time budget. | `duration_seconds: 300` |
| `failure_policy` | FailurePolicy | no | no | yes | Behavior on exhausted retries. | `on_failure: escalate_to_human` |
| `termination_conditions` | array<TerminationCondition> | no | no | yes | Conditions that end the execution. | `[]` |
| `required_agents` | array<string> | yes | no | yes | agent_type values required. | `["research"]` |
| `required_capabilities` | array<string> | yes | no | yes | Capability ids required. | `["research"]` |

## WorkflowExecution

| Field | Type | Required | Unique | Mutable | Description | Example |
|---|---|---|---|---|---|---|
| `workflow_execution_id` | uuid | yes | yes | no | Identifier of this run. | `a1b2c3d4-e5f6-4a1b-8c9d-0e1f2a3b4c5d` |
| `workflow_id` | string | yes | no | no | Definition this run invokes. | `wf.research.v1` |
| `case_id` | uuid | yes | no | no | Owning case. | `5e6f7a8b-9c0d-4e1f-9a0b-1c2d3e4f5a6b` |
| `status` | enum | yes | no | yes | `pending`\|`running`\|`completed`\|`failed`\|`cancelled`. | `running` |
| `state` | WorkflowState | no | no | yes | Current step-state snapshot. | see schema |
| `started_at` | timestamp | yes | no | no | Run start time. | `2026-07-15T09:05:00Z` |
