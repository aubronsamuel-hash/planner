import { TimesheetEntry } from "../../lib/types/timesheets";
import { Button } from "../ui/Button";

type TimesheetApprovalModalProps = {
  entry: TimesheetEntry | null;
  onApprove: (entry: TimesheetEntry) => void;
  onClose: () => void;
};

export const TimesheetApprovalModal = ({ entry, onApprove, onClose }: TimesheetApprovalModalProps) => {
  if (!entry) {
    return null;
  }

  const handleApprove = () => {
    onApprove(entry);
  };

  return (
    <div role="dialog" aria-modal="true">
      <h3>Valider la feuille</h3>
      <p>
        Mission {entry.mission_id} — {entry.entry_date}
      </p>
      <Button type="button" onClick={handleApprove}>
        Approuver
      </Button>
      <Button type="button" onClick={onClose}>
        Fermer
      </Button>
    </div>
  );
};
