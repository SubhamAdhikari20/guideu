import jwt from 'jsonwebtoken';

import { config } from './config';
import { AuthedUser } from './types';

/**
 * Verify a SimpleJWT access token using the shared HS256 secret.
 *
 * Django's default SimpleJWT payload carries `user_id` (and `token_type`). We
 * trust only the identity; the core engine remains the source of truth for
 * roles and permissions.
 */
export function verifyToken(token: string): AuthedUser | null {
  try {
    const decoded = jwt.verify(token, config.jwtSecret, { algorithms: ['HS256'] }) as Record<string, unknown>;
    const userId = decoded.user_id;
    if (typeof userId !== 'number') return null;
    return { userId, role: typeof decoded.role === 'string' ? decoded.role : undefined };
  } catch {
    return null;
  }
}
