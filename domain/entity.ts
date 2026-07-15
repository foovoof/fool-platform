/**
 * domain/entity.ts
 *
 * Entity is the pure domain model for a typed node in the knowledge graph —
 * a person, organization, device, account, location, or asset — distinct
 * from Identity, which aggregates the identifiers that resolve to a subject.
 * An Entity may optionally point back to the Identity it belongs to.
 *
 * Mirrors contracts/domain/entity.schema.json field-for-field.
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

export enum EntityType {
  Person = "person",
  Organization = "organization",
  Device = "device",
  Account = "account",
  Location = "location",
  Asset = "asset",
  Document = "document",
  Other = "other",
}

export interface EntityInit {
  readonly entityType: EntityType;
  readonly name?: string;
  readonly identityRef?: Reference;
  readonly attributes?: Metadata;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly relationshipRefs?: ReadonlyArray<Reference>;
  readonly evidenceRefs?: ReadonlyArray<Reference>;
  readonly sourceRefs?: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/**
 * Entity is an immutable node in the knowledge graph. Relationship
 * attachments are tracked by reference only; the Entity itself never holds
 * a live pointer to a Relationship instance, preserving layer boundaries.
 */
export class Entity {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly entityType: EntityType;
  readonly name?: string;
  readonly identityRef?: Reference;
  readonly attributes: Metadata;
  readonly relationshipRefs: ReadonlyArray<Reference>;
  readonly evidenceRefs: ReadonlyArray<Reference>;
  readonly sourceRefs: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: EntityInit) {
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Internal;
    this.entityType = init.entityType;
    this.name = init.name;
    this.identityRef = init.identityRef;
    this.attributes = init.attributes ?? EMPTY_METADATA;
    this.relationshipRefs = freezeRefs(init.relationshipRefs);
    this.evidenceRefs = freezeRefs(init.evidenceRefs);
    this.sourceRefs = freezeRefs(init.sourceRefs);
    this.confidence = init.confidence;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static create(init: EntityInit): Entity {
    const timestamp = now();
    return new Entity(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** Returns a new Entity with the given relationship reference attached. */
  withRelationshipRef(relationshipRef: Reference): Entity {
    if (this.relationshipRefs.some((ref) => ref.refId === relationshipRef.refId)) {
      return this;
    }
    return new Entity(this.id, this.version, this.createdAt, now(), {
      entityType: this.entityType,
      name: this.name,
      identityRef: this.identityRef,
      attributes: this.attributes,
      status: this.status,
      classification: this.classification,
      relationshipRefs: [...this.relationshipRefs, relationshipRef],
      evidenceRefs: this.evidenceRefs,
      sourceRefs: this.sourceRefs,
      confidence: this.confidence,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }
}
