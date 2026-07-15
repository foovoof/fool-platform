import { describe, expect, it } from "vitest";
import { Source, SourceType } from "../source.js";
import { ConfidenceScore } from "../confidence_score.js";
import { createProvenance } from "../common.js";

describe("Source creation", () => {
  it("creates a source without a reliability assessment yet", () => {
    const source = Source.create({
      sourceType: SourceType.PublicRegistry,
      name: "National Business Registry",
      provenance: createProvenance("research-agent"),
    });
    expect(source.isUnassessed()).toBe(true);
  });

  it("creates a source with a reliability assessment", () => {
    const source = Source.create({
      sourceType: SourceType.SearchEngine,
      name: "Example Search",
      reliability: ConfidenceScore.create({ score: 0.6, method: "institutional_authority" }),
      provenance: createProvenance("research-agent"),
    });
    expect(source.isUnassessed()).toBe(false);
    expect(source.reliability?.level).toBe("moderate");
  });

  it("rejects a source with an empty name", () => {
    expect(() =>
      Source.create({ sourceType: SourceType.Other, name: "  ", provenance: createProvenance("research-agent") })
    ).toThrow(/must not be empty/);
  });
});
