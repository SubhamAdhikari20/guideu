# `infra/` — deployment & orchestration

Infrastructure assets that surround the application services.

```text
infra/
├── nginx/
│   ├── nginx.conf            # main nginx config (worker/http/gzip + conf.d include)
│   └── conf.d/guideu.conf    # path-based routing to all services
└── README.md
```

## API gateway (nginx)

`nginx` (see [`../docker-compose.yml`](../docker-compose.yml)) fronts the stack and
routes by path:

| Path           | Upstream            | Service            |
| -------------- | ------------------- | ------------------ |
| `/api/`        | `core-engine:8000`  | Django REST API    |
| `/admin/`      | `core-engine:8000`  | Django admin       |
| `/static/`, `/media/` | `core-engine:8000` | Django assets |
| `/ml/`         | `analytics-engine:8001` | FastAPI ML       |
| `/socket.io/`  | `real-time-engine:8002` | Socket.IO        |
| `/`            | `host.docker.internal:3000` | Next.js admin (host) |

## Dockerfiles live with their services

Each service owns its `Dockerfile` (`services/<svc>/Dockerfile`) so its build
context is self-contained and the image can be built independently of the repo
root. `docker-compose.yml` references them via per-service `build.context`. This
is a deliberate deviation from a central `infra/docker/` directory — see
[`../docs/DECISIONS.md`](../docs/DECISIONS.md) (ADR-0009).

## Bringing the stack up

```bash
cp .env.example .env        # from the repo root
docker compose up --build   # postgres, mongo, redis, 3 services, mlflow, nginx
```

`docker-compose.override.yml` is auto-merged for local development (source
mounts + hot-reload dev servers). Python deps are installed system-wide in the
images, so bind-mounting source over `/app` is safe.
