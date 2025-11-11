import { PropsWithChildren } from "react";
import { Link } from "react-router-dom";

export const Shell = ({ children }: PropsWithChildren) => {
  return (
    <div className="app-shell">
      <aside>
        <nav>
          <ul>
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
            <li>
              <Link to="/missions">Missions</Link>
            </li>
            <li>
              <Link to="/timesheets">Timesheets</Link>
            </li>
          </ul>
        </nav>
      </aside>
      <main>{children}</main>
    </div>
  );
};
