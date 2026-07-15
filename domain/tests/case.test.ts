import { describe, expect, it } from "vitest";
import { Case } from "../case.js";
import { createProvenance, reference } from "../common.js";

describe("Case creation", () => {
  it("opens a case with a title and an accountable owner", () => {
    const openedCase = Case.open({
      title: "Case-2026-0142",
      owner: "analyst.lead@fool-platform.dev",
      provenance: createProvenance("case-intake"),
    });
    expect(openedCase.status).toBe("active");
    expect(openedCase.owner).toBe("analyst.lead@fool-platform.dev");
  });

  it("rejects a case without an owner", () => {
    expect(() =>
      Case.open({ title: "Untitled", owner: "", provenance: createProvenance("case-intake") })
    ).toThrow(/accountable human owner/);
  });

  it("close() returns a new archived instance and rejects double-closing", () => {
    const openedCase = Case.open({ title: "Case-A", owner: "owner@fool-platform.dev", provenance: createProvenance("case-intake") });
    const closedCase = openedCase.close();
    expect(closedCase.status).toBe("archived");
    expect(closedCase.closedAt).toBeTruthy();
    expect(() => closedCase.close()).toThrow(/already closed/);
  });

  it("withInvestigationRef attaches without duplication", () => {
    const openedCase = Case.open({ title: "Case-B", owner: "owner@fool-platform.dev", provenance: createProvenance("case-intake") });
    const ref = reference(crypto.randomUUID(), "investigation");
    const withInvestigation = openedCase.withInvestigationRef(ref);
    expect(withInvestigation.withInvestigationRef(ref)).toBe(withInvestigation);
  });
});
