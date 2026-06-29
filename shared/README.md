# `shared/` — cross-service contracts

Framework-agnostic, dependency-free definitions shared by the TypeScript
services so the contract is defined once.

```text
shared/
├── types/index.ts       # Redis domain events, REST envelopes, auth identity
└── constants/index.ts   # pub/sub channels, user roles, API version, dev ports
```

**Consumers:** `apps/web_admin` (Next.js) and `services/real-time-engine` (Node).

These mirror the Python side of the contract documented in
[`../docs/api-contracts.md`](../docs/api-contracts.md). When the event schema
changes, update this folder and the doc together.

> Import via a path alias / workspace reference, e.g. `@guideu/shared/types`.
> Wiring the alias into each TS consumer is a sprint-2 task (kept out of the
> foundation to avoid build coupling before the frontends exist).
