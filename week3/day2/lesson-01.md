# 1교시: D1 Handoff 검증과 운영 관점 전환

![Week 3 Day 2 Lesson 1](./assets/lesson-01-service-communication.png)

## 수업 목표
- W3D1에서 이미 수행한 정상 경로를 다시 반복하지 않는다.
- D1 evidence를 Day 2 사고 분석의 기준 자료로 재분류한다.
- 정상 흐름 설명에서 운영 사고 질문으로 관점을 전환한다.
- Day 2에서 새로 볼 시나리오의 위험 지점을 미리 표시한다.

## 오늘의 전제
Day 2는 다음을 이미 알고 있다는 전제로 시작한다.

| D1에서 이미 한 것 | D2에서의 취급 |
|---|---|
| `frontend -> api -> db` 정상 흐름 | 장애 영향 범위 비교 기준 |
| `catalog-api -> db` 상품 조회 | partial failure 비교 기준 |
| `order-api -> redis -> order-worker -> db` 정상 처리 | 깨지는 경계 분석 기준 |
| `worker -> api` background check | 사용자 경로 밖 evidence 예시 |
| `audit_logs` 조회 | 사고 타임라인 자료 |

따라서 오늘 다시 할 일이 아니다.

```text
정상 주문 생성
정상 worker log 확인
정상 queue length 0 확인
```

이것들은 D1의 실습 결과다. D2에서는 이 정상 기준이 깨지는 상황을 만든다.

## D1 Evidence를 운영 기준으로 바꾸기
D1에서 수집한 evidence를 다음처럼 다시 분류한다.

| Evidence | D1 의미 | D2 의미 |
|---|---|---|
| `curl /api/orders` | 주문 API가 동작한다 | 사고 후 주문 상태가 꼬였는지 비교한다 |
| `LLEN order-events` | queue가 비어 있다 | backlog 또는 event 유실을 판단한다 |
| `order-worker` log | worker가 처리했다 | worker가 멈췄는지, error를 냈는지 판단한다 |
| `audit_logs` | 처리 이력이 남는다 | 어느 단계까지 실행됐는지 timeline을 만든다 |
| `orders.status` | `processed` 확인 | `pending`, duplicate, ghost row를 찾는다 |

## Day 2에서 보는 진짜 질문
정상 구조:

```text
order-api
  -> DB에 주문 생성
  -> Redis queue에 event push

order-worker
  -> Redis queue에서 event consume
  -> DB 주문 상태 update
  -> audit_logs 기록
```

운영 사고 질문:

| 질문 | 왜 중요한가 |
|---|---|
| DB commit은 됐는데 queue publish가 실패하면? | client 실패와 DB 상태가 어긋난다 |
| worker가 멈춘 동안 주문이 계속 들어오면? | backlog와 처리 지연이 생긴다 |
| queue에 잘못된 message가 들어오면? | worker error, message 유실, DLQ 필요성이 생긴다 |
| 같은 요청이 두 번 들어오면? | request id만으로는 중복 방지가 안 된다 |
| API는 200인데 업무는 끝나지 않았으면? | user-visible success 판단이 필요하다 |

## D2 전용 Lab 확인
```bash
ls week3/day2/labs/incident-scenarios
```

| Script | 수업 역할 |
|---|---|
| `01_ghost_pending_order.sh` | DB commit과 queue publish 사이 장애 |
| `02_backlog_drain.sh` | worker 중지 중 backlog와 복구 |
| `03_poison_message.sh` | 잘못된 queue message와 DLQ 부재 |
| `04_duplicate_request.sh` | idempotency 없는 중복 요청 |

이 스크립트들은 "정상 실행을 편하게 하기 위한 스크립트"가 아니다. 사고를 재현하고 evidence를 묶어 보기 위한 스크립트다.

## 수업 진행 규칙
| 규칙 | 이유 |
|---|---|
| 정상 curl 반복 금지 | D1과 겹친다 |
| 사고 전후 상태 비교 | 운영 판단이 된다 |
| HTTP 결과만 믿지 않기 | 내부 상태와 어긋날 수 있다 |
| DB와 queue를 같이 보기 | 업무 완료와 event 흐름을 분리해야 한다 |
| 복구 명령 후 evidence 확인 | start 명령 자체는 복구 evidence가 아니다 |

## 핵심 포인트
Day 2의 수업 문장은 이렇게 바뀌어야 한다.

나쁜 흐름:

```text
주문 API를 호출한다.
로그를 본다.
처리됐다.
```

좋은 흐름:

```text
Redis 장애 중 주문 API를 호출한다.
client는 실패를 봤지만 DB에 pending row가 남았는지 확인한다.
queue event가 없으면 worker가 처리할 수 없다는 결론을 낸다.
outbox/idempotency/runbook 필요성을 도출한다.
```

## Evidence Note
```markdown
# W3D2S1 Handoff
- D1 normal flow reused as:
- Day2 incident script:
- new failure boundary:
- evidence to compare:
- expected operational question:
```
