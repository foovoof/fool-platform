import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const DOMAIN_DIR = join(import.meta.dirname, "..");

const FORBIDDEN_IMPORT_PATTERN =
  /from\s+["'](platform|intelligence|ai|data|infrastructure|security|apps|connectors|tools)(\/|["'])/;

function listDomainSourceFiles(): string[] {
  return readdirSync(DOMAIN_DIR)
    .filter((entry) => entry.endsWith(".ts") && !entry.endsWith(".test.ts"))
    .map((entry) => join(DOMAIN_DIR, entry));
}

describe("Domain purity", () => {
  const files = listDomainSourceFiles();

  it("finds at least one domain module to check", () => {
    expect(files.length).toBeGreaterThan(0);
  });

  it.each(files)("%s imports nothing outside the standard runtime and sibling domain modules", (file) => {
    const content = readFileSync(file, "utf-8");
    expect(content).not.toMatch(FORBIDDEN_IMPORT_PATTERN);

    const importStatements = content.match(/import\s+[\s\S]*?from\s+["'][^"']+["'];/g) ?? [];
    for (const statement of importStatements) {
      const isRelative = /from\s+["']\.\//.test(statement);
      const isNodeBuiltin = /from\s+["']node:/.test(statement);
      const isVitest = /from\s+["']vitest["']/.test(statement);
      expect(isRelative || isNodeBuiltin || isVitest, `unexpected import in ${file}: ${statement}`).toBe(true);
    }
  });

  it("no domain module references a database, HTTP, or AI client", () => {
    const bannedTokens = ["fetch(", "axios", "prisma", "drizzle", "OpenAI", "Anthropic", "pg.Client", "mongodb"];
    for (const file of files) {
      const content = readFileSync(file, "utf-8");
      for (const token of bannedTokens) {
        expect(content.includes(token)).toBe(false);
      }
    }
  });
});
