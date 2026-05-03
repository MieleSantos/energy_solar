#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Uso: $0 <image_tag_anterior>"
  exit 1
fi

PREVIOUS_TAG="$1"
export IMAGE_TAG="${PREVIOUS_TAG}"

docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --remove-orphans

echo "Rollback aplicado para IMAGE_TAG=${PREVIOUS_TAG}"
