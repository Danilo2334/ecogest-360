import type { Row } from "../services/api";
import type { Field } from "./ActionForm";
import s from "../app/App.module.css";
export const origins = [
  { value: "simulado", label: "Simulado · demostración" },
  { value: "medido", label: "Medido" },
  { value: "estimado", label: "Estimado" },
];
export const today = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
};
export const fields = (...items: Field[]) => items;
export const opts = (rows: Row[], label = (r: Row) => r.name) =>
  rows.map((r) => ({ value: String(r.id), label: label(r) }));
export const kg = (value: unknown) =>
  new Intl.NumberFormat("es-CO", { maximumFractionDigits: 3 }).format(
    Number(value || 0),
  );
export function Badge({ value }: { value: string }) {
  return <span className={s.badge}>{value}</span>;
}
export function Table({
  rows,
  columns,
}: {
  rows: Row[];
  columns: { key: string; label: string }[];
}) {
  return (
    <div className={s.tableWrap}>
      <table>
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c.key}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={row.id || i}>
              {columns.map((c) => (
                <td key={c.key}>{String(row[c.key] ?? "—")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {!rows.length && (
        <p className={s.empty}>Todavía no hay registros para esta consulta.</p>
      )}
    </div>
  );
}

export type FeatureProps = {
  data: Row;
  user: Row;
  operator: boolean;
  manager: boolean;
  admin: boolean;
  refresh: () => void;
  dashboard: Row | null;
  query: string;
};
