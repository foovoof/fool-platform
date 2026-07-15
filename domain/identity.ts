/**
 * domain/identity.ts
 *
 * Identity is the central aggregation point of the FOOL Platform domain
 * model, per the Identity-Centric Architecture principle. It resolves a set
 * of observable identifiers (email, phone, username, IP, wallet address,
 * etc.) into a single subject of interest, and is the anchor that Entities,
 * Evidence, and Findings reference directly or indirectly.
 *
 * Mirrors contracts/domain/identity.schema.json field-for-field.
 *
 * Domain Purity: standard runtime and sibling domain modules only.
 */

import {
  Status,
  createProvenance,
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

export enum IdentifierType {
  Email = "email",
  Phone = "phone",
  Username = "username",
  Domain = "domain",
  IpAddress = "ip_address",
  Hash = "hash",
  WalletAddress = "wallet_address",
  Document = "document",
  Image = "image",
  PersonName = "person_name",
  Other = "other",
}

export interface IdentifierInit {
  readonly identifierType: IdentifierType;
  readonly value: string;
  readonly confidence: ConfidenceScore;
  readonly sourceRefs?: ReadonlyArray<Reference>;
}

export interface Identifier extends IdentifierInit {
  readonly sourceRefs: ReadonlyArray<Reference>;
}

export interface IdentityInit {
  readonly identifiers: ReadonlyArray<IdentifierInit>;
  readonly displayLabel?: string;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly entityRefs?: ReadonlyArray<Reference>;
  readonly evidenceRefs?: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/**
 * Identity is an immutable aggregate of resolved identifiers. Every mutation
 * (adding an identifier, linking an entity) returns a new Identity rather
 * than modifying the existing instance, preserving referential history.
 */
export class Identity {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly displayLabel?: string;
  readonly identifiers: ReadonlyArray<Identifier>;
  readonly entityRefs: ReadonlyArray<Reference>;
  readonly evidenceRefs: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(
    id: Id,
    version: string,
    createdAt: Timestamp,
    updatedAt: Timestamp,
    init: IdentityInit
  ) {
    if (init.identifiers.length === 0) {
      throw new Error("Identity must be created with at least one identifier.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Internal;
    this.displayLabel = init.displayLabel;
    this.identifiers = Object.freeze(
      init.identifiers.map((i) => ({ ...i, sourceRefs: freezeRefs(i.sourceRefs) }))
    );
    this.entityRefs = freezeRefs(init.entityRefs);
    this.evidenceRefs = freezeRefs(init.evidenceRefs);
    this.confidence = init.confidence;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static create(init: IdentityInit): Identity {
    const timestamp = now();
    return new Identity(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** Returns a new Identity with the given identifier appended. */
  withIdentifier(identifier: IdentifierInit): Identity {
    return new Identity(this.id, this.version, this.createdAt, now(), {
      identifiers: [...this.identifiers, identifier],
      displayLabel: this.displayLabel,
      status: this.status,
      classification: this.classification,
      entityRefs: this.entityRefs,
      evidenceRefs: this.evidenceRefs,
      confidence: this.confidence,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }

  /** Returns a new Identity linked to the given Entity reference. */
  withEntityRef(entityRef: Reference): Identity {
    if (this.entityRefs.some((ref) => ref.refId === entityRef.refId)) {
      return this;
    }
    return new Identity(this.id, this.version, this.createdAt, now(), {
      identifiers: this.identifiers,
      displayLabel: this.displayLabel,
      status: this.status,
      classification: this.classification,
      entityRefs: [...this.entityRefs, entityRef],
      evidenceRefs: this.evidenceRefs,
      confidence: this.confidence,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }

  hasIdentifierValue(value: string): boolean {
    return this.identifiers.some((identifier) => identifier.value === value);
  }
}

/** Convenience factory mirroring createProvenance for callers assembling an Identity inline. */
export function openIdentity(
  origin: string,
  identifiers: ReadonlyArray<IdentifierInit>,
  options: Omit<IdentityInit, "identifiers" | "provenance"> = {}
): Identity {
  return Identity.create({ ...options, identifiers, provenance: createProvenance(origin) });
}
