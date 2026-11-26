#!/usr/bin/env bash
# DevMart 세 컨테이너(db → catalog-api → web)를 손으로 띄우는 스크립트 (2주차 4일차 7교시)
# 사용법: devmart 폴더에서  bash ../day4/devmart-up.sh   (또는 경로에 맞게)
set -euo pipefail

# 1) 비밀값은 .env에서 읽는다 (명령어 기록에 남기지 않기)
if [ ! -f .env ]; then
  echo "[오류] .env 파일이 없습니다. devmart 폴더에서 실행했는지, cp .env.example .env 를 했는지 확인하세요." >&2
  exit 1
fi
set -a; source .env; set +a

# 2) 네트워크와 볼륨 (이미 있으면 그대로 쓴다)
docker network inspect devmart-net >/dev/null 2>&1 || docker network create devmart-net
docker volume inspect devmart-db  >/dev/null 2>&1 || docker volume create devmart-db

# 3) DB
docker run -d --name db --network devmart-net \
  -e POSTGRES_USER=devmart -e POSTGRES_DB=devmart -e POSTGRES_PASSWORD="$DB_PASSWORD" \
  -v devmart-db:/var/lib/postgresql \
  -v "$PWD/db/init":/docker-entrypoint-initdb.d:ro \
  postgres:18

echo -n "DB 준비 기다리는 중"
until docker exec db pg_isready -U devmart >/dev/null 2>&1; do echo -n "."; sleep 1; done
echo " 완료"

# 4) API (바깥에 포트를 열지 않는다 — 웹을 통해서만 들어온다)
docker run -d --name catalog-api --network devmart-net \
  --env-file .env -e APP_ENV=docker -e DB_HOST=db \
  devmart/catalog-api:1.0.1

# 5) 웹 (nginx) — API가 먼저 떠 있어야 한다
docker run -d --name web --network devmart-net -p 8080:80 \
  -v "$PWD/web":/usr/share/nginx/html:ro \
  -v "$PWD/nginx/default.conf":/etc/nginx/conf.d/default.conf:ro \
  nginx:1.30-alpine

docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo "브라우저에서 http://localhost:8080 을 여세요"
