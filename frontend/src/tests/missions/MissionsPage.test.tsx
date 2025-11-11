import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { Missions } from "../../routes/Missions";

vi.mock("../../lib/api", () => ({
  createApiClient: () => ({
    get: vi.fn().mockResolvedValue({ data: [] }),
  }),
}));

vi.mock("../../lib/auth", () => ({
  loadTokens: () => null,
}));

const renderMissions = async () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <Missions />
    </QueryClientProvider>
  );

  await screen.findByText(/missions/i);
};

it("affiche la section missions", async () => {
  await renderMissions();
  expect(screen.getByText(/missions/i)).toBeInTheDocument();
});
