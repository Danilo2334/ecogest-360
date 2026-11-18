import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  workers: 1,
  timeout: 60000,
  use: {
    baseURL: "http://127.0.0.1:5178",
    headless: true,
    timezoneId: "America/Bogota",
    locale: "es-CO",
    trace: "off",
    screenshot: "only-on-failure",
  },
  reporter: "list",
});
