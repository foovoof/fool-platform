/**
 * domain/report.ts
 *
 * Report is the pure domain model for the human-reviewed, publishable
 * synthesis of an Investigation's findings. Per the Human Accountability
 * principle, a Report may only transition to `active` (published) status
 * once it has both an author and a reviewer recorded — the platform may
 * draft and organize a report, but it never publishes on its own authority.
 *
 * Mirrors contracts/domain/report.schema.json field-for-field.
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

export interface ReportInit {
  readonly investigationRef: Reference;
  readonly caseRef: Reference;
  readonly title: string;
  readonly summary: string;
  readonly authoredBy: string;
  readonly reviewedBy?: string;
  readonly findingRefs?: ReadonlyArray<Reference>;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly confidence?: ConfidenceScore;
  readonly publishedAt?: Timestamp;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Report is an immutable, human-authored synthesis document scoped to one Investigation. */
export class Report {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly investigationRef: Reference;
  readonly caseRef: Reference;
  readonly title: string;
  readonly summary: string;
  readonly authoredBy: string;
  readonly reviewedBy?: string;
  readonly findingRefs: ReadonlyArray<Reference>;
  readonly confidence?: ConfidenceScore;
  readonly publishedAt?: Timestamp;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: ReportInit) {
    if (init.authoredBy.trim().length === 0) {
      throw new DomainInvariantError("Report.authoredBy must not be empty: reports may never be authorless.");
    }
    if (init.status === Status.Active && init.reviewedBy === undefined) {
      throw new DomainInvariantError("Report cannot reach 'active' status without a recorded reviewedBy.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Draft;
    this.classification = init.classification ?? ClassificationLevel.Confidential;
    this.investigationRef = init.investigationRef;
    this.caseRef = init.caseRef;
    this.title = init.title;
    this.summary = init.summary;
    this.authoredBy = init.authoredBy;
    this.reviewedBy = init.reviewedBy;
    this.findingRefs = freezeRefs(init.findingRefs);
    this.confidence = init.confidence;
    this.publishedAt = init.publishedAt;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static draft(init: Omit<ReportInit, "status" | "publishedAt" | "reviewedBy">): Report {
    const timestamp = now();
    return new Report(newId(), "1.0.0", timestamp, timestamp, { ...init, status: Status.Draft });
  }

  /** Returns a new, human-reviewed Report; does not publish it. */
  withReview(reviewedBy: string): Report {
    if (reviewedBy.trim().length === 0) {
      throw new DomainInvariantError("withReview() requires a non-empty reviewer identity.");
    }
    return new Report(this.id, this.version, this.createdAt, now(), {
      investigationRef: this.investigationRef,
      caseRef: this.caseRef,
      title: this.title,
      summary: this.summary,
      authoredBy: this.authoredBy,
      reviewedBy,
      findingRefs: this.findingRefs,
      status: Status.UnderReview,
      classification: this.classification,
      confidence: this.confidence,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }

  /** Returns a new, published Report. Requires that a reviewer was already recorded. */
  publish(publishedAt: Timestamp = now()): Report {
    if (this.reviewedBy === undefined) {
      throw new DomainInvariantError("Report cannot be published before withReview() records a human reviewer.");
    }
    return new Report(this.id, this.version, this.createdAt, now(), {
      investigationRef: this.investigationRef,
      caseRef: this.caseRef,
      title: this.title,
      summary: this.summary,
      authoredBy: this.authoredBy,
      reviewedBy: this.reviewedBy,
      findingRefs: this.findingRefs,
      status: Status.Active,
      classification: this.classification,
      confidence: this.confidence,
      publishedAt,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }
}
