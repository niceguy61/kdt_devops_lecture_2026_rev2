# Week 2 Day 3 PostgreSQL Runtime Lab

## Purpose
PostgreSQL container는 environment variable, named volume, network, logs를 한 번에 확인하기 좋은 실습 대상이다.

## Run
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

## Check
```bash
docker logs paperclip-day3-postgres
docker exec paperclip-day3-postgres pg_isready -U postgres
docker exec paperclip-day3-postgres psql -U postgres -d paperclip -c "select current_database();"
```

## Cleanup
```bash
docker rm -f paperclip-day3-postgres
docker volume rm paperclip-day3-pgdata
docker network rm paperclip-day3-net
```
