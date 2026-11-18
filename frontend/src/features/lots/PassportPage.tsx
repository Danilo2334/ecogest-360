import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { kg } from "../../components/shared";
import s from "./Passport.module.css";
type Event = {
  key: string;
  kind: string;
  date: string;
  actor: string | null;
  kg: string | null;
  balance_effect: string;
  description: string;
  process: number | null;
  evidence_url: string | null;
};
type Passport = {
  lot: { id: number; public_id: string; provenance: string; state: string };
  balance: { assigned: string; available: string; consumed: string };
  sources: {
    generation: number;
    area: string;
    area_id: number;
    material: string;
    material_id: number;
    assigned: string;
    generated: string;
    date: string;
    provenance: string;
  }[];
  events: Event[];
  processes: {
    id: number;
    state: string;
    provenance: string;
    lot_input: string;
    total_input: string;
    output: string | null;
    shared: boolean;
    verified: boolean;
  }[];
  cutoff: string;
  limitations: string;
};
const names: Record<string, string> = {
  generacion: "Registro de origen",
  lote: "Lote creado",
  logistico: "Traslado sin consumo",
  entrega: "Entrega a tercero",
  entrada_compostaje: "Entrada a compostaje",
  control: "Control del proceso",
  salida: "Compost obtenido",
  evidencia: "Evidencia de destino",
  validacion: "Revisión del resultado",
  revision: "Cambio auditado",
};
const date = (value: string) =>
  new Date(value).toLocaleString("es-CO", {
    timeZone: "America/Bogota",
    dateStyle: "medium",
    timeStyle: "short",
  });
