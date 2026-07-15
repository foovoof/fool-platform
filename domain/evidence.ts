/**
 * domain/evidence.ts
 *
 * Evidence is the pure domain model for a discrete, provenance-bearing
 * artifact collected from a Source in support of an Identity, Entity,
 * Relationship, or Finding. Evidence is the atomic unit of proof in the
 * platform: no assertion may exist without at least one evidence or source
 * reference, per the Provenance Everywhere principle.
 *
 * Mirrors contracts/domain/evidence.schema.json field-for-field.
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

export enum EvidenceType {
  Document = "document",
  Screenshot = "screenshot",
  DatasetRecord = "dataset_record",
  Message = "message",
  Transaction = "transaction",
  Media = "media",
  LogEntry = "log_entry",
  Other = "other",
}

export interface EvidenceInit {
  readonly evidenceType: EvidenceType;
  readonly collectedAt: Timestamp;
  readonly sourceRef: Reference;
  readonly description?: string;
  readonly contentRef?: string;
  readonly contentHash?: string;
  readonly identityRefs?: ReadonlyArray<Reference>;
  readonly entityRefs?: ReadonlyArray<Reference>;
  readonly chainOfCustodyRefs?: ReadonlyArray<Reference>;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Evidence is an immutable, provenance-bearing artifact referencing exactly one collecting Source. */
export class Evidence {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly evidenceType: EvidenceType;
  readonly description?: string;
  readonly contentRef?: string;
  readonly contentHash?: string;
  readonly collectedAt: Timestamp;
  readonly sourceRef: Reference;
  readonly identityRefs: ReadonlyArray<Reference>;
  readonly entityRefs: ReadonlyArray<Reference>;
  readonly chainOfCustodyRefs: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: EvidenceInit) {
    if (init.collectedAt > now()) {
      throw new DomainInvariantError("Evidence.collectedAt must not be in the future.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Restricted;
    this.evidenceType = init.evidenceType;
    this.description = init.description;
    this.contentRef = init.contentRef;
    this.contentHash = init.contentHash;
    this.collectedAt = init.collectedAt;
    this.sourceRef = init.sourceRef;
    this.identityRefs = freezeRefs(init.identityRefs);
    this.entityRefs = freezeRefs(init.entityRefs);
    this.chainOfCustodyRefs = freezeRefs(init.chainOfCustodyRefs);
    this.confidence = init.confidence;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static create(init: EvidenceInit): Evidence {
    const timestamp = now();
    return new Evidence(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** True if this evidence's integrity hash has been recorded. */
  hasIntegrityHash(): boolean {
    return this.contentHash !== undefined && this.contentHash.length > 0;
  }
}
