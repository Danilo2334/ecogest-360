import { afterEach, expect, it, vi } from "vitest";
import { today } from "../src/components/shared";
afterEach(() => {
  vi.useRealTimers();
});
it("mantiene el día local al registrar al final de la noche", () => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(2026, 10, 15, 23, 30));
  expect(today()).toBe("2026-11-15");
});
