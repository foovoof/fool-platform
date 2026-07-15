import { describe, expect, it } from "vitest";
import { Relationship, RelationshipType } from "../relationship.js";
import { createProvenance, reference } from "../common.js";

describe("Relationship creation", () => {
  const sourceRef = reference(crypto.randomUUID(), "entity");
  const targetRef = reference(crypto.randomUUID(), "entity");

  it("creates a relationship between two distinct entities", () => {
    const relationship = Relationship.create({
      relationshipType: RelationshipType.EmployedBy,
      sourceEntityRef: sourceRef,
      targetEntityRef: targetRef,
      provenance: createProvenance("investigation-agent"),
    });
    expect(relationship.directional).toBe(true);
    expect(relationship.involves(sourceRef)).toBe(true);
    expect(relationship.involves(targetRef)).toBe(true);
  });

  it("rejects a relationship whose endpoints are the same entity", () => {
    expect(() =>
      Relationship.create({
        relationshipType: RelationshipType.AssociatedWith,
        sourceEntityRef: sourceRef,
        targetEntityRef: sourceRef,
        provenance: createProvenance("investigation-agent"),
      })
    ).toThrow(/distinct entities/);
  });

  it("rejects a validTo earlier than validFrom", () => {
    expect(() =>
      Relationship.create({
        relationshipType: RelationshipType.AssociatedWith,
        sourceEntityRef: sourceRef,
        targetEntityRef: targetRef,
        validFrom: "2026-02-01T00:00:00Z",
        validTo: "2026-01-01T00:00:00Z",
        provenance: createProvenance("investigation-agent"),
      })
    ).toThrow(/must not precede/);
  });

  it("isValidAt respects the validity window", () => {
    const relationship = Relationship.create({
      relationshipType: RelationshipType.AssociatedWith,
      sourceEntityRef: sourceRef,
      targetEntityRef: targetRef,
      validFrom: "2026-01-01T00:00:00Z",
      validTo: "2026-06-01T00:00:00Z",
      provenance: createProvenance("investigation-agent"),
    });
    expect(relationship.isValidAt("2026-03-01T00:00:00Z")).toBe(true);
    expect(relationship.isValidAt("2027-01-01T00:00:00Z")).toBe(false);
  });
});
