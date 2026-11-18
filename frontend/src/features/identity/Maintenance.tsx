import type { Row } from "../../services/api";
import { ActionForm } from "../../components/ActionForm";
import { fields, opts } from "../../components/shared";
import s from "../../app/App.module.css";
const roles = ["administrador", "gestor", "operador", "consultor"].map(
  (value) => ({ value, label: value }),
);
export function Maintenance({
  data,
  refresh,
}: {
  data: Row;
  refresh: () => void;
}) {
  return (
    <section>
      <h2>Actualizar configuración</h2>
      <div className={s.cards}>
        <ActionForm
          title="Actualizar nombre institucional"
          path="institution"
          method="PATCH"
          fields={fields({ name: "name", label: "Nombre de la universidad" })}
          onDone={refresh}
        />
        <ActionForm
          title="Actualizar rol"
          path={(d) => "users/" + d.user}
          method="PATCH"
          transform={(d) => ({ role: d.role })}
          fields={fields(
            {
              name: "user",
              label: "Usuario a actualizar",
              options: opts(data.users, (r) => r.username),
            },
            { name: "role", label: "Nuevo rol", options: roles },
          )}
          onDone={refresh}
        />
      </div>
      <details>
        <summary>Editar sedes y áreas</summary>
        <div className={s.cards}>
          {data.sites.map((r: Row) => (
            <ActionForm
              key={"site" + r.id}
              title={"Actualizar sede #" + r.id}
              path={"sites/" + r.id}
              method="PATCH"
              fields={fields({
                name: "name",
                label: "Nombre de sede",
                value: r.name,
              })}
              onDone={refresh}
            />
          ))}
          {data.areas.map((r: Row) => (
            <ActionForm
              key={"area" + r.id}
              title={"Actualizar área #" + r.id}
              path={"areas/" + r.id}
              method="PATCH"
              fields={fields(
                { name: "name", label: "Nombre de área", value: r.name },
                {
                  name: "site",
                  label: "Sede",
                  options: opts(data.sites),
                  value: String(r.site_id),
                },
              )}
              onDone={refresh}
            />
          ))}
        </div>
      </details>
      <details>
        <summary>Editar catálogo ambiental</summary>
        <div className={s.cards}>
          {data.materials.map((r: Row) => (
            <ActionForm
              key={r.id}
              title={"Actualizar material #" + r.id}
              path={"materials/" + r.id}
              method="PATCH"
              transform={(d) => ({ ...d, active: d.active === "true" })}
              fields={fields(
                { name: "name", label: "Nombre del material", value: r.name },
                {
                  name: "category",
                  label: "Categoría",
                  options: ["blanco", "verde", "negro", "especial"].map(
                    (value) => ({ value, label: value }),
                  ),
                  value: r.category,
                },
                {
                  name: "active",
                  label: "Disponibilidad",
                  options: [
                    { value: "true", label: "Activo" },
                    { value: "false", label: "Inactivo" },
                  ],
                  value: String(r.active),
                },
              )}
              onDone={refresh}
            />
          ))}
        </div>
      </details>
    </section>
  );
}
