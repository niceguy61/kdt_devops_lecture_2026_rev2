#!/usr/bin/env bash
# 장애 연습이 끝나면 원래대로 — 진단 · 복구를 직접 한 뒤에, 확인용으로만 쓴다.
set -euo pipefail
cd "$(dirname "$0")"
if [ -f ~/.devmart-db-pw.b64 ]; then
  # 장애 1이 아직 그대로일 때만 원래 비밀번호로 되돌린다 (DB 비밀번호를 바꿔 고쳤다면 건드리지 않는다)
  now=$(kubectl -n devmart get secret devmart-db -o jsonpath='{.data.DB_PASSWORD}' | base64 -d)
  if [ "$now" = "wrong-password" ]; then
    kubectl -n devmart patch secret devmart-db -p "{\"data\":{\"DB_PASSWORD\":\"$(cat ~/.devmart-db-pw.b64)\"}}"
  fi
  rm ~/.devmart-db-pw.b64
fi
kubectl -n devmart set env deployment/order-worker QUEUE_NAME- >/dev/null 2>&1 || true   # apply로는 안 지워지는 칸 (6교시 참고)
kubectl apply -k devmart/
kubectl -n devmart rollout restart deployment/catalog-api deployment/order-api deployment/order-worker
kubectl -n devmart rollout status deployment/order-api --timeout=120s
echo "원래대로 돌려놓았습니다."
