#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Uso: $0 <dominio> <email>"
  exit 1
fi

DOMAIN="$1"
EMAIL="$2"
CONF_NAME="energy-solar.conf"

sudo cp deploy/nginx/${CONF_NAME} /etc/nginx/sites-available/${CONF_NAME}
sudo sed -i "s/your-domain.com/${DOMAIN}/g" /etc/nginx/sites-available/${CONF_NAME}

sudo ln -sf /etc/nginx/sites-available/${CONF_NAME} /etc/nginx/sites-enabled/${CONF_NAME}
sudo nginx -t
sudo systemctl reload nginx

sudo certbot --nginx -d "${DOMAIN}" -d "www.${DOMAIN}" --non-interactive --agree-tos -m "${EMAIL}" --redirect
sudo systemctl enable certbot.timer

echo "TLS configurado para ${DOMAIN}."
