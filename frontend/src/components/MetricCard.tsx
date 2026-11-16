import s from "../features/reports/Observatory.module.css";
export function MetricCard({
  label,
  value,
  unit,
  caption,
  accent = false,
  index,
  onExplore,
}: {
  label: string;
  value: string;
  unit: string;
  caption: string;
  accent?: boolean;
  index: string;
  onExplore?: () => void;
}) {
  return (
    <article className={`${s.metric} ${accent ? s.accent : ""}`}>
      <div className={s.metricLabel}>
        <span>{label}</span>
        <span aria-hidden="true">{index}</span>
      </div>
      <p className={s.metricValue}>
        {value}
        <small>{unit}</small>
      </p>
      <p className={s.metricCaption}>{caption}</p>
      <button
        className={s.metricAction}
        onClick={onExplore}
        aria-label={`Consultar cohorte base de ${label}`}
      >
        Consultar cohorte ↗
      </button>
    </article>
  );
}
