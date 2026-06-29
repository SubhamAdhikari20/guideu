#!/usr/bin/env bash
# Run static checks across every service.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> core-engine: django system check"
(cd services/core-engine && uv run python manage.py check)

echo "==> real-time-engine: typecheck + eslint"
(cd services/real-time-engine && npm run typecheck && npm run lint)

if [ -d apps/web_admin ]; then
  echo "==> web-admin: eslint"
  (cd apps/web_admin && npm run lint)
fi

if [ -d apps/mobile_app ] && command -v flutter >/dev/null 2>&1; then
  echo "==> mobile-app: flutter analyze"
  (cd apps/mobile_app && flutter analyze)
fi

echo "==> lint complete"
