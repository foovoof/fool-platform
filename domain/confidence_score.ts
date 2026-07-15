/**
 * domain/confidence_score.ts
 *
 * ConfidenceScore is the pure domain model implementing the platform's
 * Confidence Everywhere principle: every conclusion or assessment must
 * support a measurable score, a human-interpretable level, a rationale, a
 * named method, provenance, and evidence/source references. Confidence is
 * never represented as a bare boolean anywhere in the domain layer.
 *
 * Domain Purity: standard runtime only, no external imports.
 */

import { ConfidenceLevel, type Reference, type Timestamp, freezeRefs, now } from "./common.js";

export interface ConfidenceScoreInit {
  readonly score: number;
  readonly method: string;
  readonly rationale?: string;
  readonly assessedBy?: string;
  readonly assessedAt?: Timestamp;
  readonly evidenceRefs?: ReadonlyArray<Reference>;
  readonly sourceRefs?: ReadonlyArray<Reference>;
}

/** Score-band boundaries mapping a numeric score to a ConfidenceLevel. */
const LEVEL_BANDS: ReadonlyArray<{ level: ConfidenceLevel; min: number }> = [
  { level: ConfidenceLevel.VeryHigh, min: 0.9 },
  { level: ConfidenceLevel.High, min: 0.7 },
  { level: ConfidenceLevel.Moderate, min: 0.4 },
  { level: ConfidenceLevel.Low, min: 0.15 },
  { level: ConfidenceLevel.VeryLow, min: 0 },
];

function levelForScore(score: number): ConfidenceLevel {
  for (const band of LEVEL_BANDS) {
    if (score >= band.min) return band.level;
  }
  return ConfidenceLevel.VeryLow;
}

/**
 * ConfidenceScore is an immutable assessment of how strongly a conclusion,
 * entity, relationship, or finding should be trusted. It is never binary:
 * a numeric score in [0, 1] is always paired with a level, a method, and a
 * timestamp, and should carry evidence/source references whenever available.
 */
export class ConfidenceScore {
  readonly score: number;
  readonly level: ConfidenceLevel;
  readonly rationale?: string;
  readonly method: string;
  readonly assessedBy?: string;
  readonly assessedAt: Timestamp;
  readonly evidenceRefs: ReadonlyArray<Reference>;
  readonly sourceRefs: ReadonlyArray<Reference>;

  private constructor(init: ConfidenceScoreInit) {
    if (init.score < 0 || init.score > 1) {
      throw new RangeError(`ConfidenceScore.score must be within [0, 1], received ${init.score}.`);
    }
    if (init.method.trim().length === 0) {
      throw new Error("ConfidenceScore.method must be a non-empty, named scoring method.");
    }
    this.score = init.score;
    this.level = levelForScore(init.score);
    this.rationale = init.rationale;
    this.method = init.method;
    this.assessedBy = init.assessedBy;
    this.assessedAt = init.assessedAt ?? now();
    this.evidenceRefs = freezeRefs(init.evidenceRefs);
    this.sourceRefs = freezeRefs(init.sourceRefs);
    Object.freeze(this);
  }

  static create(init: ConfidenceScoreInit): ConfidenceScore {
    return new ConfidenceScore(init);
  }

  /** True when neither evidence nor source references back this assessment. */
  isUnsubstantiated(): boolean {
    return this.evidenceRefs.length === 0 && this.sourceRefs.length === 0;
  }

  /** Combines this assessment with another using the weighted mean of scores. */
  combine(other: ConfidenceScore, weight = 0.5): ConfidenceScore {
    if (weight < 0 || weight > 1) {
      throw new RangeError("combine() weight must be within [0, 1].");
    }
    const combinedScore = this.score * weight + other.score * (1 - weight);
    return ConfidenceScore.create({
      score: combinedScore,
      method: "combined",
      rationale: `Weighted combination of '${this.method}' and '${other.method}'.`,
      evidenceRefs: [...this.evidenceRefs, ...other.evidenceRefs],
      sourceRefs: [...this.sourceRefs, ...other.sourceRefs],
    });
  }
}
