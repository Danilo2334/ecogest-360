import { History } from "./History";
import { useState } from "react";
import { PassportPage } from "../lots/PassportPage";
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
export function WastePage({
  data,
  user,
  operator,
  manager,
  admin,
  refresh,
  dashboard,
  query,
}: FeatureProps) {
  const [passport, setPassport] = useState<string | null>(null);
  if (passport)
    return <PassportPage uuid={passport} onBack={() => setPassport(null)} />;
  return (
    <>
      {operator && (
        <ActionForm
          title="Registrar generación"
          path="generations"
          onDone={refresh}
          defaults={{ unit: "kg" }}
          transform={(d) => ({
            ...d,
            date: new Date(d.date + "T12:00:00").toISOString(),
          })}
          fields={fields(
            { name: "date", label: "Fecha", type: "date", value: today() },
            { name: "area", label: "Área", options: opts(data.areas) },
            {
              name: "material",
              label: "Material ordinario",
              options: opts(
                data.materials.filter(
                  (r: Row) => r.active && r.category !== "especial",
                ),
              ),
            },
            { name: "kg", label: "Peso (kg)", type: "number" },
            { name: "provenance", label: "Procedencia", options: origins },
            { name: "method", label: "Método / observación", required: false },
          )}
        />
      )}
      <Table
        rows={data.generations}
        columns={[
          { key: "id", label: "ID" },
          { key: "area_name", label: "Área" },
          { key: "material_name", label: "Material" },
          { key: "kg", label: "kg generados" },
          { key: "available", label: "kg sin asignar" },
          { key: "provenance", label: "Procedencia" },
          { key: "actor", label: "Responsable" },
        ]}
      />
      {manager && (
        <ActionForm
          title="Corregir generación sin asignar"
          path={(d) => "generations/" + d.generation + "/correct"}
          transform={(d) => ({ kg: d.kg, unit: "kg", reason: d.reason })}
          onDone={refresh}
          defaults={{ unit: "kg" }}
          fields={fields(
            {
              name: "generation",
              label: "Generación a corregir",
              options: opts(
                data.generations.filter((r: Row) => r.available === r.kg),
                (r) => "Registro #" + r.id + " · " + r.kg + " kg",
              ),
            },
            { name: "kg", label: "Nuevo peso (kg)", type: "number" },
            { name: "reason", label: "Motivo auditado" },
          )}
        />
      )}
      <History rows={data.generations} manager={manager} refresh={refresh} />
      <details>
        <summary>Pasaportes de los registros filtrados</summary>
        <p>
          Los filtros de esta consulta se conservan. Cada pasaporte muestra la
          historia completa del lote.
        </p>
        {(data.lots || [])
          .filter((l: Row) =>
            l.sources.some((source: Row) =>
              data.generations.some((g: Row) => g.id === source.generation),
            ),
          )
          .map((l: Row) => (
            <p key={l.id}>
              <button onClick={() => setPassport(l.public_id)}>
                Consultar pasaporte del lote #{l.id}
              </button>
            </p>
          ))}
      </details>
    </>
  );
}
