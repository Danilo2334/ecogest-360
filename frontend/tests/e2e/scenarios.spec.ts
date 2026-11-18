import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const password = readFileSync("../.env", "utf8")
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");
test("Simulación real efímera con filtros, límites y cuatro anchos", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 1000 });
  await page.goto("/");
  await page.getByLabel("Usuario", { exact: true }).fill("intelligence_gestor");
  await page.getByLabel("Contraseña", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Ingresar al sistema" }).click();
  const filters = page.getByRole("region", { name: "Filtros" });
  await filters.getByLabel("Procedencia").selectOption("simulado");
  await filters.getByLabel("Desde", { exact: true }).fill("2026-11-02");
  await filters.getByLabel("Hasta", { exact: true }).fill("2026-11-15");
  await page.getByRole("button", { name: "Simulador", exact: true }).click();
  await expect(
    page.getByText("Límite de esta base: 87 kg", { exact: true }),
  ).toBeVisible();
  await page.getByLabel("Cantidad hipotética (kg)").fill("10");
  await page.getByRole("button", { name: "Calcular escenario" }).click();
  await expect(
    page
      .getByRole("row")
      .filter({
        has: page.getByRole("rowheader", {
          name: "Compostaje acreditado",
          exact: true,
        }),
      }),
  ).toContainText("110");
  mkdirSync("../docs/evidencias/v2/integracion/simulador", { recursive: true });
  for (const width of [1280, 768, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.evaluate(() => {
      (document.activeElement as HTMLElement)?.blur();
      window.scrollTo(0, 0);
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBeTruthy();
    await page.screenshot({
      path: `../docs/evidencias/v2/integracion/simulador/simulador-${width}.png`,
      fullPage: true,
    });
  }
  await page.getByLabel("Cantidad hipotética (kg)").fill("88");
  await page.getByRole("button", { name: "Calcular escenario" }).click();
  await expect(page.getByRole("alert")).toContainText("supera");
  await page.getByRole("button", { name: /Recargar base actual/ }).click();
  await expect(page.getByLabel("Cantidad hipotética (kg)")).toHaveValue("0");
});
