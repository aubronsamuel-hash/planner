import { Assignment } from "../../lib/types/missions";

type AssignmentListProps = {
  assignments: Assignment[];
};

export const AssignmentList = ({ assignments }: AssignmentListProps) => {
  if (assignments.length === 0) {
    return <p>Aucune affectation.</p>;
  }
  return (
    <ul>
      {assignments.map((assignment) => (
        <li key={assignment.id}>
          {assignment.user_email} — {assignment.role} ({assignment.capacity}% )
        </li>
      ))}
    </ul>
  );
};