export function PassportPage({
  uuid,
  onBack,
}: {
  uuid: string;
  onBack: () => void;
}) {
  const [data, setData] = useState<Passport | null>(null),
    [error, setError] = useState(""),
    [retry, setRetry] = useState(0);
  const [includeOrigins, setIncludeOrigins] = useState(false);
  function cohortQuery() {
    if (!data || !data.sources.length) return "";
    const dates = data.sources
      .map((x) =>
        new Date(x.date).toLocaleDateString("sv-SE", {
          timeZone: "America/Bogota",
        }),
      )
      .sort();
    const areas = [...new Set(data.sources.map((x) => x.area_id))];
    const materials = [...new Set(data.sources.map((x) => x.material_id))];
    return new URLSearchParams({
      provenance: data.lot.provenance,
      generated_from: dates[0],
      generated_to: dates[dates.length - 1],
      ...(areas.length === 1 ? { area: String(areas[0]) } : {}),
      ...(materials.length === 1 ? { material: String(materials[0]) } : {}),
    }).toString();
  }
  useEffect(() => {
    let active = true;
    setData(null);
    setError("");
    api(`v2/lots/${encodeURIComponent(uuid)}/passport`)
      .then((d) => {
        if (active) setData(d);
      })
      .catch((e) => {
        if (active) setError(e.message);
      });
    return () => {
      active = false;
    };
  }, [uuid, retry]);
  return (
    <section className={s.passport} aria-label="Pasaporte ambiental">
      <button className={s.back} onClick={onBack}>
        ← Volver a trazabilidad
      </button>
      {error ? (
        <div role="alert">
          <h2>No se pudo consultar este lote</h2>
          <p>{error}</p>
          <button onClick={() => setRetry((x) => x + 1)}>
            Reintentar consulta
          </button>
        </div>
      ) : !data ? (
        <p role="status">Consultando historia del lote…</p>
      ) : (
        <>
          <header className={s.hero}>
            <span>PASAPORTE AMBIENTAL · CONSULTA AUTORIZADA</span>
            <h2>La historia del lote #{data.lot.id}</h2>
            <p>
              {[...new Set(data.sources.map((x) => x.material))].join(" · ") ||
                "Material no registrado"}
            </p>
            <p>
              {data.lot.provenance.toUpperCase()} · {data.lot.state}
            </p>
            <small>{data.lot.public_id}</small>
          </header>
          {data.sources.length > 0 && (
            <p className={s.note}>
              Explora la cohorte del período y origen de este lote; puede
              incluir otros registros del mismo universo.{" "}
              <a href={"/simulador?" + cohortQuery()}>
                Simular una alternativa
              </a>{" "}
              ·{" "}
              <a href={"/asistente?" + cohortQuery()}>Consultar al asistente</a>
            </p>
          )}
          <div className={s.balance} aria-label="Balance del lote">
            {[
              ["Asignado", data.balance.assigned],
              ["Disponible", data.balance.available],
              ["Consumido", data.balance.consumed],
            ].map(([label, value]) => (
              <article key={label}>
                <span>{label}</span>
                <strong>
                  {kg(value)} <small>kg</small>
                </strong>
              </article>
            ))}
          </div>
          <p className={s.note}>
            Asignado − consumos = disponible. Los traslados tienen efecto cero.
            Corte: {date(data.cutoff)}.
          </p>
          <div className={s.layout}>
            <section className={s.panel}>
              <h3>Del origen al destino</h3>
              <p>
                Cada hito corresponde a un registro existente. Abre sus detalles
                para revisar quién lo registró y cómo afecta el saldo.
              </p>
              <label>
                <input
                  type="checkbox"
                  checked={includeOrigins}
                  onChange={(e) => setIncludeOrigins(e.target.checked)}
                />
                Incluir eventos de generación ({data.sources.length})
              </label>
              <ol className={s.timeline}>
                {data.events
                  .filter((e) => includeOrigins || e.kind !== "generacion")
                  .map((e) => (
                    <li key={e.key}>
                      <div>
                        <time dateTime={e.date}>{date(e.date)}</time>
                        <h4>
                          {names[e.kind] || e.kind}
                          {e.process ? ` · proceso #${e.process}` : ""}
                        </h4>
                        <p>
                          {e.kg !== null ? `${kg(e.kg)} kg · ` : ""}Efecto en
                          saldo: {kg(e.balance_effect)} kg
                        </p>
                        <details>
                          <summary>Ver responsable y evidencia</summary>
                          <p>
                            Responsable registrado:{" "}
                            {e.actor || "No disponible en el registro original"}
                          </p>
                          <p>{e.description}</p>
                          {e.evidence_url && (
                            <a href={e.evidence_url}>
                              Descargar evidencia autorizada
                            </a>
                          )}
                        </details>
                      </div>
                    </li>
                  ))}
              </ol>
            </section>
            <aside className={s.side}>
              <details className={s.panel}>
                <summary>Orígenes documentados ({data.sources.length})</summary>
                {data.sources.map((x) => (
                  <div className={s.source} key={x.generation}>
                    <strong>
                      {x.area} · {x.material}
                    </strong>
                    <p>
                      Registro #{x.generation}: {kg(x.assigned)} kg asignados de{" "}
                      {kg(x.generated)} kg generados.
                    </p>
                    <p>
                      {x.provenance} · {date(x.date)}
                    </p>
                  </div>
                ))}
              </details>
              <section className={s.panel}>
                <h3>Tratamiento y evidencia</h3>
                {!data.processes.length && <p>Sin tratamiento registrado.</p>}
                {!data.processes.some((x) => x.verified) && (
                  <p>Sin verificación registrada.</p>
                )}
                {data.processes.map((p) => (
                  <article className={s.source} key={p.id}>
                    <h4>
                      Proceso #{p.id} · {p.provenance}
                    </h4>
                    <p>
                      Entrada de este lote:{" "}
                      <strong>{kg(p.lot_input)} kg</strong>
                    </p>
                    <p>Entrada total del proceso: {kg(p.total_input)} kg</p>
                    <p>
                      Salida independiente:{" "}
                      {p.output === null
                        ? "Sin registro"
                        : `${kg(p.output)} kg`}
                    </p>
                    {p.shared && (
                      <p>
                        Proceso compartido: la salida pertenece al proceso
                        completo, no se reparte como medición de cada lote.
                      </p>
                    )}
                    <p>
                      {p.state} ·{" "}
                      {p.verified
                        ? "Con verificación registrada"
                        : "Sin verificación registrada"}
                    </p>
                  </article>
                ))}
              </section>
              <details className={s.panel}>
                <summary>QR e identificación del lote</summary>
                <img
                  src={`/api/lots/${data.lot.id}/image`}
                  width="180"
                  height="180"
                  alt={`QR de consulta autorizada del lote ${data.lot.id}`}
                />
                <p>
                  El QR conserva la identificación original y exige sesión
                  autorizada.
                </p>
                <a
                  href={`/api/lots/${data.lot.id}/image`}
                  download={`lote-${data.lot.id}.png`}
                >
                  Descargar QR
                </a>
              </details>
            </aside>
          </div>
          <p className={s.note}>{data.limitations}</p>
        </>
      )}
    </section>
  );
}
