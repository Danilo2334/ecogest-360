import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const password = readFileSync("../.env", "utf8")
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");
test("Observatorio real: roles, filtros, teclado y cuatro anchos", async ({
  page,
}) => {
  mkdirSync("../docs/evidencias/v2/integracion", { recursive: true });
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  for (const role of ["administrador", "operador", "gestor", "consultor"]) {
    await page.setViewportSize({ width: 1440, height: 1050 });
    await page.goto("/");
    await page.getByLabel("Usuario", { exact: true }).fill("demo_" + role);
    await page.getByLabel("Contraseña", { exact: true }).fill(password);
    await page.getByRole("button", { name: "Ingresar al sistema" }).click();
    await expect(
      page.getByRole("heading", { name: "Observatorio ambiental" }),
    ).toBeVisible();
    await expect(page.getByText("Actualizando datos…")).toHaveCount(0);
    const filters = page.getByRole("region", { name: "Filtros" });
    await filters.getByLabel("Procedencia").selectOption("simulado");
    await expect(page.getByText("Actualizando datos…")).toHaveCount(0);
    await expect(
      page.getByText("SIMULADO · demostración", { exact: true }),
    ).toBeVisible();
    await expect(
      page.getByRole("button", { name: "Institución", exact: true }),
    ).toHaveCount(role === "administrador" ? 1 : 0);
    if (role === "gestor") {
      for (const width of [1280, 768, 390, 360]) {
        await page.setViewportSize({ width, height: 1000 });
        expect(
          await page.evaluate(
            () => document.documentElement.scrollWidth <= innerWidth,
          ),
        ).toBeTruthy();
        await page.screenshot({
          path: `../docs/evidencias/v2/integracion/observatorio-${width}.png`,
          fullPage: true,
        });
      }
      await page.getByRole("button", { name: /Menú/ }).focus();
      await page.keyboard.press("Enter");
      await expect(
        page.getByRole("button", { name: "Registros", exact: true }),
      ).toBeVisible();
      await page.setViewportSize({ width: 1280, height: 1000 });
      await page
        .getByRole("button", { name: /Revisar registros/ })
        .first()
        .click();
      await expect(
        page.getByRole("heading", { name: "Registros", exact: true }),
      ).toBeVisible();
      await expect(
        page.getByRole("region", { name: "Filtros" }).getByLabel("Procedencia"),
      ).toHaveValue("simulado");
    }
    await page.getByRole("button", { name: "Cerrar sesión" }).click();
    await expect(
      page.getByRole("heading", { name: "Ingresa a EcoGest 360" }),
    ).toBeVisible();
  }
  expect(errors).toEqual([]);
});
