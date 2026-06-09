# Week 3 Day 2 Hands-on Lab: MSA 운영 Evidence

## 목적
이 문서는 Day 2 교시별 실습을 하나의 실행 흐름으로 묶는다. 표준 실습 앱은 `week3/day1/labs/msa-demo`에 있으며, 모든 실습은 실행, 확인, 장애 재현, 복구, cleanup 기준을 남기는 방식으로 진행한다.

## 공통 준비
```bash
cd week3/day1/labs/msa-demo
docker compose version
docker compose config
```

## 실행
```bash
docker compose up --build -d
docker compose ps
curl -s http://localhost:18083/api/status
```

## 로그 확인
```bash
docker compose logs --tail=60 frontend
docker compose logs --tail=60 api
docker compose logs --tail=60 worker
docker compose logs --tail=60 db
```

## 장애 Drill
| Drill | 명령 또는 변경 | 관찰할 것 | 복구 |
|---|---|---|---|
| API 중지 | `docker compose stop api` | frontend의 API 오류, worker 실패 로그 | `docker compose start api` |
| DB host 오류 | `.env`의 DB_HOST를 틀린 값으로 변경 후 재실행 | api health degraded | 값 복구 후 `docker compose up -d --build api` |
| worker 중지 | `docker compose stop worker` | 사용자 화면은 유지되지만 background 처리 로그 중단 | `docker compose start worker` |
| frontend port 충돌 | 다른 프로세스가 18083 사용 | compose up 실패 | host port 변경 또는 기존 프로세스 정리 |

## Cleanup
```bash
docker compose down
docker compose down -v
```

`down -v`는 실습 데이터 volume까지 지운다. 실제 운영 데이터에는 신중하게 사용한다.

## 제출 Evidence
```markdown
# Day 2 MSA Lab Evidence

## Run
- command:
- service status:
- URL checked:

## Failure drill
- symptom:
- command/change:
- logs observed:
- recovery:
- prevention note:

## Kubernetes readiness
- Which service becomes Deployment?
- Which config becomes ConfigMap?
- Which sensitive value becomes Secret?
- Which entrypoint becomes Service or Ingress?
```
