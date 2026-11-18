import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const password = readFileSync("../.env", "utf8")
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");
test("Asistente degradado honesto, fuentes, teclado y cuatro anchos sin llamadas externas", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 1000 });
  await page.goto("/");
  await page
    .getByLabel("Usuario", { exact: true })
    .fill("intelligence_consultor");
  await page.getByLabel("Contraseña", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Ingresar al sistema" }).click();
  const filters = page.getByRole("region", { name: "Filtros" });
  await filters.getByLabel("Procedencia").selectOption("simulado");
  await filters.getByLabel("Desde", { exact: true }).fill("2026-11-02");
  await filters.getByLabel("Hasta", { exact: true }).fill("2026-11-15");
  await page.getByRole("button", { name: "Asistente", exact: true }).click();
  await expect(
    page.getByText("OpenAI no disponible · consulta local disponible"),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: /Consultar con OpenAI/ }),
  ).toBeDisabled();
  await expect(page.getByText("365 kg", { exact: true })).toBeVisible();
  await page
    .getByRole("button", {
      name: "¿Cuánto está acreditado y cuánto pendiente?",
    })
    .focus();
  await page.keyboard.press("Enter");
  await expect(page.getByLabel("Tu pregunta")).toBeFocused();
  await expect(page.getByLabel("Tu pregunta")).toHaveValue(
    "¿Cuánto está acreditado y cuánto pendiente?",
  );
  mkdirSync("../docs/evidencias/v2/asistente", { recursive: true });
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
      path: `../docs/evidencias/v2/asistente/asistente-local-${width}.png`,
      fullPage: true,
    });
  }
  await page.getByRole("button", { name: "Explorar un escenario →" }).click();
  await expect(
    page.getByRole("heading", { name: "Simulador", exact: true }),
  ).toBeVisible();
  await expect(page.getByText(/ESCENARIO HIPOTÉTICO/).first()).toBeVisible();
  await expect(page).toHaveURL(/\/simulador\?.*provenance=simulado/);
  await page.reload();
  await expect(
    page.getByRole("heading", { name: "Simulador", exact: true }),
  ).toBeVisible();
  await expect(page.getByText(/365/).first()).toBeVisible();
  await page.goBack();
  await expect(
    page.getByRole("heading", { name: "Asistente", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Restablecer filtros" }).click();
  await expect(page).toHaveURL(/provenance=medido/);
  await expect(
    page.getByText("No hay registros para este período y procedencia."),
  ).toBeVisible();
});
