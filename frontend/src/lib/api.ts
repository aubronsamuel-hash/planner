import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

export const createApiClient = (getToken: () => string | null): AxiosInstance => {
  const instance = axios.create({
    baseURL: "/api/v1",
    withCredentials: false,
  });

  instance.interceptors.request.use((config: AxiosRequestConfig) => {
    const token = getToken();
    if (token) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  return instance;
};
