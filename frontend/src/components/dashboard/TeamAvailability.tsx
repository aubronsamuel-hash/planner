export type Availability = {
  user: string;
  availability: number;
};

type TeamAvailabilityProps = {
  availability: Availability[];
};

export const TeamAvailability = ({ availability }: TeamAvailabilityProps) => (
  <section>
    <h3>Disponibilité équipe</h3>
    <ul>
      {availability.map((item) => (
        <li key={item.user}>
          {item.user}: {item.availability}%
        </li>
      ))}
    </ul>
  </section>
);
