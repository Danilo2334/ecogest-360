import {
  render,
  screen,
  cleanup,
  fireEvent,
  within,
} from "@testing-library/react";
import { it, expect, vi, afterEach } from "vitest";
import { AssistantPage } from "../src/features/assistant/AssistantPage";
import { api } from "../src/services/api";
vi.mock("../src/services/api", () => ({ api: vi.fn() }));
afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});
const context = {
  status: "no_disponible",
  reason: "Falta presupuesto autorizado",
  has_data: true,
  answer: null,
  context: {
    provenance: "simulado",
    cutoff: "2026-11-16T12:00:00Z",
    formula: "A/G",
    limitations: "Solo compostaje",
  },
  facts: [
    {
      id: "cohort",
      title: "Balance de la cohorte seleccionada",
      values: { generated: "25.000" },
      page: "Resumen",
    },
  ],
  explanations: { rate: "La tasa usa entradas verificadas." },
  actions: { review: { text: "Revisar evidencia", page: "Registros" } },
};
it("explicación local disponible sin fingir IA ni permitir envío pagado", async () => {
  vi.mocked(api).mockResolvedValue(context);
  render(<AssistantPage query="provenance=simulado" onNavigate={() => {}} />);
  expect(await screen.findByText(/OpenAI no disponible/)).toBeVisible();
  expect(
    screen.getByRole("button", { name: /Consultar con OpenAI/ }),
  ).toBeDisabled();
  expect(
    screen.getByRole("heading", { name: "Comprender sin IA" }),
  ).toBeVisible();
  expect(vi.mocked(api).mock.calls.every((c) => c.length === 1)).toBe(true);
});
it("respuesta simulada muestra fuentes y conserva navegación autorizada", async () => {
  const navigate = vi.fn();
  vi.mocked(api)
    .mockResolvedValueOnce({ ...context, status: "disponible", reason: "" })
    .mockResolvedValue({
      ...context,
      status: "disponible",
      reason: "",
      answer: {
        sources: ["cohort"],
        explanations: ["rate"],
        actions: ["review"],
        insufficient: false,
      },
    });
  render(<AssistantPage query="provenance=simulado" onNavigate={navigate} />);
  await screen.findByText("OpenAI habilitado");
  fireEvent.change(screen.getByLabelText("Tu pregunta"), {
    target: { value: "¿Qué revisar?" },
  });
  fireEvent.click(screen.getByRole("button", { name: /Consultar con OpenAI/ }));
  expect(
    await screen.findByRole("heading", { name: "Orientación de IA" }),
  ).toBeVisible();
  fireEvent.click(screen.getByRole("button", { name: /Abrir siguiente paso/ }));
  expect(navigate).toHaveBeenCalledWith("Registros");
});
it("cambiar filtros descarta conversación y respuesta tardía", async () => {
  let resolve!: (value: unknown) => void;
  vi.mocked(api).mockImplementation((_path, data) =>
    data === undefined
      ? Promise.resolve({ ...context, status: "disponible" })
      : new Promise((r) => {
          resolve = r;
        }),
  );
  const view = render(<AssistantPage query="area=1" onNavigate={() => {}} />);
  await screen.findByText("OpenAI habilitado");
  fireEvent.change(screen.getByLabelText("Tu pregunta"), {
    target: { value: "Consulta anterior" },
  });
  fireEvent.click(screen.getByRole("button", { name: /Consultar con OpenAI/ }));
  view.rerender(<AssistantPage query="area=2" onNavigate={() => {}} />);
  resolve(context);
  await screen.findByText("OpenAI habilitado");
  expect(screen.queryByText("Consulta anterior")).not.toBeInTheDocument();
});

it("respuesta previa conserva contexto y desactiva acciones con filtros diferentes", async () => {
  vi.mocked(api).mockImplementation((_path, data) =>
    Promise.resolve(
      data === undefined
        ? { ...context, status: "disponible" }
        : {
            ...context,
            status: "disponible",
            answer: {
              sources: ["cohort"],
              explanations: ["rate"],
              actions: ["review"],
              insufficient: false,
            },
          },
    ),
  );
  const view = render(<AssistantPage query="area=1" onNavigate={() => {}} />);
  await screen.findByText("OpenAI habilitado");
  fireEvent.change(screen.getByLabelText("Tu pregunta"), {
    target: { value: "Pregunta de la primera área" },
  });
  fireEvent.click(screen.getByRole("button", { name: /Consultar con OpenAI/ }));
  await screen.findByRole("heading", { name: "Orientación de IA" });
  view.rerender(<AssistantPage query="area=2" onNavigate={() => {}} />);
  expect(
    await screen.findByText(/Esta respuesta corresponde a filtros anteriores/),
  ).toBeVisible();
  const response = screen
    .getByRole("heading", { name: "Orientación de IA" })
    .closest("article")!;
  expect(
    within(response).getByRole("button", { name: /Abrir siguiente paso/ }),
  ).toBeDisabled();
  expect(
    within(response).getByRole("button", { name: /Ver evidencia/ }),
  ).toBeDisabled();
  fireEvent.click(
    within(response).getByRole("button", { name: "Limpiar conversación" }),
  );
  expect(
    screen.queryByText("Pregunta de la primera área"),
  ).not.toBeInTheDocument();
});
