import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { createApiClient } from "../lib/api";
import { loadTokens } from "../lib/auth";
import { TimesheetEntry } from "../lib/types/timesheets";
import { TimesheetApprovalModal } from "../components/timesheets/TimesheetApprovalModal";
import { TimesheetTable } from "../components/timesheets/TimesheetTable";

const client = createApiClient(() => loadTokens()?.accessToken ?? null);

export const Timesheets = () => {
  const { data: entries = [] } = useQuery<TimesheetEntry[]>(["timesheets"], async () => {
    const response = await client.get("/timesheets/");
    return response.data as TimesheetEntry[];
  });
  const [selected, setSelected] = useState<TimesheetEntry | null>(null);

  return (
    <section>
      <h2>Feuilles de temps</h2>
      <TimesheetTable entries={entries} />
      <TimesheetApprovalModal entry={selected} onApprove={() => undefined} onClose={() => setSelected(null)} />
    </section>
  );
};

export default Timesheets;
