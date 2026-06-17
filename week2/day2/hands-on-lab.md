# Week 2 Day 2 Hands-on Lab: Storage and Network

이 lab은 Day 1 PostgreSQL container를 출발점으로 volume, bind mount, custom network, container DNS를 검증한다.

## Phase A: no-volume data loss
```bash
docker stop paperclip-pg16 || true
docker rm paperclip-pg16 || true
docker run -d --name paperclip-pg16 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=paperclip -p 15432:5432 postgres:16
```

```bash
docker exec paperclip-pg16 psql -U postgres -d paperclip -c "\dt"
```

## Phase B: named volume persistence
```bash
docker stop paperclip-pg16 || true
docker rm paperclip-pg16 || true
docker volume create paperclip-pg16-data
docker run -d --name paperclip-pg16 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=paperclip -p 15432:5432 -v paperclip-pg16-data:/var/lib/postgresql/data postgres:16
```

```bash
docker exec paperclip-pg16 psql -U postgres -d paperclip -c "CREATE TABLE IF NOT EXISTS notes(id serial PRIMARY KEY, body text); INSERT INTO notes(body) VALUES ('volume persistence'); SELECT * FROM notes;"
docker stop paperclip-pg16
docker rm paperclip-pg16
docker run -d --name paperclip-pg16-v2 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=paperclip -p 15432:5432 -v paperclip-pg16-data:/var/lib/postgresql/data postgres:16
docker exec paperclip-pg16-v2 psql -U postgres -d paperclip -c "SELECT * FROM notes;"
```

## Phase C: volume inspect
```bash
docker volume ls | grep paperclip-pg16-data
docker volume inspect paperclip-pg16-data
```

## Phase D: bind mount
```bash
mkdir -p week2/day2/tmp-bind/html
printf "<h1>bind mount v1</h1>" > week2/day2/tmp-bind/html/index.html
docker run -d --name paperclip-bind-web -p 18082:80 -v "$PWD/week2/day2/tmp-bind/html:/usr/share/nginx/html:ro" nginx:alpine
curl -s http://localhost:18082
printf "<h1>bind mount v2</h1>" > week2/day2/tmp-bind/html/index.html
curl -s http://localhost:18082
docker inspect paperclip-bind-web --format "{{ json .Mounts }}"
```

## Phase E: custom network and DNS
```bash
docker network create paperclip-day2-net || true
docker run -d --name paperclip-net-pg --network paperclip-day2-net -e POSTGRES_PASSWORD=postgres -v paperclip-pg16-data:/var/lib/postgresql/data postgres:16
docker run --rm --network paperclip-day2-net postgres:16 pg_isready -h paperclip-net-pg -U postgres
```

## Phase F: host port vs container DNS
```bash
docker stop paperclip-net-pg || true
docker rm paperclip-net-pg || true
docker run -d --name paperclip-net-pg --network paperclip-day2-net -e POSTGRES_PASSWORD=postgres -p 15432:5432 -v paperclip-pg16-data:/var/lib/postgresql/data postgres:16
docker ps --filter name=paperclip-net-pg
docker run --rm --network paperclip-day2-net -e PGPASSWORD=postgres postgres:16 psql -h paperclip-net-pg -U postgres -d paperclip -c "SELECT 1;"
```

## Cleanup
```bash
docker stop paperclip-pg16-v2 paperclip-bind-web paperclip-net-pg || true
docker rm paperclip-pg16-v2 paperclip-bind-web paperclip-net-pg || true
docker network rm paperclip-day2-net || true
rm -rf week2/day2/tmp-bind
# 데이터 삭제가 필요할 때만 실행
# docker volume rm paperclip-pg16-data
```

## 주의할 점
- `docker rm`은 container를 지우는 명령이고, `docker volume rm`은 data를 지우는 명령이다. data 초기화가 목적이 아닐 때는 volume을 삭제하지 않는다.
- PostgreSQL volume target은 `/var/lib/postgresql/data`를 기준으로 둔다. target path를 틀리면 volume을 붙였어도 기대한 data가 남지 않는다.
- bind mount는 `$PWD` 기준 host 경로를 container에 노출한다. 경로를 잘못 잡으면 비어 있는 directory를 mount하거나 다른 파일을 덮어쓴 것처럼 보일 수 있다.
- `localhost`는 명령을 실행하는 위치에 따라 의미가 달라진다. host terminal의 `localhost`와 client container 내부의 `localhost`를 같은 대상으로 보지 않는다.
- Cleanup에서 network는 지워도 volume은 기본적으로 남긴다. Day 5 Compose 실습에서 같은 data lifecycle 개념을 다시 사용한다.
