/**
 * domain/relationship.ts
 *
 * Relationship is the pure domain model for a typed, evidence-backed edge in
 * the knowledge graph connecting two Entity references. A Relationship
 * carries its own confidence and optional temporal validity window,
 * independent of the confidence of either endpoint entity.
 *
 * Mirrors contracts/domain/relationship.schema.json field-for-field.
 *
 * Domain Purity: standard runtime and sibling domain modules only.
 */

import {
  Status,
  freezeRefs,
  freezeTags,
  newId,
  now,
  type Id,
  type Metadata,
  type Provenance,
  type Reference,
  type Timestamp,
  EMPTY_METADATA,
} from "./common.js";
import { ClassificationLevel } from "./classification_level.js";
import { ConfidenceScore } from "./confidence_score.js";
import { DomainInvariantError } from "./common.js";

export enum RelationshipType {
  AssociatedWith = "associated_with",
  Owns = "owns",
  EmployedBy = "employed_by",
  LocatedAt = "located_at",
  CommunicatesWith = "communicates_with",
  Controls = "controls",
  MemberOf = "member_of",
  TransactedWith = "transacted_with",
  Other = "other",
}

export interface RelationshipInit {
  readonly relationshipType: RelationshipType;
  readonly sourceEntityRef: Reference;
  readonly targetEntityRef: Reference;
  readonly directional?: boolean;
  readonly validFrom?: Timestamp;
  readonly validTo?: Timestamp;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly evidenceRefs?: ReadonlyArray<Reference>;
  readonly sourceRefs?: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Relationship is an immutable, typed edge between two entity references. */
export class Relationship {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly relationshipType: RelationshipType;
  readonly sourceEntityRef: Reference;
  readonly targetEntityRef: Reference;
  readonly directional: boolean;
  readonly validFrom?: Timestamp;
  readonly validTo?: Timestamp;
  readonly evidenceRefs: ReadonlyArray<Reference>;
  readonly sourceRefs: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: RelationshipInit) {
    if (init.sourceEntityRef.refId === init.targetEntityRef.refId) {
      throw new DomainInvariantError("Relationship.sourceEntityRef and targetEntityRef must reference distinct entities.");
    }
    if (init.validFrom !== undefined && init.validTo !== undefined && init.validTo < init.validFrom) {
      throw new DomainInvariantError("Relationship.validTo must not precede validFrom.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Internal;
    this.relationshipType = init.relationshipType;
    this.sourceEntityRef = init.sourceEntityRef;
    this.targetEntityRef = init.targetEntityRef;
    this.directional = init.directional ?? true;
    this.validFrom = init.validFrom;
    this.validTo = init.validTo;
    this.evidenceRefs = freezeRefs(init.evidenceRefs);
    this.sourceRefs = freezeRefs(init.sourceRefs);
    this.confidence = init.confidence;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static create(init: RelationshipInit): Relationship {
    const timestamp = now();
    return new Relationship(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** True if `entityRef` is either endpoint of this relationship. */
  involves(entityRef: Reference): boolean {
    return this.sourceEntityRef.refId === entityRef.refId || this.targetEntityRef.refId === entityRef.refId;
  }

  /** True if this relationship's validity window includes the given timestamp. */
  isValidAt(timestamp: Timestamp): boolean {
    if (this.validFrom !== undefined && timestamp < this.validFrom) return false;
    if (this.validTo !== undefined && timestamp > this.validTo) return false;
    return true;
  }
}
