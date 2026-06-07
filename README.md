# GuideU: Smart Travel Companion

GuideU is an enterprise-grade, polyglot microservices platform designed to revolutionize tourism and trekking safety in Nepal. Built to scale under high concurrent loads, the system automates structured trekking permit management (TIMS, National Park clearances), secure tour guide matching, escrowed payment lifecycles, real-time telemetry location tracking, and intelligent machine learning travel recommendations.

This repository acts as a unified monorepo housing decoupled microservices optimized with modern environment orchestrators (`uv` for Python and `npm` for Node.js).

---

## 🏛️ Distributed System Architecture

To balance complex transaction lifecycles against extreme asynchronous and heavy algorithmic computing demands, GuideU utilizes a distributed, fault-isolated **Polyglot Microservices Architecture**.

```text
                               ┌────────────────────────┐
                               │   Flutter Mobile App   │
                               │  & Next.js Dashboard   │
                               └───────────┬────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │ HTTP REST (JSON)                │ WebSockets (Socket.io)          │ HTTP REST (Inference)
         ▼                                 ▼                                 ▼
┌──────────────────┐              ┌──────────────────┐              ┌──────────────────┐
│   core-engine    │              │ real-time-engine │              │ analytics-engine │
│ (Django + DRF)   │              │ (Node.js + Express)             │    (FastAPI)     │
└────────┬─────────┘              └────────┬─────────┘              └────────┬─────────┘
         │                                 │                                 │
         │ Publishes Events                │ Subscribes to Events            │ Pulls Batch Logs
         └───────────────────► ┌───────────┴┐ ◄──────────────────────────────┘
                               │   Redis    │
                               │   Broker   │
                               └─────┬──────┘
                                     │
         ┌───────────────────────────┴───────────────────────────┐
         ▼                                                       ▼
┌──────────────────┐                                    ┌──────────────────┐
│    PostgreSQL    │                                    │     MongoDB      │
│ (Relational Data)│                                    │  (NoSQL Document)│
└──────────────────┘                                    └──────────────────┘

```

### 1. Core Relational Engine (`services/core-engine`)

* **Technology Stack:** Django, Django REST Framework (DRF), `uv` environment runner.
* **Storage Layer:** PostgreSQL / MySQL (ACID compliant).
* **Responsibility:** Serves as the authoritative relational engine. Manages user identities via role-based access control (RBAC), custom JWT creation, automated business rule processing for trekking permits, financial ledger lines, and the centralized admin panel.

### 2. Low-Latency Real-Time Engine (`services/real-time-engine`)

* **Technology Stack:** Node.js, Express.js, Socket.io.
* **Storage Layer:** Redis (In-Memory pub/sub and ephemeral caching).
* **Responsibility:** Handles persistent long-lived network connections. It processes high-frequency spatial streams from hikers' GPS coordinates, coordinates live-chat protocols, and dispatches instantaneous crisis alerts without blocking downstream worker cycles.

### 3. Intelligence & Analytics Engine (`services/analytics-engine`)

* **Technology Stack:** FastAPI, `uv`, Scikit-learn / PyTorch / Pandas.
* **Storage Layer:** MongoDB (NoSQL) for highly polymorphic un-normalized data.
* **Responsibility:** Executes compute-heavy calculations. It runs background pipelines for travel destination recommendations, custom itinerary synthesis, pathing analysis, and tourist demand-forecasting models.

---

## 🗄️ Database Polyglotism Strategy

GuideU intentionally rejects the "one-size-fits-all" database pattern, applying specialized engines based directly on data form and usage attributes:

* **PostgreSQL / MySQL (Relational SQL):** Used for Core Entities (`Users`, `Profiles`, `Permits`, `Payments`). Structural strictness guarantees absolute data protection, prevents race conditions on escrow transactions, and ensures reliable relational mapping via Foreign Key constraints.
* **MongoDB (Document NoSQL):** Used for unstructured data profiles (`Flexible Multi-day Itineraries`, `User Activity/Click Logs`, `Dynamic Review Questionnaires`). Its schemaless nature accommodates diverse API inputs from tour configurations without requiring constant database migration downtime.
* **Redis (In-Memory Key-Value):** Used as a distributed volatile layer. It performs three vital functions: serving as the cross-service Pub/Sub message broker, caching active user JWT blocklists, and housing ephemeral coordinates during active tracking sessions.

