# 6교시: 카카오형 메시징/worker template

![Messaging worker architecture](./assets/day5-arch-05-messaging-worker.png)

## 수업 목표
- HTTP producer, Redis queue, worker 구조를 Compose로 실행한다.
- worker logs로 job 소비를 확인한다.
- queue, worker, DB service boundary를 구분한다.

## 언제 쓰는가
W1D4의 메시징/스트리밍 사례를 Compose로 줄인다. API가 직접 모든 일을 끝내지 않고 queue에 job을 넣고, worker가 Redis queue에서 job을 꺼낸다.

## Template
```bash
cd week2/day5/labs/compose-architectures/05-queue-worker-db
docker compose config
docker compose up -d
docker compose ps
```

구성:

| Service | 역할 | 공개 범위 |
|---|---|---|
| `message-api` | HTTP producer, queue에 job 입력 | host `18105` |
| `queue` | Redis queue | Compose network 내부 |
| `worker` | job consumer | logs로 결과 확인 |
| `db` | 처리 결과 저장 대상 | Compose network 내부 |

## Check
```bash
curl -s 'http://localhost:18105/publish?job=send-email:42'
docker compose logs worker --tail 40
docker compose exec db psql -U postgres -d jobs -c "SELECT current_database();"
```

Expected:

```text
send-email:42
current_database
jobs
```

## 실무 해석
사용자는 worker를 직접 호출하지 않는다. app은 queue에 job을 넣고, worker는 queue에서 꺼낸다. 장애 확인도 web response만 보지 말고 queue length, worker logs, DB 기록을 함께 봐야 한다.

queue 길이를 직접 보고 싶을 때만 다음 명령을 추가로 사용한다.

```bash
docker compose exec queue redis-cli LLEN jobs
```

## Cleanup
```bash
docker compose down
# DB를 초기화할 때만
# docker compose down -v
```
