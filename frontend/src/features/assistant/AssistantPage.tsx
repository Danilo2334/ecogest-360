import { useEffect, useRef, useState } from "react";
import { api } from "../../services/api";
import { kg } from "../../components/shared";
import s from "./Assistant.module.css";

type Fact = {
  id: string;
  title: string;
  values: Record<string, string | null>;
  page: string;
  area?: string;
  uuid?: string;
};
type Context = {
  status: string;
  reason: string;
  has_data: boolean;
  facts: Fact[];
  context: {
    provenance: string;
    cutoff: string;
    formula: string;
    limitations: string;
    filters?: Record<string, string>;
  };
  explanations: Record<string, string>;
  actions: Record<string, { text: string; page: string }>;
  answer: null | {
    sources: string[];
    explanations: string[];
    actions: string[];
    insufficient: boolean;
  };
};
const examples: Record<string, string[]> = {
  mis_datos: [
    "¿Qué área produjo más residuos?",
    "¿Cuánto está acreditado y cuánto pendiente?",
    "¿Qué lotes tienen procesos sin validación?",
  ],
  explicar: [
    "¿Qué significa la tasa de compostaje?",
    "¿Por qué no sumamos entrada y salida de compost?",
    "¿Qué diferencia hay entre medido, estimado y simulado?",
  ],
  proponer: [
    "¿Qué debo revisar primero en el área seleccionada?",
    "¿Cómo puedo comparar una mejora sin atribuirle una causa?",
  ],
};
const labels: Record<string, string> = {
  generated: "Generado",
  verified_compost: "Compostaje acreditado",
  pending: "Pendiente",
  rate: "Tasa de compostaje",
};

