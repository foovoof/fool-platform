/**
 * domain/chain_of_custody.ts
 *
 * ChainOfCustody is the pure domain model recording the ordered handling
 * history of an Evidence object, satisfying the Provenance Everywhere
 * principle for evidentiary integrity. It is an append-only ledger: each
 * entry is immutable once recorded, and a new ChainOfCustody with the entry
 * appended is returned rather than mutating the existing one.
 *
 * Domain Purity: standard runtime only, no external imports.
 */

import { newId, now, type Id, type Reference, type Timestamp } from "./common.js";

export interface CustodyEntryInit {
  readonly actor: string;
  readonly action: CustodyAction;
  readonly occurredAt?: Timestamp;
  readonly notes?: string;
}

export enum CustodyAction {
  Collected = "collected",
  Transferred = "transferred",
  Analyzed = "analyzed",
  Copied = "copied",
  Sealed = "sealed",
  Released = "released",
}

export interface CustodyEntry extends CustodyEntryInit {
  readonly entryId: Id;
  readonly occurredAt: Timestamp;
}

/**
 * ChainOfCustody is an immutable, append-only sequence of CustodyEntry
 * records anchored to a single Evidence reference. Construction always
 * begins with a `Collected` entry, guaranteeing that no evidence enters the
 * chain without a recorded point of origin.
 */
export class ChainOfCustody {
  readonly id: Id;
  readonly evidenceRef: Reference;
  readonly entries: ReadonlyArray<CustodyEntry>;

  private constructor(id: Id, evidenceRef: Reference, entries: ReadonlyArray<CustodyEntry>) {
    this.id = id;
    this.evidenceRef = evidenceRef;
    this.entries = Object.freeze([...entries]);
    Object.freeze(this);
  }

  static open(evidenceRef: Reference, firstEntry: CustodyEntryInit): ChainOfCustody {
    if (firstEntry.action !== CustodyAction.Collected) {
      throw new Error("ChainOfCustody must open with a 'collected' entry.");
    }
    const entry: CustodyEntry = {
      entryId: newId(),
      actor: firstEntry.actor,
      action: firstEntry.action,
      occurredAt: firstEntry.occurredAt ?? now(),
      notes: firstEntry.notes,
    };
    return new ChainOfCustody(newId(), evidenceRef, [entry]);
  }

  /** Returns a new ChainOfCustody with the given entry appended; does not mutate this instance. */
  withEntry(next: CustodyEntryInit): ChainOfCustody {
    const lastEntry = this.entries[this.entries.length - 1];
    const nextOccurredAt = next.occurredAt ?? now();
    if (lastEntry !== undefined && nextOccurredAt < lastEntry.occurredAt) {
      throw new Error("ChainOfCustody entries must be non-decreasing in time.");
    }
    const entry: CustodyEntry = {
      entryId: newId(),
      actor: next.actor,
      action: next.action,
      occurredAt: nextOccurredAt,
      notes: next.notes,
    };
    return new ChainOfCustody(this.id, this.evidenceRef, [...this.entries, entry]);
  }

  currentHolder(): string {
    const lastEntry = this.entries[this.entries.length - 1];
    if (lastEntry === undefined) {
      throw new Error("ChainOfCustody invariant violated: no entries present.");
    }
    return lastEntry.actor;
  }
}
