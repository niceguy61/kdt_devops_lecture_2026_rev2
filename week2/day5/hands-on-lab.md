# Week 2 Day 5 Hands-on Lab: Compose Architecture Lab

이 lab은 제공된 architecture folder를 사용해 유명한 로컬 Compose 패턴을 실행한다.

## Common verification loop
각 architecture directory에서 같은 루프를 사용한다.

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail 80
```

Cleanup:

```bash
docker compose down
# data reset이 필요한 실습에서만 실행
# docker compose down -v
```

## Architecture 01: Web + PostgreSQL
```bash
cd week2/day5/labs/compose-architectures/01-web-postgres
docker compose config
docker compose up -d
curl -I http://localhost:18085
docker compose exec db psql -U postgres -d app -c "SELECT current_database();"
docker compose down
```

## Architecture 02: Web + PostgreSQL + Adminer
```bash
cd week2/day5/labs/compose-architectures/02-web-postgres-admin
docker compose config
docker compose up -d
curl -I http://localhost:18086
curl -I http://localhost:18087
docker compose down
```

## Architecture 03: Web + Redis
```bash
cd week2/day5/labs/compose-architectures/03-web-redis
docker compose config
docker compose up -d
curl -I http://localhost:18088
docker compose run --rm redis-cli
docker compose exec redis redis-cli SET lesson day5
docker compose exec redis redis-cli GET lesson
docker compose down
```

## Architecture 04: Reverse Proxy
```bash
cd week2/day5/labs/compose-architectures/04-nginx-reverse-proxy
docker compose config
docker compose up -d
curl -s http://localhost:18089/a/
curl -s http://localhost:18089/b/
docker compose down
```

## Architecture 05: Queue + Worker + DB
```bash
cd week2/day5/labs/compose-architectures/05-queue-worker-db
docker compose config
docker compose up -d
docker compose exec queue redis-cli LPUSH jobs "send-email:42"
docker compose logs worker --tail 40
docker compose exec db psql -U postgres -d jobs -c "SELECT current_database();"
docker compose down
```

## 주의할 점
- at least two architecture folders executed
- config/up/ps/logs/check 확인 지점
- one failure drill
- down vs down -v decision
- Week 3 service boundary note
