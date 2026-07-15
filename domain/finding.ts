/**
 * domain/finding.ts
 *
 * Finding is the pure domain model for a single analytical conclusion drawn
 * from one or more pieces of Evidence within an Investigation. Findings are
 * conclusions, not raw observations: they must always carry a confidence
 * assessment with an explicit rationale, never a bare score.
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

export interface FindingInit {
  readonly investigationRef: Reference;
  readonly statement: string;
  readonly confidence: ConfidenceScore;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly evidenceRefs?: ReadonlyArray<Reference>;
  readonly entityRefs?: ReadonlyArray<Reference>;
  readonly relationshipRefs?: ReadonlyArray<Reference>;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Finding is an immutable, evidence-backed conclusion belonging to exactly one Investigation. */
export class Finding {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly investigationRef: Reference;
  readonly statement: string;
  readonly confidence: ConfidenceScore;
  readonly evidenceRefs: ReadonlyArray<Reference>;
  readonly entityRefs: ReadonlyArray<Reference>;
  readonly relationshipRefs: ReadonlyArray<Reference>;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: FindingInit) {
    if (init.statement.trim().length === 0) {
      throw new DomainInvariantError("Finding.statement must not be empty.");
    }
    if (init.confidence.rationale === undefined || init.confidence.rationale.trim().length === 0) {
      throw new DomainInvariantError("Finding.confidence must carry an explicit rationale; conclusions may never rest on a bare score.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Confidential;
    this.investigationRef = init.investigationRef;
    this.statement = init.statement;
    this.confidence = init.confidence;
    this.evidenceRefs = freezeRefs(init.evidenceRefs);
    this.entityRefs = freezeRefs(init.entityRefs);
    this.relationshipRefs = freezeRefs(init.relationshipRefs);
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static create(init: FindingInit): Finding {
    const timestamp = now();
    return new Finding(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** True when the finding rests on no evidence, relationship, or entity reference at all. */
  isUnsupported(): boolean {
    return this.evidenceRefs.length === 0 && this.entityRefs.length === 0 && this.relationshipRefs.length === 0;
  }
}
