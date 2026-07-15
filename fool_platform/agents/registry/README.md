# Agent Registry

This directory is the canonical, data-only registry of agent types and
capabilities recognized by the FOOL Platform. It contains no executable
agent logic — agent runtimes, orchestration, and execution are Phase 2
concerns layered on top of this registry.

## Files

- `capabilities.yaml` — the capabilities an agent can claim to implement,
  each with an id, version, description, and the contract schemas its
  input/output must conform to.
- `agents.yaml` — the agent types known to the platform, each declaring
  which capability ids (from `capabilities.yaml`) it implements.

## How this is consulted

A `WorkflowDefinition` (see `contracts/workflow/workflow-definition.schema.json`
and `workflows/`) declares `required_agents` and `required_capabilities` by
id. Workflow validation cross-checks those ids against this registry to
confirm every step's requirements can be satisfied by at least one
registered agent type before the workflow is considered valid — see
`testing/architecture/workflow_registry_consistency.test.ts`.

## Adding a new agent type or capability

1. Add the capability to `capabilities.yaml` first, with a schema reference
   for both its input and output shape (usually `agent-task.schema.json` and
   a domain or agent contract schema).
2. Add or update the agent type in `agents.yaml`, referencing the
   capability id.
3. Re-run `pnpm test:architecture` to confirm consistency with any
   workflows that reference the new capability.
