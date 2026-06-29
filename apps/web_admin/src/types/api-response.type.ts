/** Standard API envelopes returned by the core-engine (Django REST Framework). */

export interface ApiError {
  detail?: string;
  [field: string]: unknown;
}

/** DRF page-number pagination envelope. */
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type UserRole = 'TOURIST' | 'GUIDE' | 'ADMIN';
