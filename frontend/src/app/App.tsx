import { Badge, origins, type FeatureProps } from "../components/shared";
import { IdentityPage } from "../features/identity/IdentityPage";
import { IncidentsPage } from "../features/incidents/IncidentsPage";
import { CompostPage } from "../features/compost/CompostPage";
import { LotsPage } from "../features/lots/LotsPage";
import { WastePage } from "../features/waste/WastePage";
import { ReportsPage } from "../features/reports/ReportsPage";
import { ScenarioPage } from "../features/scenarios/ScenarioPage";
import type { Scenario } from "../features/scenarios/ScenarioPage";
import { PlansPage } from "../features/plans/PlansPage";
import { useEffect, useState } from "react";
import { api, type Row } from "../services/api";
import s from "./App.module.css";

function initialFilters(): Row {
  const end = new Date();
  end.setDate(end.getDate() - 1);
  const start = new Date(end);
  start.setDate(start.getDate() - 29);
  const local = (d: Date) =>
    `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  return {
    provenance: "medido",
    generated_from: local(start),
    generated_to: local(end),
  };
}
const navLabel = (name: string) =>
  name === "Resumen"
    ? "Observatorio"
    : name === "Lotes"
      ? "Trazabilidad"
      : name;
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
    [filters, setFilters] = useState<Row>(initialFilters);
  const [menuOpen, setMenuOpen] = useState(false);
  const [proposal, setProposal] = useState<Scenario | null>(null);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const refresh = () => {
    setNotice("Operación guardada. Los datos se actualizaron.");
    setRevision((x) => x + 1);
  };
  const query = new URLSearchParams(
    Object.entries(filters)
      .filter(([k, v]) => v && k !== "cutoffLocal")
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
    setDashboard(null);
    setError("");
    Promise.all([
      api("areas"),
      api("sites"),
      api("materials"),
      ["Registros", "Lotes"].includes(page)
        ? api("generations?" + (page === "Registros" ? query : ""))
        : Promise.resolve([]),
      ["Lotes", "Compostaje", "Registros"].includes(page)
        ? api("lots")
        : Promise.resolve([]),
      page === "Compostaje" ? api("compost/processes") : Promise.resolve([]),
      page === "Resumen" ? api("observatory?" + query) : Promise.resolve(null),
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
      setFilters(initialFilters());
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
    "Simulador",
    "Planes de acción",
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
      <a className={s.skipLink} href="#main-content">
        Ir al contenido
      </a>
      <aside className={s.sidebar}>
        <div className={s.logo}>
          ◉ EcoGest <b>360</b>
        </div>
        <p className={s.eyebrow}>INTELLIGENCE / CAMPUS</p>
        <button
          className={s.mobileToggle}
          aria-expanded={menuOpen}
          aria-controls="main-navigation"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          Menú {menuOpen ? "−" : "+"}
        </button>
        <nav
          id="main-navigation"
          aria-label="Principal"
          className={menuOpen ? s.navOpen : undefined}
        >
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
              {navLabel(name)}
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
              setProposal(null);
              setDashboard(null);
              setData({
                areas: [],
                sites: [],
                materials: [],
                generations: [],
                lots: [],
                processes: [],
                users: [],
                incidents: [],
              });
              setFilters(initialFilters());
              setPage("Resumen");
              setMenuOpen(false);
            }}
          >
            Cerrar sesión
          </button>
        </div>
      </aside>
      <div className={s.content}>
        <header className={s.topbar}>
          <span>{user.institution}</span>
          <span className={s.environment}>
            ● Entorno local · Piloto universitario
          </span>
        </header>
        <main id="main-content">
          <div className={s.heading}>
            <div>
              <span className={s.eyebrow}>
                CONSOLA AMBIENTAL / {navLabel(page).toUpperCase()}
              </span>
              <h1>
                {page === "Resumen" ? "Observatorio ambiental" : navLabel(page)}
              </h1>
              <p>
                {page === "Resumen"
                  ? "Entiende el presente. Decide el siguiente paso."
                  : "Cada operación conserva su origen, responsable y evidencia."}
              </p>
            </div>
            <span className={s.date}>
              {new Date().toLocaleDateString("es-CO", { dateStyle: "long" })}
            </span>
          </div>
          {error && (
            <div role="alert" className={s.error}>
              <p>{error}</p>
              <button onClick={() => setRevision((x) => x + 1)}>
                Reintentar consulta
              </button>
            </div>
          )}
          {notice && (
            <p role="status" className={s.success}>
              {notice}
            </p>
          )}
          {loading && (
            <div className={s.loading} role="status">
              Actualizando datos…
              <div className={s.loadingBar} />
            </div>
          )}
          {["Resumen", "Registros", "Simulador", "Planes de acción"].includes(
            page,
          ) && (
            <section
              className={`${s.filters} ${filtersOpen ? "" : s.filtersCollapsed}`}
              aria-label="Filtros"
            >
              <p className={s.filterPeriod}>
                Período:{" "}
                {filters.generated_from
                  ? new Date(
                      filters.generated_from + "T12:00:00",
                    ).toLocaleDateString("es-CO", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })
                  : "sin inicio"}{" "}
                —{" "}
                {filters.generated_to
                  ? new Date(
                      filters.generated_to + "T12:00:00",
                    ).toLocaleDateString("es-CO", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })
                  : "sin fin"}
              </p>
              <button
                className={s.filterToggle}
                aria-expanded={filtersOpen}
                aria-controls="filter-controls"
                onClick={() => setFiltersOpen(!filtersOpen)}
              >
                {filtersOpen ? "Ocultar filtros" : "Ajustar filtros"}
              </button>
              <div id="filter-controls" className={s.filterControls}>
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
                    value={filters.cutoffLocal || ""}
                    type="datetime-local"
                    onChange={(e) =>
                      setFilters({
                        ...filters,
                        cutoffLocal: e.target.value,
                        cutoff: e.target.value
                          ? new Date(e.target.value).toISOString()
                          : "",
                      })
                    }
                  />
                </label>
              </div>
            </section>
          )}
          {page === "Resumen" && !loading && (
            <ReportsPage
              {...featureProps}
              onExplore={(area) => {
                if (area) setFilters({ ...filters, area: String(area) });
                setPage("Registros");
              }}
            />
          )}
          {page === "Registros" && <WastePage {...featureProps} />}
          {page === "Simulador" && (
            <ScenarioPage
              query={query}
              onPlan={
                manager
                  ? (scenario) => {
                      setProposal(scenario);
                      setPage("Planes de acción");
                    }
                  : undefined
              }
            />
          )}
          {page === "Planes de acción" && (
            <PlansPage
              data={data}
              manager={manager}
              query={query}
              proposal={proposal}
              onClearProposal={() => setProposal(null)}
            />
          )}
          {page === "Lotes" && <LotsPage {...featureProps} />}
          {page === "Compostaje" && <CompostPage {...featureProps} />}
          {page === "Incidencias" && <IncidentsPage {...featureProps} />}
          {page === "Institución" && <IdentityPage {...featureProps} />}
        </main>
        <footer className={s.footer}>
          EcoGest 360 Intelligence · Piloto universitario{" "}
          <span>Datos con origen. Decisiones con evidencia.</span>
        </footer>
      </div>
    </div>
  );
}
