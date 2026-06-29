# GuideU — real-time-engine (Node + TypeScript + Socket.IO)

Low-latency transport for GuideU. It does **not** own business logic; it
subscribes to the Redis event bus that the Django `core-engine` already publishes
to and fans those events out to the right Socket.IO rooms, and it relays chat,
guide-availability and presence between clients.

## What it does
- **Bridges** `guideu:booking.events`, `guideu:payment.events`,
  `guideu:permit.events`, `guideu:notification.events` → `booking:update`,
  `payment:update`, `permit:update`, `notification:new` socket events.
- **Auth** on the handshake: verifies the same SimpleJWT access token Django
  issues (HS256, shared secret) and joins the socket to `user:<id>` /
  `guide:<id>` / `tourist:<id>` rooms.
- **Chat** in `booking:<reference>` rooms and live **guide availability** +
  **presence** broadcasts.

See `../../docs/api-contracts.md` for the full event contract.

## Run locally
```bash
npm install
npm run dev          # tsx watch (hot reload)
# or
npm run build && npm start
```
Health: `GET http://localhost:8002/health`.

## Client example
```ts
import { io } from 'socket.io-client';
const socket = io('http://localhost:8002', { auth: { token: accessToken } });
socket.on('booking:update', (e) => console.log('booking', e));
socket.emit('chat:join', { room: 'booking:AB12CD34EF90' });
socket.emit('chat:message', { room: 'booking:AB12CD34EF90', body: 'Namaste!' });
```

## Quality
```bash
npm run typecheck    # tsc --noEmit
npm run lint         # eslint
```
