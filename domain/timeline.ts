/**
 * domain/timeline.ts
 *
 * Timeline is the pure domain model for a chronologically ordered sequence
 * of Event references scoped to a single subject (an Investigation, Case,
 * or Identity). A Timeline never stores full Event payloads — only ordered
 * references — keeping the timeline itself lightweight and derivable.
 *
 * Domain Purity: standard runtime and sibling domain modules only.
 */

import { newId, type Id, type Reference, type Timestamp } from "./common.js";
import { DomainInvariantError } from "./common.js";

export interface TimelineEntry {
  readonly eventRef: Reference;
  readonly occurredAt: Timestamp;
}

/** Timeline is an immutable, time-ordered sequence of event references for one subject. */
export class Timeline {
  readonly id: Id;
  readonly subjectRef: Reference;
  readonly entries: ReadonlyArray<TimelineEntry>;

  private constructor(id: Id, subjectRef: Reference, entries: ReadonlyArray<TimelineEntry>) {
    this.id = id;
    this.subjectRef = subjectRef;
    this.entries = Object.freeze([...entries].sort((a, b) => (a.occurredAt < b.occurredAt ? -1 : a.occurredAt > b.occurredAt ? 1 : 0)));
    Object.freeze(this);
  }

  static empty(subjectRef: Reference): Timeline {
    return new Timeline(newId(), subjectRef, []);
  }

  /** Returns a new Timeline with the given entry inserted in chronological order. */
  withEntry(entry: TimelineEntry): Timeline {
    if (this.entries.some((existing) => existing.eventRef.refId === entry.eventRef.refId)) {
      throw new DomainInvariantError("Timeline already contains an entry for this eventRef.");
    }
    return new Timeline(this.id, this.subjectRef, [...this.entries, entry]);
  }

  /** Entries whose occurredAt falls within [from, to], inclusive. */
  between(from: Timestamp, to: Timestamp): ReadonlyArray<TimelineEntry> {
    return this.entries.filter((entry) => entry.occurredAt >= from && entry.occurredAt <= to);
  }

  earliest(): TimelineEntry | undefined {
    return this.entries[0];
  }

  latest(): TimelineEntry | undefined {
    return this.entries[this.entries.length - 1];
  }
}
