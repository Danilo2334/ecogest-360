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
export function CompostPage({
  data,
  user,
  operator,
  manager,
  admin,
  refresh,
  dashboard,
  query,
}: FeatureProps) {
  return (
    <>
      {operator && (
        <ActionForm
          title="Iniciar compostaje"
          path="compost/processes"
          onDone={refresh}
          fields={fields(
            { name: "provenance", label: "Procedencia", options: origins },
            { name: "observations", label: "Observaciones", required: false },
          )}
        />
      )}
      <div className={s.cards}>
        {data.processes.map((p: Row) => (
          <article className={s.card} key={p.id}>
            <div className={s.cardHead}>
              <h2>Proceso #{p.id}</h2>
              <Badge value={p.verified ? "confirmado" : p.state} />
            </div>
            <Badge value={p.provenance} />
            <p>
              Salida independiente:{" "}
              <b>{p.output ? p.output + " kg" : "Pendiente"}</b>
            </p>
            <Table
              rows={p.inputs}
              columns={[
                { key: "lot", label: "Lote" },
                { key: "kg", label: "Entrada kg" },
              ]}
            />
            {operator && p.state === "en_proceso" && (
              <>
                <ActionForm
                  title="Ingresar orgánicos"
                  path={"compost/processes/" + p.id + "/inputs"}
                  defaults={{ unit: "kg" }}
                  onDone={refresh}
                  fields={fields(
                    {
                      name: "lot",
                      label: "Lote",
                      options: opts(
                        data.lots.filter(
                          (l: Row) =>
                            Number(l.available) > 0 &&
                            l.provenance === p.provenance,
                        ),
                        (r) => "Lote #" + r.id + " · " + r.available + " kg",
                      ),
                    },
                    { name: "kg", label: "Entrada (kg)", type: "number" },
                  )}
                />
                <ActionForm
                  title="Registrar control"
                  path={"compost/processes/" + p.id + "/measurements"}
                  defaults={{ date: new Date().toISOString() }}
                  onDone={refresh}
                  fields={fields(
                    { name: "type", label: "Tipo de control" },
                    { name: "value", label: "Valor", type: "number" },
                    { name: "unit", label: "Unidad" },
                  )}
                />
                <ActionForm
                  title="Finalizar proceso"
                  path={"compost/processes/" + p.id + "/finalize"}
                  defaults={{ unit: "kg", provenance: p.provenance }}
                  onDone={refresh}
                  fields={fields(
                    {
                      name: "kg",
                      label: "Salida independiente (kg)",
                      type: "number",
                    },
                    { name: "destination", label: "Destino declarado" },
                  )}
                />
              </>
            )}
            {(operator || manager) && !p.verified && (
              <ActionForm
                title="Agregar evidencia verificable"
                path={"compost/processes/" + p.id + "/evidence"}
                onDone={refresh}
                fields={fields(
                  { name: "receiver", label: "Receptor" },
                  {
                    name: "reference",
                    label: "Referencia verificable del comprobante",
                    required: false,
                  },
                  {
                    name: "file",
                    label: "Documento privado (PDF, PNG, JPEG)",
                    type: "file",
                    required: false,
                  },
                  {
                    name: "date",
                    label: "Fecha de destino",
                    type: "date",
                    value: today(),
                  },
                  { name: "description", label: "Descripción / verificación" },
                )}
              />
            )}
            <Table
              rows={p.evidence}
              columns={[
                { key: "reference", label: "Comprobante" },
                { key: "receiver", label: "Receptor" },
                { key: "date", label: "Fecha" },
              ]}
            />
            {manager && !p.verified && (
              <ActionForm
                title="Validar resultado"
                path={"compost/processes/" + p.id + "/verify"}
                onDone={refresh}
                fields={fields(
                  {
                    name: "decision",
                    label: "Decisión",
                    options: [
                      {
                        value: "confirmado",
                        label: "Confirmar evidencia completa",
                      },
                      {
                        value: "rechazado",
                        label: "Rechazar: queda pendiente",
                      },
                    ],
                  },
                  { name: "reason", label: "Qué verificaste / motivo" },
                )}
              />
            )}
            <Table
              rows={p.measurements}
              columns={[
                { key: "type", label: "Control" },
                { key: "value", label: "Valor" },
                { key: "unit", label: "Unidad" },
                { key: "date", label: "Fecha" },
              ]}
            />
            {p.evidence
              .filter((e: Row) => e.file)
              .map((e: Row) => (
                <p key={e.id}>
                  <a href={"/api/evidence/" + e.id + "/download"}>
                    Descargar documento privado #{e.id}
                  </a>
                </p>
              ))}
            <Table
              rows={p.verifications}
              columns={[
                { key: "decision", label: "Decisión" },
                { key: "reason", label: "Motivo" },
                { key: "actor", label: "Gestor" },
              ]}
            />
          </article>
        ))}
      </div>
      {!data.processes.length && (
        <p className={s.empty}>
          Sin procesos registrados. No se generan datos automáticamente.
        </p>
      )}
    </>
  );
}
