/**
 * testing/architecture/schemas_valid.test.ts
 *
 * Architecture test: every JSON Schema under contracts/ must be a
 * structurally valid Draft 2020-12 schema, must declare a stable $id, and
 * every `examples` entry it carries must validate against its own schema.
 * This is the automated backbone of the Contracts First principle — a
 * schema that does not compile or whose own examples fail is not a usable
 * contract.
 */
import { describe, expect, it } from "vitest";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const CONTRACTS_DIR = join(import.meta.dirname, "..", "..", "contracts");

function listSchemaFiles(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir)) {
    const fullPath = join(dir, entry);
    if (statSync(fullPath).isDirectory()) {
      out.push(...listSchemaFiles(fullPath));
    } else if (entry.endsWith(".schema.json")) {
      out.push(fullPath);
    }
  }
  return out;
}

const schemaFiles = listSchemaFiles(CONTRACTS_DIR);

function buildAjv(): Ajv2020 {
  const ajv = new Ajv2020({ strict: false, allErrors: true });
  addFormats(ajv);
  // Pre-register every schema by its $id so cross-file $ref resolution works
  // regardless of load order.
  for (const file of schemaFiles) {
    const schema = JSON.parse(readFileSync(file, "utf-8"));
    if (!ajv.getSchema(schema.$id)) {
      ajv.addSchema(schema, schema.$id);
    }
  }
  return ajv;
}

describe("Contract schemas", () => {
  it("finds at least one schema file to validate", () => {
    expect(schemaFiles.length).toBeGreaterThan(0);
  });

  const ajv = buildAjv();

  it.each(schemaFiles)("%s is a valid, compilable Draft 2020-12 schema with a stable $id", (file) => {
    const schema = JSON.parse(readFileSync(file, "utf-8"));
    expect(schema.$id, `${relative(CONTRACTS_DIR, file)} must declare $id`).toBeTruthy();
    expect(schema.$schema, `${relative(CONTRACTS_DIR, file)} must declare $schema`).toContain("2020-12");
    const validate = ajv.getSchema(schema.$id) ?? ajv.compile(schema);
    expect(typeof validate).toBe("function");
  });

  it.each(schemaFiles)("%s: every declared example validates against its own schema", (file) => {
    const schema = JSON.parse(readFileSync(file, "utf-8"));
    const examples: unknown[] = schema.examples ?? [];
    if (examples.length === 0) {
      // Some low-level shared/common schemas legitimately have no top-level
      // examples of their own (they exist to be referenced via $ref).
      return;
    }
    const validate = ajv.getSchema(schema.$id)!;
    for (const example of examples) {
      const valid = validate(example);
      if (!valid) {
        throw new Error(
          `${relative(CONTRACTS_DIR, file)} example failed validation: ${JSON.stringify(validate.errors)}`
        );
      }
    }
  });
});
