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
export function IncidentsPage({
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
      {user.role !== "consultor" && (
        <ActionForm
          title="Registrar incidencia"
          path="incidents"
          onDone={refresh}
          fields={fields(
            {
              name: "entity",
              label: "Referencia (lot:1, generation:1 o process:1)",
            },
            { name: "reason", label: "Motivo" },
          )}
        />
      )}
      <p>Las incidencias quedan pendientes; no modifican masas ni historial.</p>
      <Table
        rows={data.incidents}
        columns={[
          { key: "entity", label: "Referencia" },
          { key: "reason", label: "Motivo" },
          { key: "state", label: "Estado" },
        ]}
      />
    </>
  );
}
