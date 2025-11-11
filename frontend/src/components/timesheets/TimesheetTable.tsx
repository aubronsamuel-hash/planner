import { TimesheetEntry } from "../../lib/types/timesheets";

type TimesheetTableProps = {
  entries: TimesheetEntry[];
};

export const TimesheetTable = ({ entries }: TimesheetTableProps) => {
  if (entries.length === 0) {
    return <p>Aucune saisie</p>;
  }
  return (
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Mission</th>
          <th>Heures</th>
          <th>Statut</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry) => (
          <tr key={entry.id}>
            <td>{entry.entry_date}</td>
            <td>{entry.mission_id}</td>
            <td>{entry.hours}</td>
            <td>{entry.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
