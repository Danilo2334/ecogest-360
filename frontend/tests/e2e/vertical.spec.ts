import { test, expect, type Page } from "@playwright/test";
import { readFileSync } from "node:fs";
const env = readFileSync("../.env", "utf8");
const password = env
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");
async function login(page: Page, role: string) {
  await page.goto("/");
  await page.getByLabel("Usuario", { exact: true }).fill("demo_" + role);
  await page.getByLabel("Contraseña", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Ingresar al sistema" }).click();
  await expect(
    page.getByRole("heading", { name: "El ciclo de tus residuos" }),
  ).toBeVisible();
  await expect(page.getByText("Actualizando datos…")).toHaveCount(0);
}
test("flujo web: generación, lote, compostaje, evidencia, validación y CSV", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await login(page, "operador");
  await page.getByRole("button", { name: "Registros", exact: true }).click();
  const form = page.locator("form").filter({
    has: page.getByRole("heading", { name: "Registrar generación" }),
  });
  await form
    .getByLabel("Área", { exact: true })
    .selectOption({ label: "Cafetería" });
  await form
    .getByLabel("Material ordinario")
    .selectOption({ label: "Orgánicos de cafetería" });
  await form.getByLabel("Peso (kg)", { exact: true }).fill("25");
  await form.getByLabel("Procedencia").selectOption("simulado");
  const generated = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/generations") && r.request().method() === "POST",
  );
  await form
    .getByRole("button", { name: "Registrar generación", exact: true })
    .click();
  const gen = (await (await generated).json()).id;
  await expect(
    page.getByText("Operación guardada.", { exact: false }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Lotes", exact: true }).click();
  const lotForm = page.locator("form").filter({
    has: page.getByRole("heading", { name: "Crear lote", exact: true }),
  });
  await lotForm.getByLabel("Registro de origen").selectOption(String(gen));
  await lotForm.getByLabel("Masa a asignar").fill("25");
  const created = page.waitForResponse(
    (r) => r.url().endsWith("/api/lots") && r.request().method() === "POST",
  );
  await lotForm
    .getByRole("button", { name: "Crear lote", exact: true })
    .click();
  const lot = (await (await created).json()).id;
  await page.getByRole("button", { name: "Compostaje", exact: true }).click();
  const start = page.locator("form").filter({
    has: page.getByRole("heading", {
      name: "Iniciar compostaje",
      exact: true,
    }),
  });
  await start.getByLabel("Procedencia").selectOption("simulado");
  const started = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/compost/processes") &&
      r.request().method() === "POST",
  );
  await start
    .getByRole("button", { name: "Iniciar compostaje", exact: true })
    .click();
  const process = (await (await started).json()).id;
  let card = page.locator("article").filter({
    has: page.getByRole("heading", {
      name: "Proceso #" + process,
      exact: true,
    }),
  });
  await card.getByLabel("Lote", { exact: true }).selectOption(String(lot));
  await card.getByLabel("Entrada (kg)").fill("20");
  await card
    .getByRole("button", { name: "Ingresar orgánicos", exact: true })
    .click();
  await expect(
    card.getByRole("cell", { name: "20.000", exact: true }),
  ).toBeVisible();
  await card.getByLabel("Salida independiente (kg)").fill("8");
  await card.getByLabel("Destino declarado").fill("Huerta DEMO");
  await card
    .getByRole("button", { name: "Finalizar proceso", exact: true })
    .click();
  await expect(card.getByText("8.000 kg", { exact: true })).toBeVisible();
  await card.getByLabel("Receptor", { exact: true }).fill("Huerta DEMO");
  await card
    .getByLabel("Referencia verificable")
    .fill("SIMULADO-E2E-" + process);
  await card
    .getByLabel("Descripción / verificación")
    .fill("Comprobante simulado de entrega, no medición real.");
  await card
    .getByRole("button", { name: "Agregar evidencia verificable", exact: true })
    .click();
  await expect(
    card.getByRole("cell", { name: "SIMULADO-E2E-" + process, exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Cerrar sesión" }).click();
  await login(page, "gestor");
  await page.getByRole("button", { name: "Compostaje", exact: true }).click();
  card = page.locator("article").filter({
    has: page.getByRole("heading", {
      name: "Proceso #" + process,
      exact: true,
    }),
  });
  await card.getByLabel("Decisión", { exact: true }).selectOption("confirmado");
  await card
    .getByLabel("Qué verificaste / motivo")
    .fill("Verificados proceso, pesaje independiente y destino SIMULADOS.");
  await card
    .getByRole("button", { name: "Validar resultado", exact: true })
    .click();
  await expect(
    card.getByRole("cell", { name: "confirmado", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Resumen", exact: true }).click();
  await expect(
    page.getByText("Compostaje acreditado", { exact: true }),
  ).toBeVisible();
  const download = page.waitForEvent("download");
  await page
    .getByRole("link", { name: "Exportar CSV filtrado", exact: false })
    .click();
  expect((await download).suggestedFilename()).toBe("ecogest-generacion.csv");
  await page.screenshot({
    path: "test-results/dashboard-desktop.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 360, height: 800 });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
  await page.screenshot({
    path: "test-results/dashboard-mobile.png",
    fullPage: true,
  });
  expect(errors).toEqual([]);
});
test("consultor: consulta sin formularios de escritura", async ({ page }) => {
  await login(page, "consultor");
  await page.getByRole("button", { name: "Registros", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Registrar generación", exact: true }),
  ).toHaveCount(0);
  await page.keyboard.press("Tab");
  expect(
    await page.evaluate(() => document.activeElement?.tagName !== "BODY"),
  ).toBeTruthy();
});

test("recorrido por teclado y cinco pantallas adaptables", async ({ page }) => {
  await login(page, "operador");
  await page.getByRole("button", { name: "Registros", exact: true }).focus();
  await page.keyboard.press("Enter");
  const form = page
    .locator("form")
    .filter({
      has: page.getByRole("heading", {
        name: "Registrar generación",
        exact: true,
      }),
    });
  await form.getByLabel("Área", { exact: true }).focus();
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("Tab");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("Tab");
  await page.keyboard.type("1");
  await page.keyboard.press("Tab");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("Tab");
  await page.keyboard.type("SIMULADO teclado");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Enter");
  await expect(
    page.getByText("Operación guardada.", { exact: false }),
  ).toBeVisible();
  for (const width of [360, 1280]) {
    await page.setViewportSize({ width, height: 800 });
    for (const name of [
      "Resumen",
      "Registros",
      "Lotes",
      "Compostaje",
      "Incidencias",
    ]) {
      await page.getByRole("button", { name, exact: true }).click();
      await expect(page.getByText("Actualizando datos…")).toHaveCount(0);
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBeTruthy();
    }
  }
});
