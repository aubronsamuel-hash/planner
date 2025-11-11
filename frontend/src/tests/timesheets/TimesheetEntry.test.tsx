import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { Timesheets } from "../../routes/Timesheets";

vi.mock("../../lib/api", () => ({
  createApiClient: () => ({
    get: vi.fn().mockResolvedValue({ data: [] }),
  }),
}));

vi.mock("../../lib/auth", () => ({
  loadTokens: () => null,
}));

it("affiche le tableau des feuilles de temps", async () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <Timesheets />
    </QueryClientProvider>
  );

  expect(await screen.findByText(/feuilles de temps/i)).toBeInTheDocument();
});
