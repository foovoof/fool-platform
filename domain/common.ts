/**
 * domain/common.ts
 *
 * Shared value types for the FOOL Platform domain layer.
 *
 * Domain Purity: this module imports nothing beyond the TypeScript/JavaScript
 * standard runtime (`crypto.randomUUID`). It must never import from platform,
 * intelligence, ai, data, infrastructure, security, apps, connectors, or tools.
 * These types mirror contracts/common/common-defs.schema.json field-for-field;
 * the JSON Schema remains the canonical source of truth for wire shape, this
 * module is the canonical source of truth for in-process domain shape.
 */

/** Canonical unique identifier for any domain object. Always a UUID. */
export type Id = string;

/** Timezone-aware ISO 8601 timestamp (RFC 3339). */
export type Timestamp = string;

/** Semantic version string, e.g. "1.0.0". */
export type SemanticVersion = string;

/** Generates a new canonical identifier for a domain object. */
export function newId(): Id {
  return crypto.randomUUID();
}

/** Produces a timezone-aware ISO 8601 timestamp for "now". */
export function now(): Timestamp {
  return new Date().toISOString();
}

/** Sensitivity classification of a domain object, per ClassificationLevel. */
export enum ClassificationLevelValue {
  Public = "public",
  Internal = "internal",
  Restricted = "restricted",
  Confidential = "confidential",
}

/** Canonical lifecycle status shared by case/investigation/report style objects. */
export enum Status {
  Draft = "draft",
  Active = "active",
  UnderReview = "under_review",
  Archived = "archived",
  Retracted = "retracted",
}

/** A pointer from one domain object to another by id and type. */
export interface Reference {
  readonly refId: Id;
  readonly refType: string;
  readonly refVersion?: SemanticVersion;
}

export function reference(refId: Id, refType: string, refVersion?: SemanticVersion): Reference {
  return refVersion === undefined ? { refId, refType } : { refId, refType, refVersion };
}

/** Human-interpretable confidence bucket derived from a confidence score. */
export enum ConfidenceLevel {
  VeryLow = "very_low",
  Low = "low",
  Moderate = "moderate",
  High = "high",
  VeryHigh = "very_high",
}

/** Origin, lineage, and custody trail attached to any information-bearing object. */
export interface Provenance {
  readonly origin: string;
  readonly recordedAt: Timestamp;
  readonly lineage: ReadonlyArray<string>;
  readonly custodyRefs: ReadonlyArray<Reference>;
  readonly sourceRefs: ReadonlyArray<Reference>;
}

export function createProvenance(
  origin: string,
  options: {
    recordedAt?: Timestamp;
    lineage?: ReadonlyArray<string>;
    custodyRefs?: ReadonlyArray<Reference>;
    sourceRefs?: ReadonlyArray<Reference>;
  } = {}
): Provenance {
  if (origin.trim().length === 0) {
    throw new Error("Provenance.origin must not be empty: no domain object may be anonymous.");
  }
  return Object.freeze({
    origin,
    recordedAt: options.recordedAt ?? now(),
    lineage: Object.freeze([...(options.lineage ?? [])]),
    custodyRefs: Object.freeze([...(options.custodyRefs ?? [])]),
    sourceRefs: Object.freeze([...(options.sourceRefs ?? [])]),
  });
}

/** Open key/value bag for non-canonical, extension-owned attributes. */
export type Metadata = Readonly<Record<string, unknown>>;

export const EMPTY_METADATA: Metadata = Object.freeze({});

export function freezeTags(tags: ReadonlyArray<string> = []): ReadonlyArray<string> {
  return Object.freeze([...new Set(tags)]);
}

export function freezeRefs(refs: ReadonlyArray<Reference> = []): ReadonlyArray<Reference> {
  return Object.freeze([...refs]);
}

/** Raised when a domain invariant is violated during pure, local construction. */
export class DomainInvariantError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DomainInvariantError";
  }
}
