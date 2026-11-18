import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const password = readFileSync("../.env", "utf8")
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");
test("Pasaporte real conserva balance, QR, teclado y cuatro anchos", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByLabel("Usuario", { exact: true }).fill("intelligence_gestor");
  await page.getByLabel("Contraseña", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Ingresar al sistema" }).click();
  await page.getByRole("button", { name: "Trazabilidad", exact: true }).click();
  await page
    .getByRole("button", { name: /Abrir pasaporte ambiental/ })
    .first()
    .click();
  await expect(
    page.getByRole("heading", { name: /La historia del lote/ }),
  ).toBeVisible();
  await expect(page.getByText("87 kg", { exact: true })).toBeVisible();
  await expect(page.getByText("31 kg", { exact: false }).first()).toBeVisible();
  mkdirSync("../docs/evidencias/v2/integracion/pasaporte", { recursive: true });
  for (const width of [1280, 768, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.evaluate(() => window.scrollTo(0, 0));
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBeTruthy();
    await page.screenshot({
      path: `../docs/evidencias/v2/integracion/pasaporte/pasaporte-${width}.png`,
      fullPage: true,
    });
  }
  await page.getByText("QR e identificación del lote", { exact: true }).focus();
  await page.keyboard.press("Enter");
  await expect(
    page.getByRole("img", { name: /QR de consulta autorizada/ }),
  ).toBeVisible();
  await page.getByRole("button", { name: /Volver a trazabilidad/ }).click();
  await expect(
    page.getByRole("button", { name: /Abrir pasaporte ambiental/ }).first(),
  ).toBeVisible();
  await page
    .getByRole("button", { name: /Abrir pasaporte ambiental/ })
    .first()
    .click();
  await page.getByRole("link", { name: "Simular una alternativa" }).click();
  await expect(
    page.getByRole("heading", { name: "Simulador", exact: true }),
  ).toBeVisible();
  await expect(page).toHaveURL(/provenance=simulado/);
  await expect(page.getByText(/Límite de esta base: 87 kg/)).toBeVisible();
  const lots = await page.request.get("/api/lots").then((r) => r.json());
  const lot = lots[0];
  await page.goto(
    "/lotes/" +
      lot.public_id +
      "?provenance=simulado&generated_from=2026-11-02&generated_to=2026-11-15",
  );
  await expect(
    page.getByRole("heading", { name: /La historia del lote/ }),
  ).toBeVisible();
  await page.getByRole("button", { name: /Volver a trazabilidad/ }).click();
  await expect(page).toHaveURL(/\/lotes\?provenance=simulado/);
  await page.reload();
  await expect(
    page.getByRole("button", { name: /Abrir pasaporte ambiental/ }).first(),
  ).toBeVisible();
});
