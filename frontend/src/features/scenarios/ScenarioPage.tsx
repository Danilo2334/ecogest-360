import { useEffect, useState, useRef } from "react";
import { api } from "../../services/api";
import { kg } from "../../components/shared";
import s from "../lots/Passport.module.css";
type Values = {
  generated: string;
  verified_compost: string;
  pending: string;
  rate: string | null;
};
export type Scenario = {
  base: Values & { cutoff: string; provenance: string };
  result: Values;
  eligible: string;
  nonrecoverable: string;
  base_token: string;
  formula: string;
  limitations: string;
  delta: {
    generated: string;
    verified_compost: string;
    generated_percent: string | null;
    rate_points: string | null;
  };
  filters: Record<string, string>;
  hypothesis: string;
  amount: string;
};
export function ScenarioPage({
  query,
  onPlan,
}: {
  query: string;
  onPlan?: (scenario: Scenario) => void;
}) {
  const epoch = useRef(0);
  const [hypothesis, setHypothesis] = useState("increase_compost"),
    [amount, setAmount] = useState("0"),
    [data, setData] = useState<Scenario | null>(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false),
    [revision, setRevision] = useState(0);
  useEffect(() => {
    epoch.current++;
    let active = true;
    setData(null);
    setError("");
    setAmount("0");
    setBusy(true);
    api("v2/scenarios/preview", {
      filters: Object.fromEntries(new URLSearchParams(query)),
      hypothesis,
      amount: "0",
    })
      .then((d) => {
        if (active) setData(d);
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setBusy(false);
      });
    return () => {
      active = false;
      epoch.current++;
    };
  }, [query, hypothesis, revision]);
  async function calculate(e: React.FormEvent) {
    e.preventDefault();
    if (!data) return;
    setBusy(true);
    setError("");
    const started = epoch.current;
    try {
      const result = await api("v2/scenarios/preview", {
        filters: data.filters,
        hypothesis,
        amount,
        base_token: data.base_token,
      });
      if (started === epoch.current) setData(result);
    } catch (e) {
      if (started === epoch.current) setError((e as Error).message);
    } finally {
      if (started === epoch.current) setBusy(false);
    }
  }
  return (
    <section className={s.passport} aria-label="Simulador ambiental">
      <header className={s.hero}>
        <span>ESCENARIO HIPOTÉTICO</span>
        <h2>Explora una alternativa antes de actuar.</h2>
        <p>No modifica mediciones ni datos operativos.</p>
      </header>
      <div className={s.layout} style={{ marginTop: 20 }}>
        <section className={s.panel}>
          <h3>¿Qué quieres explorar?</h3>
          <form onSubmit={calculate}>
            <label>
              Hipótesis
              <select
                value={hypothesis}
                onChange={(e) => setHypothesis(e.target.value)}
              >
                <option value="increase_compost">
                  Aumentar compostaje acreditado hipotético
                </option>
                <option value="reduce_nonrecoverable">
                  Reducir generación no aprovechable
                </option>
              </select>
            </label>
            <p>
              Solo una hipótesis por cálculo. Cambiar filtros exige una nueva
              base.
            </p>
            <label>
              Cantidad hipotética (kg)
              <input
                type="number"
                step="0.001"
                min="0"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </label>
            <p>
              {data
                ? `Límite de esta base: ${kg(hypothesis === "increase_compost" ? data.eligible : data.nonrecoverable)} kg`
                : "Selecciona filtros con registros y procedencia única."}
            </p>
            <button disabled={busy || !data}>Calcular escenario</button>
          </form>
          <button
            className={s.back}
            onClick={() => setRevision((x) => x + 1)}
            disabled={busy}
          >
            Recargar base actual y restablecer
          </button>
          {busy && <p role="status">Consultando la base autorizada…</p>}
          {error && <p role="alert">{error}</p>}
        </section>
        <section className={s.panel}>
          <h3>Base frente a hipótesis</h3>
          {data && (
            <>
              <p>
                {data.base.provenance.toUpperCase()} · corte{" "}
                {new Date(data.base.cutoff).toLocaleString("es-CO")}
              </p>
              <div style={{ overflowX: "auto" }}>
                <table>
                  <caption>Valores en kg, salvo tasa (%)</caption>
                  <thead>
                    <tr>
                      <th>Indicador</th>
                      <th>Base</th>
                      <th>Hipótesis</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(
                      [
                        ["generated", "Generación"],
                        ["verified_compost", "Compostaje acreditado"],
                        ["pending", "Pendiente"],
                        ["rate", "Tasa de compostaje"],
                      ] as const
                    ).map(([key, label]) => (
                      <tr key={key}>
                        <th>{label}</th>
                        <td>
                          {data.base[key] === null
                            ? "No calculable"
                            : kg(data.base[key])}
                        </td>
                        <td>
                          {data.result[key] === null
                            ? "No calculable"
                            : kg(data.result[key])}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p>
                Diferencia en generación: {kg(data.delta.generated)} kg (
                {data.delta.generated_percent === null
                  ? "No calculable"
                  : `${kg(data.delta.generated_percent)} %`}
                ).
              </p>
              <p>
                Diferencia en acreditación hipotética:{" "}
                {kg(data.delta.verified_compost)} kg. Variación de tasa:{" "}
                {data.delta.rate_points === null
                  ? "No calculable"
                  : `${kg(data.delta.rate_points)} puntos porcentuales`}
                .
              </p>
              <details>
                <summary>Fórmula, supuestos y límites</summary>
                <p>{data.formula}</p>
                <p>{data.limitations}</p>
              </details>
              {onPlan && (
                <button
                  disabled={
                    busy ||
                    !!error ||
                    !data.filters.area ||
                    (amount !== data.amount &&
                      Number(amount) !== Number(data.amount))
                  }
                  onClick={() => onPlan(data)}
                >
                  Revisar propuesta de plan
                </button>
              )}
              {onPlan && !data.filters.area && (
                <p>
                  Selecciona un área en los filtros para preparar un plan con
                  responsable y alcance concreto.
                </p>
              )}
            </>
          )}
        </section>
      </div>
    </section>
  );
}
