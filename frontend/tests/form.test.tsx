import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { vi, it, expect, beforeEach } from "vitest";
import { api } from "../src/services/api";
import { ActionForm } from "../src/components/ActionForm";
vi.mock("../src/services/api", () => ({
  api: vi.fn().mockRejectedValue(new Error("Saldo insuficiente.")),
}));
beforeEach(() => {
  vi.mocked(api).mockClear();
});
it("conserva el peso y presenta rechazo del servidor", async () => {
  render(
    <ActionForm
      title="Guardar"
      path="lots"
      fields={[{ name: "kg", label: "Peso" }]}
      onDone={() => {}}
    />,
  );
  fireEvent.change(screen.getByLabelText("Peso"), { target: { value: "6" } });
  fireEvent.click(screen.getByRole("button", { name: "Guardar" }));
  await waitFor(() =>
    expect(screen.getByRole("alert")).toHaveTextContent("Saldo insuficiente"),
  );
  expect(screen.getByLabelText("Peso")).toHaveValue("6");
});

it("reintenta la misma operación sin duplicarla y cambia clave al corregir la masa", async () => {
  const done = vi.fn();
  render(
    <ActionForm
      title="Mover"
      path="lots/1/movements"
      fields={[{ name: "kg", label: "Masa" }]}
      onDone={done}
    />,
  );
  fireEvent.change(screen.getByLabelText("Masa"), { target: { value: "6" } });
  fireEvent.click(screen.getByRole("button", { name: "Mover" }));
  await screen.findByRole("alert");
  const first = vi.mocked(api).mock.calls[0][3];
  fireEvent.click(screen.getByRole("button", { name: "Mover" }));
  await screen.findByRole("alert");
  expect(vi.mocked(api).mock.calls[1][3]).toBe(first);
  vi.mocked(api).mockResolvedValueOnce({ id: 1 });
  fireEvent.change(screen.getByLabelText("Masa"), { target: { value: "5" } });
  fireEvent.click(screen.getByRole("button", { name: "Mover" }));
  await waitFor(() => expect(done).toHaveBeenCalledOnce());
  expect(vi.mocked(api).mock.calls[2][3]).not.toBe(first);
  expect(screen.getByLabelText("Masa")).toHaveValue("");
});