export function AssistantPage({
  query,
  onNavigate,
}: {
  query: string;
  onNavigate: (page: string, area?: string, uuid?: string) => void;
}) {
  const [context, setContext] = useState<Context | null>(null),
    [mode, setMode] = useState("mis_datos"),
    [question, setQuestion] = useState("");
  const [error, setError] = useState(""),
    [busy, setBusy] = useState(false),
    [revision, setRevision] = useState(0);
  const [exchange, setExchange] = useState<{
    question: string;
    result: Context;
    query: string;
  } | null>(null);
  const epoch = useRef(0),
    submitting = useRef(false);
  const prompt = useRef<HTMLTextAreaElement>(null);
  const activeRequest = useRef<AbortController | null>(null);
  useEffect(() => {
    let active = true;
    epoch.current++;
    setContext(null);
    setQuestion("");
    setError("");
    setBusy(false);
    submitting.current = false;
    api("v2/assistant/context?" + query)
      .then((d) => {
        if (active) setContext(d);
      })
      .catch((e) => {
        if (active) setError(e.message);
      });
    return () => {
      active = false;
      epoch.current++;
      activeRequest.current?.abort();
    };
  }, [query, revision]);
  async function send(e: React.FormEvent) {
    e.preventDefault();
    if (submitting.current) return;
    submitting.current = true;
    setBusy(true);
    setError("");
    const started = epoch.current,
      asked = question;
    const controller = new AbortController();
    activeRequest.current = controller;
    const deadline = window.setTimeout(() => controller.abort(), 30000);
    try {
      const result = await api(
        "v2/assistant",
        {
          mode,
          question: asked,
          filters: Object.fromEntries(new URLSearchParams(query)),
        },
        "POST",
        undefined,
        controller.signal,
      );
      if (started === epoch.current) {
        setExchange({ question: asked, result, query });
        if (result.status === "disponible") setContext(result);
      }
    } catch (e) {
      if (started === epoch.current)
        setError(
          controller.signal.aborted
            ? "La consulta superó el tiempo de espera. Puedes consultar las fuentes locales. Una consulta ya enviada puede consumir la reserva; no se reintenta automáticamente."
            : (e as Error).message,
        );
    } finally {
      window.clearTimeout(deadline);
      if (started === epoch.current) {
        setBusy(false);
        submitting.current = false;
      }
    }
  }
  function fact(f: Fact, stale = false) {
    return (
      <article className={s.fact} key={f.id}>
        <h4>{f.title}</h4>
        <dl>
          {Object.entries(f.values).map(([key, value]) => (
            <div key={key}>
              <dt>{labels[key] || key}</dt>
              <dd>
                {value === null
                  ? "No calculable"
                  : key === "rate"
                    ? `${Number(value).toLocaleString("es-CO")} %`
                    : `${kg(value)} kg`}
              </dd>
            </div>
          ))}
        </dl>
        <button
          type="button"
          disabled={stale}
          onClick={() => onNavigate(f.page, f.area, f.uuid)}
        >
          Ver evidencia{f.uuid ? " del lote" : ""} →
        </button>
      </article>
    );
  }
  return (
    <section className={s.assistant} aria-label="Asistente ambiental">
      <header className={s.hero}>
        <span>ASISTENTE AMBIENTAL · IA CON FUENTES</span>
        <h2>De la pregunta al siguiente paso.</h2>
        <p>
          Consulta lo que muestran tus datos. Comprende el indicador. Decide qué
          revisar.
        </p>
      </header>
      {error && (
        <div role="alert">
          <p>{error}</p>
          {!context && (
            <button onClick={() => setRevision((x) => x + 1)}>
              Reintentar contexto
            </button>
          )}
        </div>
      )}
      {!context && !error && (
        <p role="status">Preparando contexto autorizado…</p>
      )}
      {context && (
        <>
          <div className={s.status}>
            <strong>
              {context.status === "disponible"
                ? "OpenAI habilitado"
                : "OpenAI no disponible · consulta local disponible"}
            </strong>
            <span>
              {context.context.provenance.toUpperCase()} · Corte{" "}
              {new Date(context.context.cutoff).toLocaleString("es-CO")}
            </span>
          </div>
          <div className={s.layout}>
            <div className={s.conversation}>
              <form onSubmit={send} className={s.composer}>
                <label>
                  ¿Qué quieres hacer?
                  <select
                    value={mode}
                    onChange={(e) => {
                      setMode(e.target.value);
                      setQuestion("");
                    }}
                  >
                    <option value="mis_datos">Consultar mis datos</option>
                    <option value="explicar">Entender un concepto</option>
                    <option value="proponer">Proponer próximos pasos</option>
                  </select>
                </label>
                <div className={s.examples}>
                  {examples[mode].map((q) => (
                    <button
                      type="button"
                      key={q}
                      onClick={() => {
                        setQuestion(q);
                        prompt.current?.focus();
                      }}
                    >
                      {q}
                    </button>
                  ))}
                </div>
                <label>
                  Tu pregunta
                  <textarea
                    ref={prompt}
                    required
                    maxLength={2000}
                    rows={3}
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Por ejemplo: ¿qué significa la masa pendiente?"
                    aria-describedby="privacy-note"
                  />
                </label>
                <p id="privacy-note" className={s.note}>
                  No escribas nombres, correos, claves ni información privada.
                  Si habilitas OpenAI, se enviarán esta pregunta y agregados sin
                  nombres. La conversación desaparece al salir. No se guarda
                  historial en el servidor.
                </p>
                <button
                  type="submit"
                  disabled={busy || context.status !== "disponible"}
                >
                  {busy ? "Consultando fuentes…" : "Consultar con OpenAI →"}
                </button>
                {context.reason && (
                  <p role="status" className={s.note}>
                    {context.reason}
                  </p>
                )}
              </form>
              <div aria-live="polite" aria-busy={busy}>
                {exchange && (
                  <article className={s.response}>
                    <span>Tu consulta</span>
                    <p>{exchange.question}</p>
                    <h3>Orientación de IA</h3>
                    {exchange.query !== query && (
                      <p role="status">
                        Esta respuesta corresponde a filtros anteriores.
                        Conserva su corte y fuentes originales; realiza una
                        nueva consulta para el contexto actual.
                      </p>
                    )}
                    <p className={s.note}>
                      Corte original:{" "}
                      {new Date(exchange.result.context.cutoff).toLocaleString(
                        "es-CO",
                      )}{" "}
                      · {exchange.result.context.provenance.toUpperCase()}
                    </p>
                    <p className={s.note}>
                      Período original:{" "}
                      {exchange.result.context.filters?.generated_from ||
                        "ver contexto"}{" "}
                      —{" "}
                      {exchange.result.context.filters?.generated_to ||
                        "ver contexto"}
                    </p>
                    <button
                      disabled={busy}
                      onClick={() => {
                        setExchange(null);
                        setQuestion("");
                      }}
                    >
                      Limpiar conversación
                    </button>
                    {!exchange.result.answer ? (
                      <p>{exchange.result.reason}</p>
                    ) : exchange.result.answer.insufficient ? (
                      <p>
                        No hay evidencia suficiente en el contexto para
                        responder. Revisa las fuentes o reformula la pregunta.
                      </p>
                    ) : (
                      <>
                        <p className={s.note}>
                          La IA seleccionó estas evidencias y próximos pasos del
                          catálogo verificado. Las cifras las calcula EcoGest.
                        </p>
                        {exchange.result.facts
                          .filter((f) =>
                            exchange.result.answer!.sources.includes(f.id),
                          )
                          .map((f) => fact(f, exchange.query !== query))}
                        {exchange.result.answer.explanations.map((code) => (
                          <p key={code}>{exchange.result.explanations[code]}</p>
                        ))}
                        {exchange.result.answer.actions.length > 0 && (
                          <h4>Sugerencias · requieren decisión humana</h4>
                        )}
                        {exchange.result.answer.actions.map((code) => (
                          <p key={code}>
                            {exchange.result.actions[code].text}{" "}
                            <button
                              disabled={exchange.query !== query}
                              onClick={() =>
                                onNavigate(exchange.result.actions[code].page)
                              }
                            >
                              Abrir siguiente paso →
                            </button>
                          </p>
                        ))}
                      </>
                    )}
                    <p className={s.note}>
                      La IA puede equivocarse; verifica las fuentes. No
                      constituye certificación profesional.
                    </p>
                  </article>
                )}
              </div>
              <section className={s.method}>
                <h3>Comprender sin IA</h3>
                <p>
                  Explicaciones locales revisadas, disponibles sin conexión con
                  OpenAI.
                </p>
                {Object.entries(context.explanations).map(([code, value]) => (
                  <details key={code}>
                    <summary>
                      {
                        {
                          rate: "¿Cómo se calcula la tasa?",
                          output: "¿Por qué entrada y salida no se suman?",
                          provenance: "Medido, estimado y simulado",
                          pending: "¿Qué significa pendiente?",
                          comparison: "Comparar sin inventar causas",
                          safety: "Límites del apoyo ambiental",
                        }[code]
                      }
                    </summary>
                    <p>{value}</p>
                  </details>
                ))}
              </section>
            </div>
            <aside className={s.sources}>
              <h3>La evidencia primero</h3>
              <p className={s.note}>
                Datos de tus filtros. Áreas: hasta tres, por masa descendente.
                Lotes: muestra de hasta cinco con procesos sin validación al
                corte.
              </p>
              {!context.has_data && (
                <p>No hay registros para este período y procedencia.</p>
              )}
              {context.facts.slice(0, 2).map((f) => fact(f))}
              {context.facts.length > 2 && (
                <details>
                  <summary>
                    Ver más fuentes ({context.facts.length - 2})
                  </summary>
                  {context.facts.slice(2).map((f) => fact(f))}
                </details>
              )}
              <details>
                <summary>Ver metodología y límites</summary>
                <p>{context.context.formula}</p>
                <p>{context.context.limitations}</p>
              </details>
              <button onClick={() => onNavigate("Simulador")}>
                Explorar un escenario →
              </button>
            </aside>
          </div>
        </>
      )}
    </section>
  );
}
