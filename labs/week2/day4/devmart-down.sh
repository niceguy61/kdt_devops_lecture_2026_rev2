#!/usr/bin/env bash
# DevMart 세 컨테이너를 지운다. 데이터(볼륨 devmart-db)는 남긴다.
# 데이터까지 지우려면:  bash devmart-down.sh --volumes
docker rm -f web catalog-api db 2>/dev/null || true
docker network rm devmart-net 2>/dev/null || true
if [ "${1:-}" = "--volumes" ]; then
  docker volume rm devmart-db && echo "볼륨 devmart-db 삭제 — 다음 실행 때 상품 5개로 새로 시작합니다"
fi
docker ps -a --format 'table {{.Names}}\t{{.Status}}'
