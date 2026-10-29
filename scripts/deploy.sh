#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "  Deploying Autonomous Job Application Agent SaaS"
echo "=========================================================="

# 1. Pull latest code from master
echo "--> Pulling latest git changes..."
git pull origin master

# 2. Build Docker containers
echo "--> Building containers..."
docker compose build --pull

# 3. Apply database migrations
echo "--> Running Alembic database migrations..."
docker compose run --rm backend python -m alembic upgrade head

# 4. Restart services
echo "--> Starting / updating services..."
docker compose up -d --remove-orphans

# 5. Verify health check
echo "--> Waiting for backend service health..."
sleep 5
for i in {1..12}; do
    if curl -s -f http://localhost:8000/health > /dev/null; then
        echo "--> Backend is HEALTHY! Application successfully deployed."
        exit 0
    fi
    echo "    Waiting for healthcheck... ($i/12)"
    sleep 3
done

echo "ERROR: Health check timed out!"
docker compose logs --tail=50 backend
exit 1

