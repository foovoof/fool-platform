/**
 * domain/investigation.ts
 *
 * Investigation is the pure domain model for a bounded unit of analytical
 * work within a Case, pursuing a specific stated objective. Investigations
 * aggregate the identities, entities, evidence, and findings produced by
 * workflow execution, without themselves executing any workflow logic.
 *
 * Mirrors contracts/domain/investigation.schema.json field-for-field.
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

export interface InvestigationInit {
  readonly caseRef: Reference;
  readonly title: string;
  readonly objective: string;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly identityRefs?: ReadonlyArray<Reference>;
  readonly entityRefs?: ReadonlyArray<Reference>;
  readonly evidenceRefs?: ReadonlyArray<Reference>;
  readonly findingRefs?: ReadonlyArray<Reference>;
  readonly workflowRefs?: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Investigation is an immutable, objective-driven unit of work scoped to a single Case. */
export class Investigation {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly caseRef: Reference;
  readonly title: string;
  readonly objective: string;
  readonly identityRefs: ReadonlyArray<Reference>;
  readonly entityRefs: ReadonlyArray<Reference>;
  readonly evidenceRefs: ReadonlyArray<Reference>;
  readonly findingRefs: ReadonlyArray<Reference>;
  readonly workflowRefs: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: InvestigationInit) {
    if (init.objective.trim().length === 0) {
      throw new DomainInvariantError("Investigation.objective must not be empty: no investigation may proceed without a stated objective.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Confidential;
    this.caseRef = init.caseRef;
    this.title = init.title;
    this.objective = init.objective;
    this.identityRefs = freezeRefs(init.identityRefs);
    this.entityRefs = freezeRefs(init.entityRefs);
    this.evidenceRefs = freezeRefs(init.evidenceRefs);
    this.findingRefs = freezeRefs(init.findingRefs);
    this.workflowRefs = freezeRefs(init.workflowRefs);
    this.confidence = init.confidence;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static open(init: InvestigationInit): Investigation {
    const timestamp = now();
    return new Investigation(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** Returns a new Investigation with the given finding reference attached. */
  withFindingRef(findingRef: Reference): Investigation {
    if (this.findingRefs.some((ref) => ref.refId === findingRef.refId)) {
      return this;
    }
    return new Investigation(this.id, this.version, this.createdAt, now(), {
      caseRef: this.caseRef,
      title: this.title,
      objective: this.objective,
      status: this.status,
      classification: this.classification,
      identityRefs: this.identityRefs,
      entityRefs: this.entityRefs,
      evidenceRefs: this.evidenceRefs,
      findingRefs: [...this.findingRefs, findingRef],
      workflowRefs: this.workflowRefs,
      confidence: this.confidence,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }
}
