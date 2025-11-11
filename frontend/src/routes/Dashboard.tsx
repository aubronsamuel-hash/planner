import { useQuery } from "@tanstack/react-query";
import { createApiClient } from "../lib/api";
import { loadTokens } from "../lib/auth";
import { Mission } from "../lib/types/missions";
import { KpiCards } from "../components/dashboard/KpiCards";
import { TeamAvailability } from "../components/dashboard/TeamAvailability";
import { UpcomingMissions } from "../components/dashboard/UpcomingMissions";

const client = createApiClient(() => loadTokens()?.accessToken ?? null);

export type DashboardSummary = {
  kpis: {
    active_missions: number;
    submitted_hours: number;
    pending_timesheets: number;
  };
};

export const Dashboard = () => {
  const { data: summary = null } = useQuery<DashboardSummary | null>(["dashboard"], async () => {
    const response = await client.get("/dashboard/summary");
    return response.data as DashboardSummary;
  });

  const { data: missions = [] } = useQuery<Mission[]>(["dashboard-missions"], async () => {
    const response = await client.get("/missions/");
    return response.data as Mission[];
  });

  return (
    <div>
      <h2>Vue d'ensemble</h2>
      <KpiCards summary={summary} />
      <UpcomingMissions missions={missions} />
      <TeamAvailability availability={[{ user: "Alice", availability: 80 }]} />
    </div>
  );
};

export default Dashboard;
