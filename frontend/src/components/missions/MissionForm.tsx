import { FormEvent, useState } from "react";
import { Mission } from "../../lib/types/missions";
import { Button } from "../ui/Button";
import { TextField } from "../ui/TextField";

type MissionFormProps = {
  onSubmit: (mission: Omit<Mission, "id">) => void;
};

export const MissionForm = ({ onSubmit }: MissionFormProps) => {
  const [name, setName] = useState("");
  const [client, setClient] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit({ name, client, start_date: startDate, end_date: endDate, status: "planned" });
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField label="Mission" name="name" value={name} onChange={setName} required />
      <TextField label="Client" name="client" value={client} onChange={setClient} required />
      <TextField label="Début" name="start_date" value={startDate} onChange={setStartDate} type="date" required />
      <TextField label="Fin" name="end_date" value={endDate} onChange={setEndDate} type="date" required />
      <Button type="submit">Créer</Button>
    </form>
  );
};
