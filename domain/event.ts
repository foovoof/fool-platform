/**
 * domain/event.ts
 *
 * Event is the pure domain model implementing the Event-Driven Language
 * principle: events are the official, versionable language the platform
 * uses to describe things that happened to a domain object. Events are
 * immutable historical facts — they are never updated after creation.
 *
 * Domain Purity: standard runtime and sibling domain modules only.
 */

import { freezeRefs, newId, now, type Id, type Metadata, type Reference, type Timestamp, EMPTY_METADATA } from "./common.js";

export interface EventInit {
  readonly eventType: string;
  readonly subjectRef: Reference;
  readonly occurredAt?: Timestamp;
  readonly version?: string;
  readonly payload?: Metadata;
  readonly relatedRefs?: ReadonlyArray<Reference>;
  readonly traceId?: Id;
}

/**
 * Event is an immutable record that something happened to `subjectRef` at
 * `occurredAt`. `eventType` must follow the dotted, namespaced convention
 * used across contracts (e.g. "identity.identifier.added").
 */
export class Event {
  readonly id: Id;
  readonly eventType: string;
  readonly version: string;
  readonly subjectRef: Reference;
  readonly occurredAt: Timestamp;
  readonly payload: Metadata;
  readonly relatedRefs: ReadonlyArray<Reference>;
  readonly traceId?: Id;

  private constructor(id: Id, init: EventInit) {
    if (!/^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)+$/.test(init.eventType)) {
      throw new Error(`Event.eventType must be dotted and namespaced (e.g. "identity.identifier.added"), received "${init.eventType}".`);
    }
    this.id = id;
    this.eventType = init.eventType;
    this.version = init.version ?? "1.0.0";
    this.subjectRef = init.subjectRef;
    this.occurredAt = init.occurredAt ?? now();
    this.payload = init.payload ?? EMPTY_METADATA;
    this.relatedRefs = freezeRefs(init.relatedRefs);
    this.traceId = init.traceId;
    Object.freeze(this);
  }

  static record(init: EventInit): Event {
    return new Event(newId(), init);
  }
}
