import cors from 'cors';
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';

import { verifyToken } from './auth';
import { config } from './config';
import { logger } from './logger';
import type { AuthedUser } from './types';

/**
 * GuideU real-time-engine — Sprint 1 foundation.
 *
 * Boots an Express health endpoint and a Socket.IO server with optional JWT
 * handshake authentication. Domain event handlers (chat, live booking / permit /
 * payment updates, guide availability) and the Redis -> Socket.IO bridge are
 * delivered from sprint-2 onward.
 */
async function main(): Promise<void> {
  const app = express();
  app.use(cors({ origin: config.corsOrigins }));
  app.use(express.json());

  app.get('/health', (_req, res) => {
    res.json({ status: 'healthy', service: 'guideu-real-time-engine' });
  });

  const httpServer = createServer(app);
  const io = new Server(httpServer, {
    cors: { origin: config.corsOrigins, methods: ['GET', 'POST'] },
  });

  // Optional handshake auth: attach the verified identity when a token is sent.
  // Strict per-namespace enforcement arrives with the feature handlers (sprint-2).
  io.use((socket, next) => {
    const token = socket.handshake.auth.token as string | undefined;
    const user: AuthedUser | null = token ? verifyToken(token) : null;
    (socket.data as { user: AuthedUser | null }).user = user;
    next();
  });

  io.on('connection', (socket) => {
    const { user } = socket.data as { user: AuthedUser | null };
    logger.info('socket connected', { id: socket.id, userId: user?.userId ?? null });
    socket.on('disconnect', (reason) => {
      logger.info('socket disconnected', { id: socket.id, reason });
    });
  });

  httpServer.listen(config.port, () => {
    logger.info('real-time-engine listening', { port: config.port });
  });

  const shutdown = (signal: string): void => {
    logger.info('shutting down', { signal });
    io.close();
    httpServer.close(() => process.exit(0));
    // Force-exit if connections linger.
    setTimeout(() => process.exit(0), 5000).unref();
  };

  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
}

main().catch((err) => {
  logger.error('fatal startup error', { err: String(err) });
  process.exit(1);
});
