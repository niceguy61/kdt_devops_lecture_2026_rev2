# Week 3 MSA Demo App

## 목적
이 앱은 frontend, api, worker, database가 함께 실행되는 최소 MSA 실습 환경이다. 개발 프레임워크 학습이 아니라 service boundary, network, health, logs, failure propagation을 관찰하기 위한 예제다.

## Service Map
| Service | Role | Internal address | External access | Health/log evidence |
|---|---|---|---|---|
| frontend | 사용자 진입점, API proxy | `frontend:80` | http://localhost:18083 | `docker compose logs frontend` |
| api | 상태 API, DB 연결 확인 | `api:8080` | http://localhost:18084 | `/health`, `/api/status` |
| worker | background check loop | `worker` | 없음 | `docker compose logs worker` |
| db | PostgreSQL service | `db:5432` | 없음 | healthcheck, db logs |

## Run
```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl -s http://localhost:18083/api/status
```

Browser check:
- http://localhost:18083

## Logs
```bash
docker compose logs --tail=60 api
docker compose logs --tail=60 worker
docker compose logs --tail=60 db
```

## Failure Drills
```bash
docker compose stop api
curl -s http://localhost:18083/api/status
docker compose start api
```

```bash
docker compose stop db
docker compose logs --tail=40 api
docker compose start db
```

## Cleanup
```bash
docker compose down
# Remove local database volume only when practice data can be discarded.
docker compose down -v
```

## Handoff Questions
- 사용자가 들어오는 external entrypoint는 어디인가?
- api가 database를 찾는 이름은 무엇인가?
- worker는 사용자 요청 경로에 직접 포함되는가?
- DB가 내려가면 frontend, api, worker에는 어떤 증상이 생기는가?
- Kubernetes로 옮기면 어떤 service가 Deployment가 되고 어떤 값이 ConfigMap/Secret이 되는가?
