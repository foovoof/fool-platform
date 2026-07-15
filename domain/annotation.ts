/**
 * domain/annotation.ts
 *
 * Annotation is the pure domain model for a human-authored note attached to
 * any domain object (Entity, Evidence, Finding, etc.). Annotations are
 * distinct from Findings: an Annotation carries no confidence assessment
 * and asserts nothing about the world — it records an analyst's remark,
 * question, or context for other humans, preserving the Human Accountability
 * principle by keeping subjective commentary separate from evidenced claims.
 *
 * Domain Purity: standard runtime and sibling domain modules only.
 */

import { newId, now, type Id, type Reference, type Timestamp } from "./common.js";
import { DomainInvariantError } from "./common.js";

export interface AnnotationInit {
  readonly subjectRef: Reference;
  readonly authoredBy: string;
  readonly body: string;
  readonly createdAt?: Timestamp;
}

/** Annotation is an immutable, human-authored remark attached to a subject reference. */
export class Annotation {
  readonly id: Id;
  readonly subjectRef: Reference;
  readonly authoredBy: string;
  readonly body: string;
  readonly createdAt: Timestamp;

  private constructor(id: Id, init: AnnotationInit) {
    if (init.authoredBy.trim().length === 0) {
      throw new DomainInvariantError("Annotation.authoredBy must not be empty: every annotation must be attributable to a human.");
    }
    if (init.body.trim().length === 0) {
      throw new DomainInvariantError("Annotation.body must not be empty.");
    }
    this.id = id;
    this.subjectRef = init.subjectRef;
    this.authoredBy = init.authoredBy;
    this.body = init.body;
    this.createdAt = init.createdAt ?? now();
    Object.freeze(this);
  }

  static write(init: AnnotationInit): Annotation {
    return new Annotation(newId(), init);
  }
}
