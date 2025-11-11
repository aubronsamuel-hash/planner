import { useCallback, useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { createApiClient } from "../lib/api";
import { AuthTokens, clearTokens, loadTokens, saveTokens } from "../lib/auth";

const client = createApiClient(() => loadTokens()?.accessToken ?? null);

export type AuthState = {
  tokens: AuthTokens | null;
  login: (payload: { email: string; password: string }) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
};

export const useAuth = (): AuthState => {
  const [tokens, setTokens] = useState<AuthTokens | null>(() => loadTokens());

  const loginMutation = useMutation(async ({ email, password }: { email: string; password: string }) => {
    const response = await client.post("/auth/login", { email, password });
    const data = response.data as { access_token: string; refresh_token: string };
    const nextTokens = { accessToken: data.access_token, refreshToken: data.refresh_token };
    saveTokens(nextTokens);
    setTokens(nextTokens);
  });

  const logout = useCallback(async () => {
    const refreshToken = tokens?.refreshToken;
    if (refreshToken) {
      await client.post("/auth/logout", { refresh_token: refreshToken });
    }
    clearTokens();
    setTokens(null);
  }, [tokens]);

  const login = useCallback(
    async ({ email, password }: { email: string; password: string }) => {
      await loginMutation.mutateAsync({ email, password });
    },
    [loginMutation]
  );

  return useMemo(
    () => ({
      tokens,
      login,
      logout,
      isAuthenticated: Boolean(tokens?.accessToken),
    }),
    [login, logout, tokens]
  );
};
