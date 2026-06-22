# 7교시: 장애 시나리오 1 - API URL, DB host, 환경변수

![Week 3 Day 1 Lesson 7](./assets/lesson-07-environment-check.png)

## 수업 목표
- API 중지, DB 중지, 환경변수 오류가 서로 다른 증상을 만든다는 것을 확인한다.
- `logs`, `inspect`, `exec`, `/health` 중 무엇을 먼저 볼지 판단한다.
- 장애 리포트에 들어갈 증거를 짧고 명확하게 남긴다.

## 준비
```bash
cd week3/day1/labs/msa-demo
docker compose up --build -d
docker compose ps
```

정상 baseline을 먼저 확인한다.

```bash
curl -s http://localhost:18083/api/status
curl -s http://localhost:18084/health
```

## 장애 1: API 중지
```bash
docker compose stop api
curl -i http://localhost:18083/api/status
docker compose logs --tail=60 frontend
docker compose logs --tail=60 worker
```

예상 해석:

| 관찰 | 의미 |
|---|---|
| frontend 요청이 502 또는 실패 | nginx가 upstream `api:8080`에 연결하지 못함 |
| worker log에 connection refused | worker도 API dependency에 실패 |
| db는 healthy | DB 장애가 아니라 API service 장애 가능성 |

복구:

```bash
docker compose start api
curl -s http://localhost:18084/health
```

## 장애 2: DB 중지
```bash
docker compose stop db
curl -i http://localhost:18084/health
curl -i http://localhost:18083/api/status
docker compose logs --tail=60 api
```

예상 해석:

| 관찰 | 의미 |
|---|---|
| API container는 Up | process는 살아 있음 |
| `/health`가 503 | readiness 실패 |
| `database_reachable=false` | DB dependency 실패 |
| frontend도 API 결과를 정상으로 표시하지 못함 | 사용자 경로에도 전파 |

복구:

```bash
docker compose start db
sleep 5
curl -s http://localhost:18084/health
```

## 장애 3: DB_HOST 오류
환경변수를 일부러 틀리게 실행한다.

```bash
docker compose down
DB_HOST=wrong-db docker compose up --build -d
sleep 5
curl -i http://localhost:18084/health
docker compose logs --tail=60 api
```

예상 해석:

| 관찰 | 의미 |
|---|---|
| `db_host`가 `wrong-db` | runtime config가 잘못 들어감 |
| name resolution 또는 connection error | service name DNS 실패 |
| db container는 healthy일 수 있음 | DB 자체 장애가 아니라 API 설정 장애 |

복구:

```bash
docker compose down
docker compose up --build -d
```

## `inspect`로 env 확인
```bash
docker compose exec api env | sort | grep DB_
```

또는:

```bash
docker inspect $(docker compose ps -q api) --format '{{json .Config.Env}}'
```

수업에서는 `exec`로 상태 확인을 할 수 있지만, 운영 container를 임의로 수정하는 shell 작업은 피해야 한다. 상태 확인용 `exec`와 변경 작업용 `exec`는 다르다.

## 장애 리포트 미니 템플릿
| 항목 | 예시 |
|---|---|
| 증상 | frontend `/api/status` 실패 |
| 영향 범위 | frontend 사용자 경로, worker background check |
| 정상 service | db healthy |
| 의심 service | api stopped |
| 첫 확인 명령 | `docker compose ps`, `logs frontend`, `logs worker` |
| 복구 | `docker compose start api` |
| 예방 | healthcheck, alert, runbook |

## Evidence Note
```markdown
# W3D1S7 Failure Drill
- injected failure:
- user visible symptom:
- first command:
- root cause candidate:
- recovery command:
- prevention note:
```

## Cleanup
```bash
docker compose down
```

## 핵심 포인트
장애 분석은 많은 명령을 치는 경연이 아니다. 사용자 증상에서 시작해 dependency map을 따라가며 가장 먼저 확인할 증거를 고르는 일이다.
