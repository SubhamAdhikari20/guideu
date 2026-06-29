#!/usr/bin/env bash
# One-command local setup for the GuideU monorepo.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Setting up GuideU development environment"

command -v uv >/dev/null 2>&1   || { echo "ERROR: uv is required — https://docs.astral.sh/uv/"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js is required"; exit 1; }

if [ ! -f .env ]; then cp .env.example .env; echo "==> created .env from .env.example (fill in real values)"; fi

echo "==> core-engine (uv sync)";       (cd services/core-engine && uv sync)
echo "==> analytics-engine (uv sync)";  (cd services/analytics-engine && uv sync)
echo "==> real-time-engine (npm install)"; (cd services/real-time-engine && npm install)

[ -d apps/web_admin ]  && { echo "==> web-admin (npm install)"; (cd apps/web_admin && npm install); }
if [ -d apps/mobile_app ] && command -v flutter >/dev/null 2>&1; then
  echo "==> mobile-app (flutter pub get)"; (cd apps/mobile_app && flutter pub get)
fi

echo "==> Done. Start the stack with:  docker compose up --build   (or see 'make help')"
