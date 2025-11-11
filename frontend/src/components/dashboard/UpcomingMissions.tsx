import { Mission } from "../../lib/types/missions";

type UpcomingMissionsProps = {
  missions: Mission[];
};

export const UpcomingMissions = ({ missions }: UpcomingMissionsProps) => (
  <section>
    <h3>Prochaines missions</h3>
    <ul>
      {missions.map((mission) => (
        <li key={mission.id}>
          {mission.name} — {mission.start_date}
        </li>
      ))}
    </ul>
  </section>
);