---

## 📂 Repository Directory Structure

```text
guideu/
├── .gitignore
├── README.md
└── services/
    ├── core-engine/                      # Django Relational Microservice
    │   ├── pyproject.toml                # Managed Dependencies (DRF, SimpleJWT, psycopg2)
    │   ├── uv.lock                       # Python Cryptographic Lockfile
    │   ├── manage.py                     # Execution Entrypoint Wrapper
    │   ├── config/                       # Infrastructure & Routing Matrix
    │   └── src/                          # Isolated Domain Applications
    │       ├── authentication/           # RBAC Custom Identity Logic
    │       ├── bookings/                 # Guide matching state machines
    │       └── payments/                 # Financial processing hooks (eSewa / Khalti)
    │
    ├── real-time-engine/                 # Node.js Asynchronous Telemetry Server
    │   ├── package.json                  # Node Package Manifest (Socket.io, redis, dotenv)
    │   ├── package-lock.json
    │   └── src/
    │       └── server.js                 # Event-Loop, WebSocket Handlers & Redis Subscriber
    │
    └── analytics-engine/                 # FastAPI Intelligence Engine
        ├── pyproject.toml                # Managed ML Dependencies (FastAPI, Motor, Scikit-learn)
        ├── uv.lock
        └── main.py                       # ML Inference Routes & Itinerary Processors

```

---

## 🛠️ Installation & Environment Setup

### Prerequisites

* Python 3.12+ (Managed via `uv`)
* Node.js v20+ & npm
* PostgreSQL, MongoDB, and Redis instances running locally or via Docker

### 1. Setup Core Relational Engine (Django)

```bash
cd services/core-engine
uv sync

```

Create a `.env` file within `services/core-engine/config/`:

```env
DEBUG=True
SECRET_KEY=your-secure-django-key
DATABASE_NAME=guideu_relational
DATABASE_USER=postgres
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/0

```

Run database migrations and configure the administrative dashboard:

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser

```

### 2. Setup Real-Time Engine (Node.js)

```bash
cd services/real-time-engine
npm install

```

Create a `.env` file inside `services/real-time-engine/`:

```env
PORT=8080
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

```

### 3. Setup Analytics Engine (FastAPI)

```bash
cd services/analytics-engine
uv sync

```

Create a `.env` file inside `services/analytics-engine/`:

```env
MONGO_URI=mongodb://127.0.0.1:27017/guideu_nosql
PORT=5000

```

---

## 🏃 Execution Manual

Launch your local microservices cluster by opening three parallel terminal screens and executing these framework commands:

### Start Core Business Logic Backend (Django)

From `services/core-engine/`:

```bash
uv run python manage.py runserver 127.0.0.1:8000

```

* HTTP Endpoints: `http://127.0.0.1:8000/api/v1/` | Admin Panel: `http://127.0.0.1:8000/admin/`

### Start Telemetry & WebSocket Broker (Node.js)

From `services/real-time-engine/`:

```bash
npm run dev

```

* Open Socket connections bind directly to port `8080` (`ws://127.0.0.1:8080`)

### Start Machine Learning Pipeline (FastAPI)

From `services/analytics-engine/`:

```bash
uv run uvicorn main:app --reload --port 5000

```

* ML Inference Engine Documentation: `http://127.0.0.1:5000/docs`

---

## 📊 Technical Justification for Academic Evaluation

This multi-language, multi-database blueprint provides robust engineering proof items essential for high-scoring defenses:

1. **True Polyglot Orchestration:** Demonstrates cross-boundary communication. When a transaction changes state in the Python environment (Django), a database signal serializes an event packet over an event-broker (Redis). A non-blocking JavaScript engine (Node.js) consumes it to alter client views over WebSockets instantaneously.
2. **Asynchronous Runtime Separation:** Real-time location polling generates high I/O demands. Offloading this workload from Django onto Node.js keeps your core database connections free from thread-exhaustion bottlenecks, providing absolute fault isolation.
3. **Optimized Storage Engines:** Rather than overloading a relational database with messy un-normalized tables, this architecture isolates dynamic, deep schemas (like travel routes and ML recommendation matrices) inside MongoDB, maximizing query processing speed and keeping your data model highly maintainable.

