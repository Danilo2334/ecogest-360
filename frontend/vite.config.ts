import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5178,
    strictPort: true,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  test: {
    environment: "jsdom",
    include: ["tests/**/*.test.tsx"],
    setupFiles: ["./tests/setup.ts"],
  },
});
