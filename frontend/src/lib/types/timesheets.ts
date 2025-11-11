export type TimesheetEntry = {
  id: number;
  user_email: string;
  mission_id: number;
  entry_date: string;
  hours: number;
  status: "draft" | "submitted" | "approved";
};
