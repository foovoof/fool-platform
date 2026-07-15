import { describe, expect, it } from "vitest";
import { Report } from "../report.js";
import { createProvenance, reference } from "../common.js";

describe("Report creation", () => {
  const investigationRef = reference(crypto.randomUUID(), "investigation");
  const caseRef = reference(crypto.randomUUID(), "case");

  it("drafts a report with an author and draft status", () => {
    const report = Report.draft({
      investigationRef,
      caseRef,
      title: "Identity resolution findings",
      summary: "Summary text.",
      authoredBy: "analyst.jane@fool-platform.dev",
      provenance: createProvenance("reporting-agent"),
    });
    expect(report.status).toBe("draft");
    expect(report.reviewedBy).toBeUndefined();
  });

  it("cannot publish before a human review is recorded", () => {
    const report = Report.draft({
      investigationRef,
      caseRef,
      title: "Findings",
      summary: "Summary.",
      authoredBy: "analyst.jane@fool-platform.dev",
      provenance: createProvenance("reporting-agent"),
    });
    expect(() => report.publish()).toThrow(/human reviewer/);
  });

  it("publishes only after withReview records a reviewer", () => {
    const report = Report.draft({
      investigationRef,
      caseRef,
      title: "Findings",
      summary: "Summary.",
      authoredBy: "analyst.jane@fool-platform.dev",
      provenance: createProvenance("reporting-agent"),
    });
    const reviewed = report.withReview("analyst.lead@fool-platform.dev");
    const published = reviewed.publish();
    expect(published.status).toBe("active");
    expect(published.publishedAt).toBeTruthy();
  });
});
