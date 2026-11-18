import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const password = readFileSync("../.env", "utf8")
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");
test("Gestor conecta escenario con plan, evaluación y cierre auditado", async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 1000 });
  await page.goto("/");
  await page.getByLabel("Usuario", { exact: true }).fill("intelligence_gestor");
  await page.getByLabel("Contraseña", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Ingresar al sistema" }).click();
  const filters = page.getByRole("region", { name: "Filtros" });
  await filters.getByLabel("Procedencia").selectOption("simulado");
  await filters.getByLabel("Desde", { exact: true }).fill("2026-10-19");
  await filters.getByLabel("Hasta", { exact: true }).fill("2026-11-01");
  await filters
    .getByRole("combobox", { name: "Área", exact: true })
    .selectOption({ label: "Cafetería" });
  await page.getByRole("button", { name: "Simulador", exact: true }).click();
  await page.getByRole("button", { name: "Revisar propuesta de plan" }).click();
  const problem = `Plan SIMULADO Playwright ${Date.now()}`;
  await page.getByLabel("Problema observado").fill(problem);
  await page
    .getByLabel("Responsable institucional")
    .selectOption({ label: "intelligence_gestor" });
  await page.getByLabel("Meta numérica").fill("90");
  await page.getByLabel("Dirección de la meta").selectOption("increase");
  await page.getByLabel("Fecha objetivo").fill("2026-12-31");
  await page
    .getByLabel("Motivo de esta decisión")
    .fill("Ensayo automático SIMULADO, no ejecución humana CHK013");
  await page
    .getByLabel("Indicador que evaluaremos")
    .selectOption("verified_compost");
  await page.getByRole("button", { name: "Guardar borrador del plan" }).click();
  await page
    .getByRole("article")
    .filter({ has: page.getByRole("heading", { name: problem, exact: true }) })
    .getByRole("button", { name: /Revisar plan/ })
    .click();
  const transition = page
    .locator("form")
    .filter({
      has: page.getByRole("button", { name: "Confirmar cambio de estado" }),
    });
  for (const state of ["en_curso", "en_evaluacion"]) {
    await transition.getByLabel("Nuevo estado").selectOption(state);
    await transition
      .getByLabel("Motivo de esta decisión")
      .fill("Transición de ensayo simulado");
    await transition.getByRole("button").click();
    await expect(
      page.getByText(
        state === "en_curso"
          ? /En curso · SIMULADO · versión/
          : /En evaluación · SIMULADO · versión/,
      ),
    ).toBeVisible();
  }
  const evaluation = page
    .locator("form")
    .filter({
      has: page.getByRole("button", { name: "Evaluar período posterior" }),
    });
  await evaluation
    .getByLabel("Inicio del período posterior")
    .fill("2026-11-02");
  await evaluation.getByLabel("Fin del período posterior").fill("2026-11-15");
  await evaluation
    .getByLabel("Motivo de esta decisión")
    .fill("Comparación sintética, no causal");
  await evaluation.getByRole("button").click();
  await expect(
    page.getByRole("heading", { name: "Meta alcanzada observada" }),
  ).toBeVisible();
  mkdirSync("../docs/evidencias/v2/integracion/planes", { recursive: true });
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
      path: `../docs/evidencias/v2/integracion/planes/planes-${width}.png`,
      fullPage: true,
    });
  }
  await transition.getByLabel("Nuevo estado").selectOption("cerrado");
  await transition
    .getByLabel("Motivo de esta decisión")
    .fill("Cierre automático de ensayo; evidencia simulada");
  await transition.getByRole("button").click();
  await expect(page.getByText(/Cerrado · SIMULADO · versión/)).toBeVisible();
});
