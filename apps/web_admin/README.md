# GuideU Web Admin (`apps/web_admin`)

Next.js (App Router, TypeScript, Tailwind) panel for **administrators,
moderators and operators**. The layered structure is adapted from the
`leelame-web` reference.

## Structure

```text
src/
├── app/                 # App Router; (auth) and (dashboard) route groups
│   ├── layout.tsx  globals.css  page.tsx
│   ├── (auth)/          # login / verification flows (sprint-2)
│   └── (dashboard)/     # moderation, analytics, guide verification (sprint-2)
├── components/
│   ├── ui/              # shadcn/ui primitives
│   ├── layout/          # sidebar, navbar, shells
│   └── common/          # shared composite components
├── lib/
│   ├── api/             # axios client + endpoint registry (data access)
│   └── actions/         # server actions (application/use-case layer)
├── schemas/             # zod validation schemas
├── types/               # API envelopes, roles, shared types
└── hooks/               # reusable React hooks
```

## Run

```bash
npm install
npm run dev   # http://localhost:3000
```

Set `NEXT_PUBLIC_API_BASE_URL` to the core-engine base (default
`http://localhost:8000/api/v1`). Sprint 1 ships the **foundation only** — the
dashboards and auth flows are implemented from sprint-2 onward.
