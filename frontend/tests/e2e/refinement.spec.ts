import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";
const password = readFileSync("../.env", "utf8")
  .match(/^DEMO_PASSWORD=(.*)$/m)![1]
  .trim()
  .replace(/^['"]|['"]$/g, "");

test("Cohorte aislada: comparación, balance, evidencia, teclado y capturas", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.setViewportSize({ width: 1280, height: 1000 });
  await page.goto("/");
  await page.getByLabel("Usuario", { exact: true }).fill("intelligence_gestor");
  await page.getByLabel("Contraseña", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Ingresar al sistema" }).click();
  await expect(
    page.getByRole("heading", { name: "Observatorio ambiental" }),
  ).toBeVisible();
  const filters = page.getByRole("region", { name: "Filtros" });
  await filters.getByLabel("Procedencia").selectOption("simulado");
  await filters.getByLabel("Desde", { exact: true }).fill("2026-11-02");
  await filters.getByLabel("Hasta", { exact: true }).fill("2026-11-15");
  const balance = page.getByRole("img", {
    name: "100.000 kg acreditados y 265.000 kg pendientes de 365.000 kg generados",
  });
  await expect(balance).toBeVisible();
  await expect(page.getByText("+84 kg", { exact: true })).toBeVisible();
  await expect(filters.getByText(/2 de noviembre de 2026/)).toBeVisible();
  // Computed colors of representative text, including the dark KPI and pale findings panel.
  const contrasts: number[] = [];
  for (const text of [
    page.getByRole("heading", { name: "Observatorio ambiental" }),
    page.getByText("Entradas con tratamiento y destino verificados", {
      exact: true,
    }),
    page.getByText("Masa registrada en la cohorte", { exact: true }),
    page.getByText("Reglas explícitas. Decisiones humanas.", { exact: true }),
    filters.getByText(/Período:/),
  ]) {
    const ratio = await text.evaluate((el) => {
      const rgb = (s: string) =>
        s
          .match(/[\d.]+/g)!
          .slice(0, 3)
          .map(Number);
      const luminance = (v: number[]) =>
        v
          .map((x) => {
            const c = x / 255;
            return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
          })
          .reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
      let parent: Element | null = el;
      let bg = "rgb(255,255,255)";
      while (parent) {
        const c = getComputedStyle(parent).backgroundColor;
        if (c !== "rgba(0, 0, 0, 0)" && c !== "transparent") {
          bg = c;
          break;
        }
        parent = parent.parentElement;
      }
      const a = luminance(rgb(getComputedStyle(el).color)),
        b = luminance(rgb(bg));
      return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    });
    expect(ratio).toBeGreaterThanOrEqual(4.5);
    contrasts.push(ratio);
  }
  console.log(
    "Contraste de cinco textos representativos, mínimo:",
    Math.min(...contrasts).toFixed(2),
  );
  const interpretation = page
    .getByText("Interpretación y acción sugerida", { exact: true })
    .first();
  await interpretation.focus();
  await page.keyboard.press("Enter");
  await expect(
    page.getByText(/Pendiente no significa residuo abandonado/),
  ).toBeVisible();
  await page.keyboard.press("Enter");
  await page.getByText("Ver datos de la gráfica", { exact: true }).click();
  await expect(
    page
      .getByRole("table")
      .filter({ has: page.getByText("Solo días con registros") })
      .locator("tbody tr"),
  ).toHaveCount(14);
  await page.getByText("Ver datos de la gráfica", { exact: true }).click();
  mkdirSync("../docs/evidencias/v2/despues-refinamiento", { recursive: true });
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
      path: `../docs/evidencias/v2/despues-refinamiento/observatorio-${width}.png`,
      fullPage: true,
    });
  }
  await page
    .getByRole("button", { name: "Consultar cohorte base de Generados" })
    .focus();
  await page.keyboard.press("Enter");
  await expect(
    page.getByRole("heading", { name: "Registros", exact: true }),
  ).toBeVisible();
  await filters.getByRole("button", { name: "Ajustar filtros" }).click();
  await expect(filters.getByLabel("Desde", { exact: true })).toHaveValue(
    "2026-11-02",
  );
  await expect(filters.getByLabel("Procedencia")).toHaveValue("simulado");
  await page.getByRole("button", { name: /Menú/ }).click();
  await page.getByRole("button", { name: "Observatorio", exact: true }).click();
  await page
    .getByRole("article")
    .filter({
      has: page.getByRole("heading", {
        name: "Cafetería concentra más generación",
      }),
    })
    .getByRole("button", { name: /Revisar registros/ })
    .click();
  await expect(
    page.getByRole("heading", { name: "Registros", exact: true }),
  ).toBeVisible();
  await expect(
    filters
      .getByRole("combobox", { name: "Área", exact: true })
      .locator("option:checked"),
  ).toHaveText("Cafetería");
  await expect(filters.getByLabel("Desde", { exact: true })).toHaveValue(
    "2026-11-02",
  );
  expect(errors).toEqual([]);
});
