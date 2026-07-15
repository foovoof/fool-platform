/**
 * domain/source.ts
 *
 * Source is the pure domain model for an originating channel from which
 * Evidence is collected. A Source carries an independent reliability
 * assessment (a ConfidenceScore) that propagates into the confidence of
 * everything collected from it, per the Confidence Everywhere principle.
 *
 * Mirrors contracts/domain/source.schema.json field-for-field.
 *
 * Domain Purity: standard runtime and sibling domain modules only.
 */

import {
  Status,
  freezeTags,
  newId,
  now,
  type Id,
  type Metadata,
  type Provenance,
  type Timestamp,
  EMPTY_METADATA,
} from "./common.js";
import { ClassificationLevel } from "./classification_level.js";
import { ConfidenceScore } from "./confidence_score.js";

export enum SourceType {
  PublicRegistry = "public_registry",
  SearchEngine = "search_engine",
  SocialPlatform = "social_platform",
  LeakedDataset = "leaked_dataset",
  SensorFeed = "sensor_feed",
  HumanReport = "human_report",
  InternalSystem = "internal_system",
  Other = "other",
}

export interface SourceInit {
  readonly sourceType: SourceType;
  readonly name: string;
  readonly uri?: string;
  readonly reliability?: ConfidenceScore;
  readonly status?: Status;
  readonly classification?: ClassificationLevel;
  readonly provenance: Provenance;
  readonly tags?: ReadonlyArray<string>;
  readonly metadata?: Metadata;
}

/** Source is an immutable record of a channel Evidence can be collected from. */
export class Source {
  readonly id: Id;
  readonly version: string;
  readonly createdAt: Timestamp;
  readonly updatedAt: Timestamp;
  readonly status: Status;
  readonly classification: ClassificationLevel;
  readonly sourceType: SourceType;
  readonly name: string;
  readonly uri?: string;
  readonly reliability?: ConfidenceScore;
  readonly provenance: Provenance;
  readonly tags: ReadonlyArray<string>;
  readonly metadata: Metadata;

  private constructor(id: Id, version: string, createdAt: Timestamp, updatedAt: Timestamp, init: SourceInit) {
    if (init.name.trim().length === 0) {
      throw new Error("Source.name must not be empty.");
    }
    this.id = id;
    this.version = version;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.status = init.status ?? Status.Active;
    this.classification = init.classification ?? ClassificationLevel.Public;
    this.sourceType = init.sourceType;
    this.name = init.name;
    this.uri = init.uri;
    this.reliability = init.reliability;
    this.provenance = init.provenance;
    this.tags = freezeTags(init.tags);
    this.metadata = init.metadata ?? EMPTY_METADATA;
    Object.freeze(this);
  }

  static create(init: SourceInit): Source {
    const timestamp = now();
    return new Source(newId(), "1.0.0", timestamp, timestamp, init);
  }

  /** True if this source has no independent reliability assessment yet. */
  isUnassessed(): boolean {
    return this.reliability === undefined;
  }
}
