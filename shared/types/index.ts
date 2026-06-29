/**
 * GuideU shared TypeScript types.
 *
 * Consumed by the Next.js web-admin and the Node real-time-engine so the
 * cross-service contract (Redis domain events, REST envelopes) lives in one
 * place. Keep this file dependency-free.
 */

export type UserRole = 'TOURIST' | 'GUIDE' | 'ADMIN';

/** Authenticated identity extracted from a verified JWT. */
export interface AuthedUser {
  userId: number;
  role?: UserRole;
}

/** Standard DRF-style paginated list envelope. */
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/** Base shape of every event Django publishes on the Redis bus. */
export interface DomainEvent {
  event: string;
  [key: string]: unknown;
}

export interface BookingEvent extends DomainEvent {
  booking_id: number;
  booking_reference: string;
  status: string;
  tourist_id: number;
  assigned_guide_id: number | null;
}

export interface PaymentEvent extends DomainEvent {
  payment_id: number;
  user_id: number;
  booking_id: number | null;
  status: string;
}

export interface PermitEvent extends DomainEvent {
  permit_id: number;
  applicant_id: number;
  status: string;
}

export interface NotificationEvent extends DomainEvent {
  notification_id: number;
  user_id: number;
  kind: string;
  title: string;
}
