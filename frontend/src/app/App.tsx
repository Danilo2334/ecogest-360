import { Badge, origins, type FeatureProps } from "../components/shared";
import { IdentityPage } from "../features/identity/IdentityPage";
import { IncidentsPage } from "../features/incidents/IncidentsPage";
import { CompostPage } from "../features/compost/CompostPage";
import { LotsPage } from "../features/lots/LotsPage";
import { WastePage } from "../features/waste/WastePage";
import { ReportsPage } from "../features/reports/ReportsPage";
import { useEffect, useState } from "react";
import { api, type Row } from "../services/api";
import s from "./App.module.css";

export default function App() {
  const [user, setUser] = useState<Row | null>(null),
    [page, setPage] = useState(
      window.location.pathname.startsWith("/lotes/") ? "Lotes" : "Resumen",
    ),
    [loading, setLoading] = useState(true);
  const [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [revision, setRevision] = useState(0);
  const [data, setData] = useState<Row>({
    areas: [],
    sites: [],
    materials: [],
    generations: [],
    lots: [],
    processes: [],
    users: [],
    incidents: [],
  });
  const [dashboard, setDashboard] = useState<Row | null>(null),
    [filters, setFilters] = useState<Row>({});
  const refresh = () => {
    setNotice("Operación guardada. Los datos se actualizaron.");
    setRevision((x) => x + 1);
  };
  const query = new URLSearchParams(
    Object.entries(filters)
      .filter(([, v]) => v)
      .map(([k, v]) => [k, String(v)]),
  ).toString();
  useEffect(() => {
    api("session/me")
      .then(setUser)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);
  useEffect(() => {
    if (!user) return;
    let active = true;
    setLoading(true);
    setError("");
    Promise.all([
      api("areas"),
      api("sites"),
      api("materials"),
      ["Registros", "Lotes"].includes(page)
        ? api("generations?" + (page === "Registros" ? query : ""))
        : Promise.resolve([]),
      ["Lotes", "Compostaje"].includes(page)
        ? api("lots")
        : Promise.resolve([]),
      page === "Compostaje" ? api("compost/processes") : Promise.resolve([]),
      page === "Resumen" ? api("dashboard?" + query) : Promise.resolve(null),
      page === "Incidencias" ? api("incidents") : Promise.resolve([]),
      user.role === "administrador" && page === "Institución"
        ? api("users")
        : Promise.resolve([]),
    ])
      .then(
        ([
          areas,
          sites,
          materials,
          generations,
          lots,
          processes,
          dash,
          incidents,
          users,
        ]) => {
          if (active) {
            setData({
              areas,
              sites,
              materials,
              generations,
              lots,
              processes,
              incidents,
              users,
            });
            setDashboard(dash);
          }
        },
      )
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [user, revision, query, page]);
  async function signIn(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    const form = new FormData(e.currentTarget);
    try {
      await api("session/login", Object.fromEntries(form));
      setUser(await api("session/me"));
    } catch (e) {
      setError((e as Error).message);
    }
  }
  const operator = user?.role === "operador",
    manager = user?.role === "gestor",
    admin = user?.role === "administrador";
  const nav = [
    "Resumen",
    "Registros",
    "Lotes",
    "Compostaje",
    "Incidencias",
    ...(admin ? ["Institución"] : []),
  ];
  if (!user)
    return (
      <main className={s.login}>
        <section className={s.story}>
          <div className={s.logo}>
            ◉ EcoGest <b>360</b>
          </div>
          <span className={s.eyebrow}>GESTIÓN AMBIENTAL UNIVERSITARIA</span>
          <h1>
            Cada residuo
            <br />
            tiene una historia.
          </h1>
          <p>
            Registra su origen. Sigue su recorrido.
            <br />
            Demuestra su aprovechamiento.
          </p>
          <div className={s.orbit}>
            ↻
            <small>
              Un campus.
              <br />
              Un ciclo más responsable.
            </small>
          </div>
          <footer>Trazabilidad · Evidencia · Economía circular</footer>
        </section>
        <section className={s.loginPanel}>
          <span className={s.eyebrow}>BIENVENIDO A TU CAMPUS</span>
          <h2>Ingresa a EcoGest 360</h2>
          <p>Usa tu cuenta institucional autorizada.</p>
          <form onSubmit={signIn}>
            <label>
              Usuario
              <input name="username" autoComplete="username" required />
            </label>
            <label>
              Contraseña
              <input
                name="password"
                type="password"
                autoComplete="current-password"
                required
              />
            </label>
            {error && (
              <p role="alert" className={s.error}>
                {error}
              </p>
            )}
            <button disabled={loading}>Ingresar al sistema →</button>
          </form>
          <p className={s.hint}>
            Piloto académico. Los datos de demostración se identifican como
            simulados.
          </p>
        </section>
      </main>
    );
  const featureProps: FeatureProps = {
    data,
    user,
    operator,
    manager,
    admin,
    refresh,
    dashboard,
    query,
  };
  return (
    <div className={s.shell}>
      <aside className={s.sidebar}>
        <div className={s.logo}>
          ◉ EcoGest <b>360</b>
        </div>
        <p className={s.eyebrow}>TU CAMPUS, EN EQUILIBRIO</p>
        <nav aria-label="Principal">
          {nav.map((name, i) => (
            <button
              key={name}
              aria-current={page === name ? "page" : undefined}
              className={page === name ? s.active : ""}
              onClick={() => {
                setPage(name);
                setNotice("");
              }}
            >
              <span aria-hidden="true">
                {["◫", "≡", "◇", "♧", "!", "⚙"][i]}
              </span>
              {name}
            </button>
          ))}
        </nav>
        <div className={s.sideFoot}>
          <Badge value={user.role} />
          <p>{user.username}</p>
          <button
            onClick={async () => {
              await api("session/logout", {});
              setUser(null);
            }}
          >
            Cerrar sesión
          </button>
        </div>
      </aside>
      <div className={s.content}>
        <header className={s.topbar}>
          <span>{user.institution}</span>
          <Badge value="Piloto universitario" />
        </header>
        <main>
          <div className={s.heading}>
            <div>
              <span className={s.eyebrow}>
                ECOGEST 360 / {page.toUpperCase()}
              </span>
              <h1>{page === "Resumen" ? "El ciclo de tus residuos" : page}</h1>
              <p>
                {page === "Resumen"
                  ? "Información trazable para decisiones ambientales responsables."
                  : "Cada operación conserva su origen, responsable y evidencia."}
              </p>
            </div>
            <span className={s.date}>
              {new Date().toLocaleDateString("es-CO", { dateStyle: "long" })}
            </span>
          </div>
          {error && (
            <p role="alert" className={s.error}>
              {error}
            </p>
          )}
          {notice && (
            <p role="status" className={s.success}>
              {notice}
            </p>
          )}
          {loading && <p role="status">Actualizando datos…</p>}
          {(page === "Resumen" || page === "Registros") && (
            <section className={s.filters} aria-label="Filtros">
              <label>
                Procedencia
                <select
                  value={filters.provenance || ""}
                  onChange={(e) =>
                    setFilters({ ...filters, provenance: e.target.value })
                  }
                >
                  <option value="">Todas las procedencias</option>
                  {origins.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Desde
                <input
                  type="date"
                  value={filters.generated_from || ""}
                  onChange={(e) =>
                    setFilters({ ...filters, generated_from: e.target.value })
                  }
                />
              </label>
              <label>
                Hasta
                <input
                  type="date"
                  value={filters.generated_to || ""}
                  onChange={(e) =>
                    setFilters({ ...filters, generated_to: e.target.value })
                  }
                />
              </label>
              <label>
                Área
                <select
                  value={filters.area || ""}
                  onChange={(e) =>
                    setFilters({ ...filters, area: e.target.value })
                  }
                >
                  <option value="">Todas</option>
                  {data.areas.map((r: Row) => (
                    <option key={r.id} value={r.id}>
                      {r.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Material
                <select
                  value={filters.material || ""}
                  onChange={(e) =>
                    setFilters({ ...filters, material: e.target.value })
                  }
                >
                  <option value="">Todos</option>
                  {data.materials.map((r: Row) => (
                    <option key={r.id} value={r.id}>
                      {r.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Corte de validación
                <input
                  type="datetime-local"
                  onChange={(e) =>
                    setFilters({
                      ...filters,
                      cutoff: e.target.value
                        ? new Date(e.target.value).toISOString()
                        : "",
                    })
                  }
                />
              </label>
            </section>
          )}
          {page === "Resumen" && <ReportsPage {...featureProps} />}
          {page === "Registros" && <WastePage {...featureProps} />}
          {page === "Lotes" && <LotsPage {...featureProps} />}
          {page === "Compostaje" && <CompostPage {...featureProps} />}
          {page === "Incidencias" && <IncidentsPage {...featureProps} />}
          {page === "Institución" && <IdentityPage {...featureProps} />}
        </main>
        <footer className={s.footer}>
          EcoGest 360 · Registro y trazabilidad ambiental{" "}
          <span>Datos con origen. Decisiones con evidencia.</span>
        </footer>
      </div>
    </div>
  );
}
