export type Mission = {
  id: number;
  name: string;
  client: string;
  start_date: string;
  end_date: string;
  status: "planned" | "active" | "completed";
};

export type Assignment = {
  id: number;
  mission_id: number;
  user_email: string;
  role: string;
  capacity: number;
};
