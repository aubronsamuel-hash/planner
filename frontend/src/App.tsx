import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Login } from "./routes/Login";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { Dashboard } from "./routes/Dashboard";
import { Missions } from "./routes/Missions";
import { Timesheets } from "./routes/Timesheets";
import { Shell } from "./components/layout/Shell";

const queryClient = new QueryClient();

export const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedRoute />}>
          <Route
            path="/"
            element={
              <Shell>
                <Dashboard />
              </Shell>
            }
          />
          <Route
            path="/dashboard"
            element={
              <Shell>
                <Dashboard />
              </Shell>
            }
          />
          <Route
            path="/missions"
            element={
              <Shell>
                <Missions />
              </Shell>
            }
          />
          <Route
            path="/timesheets"
            element={
              <Shell>
                <Timesheets />
              </Shell>
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;
