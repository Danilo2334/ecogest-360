import type { Row } from "../../services/api";
import { useState } from "react";
import { PassportPage } from "./PassportPage";
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
export function LotsPage({
  data,
  user,
  operator,
  manager,
  admin,
  refresh,
  dashboard,
  query,
}: FeatureProps) {
  const [selected, setSelected] = useState<string | null>(() =>
    window.location.pathname.startsWith("/lotes/")
      ? window.location.pathname.split("/")[2]
      : null,
  );
  if (selected)
    return (
      <PassportPage
        uuid={selected}
        onBack={() => {
          setSelected(null);
          if (window.location.pathname.startsWith("/lotes/"))
            window.history.replaceState(
              {},
              "",
              "/lotes" + window.location.search,
            );
        }}
      />
    );
  return (
    <>
      {operator && (
        <ActionForm
          title="Crear lote"
          path="lots"
          onDone={refresh}
          transform={(d) => ({
            sources: [{ generation: d.generation, kg: d.kg }],
          })}
          fields={fields(
            {
              name: "generation",
              label: "Registro de origen",
              options: opts(
                data.generations.filter((r: Row) => Number(r.available) > 0),
                (r) =>
                  "#" +
                  r.id +
                  " · " +
                  r.material_name +
                  " · " +
                  r.available +
                  " kg " +
                  r.provenance,
              ),
            },
            { name: "kg", label: "Masa a asignar (kg)", type: "number" },
          )}
        />
      )}
      <div className={s.cards}>
        {data.lots
          .filter(
            (l: Row) =>
              !window.location.pathname.startsWith("/lotes/") ||
              l.public_id === window.location.pathname.split("/")[2],
          )
          .map((lot: Row) => (
            <article className={s.card} key={lot.id}>
              <div className={s.cardHead}>
                <h2>Lote #{lot.id}</h2>
                <Badge value={lot.state} />
              </div>
              <Badge value={lot.provenance} />
              <button onClick={() => setSelected(lot.public_id)}>
                Abrir pasaporte ambiental del lote #{lot.id}
              </button>
              <h3>{lot.available} kg disponibles</h3>
              <details>
                <summary>QR e identificación</summary>
                <img
                  width="150"
                  height="150"
                  src={"/api/lots/" + lot.id + "/image"}
                  alt={"Código QR del lote " + lot.id}
                />
                <p>{lot.public_id}</p>
              </details>
              <Table
                rows={lot.movements}
                columns={[
                  { key: "type", label: "Evento" },
                  { key: "kg", label: "kg" },
                  { key: "destination", label: "Destino" },
                  { key: "actor", label: "Responsable" },
                ]}
              />
              {operator && !lot.closed && lot.state !== "cerrado" && (
                <>
                  <ActionForm
                    title="Registrar movimiento"
                    path={"lots/" + lot.id + "/movements"}
                    defaults={{ unit: "kg" }}
                    onDone={refresh}
                    fields={fields(
                      {
                        name: "type",
                        label: "Tipo",
                        options: [
                          {
                            value: "logistico",
                            label: "Traslado logístico (no consume)",
                          },
                          {
                            value: "entrega",
                            label: "Entrega externa (consume saldo)",
                          },
                        ],
                      },
                      { name: "kg", label: "Cantidad (kg)", type: "number" },
                      { name: "destination", label: "Destino" },
                    )}
                  />
                  {Number(lot.available) === 0 && (
                    <ActionForm
                      title="Cerrar lote"
                      path={"lots/" + lot.id + "/close"}
                      fields={[]}
                      onDone={refresh}
                    />
                  )}
                </>
              )}
            </article>
          ))}
      </div>
      {!data.lots.length && (
        <p className={s.empty}>Crea un lote desde la generación disponible.</p>
      )}
    </>
  );
}
