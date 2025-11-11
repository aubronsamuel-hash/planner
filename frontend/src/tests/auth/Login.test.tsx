import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import { Login } from "../../routes/Login";

vi.mock("../../hooks/useAuth", () => ({
  useAuth: () => ({
    login: vi.fn(),
    logout: vi.fn(),
    isAuthenticated: false,
  }),
}));

it("rend le formulaire de connexion", () => {
  render(<Login />);
  expect(screen.getByText(/accès planner/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /se connecter/i })).toBeInTheDocument();
});
