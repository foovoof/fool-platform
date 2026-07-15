import { describe, expect, it } from "vitest";
import { openIdentity, Identity, IdentifierType } from "../identity.js";
import { ConfidenceScore } from "../confidence_score.js";
import { reference } from "../common.js";

function sampleIdentifier() {
  return {
    identifierType: IdentifierType.Email,
    value: "j.doe@example.com",
    confidence: ConfidenceScore.create({ score: 0.9, method: "manual_review" }),
  };
}

describe("Identity creation", () => {
  it("creates an identity with at least one identifier", () => {
    const identity = openIdentity("test-suite", [sampleIdentifier()]);
    expect(identity.id).toBeTruthy();
    expect(identity.identifiers).toHaveLength(1);
    expect(identity.status).toBe("active");
  });

  it("rejects an identity with zero identifiers", () => {
    expect(() => openIdentity("test-suite", [])).toThrow(/at least one identifier/);
  });

  it("withIdentifier returns a new immutable instance", () => {
    const original = openIdentity("test-suite", [sampleIdentifier()]);
    const updated = original.withIdentifier({
      identifierType: IdentifierType.Phone,
      value: "+10000000000",
      confidence: ConfidenceScore.create({ score: 0.6, method: "manual_review" }),
    });
    expect(original.identifiers).toHaveLength(1);
    expect(updated.identifiers).toHaveLength(2);
    expect(updated).not.toBe(original);
  });

  it("withEntityRef is idempotent for the same reference", () => {
    const identity = openIdentity("test-suite", [sampleIdentifier()]);
    const ref = reference(crypto.randomUUID(), "entity");
    const once = identity.withEntityRef(ref);
    const twice = once.withEntityRef(ref);
    expect(twice.entityRefs).toHaveLength(1);
    expect(twice).toBe(once);
  });

  it("is frozen and cannot be mutated after construction", () => {
    const identity = openIdentity("test-suite", [sampleIdentifier()]);
    expect(() => {
      (identity as unknown as { status: string }).status = "archived";
    }).toThrow();
  });
});
