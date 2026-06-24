#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../../day1/labs/msa-demo"

REQ_ID="${REQ_ID:-day2-ghost-pending-$(date +%s)}"

echo "[scenario] Redis down during order creation"
echo "[request_id] ${REQ_ID}"

docker compose up --build -d >/dev/null
docker compose stop redis >/dev/null

echo
echo "[1] Client request while Redis is down"
curl -i -s -X POST \
  -H "x-request-id: ${REQ_ID}" \
  http://localhost:18121/api/orders || true

echo
echo "[2] Order row may already exist even when client saw failure"
docker compose exec -T db psql -U paperclip -d paperclip \
  -c "select id, status, request_id, created_at, processed_at from orders where request_id='${REQ_ID}' order by id;"

echo
echo "[3] Recover Redis and check queue"
docker compose start redis >/dev/null
sleep 3
docker compose exec -T redis redis-cli LLEN order-events

echo
echo "[4] Audit rows for this request"
docker compose exec -T db psql -U paperclip -d paperclip \
  -c "select service_name, request_id, event, created_at from audit_logs where request_id='${REQ_ID}' order by id;"

echo
echo "[5] Keep stack usable"
docker compose start order-worker >/dev/null
