# 6교시: Failure drill - 출력으로 원인 좁히기

## 수업 목표
- missing env, wrong env file, wrong port, wrong network, stale volume, bad image tag를 출력으로 구분한다.
- 실패를 config, network, image, service check 문제로 분류한다.
- 첫 확인 명령과 복구 명령을 연결한다.

## 실패 1: Missing env
```bash
docker rm -f paperclip-day4-pg-missing-env || true
docker run --name paperclip-day4-pg-missing-env postgres:16-alpine || true
docker logs paperclip-day4-pg-missing-env --tail 40 || true
```

Expected failure:

```text
Error: Database is uninitialized and superuser password is not specified.
You must specify POSTGRES_PASSWORD to a non-empty value
```

Hint: `POSTGRES_PASSWORD`가 없으므로 config 문제다. 첫 확인 명령은 `docker logs`다.

Fix:

```bash
docker rm -f paperclip-day4-pg-missing-env || true
docker run -d --name paperclip-day4-pg-ok -e POSTGRES_PASSWORD=practice-only postgres:16-alpine
docker logs paperclip-day4-pg-ok --tail 40
```

## 실패 2: Wrong env file path
```bash
docker run --rm --env-file week2/day4/labs/env-report/.env.production alpine:3.20 env || true
```

Expected failure:

```text
open week2/day4/labs/env-report/.env.production: no such file or directory
```

Hint: app 문제가 아니라 실행 전에 env file 경로가 틀린 문제다. 첫 확인 명령은 `ls week2/day4/labs/env-report`다.

## 실패 3: Wrong port
```bash
curl -I http://localhost:80 || true
curl -I http://localhost:18084 || true
docker ps --filter name=paperclip-day4-nginx
```

Expected failure:

```text
curl: (7) Failed to connect to localhost port 80
0.0.0.0:18084->80/tcp
```

Hint: container 내부 port 80과 host port 80은 다르다. `docker ps`의 `PORTS`가 첫 증거다.

## 실패 4: Wrong network
```bash
docker rm -f paperclip-day4-net-web || true
docker network rm paperclip-day4-net-a paperclip-day4-net-b || true
docker network create paperclip-day4-net-a
docker network create paperclip-day4-net-b
docker run -d --name paperclip-day4-net-web --network paperclip-day4-net-a nginx:1.27-alpine
docker run --rm --network paperclip-day4-net-b alpine:3.20 wget -S -O- http://paperclip-day4-net-web || true
```

Expected failure:

```text
bad address 'paperclip-day4-net-web'
```

Hint: container name DNS는 같은 Docker network 안에서만 기대할 수 있다.

Fix:

```bash
docker run --rm --network paperclip-day4-net-a alpine:3.20 wget -S -O- http://paperclip-day4-net-web | head
```

## 실패 5: Stale volume
```bash
docker rm -f paperclip-day4-pg-volume || true
docker volume rm paperclip-day4-pgdata || true
docker run -d --name paperclip-day4-pg-volume -e POSTGRES_PASSWORD=practice-only -e POSTGRES_DB=first -v paperclip-day4-pgdata:/var/lib/postgresql/data postgres:16-alpine
sleep 5
docker rm -f paperclip-day4-pg-volume
docker run -d --name paperclip-day4-pg-volume -e POSTGRES_PASSWORD=practice-only -e POSTGRES_DB=second -v paperclip-day4-pgdata:/var/lib/postgresql/data postgres:16-alpine
docker logs paperclip-day4-pg-volume --tail 30
```

Expected signal:

```text
Database directory appears to contain a database; Skipping initialization
```

Hint: env를 바꿔도 기존 volume의 초기화된 DB data가 남아 있으면 최초 init 설정이 다시 적용되지 않을 수 있다. 첫 확인 명령은 `docker volume inspect paperclip-day4-pgdata`와 logs다.

## 실패 6: Bad image tag
```bash
docker run --rm nginx:no-such-day4-tag || true
```

Expected failure:

```text
pull access denied
repository does not exist
manifest unknown
```

Hint: 실행 옵션 문제가 아니라 image reference 문제다. 첫 확인 명령은 `docker image ls nginx` 또는 tag 확인이다.

## RCA 표
| 실패 | 대표 출력 | 첫 확인 명령 | 수정 방향 |
|---|---|---|---|
| missing env | `POSTGRES_PASSWORD` | `docker logs` | env 주입 |
| wrong env file | `no such file or directory` | `ls`, `pwd` | env file 경로 수정 |
| wrong port | `Failed to connect`, `18084->80` | `docker ps` | host port 수정 |
| wrong network | `bad address` | `docker network inspect` | 같은 network 사용 |
| stale volume | `Skipping initialization` | `docker logs`, `volume inspect` | reset 여부 판단 |
| bad image tag | `manifest unknown` | `docker image ls` | tag 확인 |

## 다음 연결
다음 교시는 장애 드릴 뒤 남은 container, network, volume을 정리하고 data 삭제 위험을 판단한다.
