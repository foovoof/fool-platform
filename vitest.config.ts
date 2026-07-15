import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["domain/tests/**/*.test.ts", "testing/architecture/**/*.test.ts"],
    environment: "node",
  },
});
