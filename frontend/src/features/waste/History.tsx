import { useState } from "react";
import { api, type Row } from "../../services/api";
import { Table } from "../../components/shared";
import { ActionForm } from "../../components/ActionForm";
import s from "../../app/App.module.css";
export function History({
  rows,
  manager,
  refresh,
}: {
  rows: Row[];
  manager: boolean;
  refresh: () => void;
}) {
  const [detail, setDetail] = useState<Row | null>(null),
    [error, setError] = useState("");
  return (
    <section className={s.card}>
      <h2>Consultar historial de un registro</h2>
      <label>
        Registro
        <select
          aria-label="Registro para historial"
          defaultValue=""
          onChange={async (e) => {
            setError("");
            try {
              setDetail(await api("generations/" + e.target.value));
            } catch (e) {
              setError((e as Error).message);
            }
          }}
        >
          <option value="" disabled>
            Selecciona un registro
          </option>
          {rows.map((r) => (
            <option value={r.id} key={r.id}>
              #{r.id} · {r.material_name} · {r.kg} kg
            </option>
          ))}
        </select>
      </label>
      {error && <p role="alert">{error}</p>}
      {detail && (
        <>
          <p>
            Responsable: {detail.actor} · Método:{" "}
            {detail.method || "No informado"} · {detail.provenance}
          </p>
          <Table
            rows={detail.audit.map((r: Row) => ({
              ...r,
              before: JSON.stringify(r.before),
              after: JSON.stringify(r.after),
            }))}
            columns={[
              { key: "reason", label: "Motivo" },
              { key: "before", label: "Antes" },
              { key: "after", label: "Después" },
              { key: "created_at", label: "Fecha" },
            ]}
          />
          {manager && !detail.reviewed && (
            <ActionForm
              title="Validar clasificación"
              path={"generations/" + detail.id + "/review"}
              fields={[]}
              onDone={() => {
                setDetail(null);
                refresh();
              }}
            />
          )}
        </>
      )}
    </section>
  );
}
