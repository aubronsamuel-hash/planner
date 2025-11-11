import { DashboardSummary } from "../../routes/Dashboard";

type KpiCardsProps = {
  summary: DashboardSummary | null;
};

export const KpiCards = ({ summary }: KpiCardsProps) => {
  if (!summary) {
    return <p>Chargement des KPIs...</p>;
  }

  return (
    <div className="kpi-grid">
      <article>
        <h3>Missions actives</h3>
        <strong>{summary.kpis.active_missions}</strong>
      </article>
      <article>
        <h3>Heures soumises</h3>
        <strong>{summary.kpis.submitted_hours}</strong>
      </article>
      <article>
        <h3>Feuilles en attente</h3>
        <strong>{summary.kpis.pending_timesheets}</strong>
      </article>
    </div>
  );
};
