# Clean Architecture in GuideU

GuideU follows clean architecture across the stack, adapting the patterns proven
in the team's `leelame` reference project.

## The dependency rule

Dependencies point **inward**. The domain layer knows nothing about the data or
presentation layers.

```text
  presentation  ───►  domain  ◄───  data
  (UI + state)        (entities,     (datasources,
                       repo interfaces,  models,
                       use cases)        repo implementations)
```

- **domain** — pure Dart / Python. Entities, repository *interfaces*, use cases.
  No framework, no JSON, no Dio/Django imports.
- **data** — implements the domain repository interfaces. Datasources
  (remote/local), models (JSON ↔ entity), repository impls. Maps transport
  errors to domain `Failure`s.
- **presentation** — pages/widgets + state (Riverpod). Talks to use cases /
  repositories through providers; never touches Dio or raw JSON.

## Mobile (`apps/mobile_app`) — feature-first

```text
features/<feature>/
├── data/          datasources (remote/local), models, repositories (impl)
├── domain/        entities, repositories (abstract), usecases
└── presentation/  providers (Riverpod), pages, widgets, states
```

Auth example:

```text
LoginPage → authControllerProvider (Riverpod)
          → AuthRepository (interface)
          → AuthRepositoryImpl
          → AuthRemoteDataSource (Dio) → core-engine
```

Results flow back as a `(Failure?, AuthUser?)` record; the UI renders friendly
messages instead of raw errors.

## Backend (`services/core-engine`) — per Django app

`src/<app>/` keeps a thin **views** (controller) layer over a **services**
(use-case) layer over **models**; **serializers** validate input/output.
Cross-cutting helpers live in `src/common` (base models, pagination, permissions,
exception handler).

## Data flow — login

```text
Flutter form → AuthController → LoginUseCase → AuthRepositoryImpl
 → ApiClient/Dio (attaches + refreshes JWT) → nginx → Django /api/v1/auth/token/
 → PostgreSQL. Response JSON → AuthUserModel → AuthUser entity
 → AuthAuthenticated state → router pushes /home.
```

## Kept from leelame vs. improved

- **Kept:** feature-first folders; data/domain/presentation split;
  datasource + model + repository layering; a Dio interceptor for auth;
  abstract repository + implementation.
- **Improved:** a dependency-free `(Failure?, T?)` record instead of pulling in
  an `Either` package; Riverpod `Notifier` + a `sealed` `AuthState` for
  predictable UI states.
