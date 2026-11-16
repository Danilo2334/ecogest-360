import { useEffect, useState } from "react";
import { api, type Row } from "../../services/api";
import { ActionForm, type Field } from "../../components/ActionForm";
import { kg, opts, type FeatureProps } from "../../components/shared";
import type { Scenario } from "../scenarios/ScenarioPage";
import s from "../lots/Passport.module.css";
const indicators = [
  { value: "generated", label: "Generación (kg)" },
  { value: "verified_compost", label: "Compostaje acreditado (kg)" },
  { value: "rate", label: "Tasa de compostaje (%)" },
];
const directions = [
  { value: "reduce", label: "Reducir hasta la meta" },
  { value: "increase", label: "Aumentar hasta la meta" },
];
const states: Record<string, string> = {
  borrador: "Borrador",
  en_curso: "En curso",
  en_evaluacion: "En evaluación",
  cerrado: "Cerrado",
  cancelado: "Cancelado",
};
const results: Record<string, string> = {
  alcanzada: "Meta alcanzada observada",
  no_alcanzada: "Meta no alcanzada",
  no_evaluable: "No evaluable",
};
export function PlansPage({
  data,
  manager,
  query,
  proposal,
  onClearProposal,
}: { proposal?: Scenario | null; onClearProposal: () => void } & Pick<
  FeatureProps,
  "data" | "manager" | "query"
>) {
  const [plans, setPlans] = useState<Row[]>([]),
    [users, setUsers] = useState<Row[]>([]),
    [selected, setSelected] = useState<number | null>(null),
    [creating, setCreating] = useState(!!proposal),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(true),
    [revision, setRevision] = useState(0);
  useEffect(() => {
    let active = true;
    setBusy(true);
    setError("");
    Promise.all([api("v2/plans"), api("v2/plan-options")])
      .then(([p, u]) => {
        if (active) {
          setPlans(p);
          setUsers(u);
        }
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setBusy(false);
      });
    return () => {
      active = false;
    };
  }, [revision]);
  const refresh = () => {
    setRevision((x) => x + 1);
    setCreating(false);
    onClearProposal();
  };
  const filters =
    proposal?.filters || Object.fromEntries(new URLSearchParams(query));
  const p = plans.find((x) => x.id === selected);
  const editable = manager && p && !["cerrado", "cancelado"].includes(p.state);
  const reason: Field = { name: "reason", label: "Motivo de esta decisión" };
  const common: Field[] = [
    { name: "problem", label: "Problema observado" },
    { name: "action", label: "Acción que realizaremos" },
    {
      name: "responsible",
      label: "Responsable institucional",
      options: opts(users),
    },
    { name: "target", label: "Meta numérica", type: "number" },
    { name: "direction", label: "Dirección de la meta", options: directions },
    { name: "due_date", label: "Fecha objetivo", type: "date" },
    reason,
  ];
  return (
    <section className={s.passport} aria-label="Planes ambientales">
      <header className={s.hero}>
        <span>DECISIONES HUMANAS · EVIDENCIA CONSERVADA</span>
        <h2>Del hallazgo a una acción verificable.</h2>
        <p>
          Una actividad completada no equivale a una mejora ambiental. Evalúa
          con períodos comparables.
        </p>
      </header>
      {busy && <p role="status">Cargando planes…</p>}
      {error && <p role="alert">{error}</p>}
      <button className={s.back} onClick={() => setRevision((x) => x + 1)}>
        Actualizar lista y versiones
      </button>
      {manager && (
        <button
          onClick={() => {
            setCreating(!creating);
            setSelected(null);
          }}
        >
          {creating ? "Ocultar formulario" : "Preparar nuevo plan"}
        </button>
      )}
      {creating && manager && (
        <section className={s.panel} style={{ marginTop: 20 }}>
          <h3>Revisa la propuesta antes de guardar</h3>
          <p>
            Base: {filters.generated_from} — {filters.generated_to} ·{" "}
            {filters.provenance || "Selecciona procedencia"}. El servidor vuelve
            a comprobar la evidencia.
          </p>
          {proposal && (
            <p>
              Propuesta hipotética de {kg(proposal.amount)} kg, no una medición.
              La base debe seguir vigente y el área debe coincidir.
            </p>
          )}
          <ActionForm
            key={JSON.stringify(filters)}
            title="Guardar borrador del plan"
            path="v2/plans"
            onDone={refresh}
            fields={[
              ...common.map((f) =>
                f.name === "action" && proposal
                  ? {
                      ...f,
                      value: `Revisar viabilidad de hipótesis ${proposal.hypothesis === "increase_compost" ? "aumentar compostaje acreditado" : "reducir generación no aprovechable"}: ${proposal.amount} kg; decisión humana pendiente.`,
                    }
                  : f,
              ),
              {
                name: "area",
                label: "Área del plan",
                options: opts(data.areas),
                value: filters.area,
              },
              {
                name: "indicator",
                label: "Indicador que evaluaremos",
                options: indicators,
              },
            ]}
            transform={(d) => ({
              ...d,
              filters: { ...filters, area: String(d.area) },
              ...(proposal ? { scenario: proposal } : {}),
            })}
          />
        </section>
      )}
      {!p && (
        <div className={s.layout} style={{ marginTop: 20 }}>
          {plans.map((plan) => (
            <article className={s.panel} key={plan.id}>
              <span>
                {states[plan.state]} · {plan.provenance.toUpperCase()}
              </span>
              <h3>{plan.problem}</h3>
              <p>
                {plan.area_name} · {plan.responsible_name}
              </p>
              <p>
                Base {kg(plan.baseline.value)} → meta {kg(plan.target)}{" "}
                {plan.indicator === "rate" ? "%" : "kg"} · plazo {plan.due_date}
              </p>
              <button
                onClick={() => {
                  setSelected(plan.id);
                  setCreating(false);
                }}
              >
                Revisar plan #{plan.id}
              </button>
            </article>
          ))}
        </div>
      )}
      {!busy && !plans.length && (
        <p>
          Todavía no hay planes. Un gestor puede preparar uno desde un hallazgo
          o escenario.
        </p>
      )}
      {p && (
        <>
          <button className={s.back} onClick={() => setSelected(null)}>
            ← Volver a los planes
          </button>
          <div className={`${s.layout} ${s.planLayout}`}>
            <section className={s.panel}>
              <span>
                {states[p.state]} · {p.provenance.toUpperCase()} · versión{" "}
                {p.version}
              </span>
              <h3>{p.problem}</h3>
              <p>{p.action}</p>
              {p.responsible_active === false && (
                <p role="status">
                  Responsable inactivo o fuera de la institución. El gestor debe
                  revisar la asignación; se conserva el historial anterior.
                </p>
              )}
              <p>
                {p.responsible_name} · {p.area_name} · fecha objetivo:{" "}
                {p.due_date}
              </p>
              <div className={s.balance}>
                <article>
                  <span>
                    Base {p.state === "borrador" ? "provisional" : "conservada"}
                  </span>
                  <strong>{kg(p.baseline.value)}</strong>
                </article>
                <article>
                  <span>
                    Meta {p.direction === "reduce" ? "máxima" : "mínima"}
                  </span>
                  <strong>{kg(p.target)}</strong>
                </article>
              </div>
              <p>
                {indicators.find((x) => x.value === p.indicator)?.label} ·{" "}
                {p.filters.generated_from} — {p.filters.generated_to}
              </p>
              <details>
                <summary>Fuente y límites de la base</summary>
                <p>{p.baseline.summary.formula}</p>
                <p>{p.baseline.summary.limitations}</p>
                <p>
                  Registros:{" "}
                  {p.baseline.sources.map((r: Row) => `#${r.id}`).join(", ")}
                </p>
              </details>
              <h3>Evaluaciones registradas</h3>
              {!p.evaluations.length && (
                <p>Sin evaluación: no se declara meta alcanzada.</p>
              )}
              {p.evaluations.map((e: Row) => (
                <article className={s.source} key={e.id}>
                  <h4>{results[e.status]}</h4>
                  {e.version !== p.version && p.state !== "cerrado" && (
                    <p>
                      Evaluación de una versión anterior. Reevalúa antes de
                      cerrar el plan.
                    </p>
                  )}
                  <p>
                    {e.filters.generated_from} — {e.filters.generated_to}:{" "}
                    {e.observation.value === null
                      ? "No calculable"
                      : kg(e.observation.value)}
                  </p>
                  <p>{e.explanation}</p>
                  <p>
                    {e.actor} · {new Date(e.date).toLocaleString("es-CO")}
                  </p>
                </article>
              ))}
              <h3>Seguimiento humano</h3>
              {!p.followups.length && <p>Sin avances registrados.</p>}
              {p.followups.map((f: Row) => (
                <p key={f.id}>
                  {f.text} — {f.actor},{" "}
                  {new Date(f.date).toLocaleString("es-CO")}
                </p>
              ))}
            </section>
            <aside className={s.side}>
              {editable && (
                <>
                  <details className={s.panel}>
                    <summary>Editar acción, responsable o meta</summary>
                    <ActionForm
                      key={`edit-${p.version}`}
                      title="Guardar revisión del plan"
                      path={`v2/plans/${p.id}`}
                      method="PATCH"
                      defaults={{ version: p.version }}
                      fields={common.map((f) => ({
                        ...f,
                        value:
                          f.name === "reason" ? "" : String(p[f.name] ?? ""),
                      }))}
                      onDone={refresh}
                    />
                  </details>
                  <details className={s.panel}>
                    <summary>Registrar seguimiento</summary>
                    <ActionForm
                      title="Guardar seguimiento"
                      path={`v2/plans/${p.id}/followups`}
                      defaults={{ version: p.version }}
                      fields={[
                        {
                          name: "text",
                          label: "Actividad y evidencia observada",
                        },
                        reason,
                      ]}
                      onDone={refresh}
                    />
                  </details>
                  {p.state === "en_evaluacion" && (
                    <section className={s.panel}>
                      <ActionForm
                        title="Evaluar período posterior"
                        path={`v2/plans/${p.id}/evaluations`}
                        defaults={{ version: p.version }}
                        fields={[
                          {
                            name: "generated_from",
                            label: "Inicio del período posterior",
                            type: "date",
                          },
                          {
                            name: "generated_to",
                            label: "Fin del período posterior",
                            type: "date",
                          },
                          reason,
                        ]}
                        onDone={refresh}
                      />
                    </section>
                  )}
                  <section className={s.panel}>
                    <ActionForm
                      title="Confirmar cambio de estado"
                      path={`v2/plans/${p.id}/transitions`}
                      defaults={{ version: p.version }}
                      fields={[
                        {
                          name: "state",
                          label: "Nuevo estado",
                          options: [
                            {
                              value: (
                                {
                                  borrador: "en_curso",
                                  en_curso: "en_evaluacion",
                                  en_evaluacion: "cerrado",
                                } as Record<string, string>
                              )[p.state],
                              label: (
                                {
                                  borrador: "Iniciar y conservar base",
                                  en_curso: "Pasar a evaluación",
                                  en_evaluacion:
                                    "Cerrar con evaluación registrada",
                                } as Record<string, string>
                              )[p.state],
                            },
                            {
                              value: "cancelado",
                              label: "Cancelar conservando historia",
                            },
                          ],
                        },
                        reason,
                      ]}
                      onDone={refresh}
                    />
                  </section>
                </>
              )}
              <details className={s.panel}>
                <summary>
                  Historial de decisiones ({p.revisions.length})
                </summary>
                {p.revisions.map((r: Row) => (
                  <article className={s.source} key={r.id}>
                    <p>
                      {r.reason} — {r.actor}
                    </p>
                    <time>{new Date(r.date).toLocaleString("es-CO")}</time>
                    <details>
                      <summary>Valores anteriores y posteriores</summary>
                      <p>
                        Estado: {r.before.state || "Sin plan"} → {r.after.state}
                        ; meta: {r.before.target ?? "Sin meta"} →{" "}
                        {r.after.target}; versión: {r.after.version}
                      </p>
                    </details>
                  </article>
                ))}
              </details>
            </aside>
          </div>
        </>
      )}
    </section>
  );
}
