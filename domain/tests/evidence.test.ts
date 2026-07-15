import { describe, expect, it } from "vitest";
import { Evidence, EvidenceType } from "../evidence.js";
import { createProvenance, reference } from "../common.js";

describe("Evidence creation", () => {
  const sourceRef = reference(crypto.randomUUID(), "source");

  it("creates evidence referencing exactly one source", () => {
    const evidence = Evidence.create({
      evidenceType: EvidenceType.Document,
      collectedAt: "2026-01-01T08:30:00Z",
      sourceRef,
      contentHash: "sha256:abc123",
      provenance: createProvenance("research-agent"),
    });
    expect(evidence.sourceRef).toBe(sourceRef);
    expect(evidence.hasIntegrityHash()).toBe(true);
  });

  it("rejects evidence collected in the future", () => {
    const future = new Date(Date.now() + 86_400_000).toISOString();
    expect(() =>
      Evidence.create({
        evidenceType: EvidenceType.Document,
        collectedAt: future,
        sourceRef,
        provenance: createProvenance("research-agent"),
      })
    ).toThrow(/must not be in the future/);
  });

  it("defaults classification to restricted", () => {
    const evidence = Evidence.create({
      evidenceType: EvidenceType.Screenshot,
      collectedAt: "2026-01-01T08:30:00Z",
      sourceRef,
      provenance: createProvenance("research-agent"),
    });
    expect(evidence.classification.value).toBe("restricted");
  });
});
