/**
 * domain/case.ts
 *
 * Case is the pure domain model for the top-level administrative and
 * accountability container for platform work. A Case has a single
 * accountable human owner, per the Human Accountability principle: the
 * platform may assist, recommend, and organize, but it never removes a
 * human from final ownership of a case.
 *
 * Mirrors contracts/domain/case.schema.json field-for-field.
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
import { DomainInvariantError } from "./common.js";

export enum CasePriority {
  Low = "low",
  Normal = "normal",
  High = "high",
  Critical = "critical",
}

export interface CaseInit {
  readonly title: string;
  readonly owner: string;
  readonly description?: string;
  readonly priority?: CasePriority;
  readonly openedAt?: Timestamp;
  readonly closedAt?: Timestamp;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly identityRefs?: ReadonlyArray<Reference>;
  readonly investigationRefs?: ReadonlyArray<Reference>;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Case is an immutable accountability container that groups one or more Investigations. */
export class Case {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly title: string;
  readonly description?: string;
  readonly priority: CasePriority;
  readonly owner: string;
  readonly openedAt: Timestamp;
  readonly closedAt?: Timestamp;
  readonly identityRefs: ReadonlyArray<Reference>;
  readonly investigationRefs: ReadonlyArray<Reference>;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: CaseInit) {
    if (init.title.trim().length === 0) {
      throw new DomainInvariantError("Case.title must not be empty.");
    }
    if (init.owner.trim().length === 0) {
      throw new DomainInvariantError("Case.owner must not be empty: every case must have an accountable human owner.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Confidential;
    this.title = init.title;
    this.description = init.description;
    this.priority = init.priority ?? CasePriority.Normal;
    this.owner = init.owner;
    this.openedAt = init.openedAt ?? now();
    this.closedAt = init.closedAt;
    this.identityRefs = freezeRefs(init.identityRefs);
    this.investigationRefs = freezeRefs(init.investigationRefs);
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static open(init: CaseInit): Case {
    const timestamp = now();
    return new Case(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** Returns a new, closed Case. Throws if the case is already closed. */
  close(closedAt: Timestamp = now()): Case {
    if (this.status === Status.Archived) {
      throw new DomainInvariantError("Case is already closed/archived.");
    }
    return new Case(this.id, this.version, this.createdAt, now(), {
      title: this.title,
      owner: this.owner,
      description: this.description,
      priority: this.priority,
      openedAt: this.openedAt,
      closedAt,
      status: Status.Archived,
      classification: this.classification,
      identityRefs: this.identityRefs,
      investigationRefs: this.investigationRefs,
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }

  /** Returns a new Case with the given investigation reference attached. */
  withInvestigationRef(investigationRef: Reference): Case {
    if (this.investigationRefs.some((ref) => ref.refId === investigationRef.refId)) {
      return this;
    }
    return new Case(this.id, this.version, this.createdAt, now(), {
      title: this.title,
      owner: this.owner,
      description: this.description,
      priority: this.priority,
      openedAt: this.openedAt,
      closedAt: this.closedAt,
      status: this.status,
      classification: this.classification,
      identityRefs: this.identityRefs,
      investigationRefs: [...this.investigationRefs, investigationRef],
      provenance: this.provenance,
      tags: this.tags,
      metadata: this.metadata,
    });
  }
}
