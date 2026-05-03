#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/energy-solar"
DEPLOY_USER="${DEPLOY_USER:-deploy}"

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release nginx certbot python3-certbot-nginx awscli

if ! command -v docker >/dev/null 2>&1; then
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

if ! id -u "${DEPLOY_USER}" >/dev/null 2>&1; then
  sudo adduser --disabled-password --gecos "" "${DEPLOY_USER}"
fi

sudo usermod -aG docker "${DEPLOY_USER}"
sudo mkdir -p "${APP_DIR}"
sudo chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "${APP_DIR}"

echo "Bootstrap concluido. Faça logout/login para aplicar grupo docker ao usuario ${DEPLOY_USER}."
