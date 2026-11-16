import { useState } from "react";
import { kg, type FeatureProps } from "../../components/shared";
import { MetricCard } from "../../components/MetricCard";
import type { Observatory } from "./types";
import s from "./Observatory.module.css";
const dateLabel = (value: string) =>
  new Intl.DateTimeFormat("es-CO", { day: "2-digit", month: "short" }).format(
    new Date(value + "T12:00:00"),
  );

export function ReportsPage({
  dashboard,
  query,
  onExplore,
}: FeatureProps & { onExplore?: (area?: number) => void }) {
  const [ranking, setRanking] = useState<"generated" | "pending">("generated");
  if (!dashboard) return null;
  const data = dashboard as Observatory;
  const d = data.summary;
  const c = data.comparison;
  const mixed = d.provenance.startsWith("todas");
  const areas = [...data.areas].sort(
    (a, b) =>
      Number(b[ranking]) - Number(a[ranking]) ||
      a.name.localeCompare(b.name) ||
      a.id - b.id,
  );
  const maxArea = Math.max(1, ...areas.map((a) => Number(a[ranking])));
  const maxDay = Math.max(1, ...data.series.map((a) => Number(a.kg)));
  const singleDay = data.series.length === 1;
  const firstDate = data.series[0]?.date;
  const lastDate = data.series.at(-1)?.date;
  const span =
    firstDate && lastDate
      ? Math.max(1, (Date.parse(lastDate) - Date.parse(firstDate)) / 86400000)
      : 1;
  const x = (date: string) =>
    singleDay
      ? 350
      : 50 +
        ((Date.parse(date) - Date.parse(firstDate!)) / 86400000 / span) * 600;
  const y = (value: string) => 190 - (Number(value) / maxDay) * 140;
  return (
    <div className={s.observatory}>
      <section className={s.context} aria-label="Contexto del análisis">
        <span className={s.liveDot} aria-hidden="true" />
        <strong>
          {mixed
            ? "Procedencias separadas"
            : d.provenance === "simulado"
              ? "SIMULADO · demostración"
              : d.provenance === "medido"
                ? "DATOS MEDIDOS"
                : "DATOS ESTIMADOS"}
        </strong>
        <span>Lectura del universo filtrado · kg</span>
        <span className={s.contextEnd}>
          Corte {new Date(d.cutoff).toLocaleString("es-CO")}
        </span>
      </section>
      <section className={s.metrics} aria-label="Indicadores ambientales">
        <MetricCard
          label="Generados"
          value={kg(d.generated)}
          unit="kg"
          caption="Masa registrada en la cohorte"
          index="01"
          onExplore={() => onExplore?.()}
        />
        <MetricCard
          label="Compostaje acreditado"
          value={kg(d.verified_compost)}
          unit="kg"
          caption="Entradas con tratamiento y destino verificados"
          index="02"
          onExplore={() => onExplore?.()}
          accent
        />
        <MetricCard
          label="Pendientes de acreditación"
          value={kg(d.pending)}
          unit="kg"
          caption="Disponibles, en proceso o entregados sin acreditar"
          index="03"
          onExplore={() => onExplore?.()}
        />
        <MetricCard
          label="Tasa de compostaje"
          value={d.rate === null ? "—" : kg(d.rate)}
          unit={d.rate === null ? "" : "%"}
          caption={
            d.rate === null
              ? "No calculable"
              : "Entradas acreditadas / generación × 100"
          }
          index="04"
          onExplore={() => onExplore?.()}
        />
      </section>
      {mixed && (
        <section className={s.notice}>
          <strong>No mezclamos procedencias en una tasa.</strong>
          <p>
            Selecciona una procedencia para comparar. Desglose de generación:
          </p>
          <ul>
            {data.provenance_totals.map((o) => (
              <li key={o.provenance}>
                {o.provenance}: {kg(o.generated)} kg
              </li>
            ))}
          </ul>
        </section>
      )}
      <div className={s.analysisGrid}>
        <section className={s.panel} aria-labelledby="trend-title">
          <div className={s.panelHead}>
            <div>
              <span className={s.kicker}>01 / EVOLUCIÓN</span>
              <h2 id="trend-title">La generación, en perspectiva</h2>
            </div>
            <span className={s.tag}>kg / día</span>
          </div>
          <div className={s.comparison}>
            <strong>
              {c.available
                ? `${Number(c.absolute) > 0 ? "+" : ""}${kg(c.absolute)} kg`
                : "Sin comparación"}
            </strong>
            <span>
              {c.available
                ? `${Number(c.percent) > 0 ? "+" : ""}${kg(c.percent)} % frente al período anterior`
                : c.reason}
            </span>
          </div>
          {c.previous_from && (
            <p className={s.meta}>
              Actual: {dateLabel(c.current_from!)} — {dateLabel(c.current_to!)}{" "}
              · Anterior: {dateLabel(c.previous_from)} —{" "}
              {dateLabel(c.previous_to!)}
            </p>
          )}
          {data.series.length ? (
            <>
              <svg
                className={s.trend}
                viewBox="0 0 700 230"
                role="img"
                aria-label="Generación diaria registrada. Consulte la tabla de valores; los huecos son días sin registros."
              >
                {[0, 0.5, 1].map((n) => (
                  <g key={n}>
                    <line
                      x1="50"
                      y1={190 - n * 140}
                      x2="670"
                      y2={190 - n * 140}
                      stroke="#dce6df"
                      strokeDasharray="4 5"
                    />
                    <text x="42" y={194 - n * 140} textAnchor="end">
                      {kg(maxDay * n)}
                    </text>
                  </g>
                ))}
                {data.series.map((point, i) => {
                  const prev = data.series[i - 1];
                  const adjacent =
                    prev &&
                    Date.parse(point.date) - Date.parse(prev.date) === 86400000;
                  return (
                    <g key={point.date}>
                      {adjacent && (
                        <line
                          x1={x(prev.date)}
                          y1={y(prev.kg)}
                          x2={x(point.date)}
                          y2={y(point.kg)}
                          stroke="#167c68"
                          strokeWidth="3"
                        />
                      )}
                      <line
                        x1={x(point.date)}
                        y1="190"
                        x2={x(point.date)}
                        y2={y(point.kg)}
                        stroke="#167c68"
                        opacity=".12"
                        strokeWidth="12"
                      />
                      <circle
                        cx={x(point.date)}
                        cy={y(point.kg)}
                        r="4"
                        fill="#167c68"
                      >
                        <title>
                          {point.date}: {kg(point.kg)} kg · {point.count}{" "}
                          registros
                        </title>
                      </circle>
                    </g>
                  );
                })}
                <text x="50" y="220">
                  {dateLabel(firstDate!)}
                </text>
                {!singleDay && (
                  <text x="650" y="220" textAnchor="end">
                    {dateLabel(lastDate!)}
                  </text>
                )}
              </svg>
              <details className={s.details}>
                <summary>Ver datos de la gráfica</summary>
                <div className={s.tableScroll}>
                  <table>
                    <caption>Solo días con registros</caption>
                    <thead>
                      <tr>
                        <th>Fecha</th>
                        <th>kg</th>
                        <th>Registros</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.series.map((p) => (
                        <tr key={p.date}>
                          <td>{dateLabel(p.date)}</td>
                          <td>{kg(p.kg)}</td>
                          <td>{p.count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </details>
            </>
          ) : (
            <div className={s.empty}>
              <span aria-hidden="true">↗</span>
              <h3>Aún no hay una serie para mostrar</h3>
              <p>
                {Number(d.generated) === 0
                  ? "Sin generación para estos filtros."
                  : ""}
              </p>
              <p>
                Revisa el período y la procedencia. No rellenamos las gráficas
                con datos de ejemplo.
              </p>
            </div>
          )}
          <p className={s.meta}>{data.context.series_reason}</p>
          <section
            className={`${s.panel} ${s.massPanel}`}
            aria-label="Balance de masas"
          >
            <div>
              <span className={s.kicker}>
                UN ORIGEN · DOS ESTADOS DE ACREDITACIÓN
              </span>
              <h2>La masa no se cuenta dos veces.</h2>
              <p className={s.meta}>
                Generación = entrada acreditada a compostaje + pendiente. La
                salida de compost no se suma.
              </p>
            </div>
            {Number(d.generated) > 0 ? (
              <div>
                <div className={s.massTotal}>
                  {kg(d.generated)} <span>kg generados</span>
                </div>
                <div
                  className={s.massTrack}
                  role="img"
                  aria-label={`${d.verified_compost} kg acreditados y ${d.pending} kg pendientes de ${d.generated} kg generados`}
                >
                  <span
                    style={{
                      width: `${(Number(d.verified_compost) / Number(d.generated)) * 100}%`,
                    }}
                  />
                </div>
                <div className={s.massLegend}>
                  <strong>● {kg(d.verified_compost)} kg acreditados</strong>
                  <span>▧ {kg(d.pending)} kg pendientes</span>
                </div>
              </div>
            ) : (
              <p>Sin generación: no se representa una proporción.</p>
            )}
          </section>
        </section>
        <section
          className={`${s.panel} ${s.findings}`}
          aria-labelledby="findings-title"
        >
          <span className={s.kicker}>02 / LECTURA AMBIENTAL</span>
          <h2 id="findings-title">Hallazgos con evidencia</h2>
          <p className={s.meta}>Reglas explícitas. Decisiones humanas.</p>
          {data.insights.length ? (
            data.insights.map((insight, i) => (
              <article className={s.finding} key={insight.code}>
                <span className={s.findingIndex}>0{i + 1}</span>
                <div>
                  <h3>{insight.title}</h3>
                  <p>{insight.detail}</p>
                  <details className={s.insightDetails}>
                    <summary>Interpretación y acción sugerida</summary>
                    <p>{insight.interpretation}</p>
                    <p>
                      <strong>Considera:</strong> {insight.suggestion}
                    </p>
                    <p>
                      Fuente: cohorte de generación con los filtros y corte
                      actuales. Verifica sus lotes y evidencias; no todos los
                      registros están acreditados.
                    </p>
                  </details>
                  <button
                    className={s.textButton}
                    onClick={() => onExplore?.(insight.area)}
                  >
                    Revisar registros <span aria-hidden="true">↗</span>
                  </button>
                </div>
              </article>
            ))
          ) : (
            <p className={s.meta}>
              No hay hallazgos para estas reglas y filtros.
            </p>
          )}
          <div className={s.findingFooter}>
            El análisis describe registros. No certifica cumplimiento ni
            atribuye causas.
          </div>
        </section>
      </div>
      <div className={s.bottomGrid}>
        <section className={s.panel}>
          <div className={s.panelHead}>
            <div>
              <span className={s.kicker}>03 / DÓNDE ACTUAR</span>
              <h2>Áreas que componen el resultado</h2>
            </div>
            <label className={s.rankSelect}>
              Ordenar por
              <select
                value={ranking}
                onChange={(e) => setRanking(e.target.value as typeof ranking)}
              >
                <option value="generated">Generación</option>
                <option value="pending">Pendiente</option>
              </select>
            </label>
          </div>
          {areas.length ? (
            <div className={s.ranking}>
              {areas.slice(0, 5).map((a, i) => (
                <div className={s.areaRow} key={a.id}>
                  <span className={s.areaNumber}>
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <div>
                    <button
                      className={s.areaName}
                      onClick={() => onExplore?.(a.id)}
                    >
                      {a.name} <small>#{a.id}</small>
                    </button>
                    <div className={s.barTrack}>
                      <div
                        style={{
                          width: `${(Number(a[ranking]) / maxArea) * 100}%`,
                        }}
                      />
                    </div>
                  </div>
                  <strong>
                    {kg(a[ranking])}
                    <small> kg</small>
                  </strong>
                </div>
              ))}
            </div>
          ) : (
            <p className={s.empty}>
              No hay áreas con generación para estos filtros.
            </p>
          )}
          <details className={s.details}>
            <summary>Consultar todas las áreas ({areas.length})</summary>
            <div className={s.tableScroll}>
              <table>
                <thead>
                  <tr>
                    <th>Área</th>
                    <th>Generados kg</th>
                    <th>Pendientes kg</th>
                  </tr>
                </thead>
                <tbody>
                  {areas.map((a) => (
                    <tr key={a.id}>
                      <td>
                        {a.name} #{a.id}
                      </td>
                      <td>{kg(a.generated)}</td>
                      <td>{kg(a.pending)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
          <div className={s.materials}>
            <h3>Distribución por material</h3>
            {d.distribution.map((item) => (
              <div key={item.material}>
                <div className={s.materialLabel}>
                  <span>{item.material}</span>
                  <strong>{kg(item.kg)} kg</strong>
                </div>
                <div className={s.barTrack}>
                  <div
                    style={{
                      width: `${Number(d.generated) > 0 ? (Number(item.kg) / Number(d.generated)) * 100 : 0}%`,
                    }}
                  />
                </div>
              </div>
            ))}
            {!d.distribution.length && (
              <p className={s.meta}>No hay materiales con generación.</p>
            )}
            <p className={s.meta}>
              Cada barra representa su proporción de la generación filtrada; no
              expresa aprovechamiento.
            </p>
          </div>
        </section>
        <section className={`${s.panel} ${s.balance}`}>
          <span className={s.kicker}>04 / TRAZABILIDAD DEL INDICADOR</span>
          <h2>Cada cifra tiene un origen.</h2>
          <dl>
            <dt>Disponible</dt>
            <dd>{kg(d.available)} kg</dd>
            <dt>En proceso</dt>
            <dd>{kg(d.in_process)} kg</dd>
            <dt>Entregados a gestores</dt>
            <dd>{kg(d.delivered)} kg</dd>
          </dl>
          <p>
            Las entregas externas no acreditan aprovechamiento. La salida de
            compost no se suma a la entrada.
          </p>
          <a className={s.export} href={"/api/reports/generation.csv?" + query}>
            Exportar CSV filtrado <span aria-hidden="true">↓</span>
          </a>
          <p className={s.meta}>
            {d.provisional ? "Provisional · hay pendientes" : "Corte actual"}
          </p>
        </section>
      </div>
      <details className={s.method}>
        <summary>Metodología, fuentes y límites del análisis</summary>
        <p>
          <strong>Fórmula:</strong> {d.formula}
        </p>
        <p>{d.limitations}</p>
        <p>{data.context.coverage}</p>
        <p>
          Fuente interna: registros de generación, asignaciones y entradas de
          compostaje verificadas de la institución y filtros seleccionados.
          Cálculo determinista; no es una respuesta de IA.
        </p>
      </details>
    </div>
  );
}
