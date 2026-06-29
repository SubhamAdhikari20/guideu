import axios, { type AxiosInstance } from 'axios';

import { API_BASE_URL } from './endpoints';

/**
 * Shared Axios client for the admin panel (mirrors the leelame-web `lib/api`
 * layer). A request interceptor attaches the bearer token; per-domain API
 * modules (`lib/api/<domain>`) build on this from sprint-2 onward.
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 20000,
});

let accessTokenProvider: (() => string | null) | null = null;

/** Register how the client should obtain the current access token. */
export function setAccessTokenProvider(provider: () => string | null): void {
  accessTokenProvider = provider;
}

apiClient.interceptors.request.use((config) => {
  const token = accessTokenProvider?.();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
