import { Maintenance } from "./Maintenance";
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
export function IdentityPage({
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
      <div className={s.cards}>
        <ActionForm
          title="Crear sede"
          path="sites"
          fields={fields({ name: "name", label: "Nombre de sede" })}
          onDone={refresh}
        />
        <ActionForm
          title="Crear área"
          path="areas"
          fields={fields(
            { name: "name", label: "Nombre de área" },
            { name: "site", label: "Sede", options: opts(data.sites) },
          )}
          onDone={refresh}
        />
        <ActionForm
          title="Crear material"
          path="materials"
          fields={fields(
            { name: "name", label: "Nombre del material" },
            {
              name: "category",
              label: "Categoría",
              options: ["blanco", "verde", "negro", "especial"].map((x) => ({
                value: x,
                label: x,
              })),
            },
          )}
          onDone={refresh}
        />
        <ActionForm
          title="Crear usuario"
          path="users"
          fields={fields(
            { name: "username", label: "Usuario" },
            { name: "password", label: "Contraseña inicial", type: "password" },
            {
              name: "role",
              label: "Rol",
              options: ["administrador", "gestor", "operador", "consultor"].map(
                (x) => ({ value: x, label: x }),
              ),
            },
          )}
          onDone={refresh}
        />
      </div>
      <Table
        rows={data.users}
        columns={[
          { key: "username", label: "Usuario" },
          { key: "role", label: "Rol" },
        ]}
      />
      <Maintenance data={data} refresh={refresh} />
    </>
  );
}
