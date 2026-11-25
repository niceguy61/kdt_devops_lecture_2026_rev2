#!/usr/bin/env bash
# 6교시 장애 연습 — 짝의 노트북에서, 짝이 화면을 보지 않을 때 실행한다.
# 사용: bash break.sh 1   (1~4)
# 진단하는 사람은 이 파일을 열어 보지 않는다!
set -euo pipefail
NS=devmart
kc() { kubectl -n "$NS" "$@" >/dev/null 2>&1; }

case "${1:-}" in
  1)
    kubectl -n $NS get secret devmart-db -o jsonpath='{.data.DB_PASSWORD}' > ~/.devmart-db-pw.b64
    kc patch secret devmart-db -p '{"stringData":{"DB_PASSWORD":"wrong-password"}}'
    kc rollout restart deployment/catalog-api deployment/order-api deployment/order-worker
    ;;
  2)
    kc scale deployment/redis --replicas=0
    ;;
  3)
    kc set env deployment/order-worker QUEUE_NAME=order
    ;;
  4)
    kc patch configmap devmart-config -p '{"data":{"CATALOG_URL":"http://catalog-api:8080"}}'
    kc rollout restart deployment/order-api
    ;;
  *)
    echo "사용: bash break.sh 1|2|3|4"; exit 1 ;;
esac
echo "장애 $1을(를) 넣었습니다. 노트북을 짝에게 돌려주세요."
