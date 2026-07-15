import { describe, expect, it } from "vitest";
import { ConfidenceScore } from "../confidence_score.js";

describe("ConfidenceScore behavior", () => {
  it("derives a level band from the numeric score", () => {
    expect(ConfidenceScore.create({ score: 0.95, method: "m" }).level).toBe("very_high");
    expect(ConfidenceScore.create({ score: 0.75, method: "m" }).level).toBe("high");
    expect(ConfidenceScore.create({ score: 0.5, method: "m" }).level).toBe("moderate");
    expect(ConfidenceScore.create({ score: 0.2, method: "m" }).level).toBe("low");
    expect(ConfidenceScore.create({ score: 0.05, method: "m" }).level).toBe("very_low");
  });

  it("rejects scores outside [0, 1]", () => {
    expect(() => ConfidenceScore.create({ score: 1.5, method: "m" })).toThrow(RangeError);
    expect(() => ConfidenceScore.create({ score: -0.1, method: "m" })).toThrow(RangeError);
  });

  it("rejects an empty method name", () => {
    expect(() => ConfidenceScore.create({ score: 0.5, method: "" })).toThrow(/named scoring method/);
  });

  it("isUnsubstantiated is true only with no evidence and no source refs", () => {
    const bare = ConfidenceScore.create({ score: 0.5, method: "m" });
    expect(bare.isUnsubstantiated()).toBe(true);
  });

  it("combine() produces a weighted mean score", () => {
    const a = ConfidenceScore.create({ score: 0.8, method: "a" });
    const b = ConfidenceScore.create({ score: 0.4, method: "b" });
    const combined = a.combine(b, 0.5);
    expect(combined.score).toBeCloseTo(0.6, 5);
  });
});
