# Week 2 Day 3 Hands-on Lab: Runtime Options, Network, Env, Volume, DB

## 목적
이 문서는 Day 3의 전체 실습을 하나의 긴 실행 흐름으로 묶는다. 교시별 lesson은 개념과 수업 진행을 설명하고, 이 lab guide는 실제 명령, 기대 출력, failure drill, cleanup audit을 제공한다.

Day 3 실습은 네 가지 질문을 끝까지 확인한다.

```text
1. host에서 container service에 어떻게 접근하는가?
2. container끼리는 어떤 이름과 network로 통신하는가?
3. 설정과 데이터는 image가 아니라 runtime에서 어떻게 주입되는가?
4. 실패했을 때 port, env, volume, network 중 어디를 먼저 볼 것인가?
```

## Phase A: nginx port binding과 bind mount
```bash
docker run -d \
  --name paperclip-day3-web \
  -p 18083:80 \
  -v "$PWD/week2/day3/labs/runtime-site/html:/usr/share/nginx/html:ro" \
  nginx:1.27-alpine

docker ps --filter name=paperclip-day3-web
curl -I http://localhost:18083
curl -s http://localhost:18083 | grep runtime-site-v1
docker inspect paperclip-day3-web --format '{{json .Mounts}}'
```

Linux 사전 테스트 핵심 결과:

```text
0.0.0.0:18083->80/tcp
HTTP/1.1 200 OK
Server: nginx/1.27.5
runtime-site-v1
"Destination":"/usr/share/nginx/html","RW":false
```

## Phase B: environment variable 출력
```bash
cd week2/day3/labs/env-report
docker run --rm \
  -e APP_ENV=practice \
  -e APP_PORT=8080 \
  -e FEATURE_FLAG=on \
  -e DB_HOST=postgres \
  -e DB_PORT=5432 \
  -v "$PWD/report.sh:/workspace/report.sh:ro" \
  alpine:3.20 sh /workspace/report.sh
```

기대 결과:

```text
APP_ENV=practice
APP_PORT=8080
FEATURE_FLAG=on
DB_HOST=postgres
DB_PORT=5432
```

## Phase C: PostgreSQL network와 volume
```bash
docker network create paperclip-day3-net
docker volume create paperclip-day3-pgdata
docker run -d \
  --name paperclip-day3-postgres \
  --network paperclip-day3-net \
  -e POSTGRES_PASSWORD=paperclip \
  -e POSTGRES_DB=paperclip \
  -v paperclip-day3-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

확인:

```bash
docker logs paperclip-day3-postgres
docker exec paperclip-day3-postgres pg_isready -U postgres
docker exec paperclip-day3-postgres psql -U postgres -d paperclip -c "select current_database();"
docker run --rm --network paperclip-day3-net postgres:16-alpine pg_isready -h paperclip-day3-postgres -U postgres
docker inspect paperclip-day3-postgres --format '{{json .Mounts}}'
```

Linux 사전 테스트 핵심 결과:

```text
database system is ready to accept connections
/var/run/postgresql:5432 - accepting connections
current_database
paperclip
paperclip-day3-postgres:5432 - accepting connections
"Name":"paperclip-day3-pgdata","Destination":"/var/lib/postgresql/data","RW":true
```

## Phase D: missing env failure drill
```bash
docker run --name paperclip-day3-postgres-missing-env postgres:16-alpine
```

기대 실패:

```text
Error: Database is uninitialized and superuser password is not specified.
You must specify POSTGRES_PASSWORD to a non-empty value for the superuser.
```

정리:

```bash
docker rm paperclip-day3-postgres-missing-env
```

## Phase E: cleanup audit
```bash
docker rm -f paperclip-day3-web paperclip-day3-postgres
docker volume rm paperclip-day3-pgdata
docker network rm paperclip-day3-net
docker ps --filter name=paperclip-day3
docker volume ls --filter name=paperclip-day3
docker network ls --filter name=paperclip-day3
```

## 기록 템플릿
```markdown
## Day 3 Runtime Evidence
- Web container:
- Host port:
- Container port:
- HTTP status:
- Bind mount source:
- Bind mount destination:
- Environment variables:
- Network:
- DB container:
- Volume:
- Readiness result:
- SQL result:
- Failure drill:
- Cleanup result:
```
