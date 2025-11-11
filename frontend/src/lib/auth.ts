const ACCESS_TOKEN_KEY = "planner.accessToken";
const REFRESH_TOKEN_KEY = "planner.refreshToken";

export type AuthTokens = {
  accessToken: string;
  refreshToken: string;
};

export const loadTokens = (): AuthTokens | null => {
  const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY);
  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
  if (!accessToken || !refreshToken) {
    return null;
  }
  return { accessToken, refreshToken };
};

export const saveTokens = ({ accessToken, refreshToken }: AuthTokens): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

export const clearTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};
