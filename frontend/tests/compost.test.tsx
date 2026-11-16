import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { CompostPage } from "../src/features/compost/CompostPage";
it("explica que un estimado no acredita y no ofrece confirmarlo", () => {
  render(
    <CompostPage
      data={{
        processes: [
          {
            id: 1,
            provenance: "estimado",
            state: "finalizado",
            verified: false,
            inputs: [],
            evidence: [],
            measurements: [],
            verifications: [],
            output: "8.000",
          },
        ],
        lots: [],
      }}
      user={{ role: "gestor" }}
      operator={false}
      manager={true}
      admin={false}
      refresh={() => {}}
      dashboard={null}
      query=""
    />,
  );
  expect(screen.getByText(/Proceso estimado: no acredita/)).toBeInTheDocument();
  expect(
    screen.queryByRole("option", { name: "Confirmar evidencia completa" }),
  ).toBeNull();
  expect(
    screen.getByRole("option", { name: "Rechazar: queda pendiente" }),
  ).toBeInTheDocument();
});
