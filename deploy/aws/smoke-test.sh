#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-https://your-domain.com}"

echo "Running smoke tests on ${BASE_URL}"
curl -fsS "${BASE_URL}/" >/dev/null
curl -fsS "${BASE_URL}/api/plants" >/dev/null

docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs web --tail=30

echo "Smoke tests completed successfully."
