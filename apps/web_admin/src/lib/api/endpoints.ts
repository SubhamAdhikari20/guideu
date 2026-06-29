/** Backend base URL (core-engine). Configure via NEXT_PUBLIC_API_BASE_URL. */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

/** Endpoint registry. Domain endpoints are added alongside the features. */
export const endpoints = {
  auth: {
    login: '/auth/token/',
    refresh: '/auth/token/refresh/',
    me: '/auth/users/me/',
  },
} as const;
