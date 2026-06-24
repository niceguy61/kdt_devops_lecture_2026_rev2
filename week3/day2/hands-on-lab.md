# Week 3 Day 2 Hands-on Lab: Realistic MSA Incident Scenarios

## Lab Rule
Day 2에서는 Day 1에서 이미 한 정상 경로 확인을 다시 하지 않는다.

금지에 가까운 반복:

```bash
docker compose up --build -d
curl -s http://localhost:18121/api/orders
docker compose logs order-worker
```

이런 명령은 필요하면 준비 단계에서만 쓴다. 본 실습의 목적은 정상 확인이 아니라 애매한 운영 사고를 재현하고 판단하는 것이다.

## 준비
```bash
cd week3/day1/labs/msa-demo
docker compose up --build -d
docker compose ps
```

여기서 멈추지 않는다. 이 명령은 Day 2의 실습 시작 조건일 뿐이다.

## Scenario 1. Ghost Pending Order
문제 상황:

```text
client는 503을 봤다.
그런데 DB에는 주문이 pending으로 남아 있다.
queue에는 event가 없다.
```

이것은 단순 Redis 장애보다 더 현실적인 문제다. API 내부에서 DB commit과 queue publish 사이에 장애가 생기면 client 관점과 내부 상태가 어긋날 수 있다.

실행:

```bash
cd week3/day2/labs/incident-scenarios
./01_ghost_pending_order.sh
```

관찰 표:

| Evidence | 확인할 것 |
|---|---|
| HTTP response | client가 503 또는 실패 응답을 봤는가 |
| `orders` table | 같은 request id의 주문 row가 생성됐는가 |
| Redis queue | event가 남아 있는가 |
| `audit_logs` | `order_created`만 있고 `order_processed`는 없는가 |

해석:

| 상태 | 의미 |
|---|---|
| client failure + DB pending row | client는 실패로 보지만 내부 업무 흔적은 남았다. |
| queue length 0 | worker가 처리할 event가 없다. |
| pending 유지 | 후속 처리로 이어지지 않는다. |

운영 질문:

| 질문 | 답 |
|---|---|
| 사용자가 다시 주문 버튼을 누르면 어떻게 되는가 | |
| 이 주문은 취소해야 하는가, 재발행해야 하는가 | |
| order-api는 DB commit과 queue publish를 어떻게 묶어야 하는가 | |
| outbox pattern이 왜 필요한가 | |

## Scenario 2. Worker Backlog and Drain
문제 상황:

```text
worker가 멈춘 동안 주문은 계속 접수된다.
queue가 쌓인다.
worker를 복구하면 queue가 줄어든다.
```

실행:

```bash
cd week3/day2/labs/incident-scenarios
COUNT=8 ./02_backlog_drain.sh
```

관찰 표:

| Evidence | 확인할 것 |
|---|---|
| queue length before recovery | worker 중지 중 event가 몇 개 쌓였는가 |
| pending orders | 주문 상태가 pending으로 유지되는가 |
| t+1~t+5 queue length | 복구 후 queue가 줄어드는가 |
| processed orders | 최종적으로 processed가 되는가 |

해석 포인트:

| 관찰 | 운영 의미 |
|---|---|
| queue length가 빠르게 증가 | worker 처리량이 요청량을 따라가지 못함 |
| 복구 후 queue가 천천히 감소 | 처리량 추정 가능 |
| queue가 줄지 않음 | worker는 떴지만 처리 실패 가능 |
| pending이 계속 남음 | 업무 완료 지연 |

토론:

```text
worker를 2개로 늘리면 빨라질까?
중복 처리 위험은 없을까?
queue length 몇 개부터 alert를 걸어야 할까?
```

## Scenario 3. Poison Message Without DLQ
문제 상황:

```text
queue에 잘못된 message가 들어왔다.
worker가 error를 남긴다.
그 message는 다시 처리되지 않고 사라질 수 있다.
```

실행:

```bash
cd week3/day2/labs/incident-scenarios
./03_poison_message.sh
```

관찰 표:

| Evidence | 확인할 것 |
|---|---|
| worker log | `worker_error`가 보이는가 |
| queue length | poison message가 남아 있는가 사라졌는가 |
| audit log | 업무 event가 남았는가 |

해석:

| 관찰 | 의미 |
|---|---|
| worker error + queue length 0 | message가 소비된 뒤 실패했고 별도 보관되지 않았다. |
| audit log 없음 | 업무 처리 단계까지 가지 못했다. |
| DLQ 없음 | 실패 message를 나중에 조사하기 어렵다. |

운영 설계 질문:

| 질문 | 연결 개념 |
|---|---|
| 실패 message를 어디에 보관해야 하는가 | Dead Letter Queue |
| 몇 번까지 재시도해야 하는가 | retry policy |
| 실패 원인을 message에 기록해야 하는가 | error metadata |
| poison message가 worker 전체를 막으면 어떻게 할까 | circuit breaker, quarantine |

## Scenario 4. Duplicate Request Without Idempotency
문제 상황:

```text
같은 request id로 요청이 두 번 들어왔다.
주문도 두 개 생겼다.
```

실행:

```bash
cd week3/day2/labs/incident-scenarios
./04_duplicate_request.sh
```

관찰 표:

| Evidence | 확인할 것 |
|---|---|
| `orders` table | 같은 request id의 row가 여러 개인가 |
| `audit_logs` | `order_created`, `order_processed`가 중복되는가 |
| request id | request id가 중복 방지를 해주지 못한다는 점 |

핵심:

```text
request id는 추적용이다.
idempotency key는 중복 처리 방지용이다.
```

둘은 같은 개념이 아니다.

## Scenario 5. Incident Timeline 작성
위 네 시나리오 중 하나를 골라 timeline을 작성한다.

| 순서 | 시각/단계 | Evidence | 해석 |
|---|---|---|---|
| 1 | client request | HTTP status/body | 사용자가 본 결과 |
| 2 | API step | order-api log or audit | API가 수행한 단계 |
| 3 | queue step | Redis `LLEN` | event 적체/유실 여부 |
| 4 | worker step | worker log | 처리/실패 여부 |
| 5 | DB state | orders/audit query | 최종 업무 상태 |
| 6 | decision | 복구/재처리/조사 | 운영 판단 |

## Scenario 6. Remediation Design
사고별 보완책을 고른다.

| 사고 | 우선 보완책 |
|---|---|
| Ghost pending order | outbox pattern, compensating job |
| Worker backlog | queue depth alert, worker scaling |
| Poison message | DLQ, retry metadata, schema validation |
| Duplicate request | idempotency key, unique constraint |
| Dependency readiness gap | readinessProbe, startupProbe |

## Cleanup
```bash
cd week3/day1/labs/msa-demo
docker compose ps
```

컨테이너만 정리:

```bash
docker compose down
```

데이터까지 초기화:

```bash
docker compose down -v
```

주의:

Day 2에서는 DB에 남은 사고 흔적이 evidence다. 수업 중에는 `down -v`를 바로 실행하지 않는 편이 좋다.
