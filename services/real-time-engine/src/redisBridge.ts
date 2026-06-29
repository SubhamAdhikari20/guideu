import { createClient } from 'redis';
import { Server } from 'socket.io';

import { config } from './config';
import { logger } from './logger';
import {
  BookingEvent,
  CHANNELS,
  DomainEvent,
  NotificationEvent,
  PaymentEvent,
  PermitEvent,
} from './types';

export const rooms = {
  user: (id: number | string) => `user:${id}`,
  tourist: (id: number | string) => `tourist:${id}`,
  guide: (id: number | string) => `guide:${id}`,
  booking: (ref: string) => `booking:${ref}`,
};

function handleBooking(io: Server, ev: BookingEvent): void {
  const targets = [rooms.user(ev.tourist_id), rooms.booking(ev.booking_reference)];
  if (ev.assigned_guide_id) targets.push(rooms.user(ev.assigned_guide_id));
  io.to(targets).emit('booking:update', ev);
}

function handlePayment(io: Server, ev: PaymentEvent): void {
  io.to(rooms.user(ev.user_id)).emit('payment:update', ev);
}

function handlePermit(io: Server, ev: PermitEvent): void {
  io.to(rooms.user(ev.applicant_id)).emit('permit:update', ev);
}

function handleNotification(io: Server, ev: NotificationEvent): void {
  io.to(rooms.user(ev.user_id)).emit('notification:new', ev);
}

/**
 * Subscribe to the Django Redis event bus and fan messages out to the relevant
 * Socket.IO rooms. This is the consumer side of the contract Django's
 * `post_save` signals already publish (see docs/api-contracts.md).
 */
export async function startRedisBridge(io: Server): Promise<() => Promise<void>> {
  const subscriber = createClient({ url: config.redisUrl });
  subscriber.on('error', (err) => logger.error('redis subscriber error', { err: String(err) }));
  await subscriber.connect();

  const dispatch = (channel: string, raw: string): void => {
    let ev: DomainEvent;
    try {
      ev = JSON.parse(raw) as DomainEvent;
    } catch (err) {
      logger.warn('could not parse event', { channel, err: String(err) });
      return;
    }
    logger.debug('event in', { channel, event: ev.event });
    switch (channel) {
      case CHANNELS.BOOKING:
        return handleBooking(io, ev as BookingEvent);
      case CHANNELS.PAYMENT:
        return handlePayment(io, ev as PaymentEvent);
      case CHANNELS.PERMIT:
        return handlePermit(io, ev as PermitEvent);
      case CHANNELS.NOTIFICATION:
        return handleNotification(io, ev as NotificationEvent);
      default:
        logger.debug('unhandled channel', { channel });
    }
  };

  const channels = [CHANNELS.BOOKING, CHANNELS.PAYMENT, CHANNELS.PERMIT, CHANNELS.NOTIFICATION, CHANNELS.USER];
  await Promise.all(channels.map((ch) => subscriber.subscribe(ch, (msg) => dispatch(ch, msg))));
  logger.info('subscribed to Redis event bus', { channels });

  return async () => {
    await subscriber.quit();
  };
}
