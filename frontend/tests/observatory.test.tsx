import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { ReportsPage } from "../src/features/reports/ReportsPage";
afterEach(cleanup);
const dashboard = {
  summary: {
    generated: "25",
    verified_compost: "20",
    pending: "5",
    available: "5",
    in_process: "0",
    delivered: "0",
    rate: "80",
    provenance: "simulado",
    cutoff: "2026-11-15T20:00:00Z",
    formula: "A/G",
    limitations: "Solo compostaje",
    provisional: true,
    distribution: [],
  },
  comparison: {
    available: false,
    reason: "Evidencia insuficiente",
    percent: null,
    absolute: null,
  },
  series: [],
  areas: [],
  insights: [{ code: "pending", title: "Pendiente", detail: "5 kg" }],
  context: {
    coverage: "Cobertura desconocida",
    series_reason: "Sin registros",
  },
  provenance_totals: [],
};
const props = {
  data: {},
  user: {},
  operator: false,
  manager: false,
  admin: false,
  refresh: () => {},
  query: "provenance=simulado",
};
it("muestra cifras del backend, fuentes y ausencia de serie sin inventar datos", () => {
  render(<ReportsPage {...props} dashboard={dashboard} />);
  expect(screen.getByText("SIMULADO · demostración")).toBeInTheDocument();
  expect(
    screen.getByText("Aún no hay una serie para mostrar"),
  ).toBeInTheDocument();
  expect(
    screen.getByText("No hay áreas con generación para estos filtros."),
  ).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /Exportar CSV/ })).toHaveAttribute(
    "href",
    "/api/reports/generation.csv?provenance=simulado",
  );
});
it("hallazgos llevan a evidencia, no ejecutan una acción ambiental", () => {
  const open = vi.fn();
  render(<ReportsPage {...props} dashboard={dashboard} onExplore={open} />);
  fireEvent.click(screen.getByRole("button", { name: /Revisar registros/ }));
  expect(open).toHaveBeenCalledOnce();
});
it("balance conserva 25 = 20 + 5 y el KPI consulta la cohorte sin mutación", () => {
  const open = vi.fn();
  render(<ReportsPage {...props} dashboard={dashboard} onExplore={open} />);
  expect(
    screen.getByRole("img", {
      name: "20 kg acreditados y 5 kg pendientes de 25 kg generados",
    }),
  ).toBeInTheDocument();
  fireEvent.click(
    screen.getByRole("button", { name: "Consultar cohorte base de Generados" }),
  );
  expect(open).toHaveBeenCalledOnce();
});
it("el hallazgo de área transmite su filtro y expone límites y recomendación", () => {
  const open = vi.fn();
  render(
    <ReportsPage
      {...props}
      dashboard={{
        ...dashboard,
        insights: [
          {
            code: "largest_area",
            title: "Cafetería",
            detail: "25 kg",
            area: 7,
            interpretation: "No mide eficiencia",
            suggestion: "Revisar cobertura",
          },
        ],
      }}
      onExplore={open}
    />,
  );
  expect(screen.getByText("No mide eficiencia")).toBeInTheDocument();
  expect(screen.getByText(/Revisar cobertura/)).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: /Revisar registros/ }));
  expect(open).toHaveBeenCalledWith(7);
});
