/**
 * testing/architecture/workflow_registry_consistency.test.ts
 *
 * Architecture test: every WorkflowDefinition's required_agents and
 * required_capabilities must resolve to entries actually present in the
 * platform/agents/registry. This keeps Workflow-Driven Execution honest —
 * a workflow that requires an agent type or capability nobody implements
 * is not executable and must fail this check before it can be merged.
 */
import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { load } from "js-yaml";

const ROOT = join(import.meta.dirname, "..", "..");
const WORKFLOWS_DIR = join(ROOT, "workflows");
const REGISTRY_DIR = join(ROOT, "platform", "agents", "registry");

interface AgentRegistryEntry {
  agent_type: string;
  capabilities: string[];
}
interface CapabilityRegistryEntry {
  id: string;
}
interface WorkflowDefinition {
  workflow_id: string;
  required_agents: string[];
  required_capabilities: string[];
  steps: Array<{ agent_type: string; capability: string }>;
}

function loadYaml<T>(path: string): T {
  return load(readFileSync(path, "utf-8")) as T;
}

const agents = loadYaml<{ agents: AgentRegistryEntry[] }>(join(REGISTRY_DIR, "agents.yaml")).agents;
const capabilities = loadYaml<{ capabilities: CapabilityRegistryEntry[] }>(
  join(REGISTRY_DIR, "capabilities.yaml")
).capabilities;

const knownAgentTypes = new Set(agents.map((a) => a.agent_type));
const knownCapabilityIds = new Set(capabilities.map((c) => c.id));

const workflowFiles = readdirSync(WORKFLOWS_DIR).filter((f) => f.endsWith(".yaml"));

describe("Workflow / registry consistency", () => {
  it("finds at least one workflow definition to check", () => {
    expect(workflowFiles.length).toBeGreaterThan(0);
  });

  it.each(workflowFiles)("%s only requires registered agent types", (file) => {
    const workflow = loadYaml<WorkflowDefinition>(join(WORKFLOWS_DIR, file));
    for (const agentType of workflow.required_agents) {
      expect(knownAgentTypes.has(agentType), `${file} requires unregistered agent_type "${agentType}"`).toBe(true);
    }
  });

  it.each(workflowFiles)("%s only requires registered capability ids", (file) => {
    const workflow = loadYaml<WorkflowDefinition>(join(WORKFLOWS_DIR, file));
    for (const capabilityId of workflow.required_capabilities) {
      expect(knownCapabilityIds.has(capabilityId), `${file} requires unregistered capability "${capabilityId}"`).toBe(true);
    }
  });

  it.each(workflowFiles)("%s: every step's agent_type actually implements its declared capability", (file) => {
    const workflow = loadYaml<WorkflowDefinition>(join(WORKFLOWS_DIR, file));
    for (const step of workflow.steps) {
      const agent = agents.find((a) => a.agent_type === step.agent_type);
      expect(agent, `${file} step references unregistered agent_type "${step.agent_type}"`).toBeTruthy();
      expect(
        agent!.capabilities.includes(step.capability),
        `${file} step's agent_type "${step.agent_type}" does not implement capability "${step.capability}"`
      ).toBe(true);
    }
  });
});
