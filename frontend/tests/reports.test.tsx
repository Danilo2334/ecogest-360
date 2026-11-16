import { render, screen } from "@testing-library/react";
import { it, expect } from "vitest";
import { ReportsPage } from "../src/features/reports/ReportsPage";
it("no inventa una tasa para un universo vacío y conserva filtros al exportar", () => {
  render(
    <ReportsPage
      data={{}}
      user={{}}
      operator={false}
      manager={false}
      admin={false}
      refresh={() => {}}
      query="provenance=medido"
      dashboard={{
        summary: {
          generated: "0.000",
          delivered: "0.000",
          verified_compost: "0.000",
          pending: "0.000",
          available: "0.000",
          in_process: "0.000",
          distribution: [],
          rate: null,
          provenance: "medido",
          formula: "A/G × 100",
          cutoff: "2026-11-15",
        },
        comparison: { available: false, reason: "Sin datos" },
        series: [],
        areas: [],
        insights: [],
        provenance_totals: [],
        context: { coverage: "", series_reason: "Sin registros" },
      }}
    />,
  );
  expect(screen.getByText("No calculable")).toBeInTheDocument();
  expect(
    screen.getByText("Sin generación para estos filtros."),
  ).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /Exportar CSV/ })).toHaveAttribute(
    "href",
    "/api/reports/generation.csv?provenance=medido",
  );
});
