import { describe, expect, it } from "vitest";
import { Investigation } from "../investigation.js";
import { createProvenance, reference } from "../common.js";

describe("Investigation creation", () => {
  const caseRef = reference(crypto.randomUUID(), "case");

  it("opens an investigation with a non-empty objective", () => {
    const investigation = Investigation.open({
      caseRef,
      title: "Resolve subject identity",
      objective: "Confirm whether the reported identifiers resolve to one person.",
      provenance: createProvenance("case-intake"),
    });
    expect(investigation.caseRef).toBe(caseRef);
    expect(investigation.status).toBe("active");
  });

  it("rejects an investigation without an objective", () => {
    expect(() =>
      Investigation.open({ caseRef, title: "No objective", objective: "   ", provenance: createProvenance("case-intake") })
    ).toThrow(/stated objective/);
  });

  it("withFindingRef attaches without duplication", () => {
    const investigation = Investigation.open({
      caseRef,
      title: "Resolve subject identity",
      objective: "Confirm identity resolution.",
      provenance: createProvenance("case-intake"),
    });
    const findingRef = reference(crypto.randomUUID(), "finding");
    const withFinding = investigation.withFindingRef(findingRef);
    expect(withFinding.withFindingRef(findingRef)).toBe(withFinding);
  });
});
