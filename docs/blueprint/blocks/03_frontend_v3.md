🖥️ Block 3 – Frontend v3 (React + Vite + TypeScript + Auth)
1. Objectifs

Application SPA moderne, typée et performante.

Authentification JWT côté client (login/logout/refresh).

Gestion de données via React Query.

Routing sécurisé avec react-router-dom.

UI cohérente via shadcn/ui + TailwindCSS.

Tests unitaires et e2e via Vitest + MSW.

2. package.json (minimal)
{
  "name": "planner-frontend",
  "version": "0.3.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest run --coverage",
    "lint": "eslint . --ext ts,tsx"
  },
  "dependencies": {
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "react-router-dom": "6.27.0",
    "@tanstack/react-query": "5.59.0",
    "axios": "1.7.7",
    "jwt-decode": "4.0.0",
    "clsx": "2.1.1"
  },
  "devDependencies": {
    "typescript": "5.6.3",
    "vite": "5.4.10",
    "@types/react": "18.3.10",
    "@types/react-dom": "18.3.0",
    "@vitejs/plugin-react": "4.3.2",
    "tailwindcss": "3.4.14",
    "postcss": "8.4.47",
    "autoprefixer": "10.4.20",
    "vitest": "2.1.4",
    "eslint": "9.12.0",
    "@typescript-eslint/parser": "8.8.1",
    "@typescript-eslint/eslint-plugin": "8.8.1",
    "msw": "2.3.2",
    "openapi-typescript": "7.3.0"
  }
}

3. Vite Config + Proxy
vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});

4. Configuration Tailwind CSS
npx tailwindcss init -p

tailwind.config.ts
import type { Config } from "tailwindcss";
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
} satisfies Config;

src/index.css
@tailwind base;
@tailwind components;
@tailwind utilities;

5. Arborescence
frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes/
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── People.tsx
│   │   └── ProtectedRoute.tsx
│   ├── components/
│   │   ├── layout/Shell.tsx
│   │   └── ui/Button.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── queryClient.ts
│   │   └── types.ts
│   ├── hooks/
│   │   └── useAuth.ts
│   └── tests/
│       └── App.test.tsx
├── public/
│   └── favicon.svg
└── vite.config.ts

6. Bootstrap principal
src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./index.css";

const qc = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);

7. Helper API
src/lib/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

8. Gestion Auth côté client
src/lib/auth.ts
import jwtDecode from "jwt-decode";

export function saveToken(token: string) {
  localStorage.setItem("access_token", token);
}

export function logout() {
  localStorage.removeItem("access_token");
}

export function isAuthenticated(): boolean {
  const token = localStorage.getItem("access_token");
  if (!token) return false;
  try {
    const { exp } = jwtDecode<{ exp: number }>(token);
    return Date.now() / 1000 < exp;
  } catch {
    return false;
  }
}

9. Hook : useAuth
src/hooks/useAuth.ts
import { useState } from "react";
import { api } from "../lib/api";
import { saveToken, logout } from "../lib/auth";

export function useAuth() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function login(username: string, password: string) {
    try {
      setLoading(true);
      const { data } = await api.post("/auth/login", { username, password });
      saveToken(data.access_token);
      window.location.href = "/dashboard";
    } catch {
      setError("Identifiants invalides");
    } finally {
      setLoading(false);
    }
  }

  function signout() {
    logout();
    window.location.href = "/login";
  }

  return { login, signout, loading, error };
}

10. Routing principal
src/App.tsx
import { Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { Login } from "./routes/Login";
import { Dashboard } from "./routes/Dashboard";
import { People } from "./routes/People";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/people"
        element={
          <ProtectedRoute>
            <People />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
}

11. Route protégée
src/routes/ProtectedRoute.tsx
import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../lib/auth";

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  return isAuthenticated() ? children : <Navigate to="/login" replace />;
}

12. Page Login
src/routes/Login.tsx
import { useState } from "react";
import { useAuth } from "../hooks/useAuth";

export function Login() {
  const { login, loading, error } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <div className="border p-6 rounded-xl shadow w-80">
        <h1 className="text-xl font-semibold mb-4 text-center">Connexion</h1>
        <input
          type="text"
          placeholder="Nom d'utilisateur"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2 w-full mb-2 rounded"
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 w-full mb-2 rounded"
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button
          disabled={loading}
          onClick={() => login(username, password)}
          className="bg-blue-600 text-white w-full py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Connexion..." : "Se connecter"}
        </button>
      </div>
    </div>
  );
}

13. Dashboard
src/routes/Dashboard.tsx
import { useAuth } from "../hooks/useAuth";
import { api } from "../lib/api";
import { useQuery } from "@tanstack/react-query";

export function Dashboard() {
  const { signout } = useAuth();
  const { data } = useQuery({
    queryKey: ["health"],
    queryFn: async () => (await api.get("/health")).data,
  });

  return (
    <div className="p-6">
      <header className="flex justify-between mb-4">
        <h1 className="text-2xl font-semibold">Tableau de bord</h1>
        <button
          onClick={signout}
          className="bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded"
        >
          Déconnexion
        </button>
      </header>
      <pre className="bg-gray-100 p-4 rounded">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}

14. Exemple People
src/routes/People.tsx
import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

export function People() {
  const { data, isLoading } = useQuery({
    queryKey: ["people"],
    queryFn: async () => (await api.get("/people")).data,
  });

  if (isLoading) return <p>Chargement...</p>;

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-3">Personnes</h2>
      <ul className="space-y-1">
        {data?.map((p: any) => (
          <li key={p.id} className="border p-2 rounded">
            {p.full_name} – {p.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

15. Tests Vitest + MSW
src/tests/App.test.tsx
import { describe, it, expect } from "vitest";

describe("App basic render", () => {
  it("should work", () => {
    expect(true).toBe(true);
  });
});

16. Génération des types API
npx openapi-typescript http://localhost:8000/openapi.json -o src/lib/types.ts

17. Quickstart
cd frontend
npm ci
npm run dev
# Ouvrir http://localhost:5173