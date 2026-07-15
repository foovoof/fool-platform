import { describe, expect, it } from "vitest";
import { Entity, EntityType } from "../entity.js";
import { createProvenance, reference } from "../common.js";

describe("Entity creation", () => {
  it("creates an entity with a valid type and provenance", () => {
    const entity = Entity.create({
      entityType: EntityType.Person,
      name: "J. Doe",
      provenance: createProvenance("extraction-agent"),
    });
    expect(entity.entityType).toBe(EntityType.Person);
    expect(entity.status).toBe("active");
  });

  it("attaches relationship references without duplication", () => {
    const entity = Entity.create({ entityType: EntityType.Organization, provenance: createProvenance("extraction-agent") });
    const relRef = reference(crypto.randomUUID(), "relationship");
    const withRel = entity.withRelationshipRef(relRef);
    const withRelAgain = withRel.withRelationshipRef(relRef);
    expect(withRel.relationshipRefs).toHaveLength(1);
    expect(withRelAgain).toBe(withRel);
  });

  it("rejects empty provenance origin", () => {
    expect(() =>
      Entity.create({ entityType: EntityType.Device, provenance: createProvenance("") })
    ).toThrow(/must not be empty/);
  });
});
