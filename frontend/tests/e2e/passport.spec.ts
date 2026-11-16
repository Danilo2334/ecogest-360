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
  mkdirSync("../docs/evidencias/v2/pasaporte", { recursive: true });
  for (const width of [1280, 768, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.evaluate(() => window.scrollTo(0, 0));
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBeTruthy();
    await page.screenshot({
      path: `../docs/evidencias/v2/pasaporte/pasaporte-${width}.png`,
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
});
