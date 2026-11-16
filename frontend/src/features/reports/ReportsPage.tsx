import type { Row } from "../../services/api";
import { ActionForm } from "../../components/ActionForm";
import {
  origins,
  today,
  fields,
  opts,
  kg,
  Badge,
  Table,
  type FeatureProps,
} from "../../components/shared";
import s from "../../app/App.module.css";
export function ReportsPage({
  data,
  user,
  operator,
  manager,
  admin,
  refresh,
  dashboard,
  query,
}: FeatureProps) {
  if (!dashboard) return null;
  return (
    <>
      <div className={s.banner}>
        <span>ⓘ</span>
        <p>
          <b>Procedencia: {dashboard.provenance}</b>
          <br />
          El compostaje acreditado no representa todo el aprovechamiento de la
          institución.
        </p>
      </div>
      <section className={s.metrics}>
        {[
          ["generated", "Generados", "Masa registrada en el período"],
          [
            "delivered",
            "Entregados a gestores",
            "No acreditados como aprovechamiento",
          ],
          [
            "verified_compost",
            "Compostaje acreditado",
            "Entradas con tratamiento y destino verificados",
          ],
          [
            "pending",
            "Pendientes de acreditación",
            "Incluye disponible, en proceso y entregas",
          ],
        ].map(([key, title, caption]) => (
          <article key={key}>
            <span>{title}</span>
            <h2>
              {kg(dashboard[key])}
              <small> kg</small>
            </h2>
            <p>{caption}</p>
          </article>
        ))}
      </section>
      <section className={s.twoCol}>
        <article className={s.card}>
          <h2>Generación por material</h2>
          <p>Distribución del universo filtrado · kg</p>
          {dashboard.distribution.length ? (
            dashboard.distribution.map((r: Row) => (
              <div className={s.barRow} key={r.material}>
                <span>{r.material}</span>
                <strong>{kg(r.kg)} kg</strong>
                <svg
                  role="img"
                  aria-label={r.material + ": " + r.kg + " kg"}
                  viewBox="0 0 100 5"
                  preserveAspectRatio="none"
                >
                  <rect width="100" height="5" fill="#edf2eb" />
                  <rect
                    width={
                      Number(dashboard.generated)
                        ? (Number(r.kg) / Number(dashboard.generated)) * 100
                        : 0
                    }
                    height="5"
                    fill="#32785d"
                  />
                </svg>
              </div>
            ))
          ) : (
            <p className={s.empty}>Sin generación para estos filtros.</p>
          )}
          <Table
            rows={dashboard.distribution}
            columns={[
              { key: "material", label: "Material" },
              { key: "kg", label: "kg" },
            ]}
          />
        </article>
        <article className={s.card}>
          <span className={s.eyebrow}>APROVECHAMIENTO POR COMPOSTAJE</span>
          <h2 className={s.rate}>
            {dashboard.rate === null ? "No calculable" : dashboard.rate + " %"}
          </h2>
          <Badge
            value={
              dashboard.provisional
                ? "Provisional · hay pendientes"
                : "Corte actual"
            }
          />
          <p>{dashboard.formula}</p>
          <dl>
            <dt>Numerador</dt>
            <dd>{dashboard.verified_compost} kg</dd>
            <dt>Denominador</dt>
            <dd>{dashboard.generated} kg</dd>
            <dt>Disponible</dt>
            <dd>{dashboard.available} kg</dd>
            <dt>En proceso</dt>
            <dd>{dashboard.in_process} kg</dd>
          </dl>
          <a
            className={s.buttonLink}
            href={"/api/reports/generation.csv?" + query}
          >
            ↓ Exportar CSV filtrado
          </a>
        </article>
      </section>
      <p className={s.hint}>
        Corte: {dashboard.cutoff}. {dashboard.limitations}
      </p>
    </>
  );
}
