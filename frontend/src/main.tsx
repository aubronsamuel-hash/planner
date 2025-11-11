import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <main className="min-h-screen flex items-center justify-center bg-slate-900 text-slate-100">
      <section className="text-center space-y-4">
        <h1 className="text-4xl font-semibold">Planner Frontend</h1>
        <p className="max-w-md mx-auto text-lg">
          Phase 1 Codex Init provides the scaffolding for the future dashboard. Replace
          this placeholder with authenticated routes and layout components.
        </p>
      </section>
    </main>
  </QueryClientProvider>
);

const root = document.getElementById("root");

if (!root) {
  throw new Error("Root element not found");
}

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
