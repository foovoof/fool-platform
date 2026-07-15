/**
 * testing/architecture/no_placeholders.test.ts
 *
 * Architecture test enforcing the "no placeholders, no mocked data, no
 * fake implementations" constitutional rule for Phase 1. Scans every
 * source/contract/standard/workflow file for common placeholder markers.
 * A legitimate reference to "TODO"-shaped English prose inside prose
 * documentation is still disallowed here deliberately: Phase 1 must ship
 * complete, not "coming soon."
 */
import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { extname, join } from "node:path";

const ROOT = join(import.meta.dirname, "..", "..");
const SCAN_DIRS = ["contracts", "domain", "standards", "platform", "workflows"];
const SCAN_EXTENSIONS = new Set([".ts", ".json", ".yaml", ".yml", ".md"]);
const PLACEHOLDER_PATTERN = /\b(TODO|FIXME|TBD|XXX|placeholder|not implemented|coming soon)\b/i;

function listFiles(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir)) {
    const fullPath = join(dir, entry);
    if (statSync(fullPath).isDirectory()) {
      out.push(...listFiles(fullPath));
    } else if (SCAN_EXTENSIONS.has(extname(entry))) {
      out.push(fullPath);
    }
  }
  return out;
}

const files = SCAN_DIRS.flatMap((dir) => listFiles(join(ROOT, dir)));

describe("No placeholder markers in Phase 1 deliverables", () => {
  it("finds at least one file to scan", () => {
    expect(files.length).toBeGreaterThan(0);
  });

  it.each(files)("%s contains no placeholder markers", (file) => {
    const content = readFileSync(file, "utf-8");
    const match = content.match(PLACEHOLDER_PATTERN);
    expect(match, `${file} contains a placeholder marker: "${match?.[0]}"`).toBeNull();
  });
});
