/**
 * GuideU shared constants — cross-service magic values kept in one place.
 * Keep this file dependency-free.
 */

/** Redis pub/sub channels Django publishes to and the realtime engine subscribes to. */
export const CHANNELS = {
  USER: 'guideu:user.events',
  BOOKING: 'guideu:booking.events',
  PAYMENT: 'guideu:payment.events',
  PERMIT: 'guideu:permit.events',
  NOTIFICATION: 'guideu:notification.events',
  REVIEW: 'guideu:review.events',
} as const;

export const USER_ROLES = {
  TOURIST: 'TOURIST',
  GUIDE: 'GUIDE',
  ADMIN: 'ADMIN',
} as const;

export const API = {
  VERSION: 'v1',
  PREFIX: '/api/v1',
} as const;

/** Canonical local-dev ports for each service. */
export const SERVICE_PORTS = {
  CORE_ENGINE: 8000,
  ANALYTICS_ENGINE: 8001,
  REALTIME_ENGINE: 8002,
  WEB_ADMIN: 3000,
  MLFLOW: 5000,
  NGINX: 80,
} as const;
