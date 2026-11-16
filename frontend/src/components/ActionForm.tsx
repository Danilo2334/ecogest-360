import { useRef, useState } from "react";
import { api, type Row } from "../services/api";
import styles from "../app/App.module.css";
export type Field = {
  name: string;
  label: string;
  type?: string;
  options?: { value: string; label: string }[];
  required?: boolean;
  value?: string;
};
export function ActionForm({
  title,
  path,
  fields,
  defaults = {},
  method = "POST",
  transform,
  onDone,
}: {
  title: string;
  path: string | ((data: Row) => string);
  fields: Field[];
  defaults?: Row;
  method?: string;
  transform?: (data: Row) => Row;
  onDone: () => void;
}) {
  const [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const operation = useRef<{ payload: string; key: string } | null>(null);
  return (
    <form
      className={styles.form}
      onSubmit={async (event) => {
        event.preventDefault();
        setError("");
        setBusy(true);
        const form = event.currentTarget;
        const data = { ...defaults, ...Object.fromEntries(new FormData(form)) };
        const payload = transform ? transform(data) : data;
        const target = typeof path === "function" ? path(data) : path;
        const signature = target + JSON.stringify(payload);
        if (operation.current?.payload !== signature)
          operation.current = { payload: signature, key: crypto.randomUUID() };
        let body: Row | FormData = payload;
        if (fields.some((f) => f.type === "file")) {
          const multipart = new FormData();
          Object.entries(payload).forEach(([k, v]) => {
            if (v instanceof File) {
              if (v.size) multipart.append(k, v);
            } else multipart.append(k, String(v));
          });
          body = multipart;
        }
        try {
          await api(target, body, method, operation.current.key);
          operation.current = null;
          form.reset();
          onDone();
        } catch (e) {
          setError(e instanceof Error ? e.message : "Error de conexión.");
        } finally {
          setBusy(false);
        }
      }}
    >
      <h3>{title}</h3>
      <div className={styles.fields}>
        {fields.map((field) => (
          <label key={field.name}>
            {field.label}
            {field.options ? (
              <select
                aria-label={field.label}
                name={field.name}
                required={field.required !== false}
                defaultValue={field.value || ""}
              >
                <option value="" disabled>
                  Selecciona…
                </option>
                {field.options.map((o) => (
                  <option key={o.value} value={o.value}>
                    {o.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                aria-label={field.label}
                name={field.name}
                type={field.type || "text"}
                required={field.required !== false}
                defaultValue={field.value}
                step={field.type === "number" ? "0.001" : undefined}
              />
            )}
          </label>
        ))}
      </div>
      {error && (
        <p role="alert" className={styles.error}>
          {error}
        </p>
      )}
      <button disabled={busy}>{busy ? "Guardando…" : title}</button>
    </form>
  );
}
