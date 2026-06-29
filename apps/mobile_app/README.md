# GuideU Mobile (`apps/mobile_app`)

Flutter app for **tourists and guides**. Built with **clean architecture +
MVVM** and **Riverpod**, mirroring the layering used across the team's reference
projects.

## Structure

```text
lib/
├── main.dart            # ProviderScope + runApp
├── app/                 # MaterialApp shell, theme, route names
│   ├── app.dart
│   ├── routes/
│   └── theme/
├── core/                # cross-cutting foundation
│   ├── api/             # Dio client + endpoint registry
│   ├── constants/
│   ├── error/           # Failure hierarchy
│   ├── usecases/        # UseCase contract
│   ├── providers/  services/  utils/  widgets/
└── features/            # feature-first; one folder per feature
    └── <feature>/
        ├── data/        # datasources (local/remote), models, repositories
        ├── domain/      # entities, repository contracts, usecases
        └── presentation/# pages, view_models, states, widgets, providers
```

Sprint 1 ships the **foundation only** — `app/` shell, `core/` utilities and the
empty `features/{auth,destinations,guides,bookings,profile}` skeletons. Feature
screens and state are implemented from sprint-2 onward.

## Run

```bash
flutter pub get
flutter run --dart-define=GUIDEU_API_BASE_URL=http://10.0.2.2:8000/api/v1
```

`10.0.2.2` is the Android emulator's alias for the host machine's `localhost`
(where the core-engine runs).
