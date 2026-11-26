# Week 3 Day 1 Hands-on Lab: MSA 첫 실행과 토폴로지 확인

## Phase 0. 준비
```bash
cd week3/day1/labs/msa-demo
cp .env.example .env
```

## Phase 1. Compose 파일 읽기
```bash
docker compose config
```

확인할 것:

| 항목 | 기준 |
|---|---|
| frontend | host `18083`, nginx reverse proxy |
| api | internal `8080`, debug host `18084`, `DB_HOST=db` |
| worker | host port 없음, `API_URL=http://api:8080/api/status` |
| db | host port 없음, healthcheck, named volume `msa-db-data` |

## Phase 2. 전체 실행
```bash
docker compose up --build -d
docker compose ps
```

Expected shape:

```text
frontend running 0.0.0.0:18083->80/tcp
api      running 0.0.0.0:18084->8080/tcp
worker   running
db       running healthy
```

## Phase 3. 요청 흐름 확인
```bash
curl -s http://localhost:18083/api/status
curl -s http://localhost:18084/health
```

확인할 JSON key:

```text
frontend_to_api
request_id
database_reachable
db_host
```

## Phase 4. 로그 연결
```bash
docker compose logs --tail=60 api
docker compose logs --tail=60 worker
```

API log와 worker log에서 `request_id`를 찾는다. 같은 요청을 어느 service가 남겼는지 비교한다.

## Phase 5. 장애 시나리오 1: API 중지
```bash
docker compose stop api
curl -i http://localhost:18083/api/status
docker compose logs --tail=40 frontend
docker compose start api
```

기록할 것:

| 항목 | 메모 |
|---|---|
| 사용자 증상 | |
| HTTP status 또는 nginx 오류 | |
| 첫 확인 명령 | |
| 복구 명령 | |

## Phase 6. 장애 시나리오 2: DB 중지
```bash
docker compose stop db
curl -s http://localhost:18084/health
docker compose logs --tail=60 api
docker compose start db
```

API container는 running이어도 `ready=false` 또는 `503`이 될 수 있다. 이것이 running과 service ready의 차이다.

## Cleanup
```bash
docker compose down
# DB volume까지 지워도 되는 경우에만
# docker compose down -v
```
