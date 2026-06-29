#!/usr/bin/env bash
# Run the test suites across the Python services.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> core-engine: pytest"
(cd services/core-engine && uv run pytest)

echo "==> analytics-engine: pytest"
(cd services/analytics-engine && uv run pytest)

echo "==> tests complete"
