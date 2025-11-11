import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import { Dashboard } from "../../routes/Dashboard";

const getMock = vi.fn();

vi.mock("../../lib/api", () => ({
  createApiClient: () => ({
    get: getMock,
  }),
}));

vi.mock("../../lib/auth", () => ({
  loadTokens: () => null,
}));

getMock.mockImplementation((path: string) => {
  if (path === "/dashboard/summary") {
    return Promise.resolve({ data: { kpis: { active_missions: 1, submitted_hours: 12, pending_timesheets: 2 } } });
  }
  if (path === "/missions/") {
    return Promise.resolve({ data: [] });
  }
  throw new Error(`Unexpected path: ${path}`);
});

it("affiche les cartes KPI", async () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );

  await waitFor(() => expect(screen.getByText(/vue d'ensemble/i)).toBeInTheDocument());
  expect(getMock).toHaveBeenCalledWith("/dashboard/summary");
});
