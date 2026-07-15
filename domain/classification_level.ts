/**
 * domain/classification_level.ts
 *
 * ClassificationLevel is the pure domain model for the sensitivity
 * classification of any platform object. It governs handling and disclosure
 * rules but implements no enforcement itself (enforcement is an
 * infrastructure/security concern outside the domain layer).
 *
 * Domain Purity: standard runtime only, no external imports.
 */

import { ClassificationLevelValue } from "./common.js";

/** Total order of classification levels, from least to most sensitive. */
const ORDER: ReadonlyArray<ClassificationLevelValue> = [
  ClassificationLevelValue.Public,
  ClassificationLevelValue.Internal,
  ClassificationLevelValue.Restricted,
  ClassificationLevelValue.Confidential,
];

/**
 * ClassificationLevel is an immutable value object wrapping a
 * ClassificationLevelValue, with pure comparison helpers. It never reaches
 * outside the domain to enforce access — it only represents the concept.
 */
export class ClassificationLevel {
  private constructor(public readonly value: ClassificationLevelValue) {
    Object.freeze(this);
  }

  static readonly Public = new ClassificationLevel(ClassificationLevelValue.Public);
  static readonly Internal = new ClassificationLevel(ClassificationLevelValue.Internal);
  static readonly Restricted = new ClassificationLevel(ClassificationLevelValue.Restricted);
  static readonly Confidential = new ClassificationLevel(ClassificationLevelValue.Confidential);

  static of(value: ClassificationLevelValue): ClassificationLevel {
    switch (value) {
      case ClassificationLevelValue.Public:
        return ClassificationLevel.Public;
      case ClassificationLevelValue.Internal:
        return ClassificationLevel.Internal;
      case ClassificationLevelValue.Restricted:
        return ClassificationLevel.Restricted;
      case ClassificationLevelValue.Confidential:
        return ClassificationLevel.Confidential;
      default:
        throw new Error(`Unknown ClassificationLevel value: ${value satisfies never}`);
    }
  }

  /** Rank of this level in the total order (0 = least sensitive). */
  rank(): number {
    return ORDER.indexOf(this.value);
  }

  /** True if this level is at least as sensitive as `other`. */
  atLeast(other: ClassificationLevel): boolean {
    return this.rank() >= other.rank();
  }

  /** Returns the more sensitive of two classification levels. */
  static max(a: ClassificationLevel, b: ClassificationLevel): ClassificationLevel {
    return a.rank() >= b.rank() ? a : b;
  }

  toString(): string {
    return this.value;
  }
}
