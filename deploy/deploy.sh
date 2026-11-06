#!/usr/bin/env bash
# Rebuilds and restarts the stack on the VPS. Called by the GitHub deploy workflows of both repos.
#   deploy.sh          everything (backend push: compose file or Caddyfile may have changed too)
#   deploy.sh web      only the listed services (frontend push)
set -euo pipefail
cd "$(dirname "$0")"

compose() { docker compose --env-file /opt/ayg/.env -f docker-compose.prod.yml "$@"; }

# Caddy mounts the Caddyfile from a fixed path: deploys replace this whole folder, and a bind mount
# would keep pointing at the old, deleted file.
mkdir -p /opt/ayg/caddy
cp Caddyfile /opt/ayg/caddy/Caddyfile

compose up -d --build "$@"
compose exec -T caddy caddy reload --config /etc/caddy/Caddyfile >/dev/null 2>&1 || true
docker image prune -f >/dev/null
compose ps
