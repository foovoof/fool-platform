/**
 * testing/architecture/required_files_present.test.ts
 *
 * Architecture test: Phase 1 declares a fixed set of layers and files that
 * must exist for the foundation to be considered complete. This test
 * enumerates that manifest explicitly so that a missing file fails CI
 * rather than being silently forgotten.
 */
import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = join(import.meta.dirname, "..", "..");

const REQUIRED_FILES = [
  "README.md",
  "contracts/README.md",
  "contracts/common/common-defs.schema.json",
  "contracts/domain/identity.schema.json",
  "contracts/domain/entity.schema.json",
  "contracts/domain/relationship.schema.json",
  "contracts/domain/evidence.schema.json",
  "contracts/domain/source.schema.json",
  "contracts/domain/case.schema.json",
  "contracts/domain/investigation.schema.json",
  "contracts/domain/report.schema.json",
  "contracts/agent/agent-task.schema.json",
  "contracts/agent/agent-context.schema.json",
  "contracts/agent/agent-error.schema.json",
  "contracts/agent/agent-capability.schema.json",
  "contracts/agent/agent-manifest.schema.json",
  "contracts/agent/agent-result.schema.json",
  "contracts/agent/agent-event.schema.json",
  "contracts/workflow/retry-policy.schema.json",
  "contracts/workflow/timeout-policy.schema.json",
  "contracts/workflow/failure-policy.schema.json",
  "contracts/workflow/termination-condition.schema.json",
  "contracts/workflow/checkpoint.schema.json",
  "contracts/workflow/workflow-step.schema.json",
  "contracts/workflow/workflow-transition.schema.json",
  "contracts/workflow/workflow-definition.schema.json",
  "contracts/workflow/workflow-state.schema.json",
  "contracts/workflow/workflow-execution.schema.json",
  "contracts/confidence/confidence-model.schema.json",
  "contracts/confidence/scoring-model.schema.json",
  "contracts/confidence/source-reliability.schema.json",
  "contracts/confidence/evidence-confidence.schema.json",
  "contracts/confidence/entity-confidence.schema.json",
  "contracts/confidence/relationship-confidence.schema.json",
  "contracts/confidence/finding-confidence.schema.json",
  "contracts/confidence/investigation-confidence.schema.json",
  "domain/README.md",
  "domain/common.ts",
  "domain/identity.ts",
  "domain/entity.ts",
  "domain/relationship.ts",
  "domain/evidence.ts",
  "domain/source.ts",
  "domain/case.ts",
  "domain/investigation.ts",
  "domain/report.ts",
  "domain/finding.ts",
  "domain/event.ts",
  "domain/timeline.ts",
  "domain/annotation.ts",
  "domain/chain_of_custody.ts",
  "domain/confidence_score.ts",
  "domain/classification_level.ts",
  "standards/README.md",
  "standards/concepts/identity.yaml",
  "standards/concepts/entity.yaml",
  "standards/concepts/relationship.yaml",
  "standards/concepts/evidence.yaml",
  "standards/concepts/source.yaml",
  "standards/concepts/finding.yaml",
  "standards/concepts/investigation.yaml",
  "standards/concepts/case.yaml",
  "standards/concepts/report.yaml",
  "standards/concepts/workflow.yaml",
  "standards/concepts/event.yaml",
  "standards/data_dictionary/identity.md",
  "standards/data_dictionary/entity.md",
  "standards/data_dictionary/relationship.md",
  "standards/data_dictionary/evidence.md",
  "standards/data_dictionary/source.md",
  "standards/data_dictionary/finding.md",
  "standards/data_dictionary/report.md",
  "standards/data_dictionary/investigation.md",
  "standards/data_dictionary/workflow.md",
  "standards/data_dictionary/event.md",
  "standards/data_dictionary/case.md",
  "platform/agents/registry/README.md",
  "platform/agents/registry/agents.yaml",
  "platform/agents/registry/capabilities.yaml",
  "workflows/README.md",
  "workflows/research.yaml",
  "workflows/extraction.yaml",
  "workflows/discovery.yaml",
  "workflows/investigation.yaml",
  "workflows/reporting.yaml",
  "workflows/monitoring.yaml",
];

describe("Required Phase 1 files", () => {
  it.each(REQUIRED_FILES)("%s exists", (relativePath) => {
    expect(existsSync(join(ROOT, relativePath)), `missing required file: ${relativePath}`).toBe(true);
  });
});
