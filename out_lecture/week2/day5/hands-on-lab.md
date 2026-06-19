# Week 2 Day 5 Hands-on Lab: 회사형 Compose Architecture Templates

이 lab은 각 교시별 architecture folder를 실행한다. 한 번에 전부 외우는 것이 아니라 같은 루프를 반복하면서 service 관계를 읽는다.

## Common loop
각 architecture directory에서 먼저 실행한다.

```bash
docker compose config
docker compose up -d
docker compose ps
```

확인 후 정리한다.

```bash
docker compose down
# DB/cache data reset이 필요한 경우에만
# docker compose down -v
```

## 2교시: 커머스 카탈로그
![Commerce catalog architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-01-commerce-catalog.png)

```bash
cd week2/day5/labs/compose-architectures/01-web-postgres
docker compose config
docker compose up -d
curl -I http://localhost:18085
curl -s http://localhost:18101/products
docker compose exec db psql -U postgres -d app -c "SELECT current_database();"
docker compose logs db-checker --tail 30
docker compose down
```

Expected:

```text
HTTP/1.1 200 OK
"name":"local-market-starter-kit"
```

## 3교시: 백엔드 서비스 경계
![Backend boundary architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-02-backend-boundary.png)

```bash
cd week2/day5/labs/compose-architectures/02-web-postgres-admin
docker compose config
docker compose up -d
curl -I http://localhost:18086
curl -I http://localhost:18087
curl -s http://localhost:18086/identity/users
curl -s http://localhost:18086/payment/payments
docker compose logs db-checker --tail 30
docker compose down
```

Adminer login:

| 항목 | 값 |
|---|---|
| System | PostgreSQL |
| Server | `db` |
| Username | `postgres` |
| Password | `postgres` |
| Database | `app` |

## 4교시: 프론트엔드 플랫폼 설정과 cache
![Frontend platform architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-03-frontend-platform.png)

```bash
cd week2/day5/labs/compose-architectures/03-web-redis
docker compose config
docker compose up -d
curl -I http://localhost:18088
curl -s http://localhost:18103/config
docker compose logs cache-writer --tail 20
docker compose exec redis redis-cli GET compose:cache
docker compose --profile tool run --rm redis-cli
docker compose down
```

Expected:

```text
hit-from-cache-writer
PONG
```

## 5교시: Nginx reverse proxy
![Reverse proxy architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-04-reverse-proxy.png)

```bash
cd week2/day5/labs/compose-architectures/04-nginx-reverse-proxy
docker compose config
docker compose up -d
curl -s http://localhost:18089/a/
curl -s http://localhost:18089/b/
docker compose logs proxy --tail 40
```

Failure drill:

```bash
docker compose stop web-b
curl -i http://localhost:18089/b/ || true
docker compose logs proxy --tail 20
docker compose up -d web-b
docker compose down
```

## 6교시: 메시징 producer + queue + worker
![Messaging worker architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-05-messaging-worker.png)

```bash
cd week2/day5/labs/compose-architectures/05-queue-worker-db
docker compose config
docker compose up -d
curl -s 'http://localhost:18105/publish?job=send-email:42'
docker compose logs worker --tail 40
docker compose exec db psql -U postgres -d jobs -c "SELECT current_database();"
docker compose down
```

## 7교시: API + PostgreSQL
![API postgres architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-06-api-postgres.png)

```bash
cd week2/day5/labs/compose-architectures/06-api-postgrest
docker compose config
docker compose up -d
curl -s http://localhost:18090/tasks
docker compose logs api --tail 40
docker compose logs db-checker --tail 20
docker compose down
```

Expected:

```text
"title":"read compose.yaml"
"status":"done"
```

## 8교시: Frontend + gateway + API + DB
![MSA preview architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-07-msa-preview.png)

```bash
cd week2/day5/labs/compose-architectures/07-frontend-gateway-api-db
docker compose config
docker compose up -d
curl -s http://localhost:18091 | grep week2-day5-msa-preview
curl -s http://localhost:18091/api/services
docker compose logs gateway --tail 40
docker compose logs api --tail 40
docker compose down
```

Expected:

```text
week2-day5-msa-preview
"name":"gateway"
"name":"api"
```

## 제출/정리
| 항목 | 기록 |
|---|---|
| 실행한 template | folder name |
| 외부 진입점 | host port |
| 내부 service name | `db`, `redis`, `api`, `web-a` 등 |
| 연결 증거 | curl result, DB query, Redis result, worker logs |
| cleanup 선택 | `down` 또는 `down -v` 이유 |
| Week 3 질문 | dependency/failure/scale 관련 질문 |
