import { useQuery } from "@tanstack/react-query";
import { createApiClient } from "../lib/api";
import { loadTokens } from "../lib/auth";
import { Mission } from "../lib/types/missions";
import { MissionForm } from "../components/missions/MissionForm";
import { AssignmentList } from "../components/missions/AssignmentList";

const client = createApiClient(() => loadTokens()?.accessToken ?? null);

export const Missions = () => {
  const { data: missions = [] } = useQuery<Mission[]>(["missions"], async () => {
    const response = await client.get("/missions/");
    return response.data as Mission[];
  });

  const handleCreateMission = (_mission: Omit<Mission, "id">) => {
    // TODO: wire mutation once backend persistence is available
  };

  return (
    <section>
      <h2>Missions</h2>
      <MissionForm onSubmit={handleCreateMission} />
      <ul>
        {missions.map((mission) => (
          <li key={mission.id}>
            {mission.name} — {mission.client}
            <AssignmentList assignments={[]} />
          </li>
        ))}
      </ul>
    </section>
  );
};

export default Missions;
