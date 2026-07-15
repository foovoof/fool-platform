# Workflow Definitions

This directory holds `WorkflowDefinition` documents — pure, declarative data
conforming to `contracts/workflow/workflow-definition.schema.json`. Per the
Workflow-Driven Execution principle, **no runtime executor exists in this
repository**: these files describe steps, transitions, retry/timeout/failure
policies, and termination conditions, and are meant to be consumed by an
execution engine built in a later phase.

## Files

| File | workflow_id | Purpose |
|---|---|---|
| `research.yaml` | `wf.research.v1` | Enumerate and rank candidate public sources. |
| `extraction.yaml` | `wf.extraction.v1` | Collect Evidence from one identified Source. |
| `discovery.yaml` | `wf.discovery.v1` | Propose candidate Entities and Relationships. |
| `investigation.yaml` | `wf.investigation.v1` | Synthesize Findings with confidence rationale. |
| `reporting.yaml` | `wf.reporting.v1` | Draft a human-reviewable Report. |
| `monitoring.yaml` | `wf.monitoring.v1` | Re-check a monitored subject on a schedule. |

## Conventions

- `workflow_id` is a dotted, versioned identifier (`wf.<name>.v<n>`); a
  breaking change to a workflow's shape requires bumping the version and
  keeping the prior file for any in-flight executions.
- `required_agents` and `required_capabilities` must reference ids present
  in `platform/agents/registry/agents.yaml` and `capabilities.yaml`. This is
  enforced by `testing/architecture/workflow_registry_consistency.test.ts`.
- Every workflow that can produce a human-facing artifact (Report,
  published Finding) must route through an explicit human step or defer
  publication outside the workflow — see `reporting.yaml`.
- `failure_policy.on_failure: escalate_to_human` is the default; only
  `monitoring.yaml` uses `retry_with_backoff`, because a missed monitoring
  tick is not itself an actionable failure.
