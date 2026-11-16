import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import { it, expect, vi, afterEach } from "vitest";
import { PlansPage } from "../src/features/plans/PlansPage";
import { api } from "../src/services/api";
vi.mock("../src/services/api", () => ({ api: vi.fn() }));
afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});
it("consultor recibe consulta sin formulario ni acción de creación", async () => {
  vi.mocked(api).mockResolvedValue([]);
  render(
    <PlansPage
      data={{ areas: [] }}
      manager={false}
      query=""
      onClearProposal={() => {}}
    />,
  );
  expect(await screen.findByText(/Todavía no hay planes/)).toBeVisible();
  expect(
    screen.queryByRole("button", { name: "Preparar nuevo plan" }),
  ).not.toBeInTheDocument();
  expect(
    screen.queryByRole("button", { name: "Guardar borrador del plan" }),
  ).not.toBeInTheDocument();
});
it("gestor revisa formulario antes de guardar, sin creación automática", async () => {
  vi.mocked(api).mockResolvedValue([]);
  render(
    <PlansPage
      data={{ areas: [] }}
      manager
      query="provenance=simulado"
      onClearProposal={() => {}}
    />,
  );
  await screen.findByText(/Todavía no hay planes/);
  fireEvent.click(screen.getByRole("button", { name: "Preparar nuevo plan" }));
  expect(screen.getByLabelText("Problema observado")).toBeVisible();
  expect(
    screen.getByRole("button", { name: "Guardar borrador del plan" }),
  ).toBeVisible();
  expect(vi.mocked(api).mock.calls.every((c) => c.length === 1)).toBe(true);
});
