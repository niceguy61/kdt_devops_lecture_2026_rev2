# Week 3 Day2: MSA 운영 사고 시나리오와 복구 판단

## Overview
Day 2는 Day 1을 다시 반복하지 않는다.

Day 1에서 이미 확인한 것:

| Day 1에서 끝낸 것 | Day 2에서 반복하지 않는 방식 |
|---|---|
| `docker compose up --build -d` | 수업 시작 전 준비 명령으로만 취급 |
| `frontend -> api -> db` 정상 경로 | 다시 설명하지 않고 사고 영향 범위 비교에만 사용 |
| `catalog-api` 상품 조회 | 정상 조회 반복 대신 partial failure 비교에 사용 |
| `order-api -> redis -> order-worker -> db` 정상 처리 | 정상 주문 생성 반복 대신 깨지는 지점을 재현 |
| `x-request-id` 로그 grep | 단순 grep 대신 audit/DB/queue를 묶어 사건 타임라인 작성 |

Day 2의 목표는 더 현실적이다.

```text
정상 경로를 알고 있다는 전제에서
실제로 운영에서 골치 아픈 애매한 장애를 재현하고
어떤 evidence로 판단하고 복구할지 결정한다.
```

## Day 2의 핵심 사고 유형
| 사고 유형 | 왜 현실적인가 | 핵심 Evidence |
|---|---|---|
| Ghost pending order | client는 503을 봤는데 DB에는 주문이 남을 수 있다. | orders table, audit_logs, Redis queue |
| Worker backlog | API는 성공하지만 worker 처리량 부족으로 업무가 밀린다. | queue length 변화, pending count |
| Poison message | 잘못된 message가 worker를 실패시키거나 유실될 수 있다. | worker error log, queue length, DLQ 부재 |
| Duplicate request | 같은 요청이 두 번 들어와 중복 주문이 생길 수 있다. | 같은 request_id의 orders/audit rows |
| Blast radius | 장애가 전체 장애인지 특정 기능 장애인지 판단해야 한다. | 기능별 curl, service logs, dependency map |

## Day 2 전용 Lab
Day 2는 별도 사고 재현 스크립트를 사용한다.

| Script | 시나리오 |
|---|---|
| `week3/day2/labs/incident-scenarios/01_ghost_pending_order.sh` | Redis down 상태에서 주문 요청, DB에는 pending 주문이 남는지 확인 |
| `week3/day2/labs/incident-scenarios/02_backlog_drain.sh` | worker 중지 중 여러 주문 생성, queue 적체와 복구 후 drain 확인 |
| `week3/day2/labs/incident-scenarios/03_poison_message.sh` | 잘못된 queue message 주입, worker error와 DLQ 부재 확인 |
| `week3/day2/labs/incident-scenarios/04_duplicate_request.sh` | 동일 request id 두 번 전송, idempotency gap 확인 |

## Learning Goals
- D1 정상 경로를 반복하지 않고, 정상 경로가 깨질 때의 운영 판단을 수행한다.
- API 응답, DB commit, queue publish, worker 처리 완료가 서로 분리될 수 있음을 설명한다.
- queue backlog를 단순 숫자가 아니라 처리량/복구 시간 관점으로 해석한다.
- poison message와 duplicate request를 통해 retry, DLQ, idempotency 필요성을 설명한다.
- 사고 타임라인을 `request_id`, DB row, audit row, worker log로 재구성한다.
- Kubernetes로 넘어가기 전, probe/replica/Service/observability가 필요한 이유를 사고 사례에서 끌어낸다.

## Lesson Index
| 교시 | 주제 | D1과 다른 점 |
|---|---|---|
| 1교시 | D1 Handoff 검증과 운영 관점 전환 | 정상 curl 반복이 아니라 D1 evidence를 사고 분석 기준으로 재분류 |
| 2교시 | Ghost pending order | Redis 장애 중 DB commit과 client failure가 어긋나는 케이스 |
| 3교시 | Readiness gap과 transaction boundary | `/health`보다 더 깊은 업무 일관성 확인 |
| 4교시 | Worker backlog와 drain | worker stop 1회가 아니라 여러 요청 적체와 복구 속도 관찰 |
| 5교시 | Poison message와 DLQ 필요성 | 정상 message 추적이 아니라 실패 message 처리 한계 확인 |
| 6교시 | Duplicate request와 idempotency gap | 같은 request가 중복 업무를 만드는 문제 확인 |
| 7교시 | Incident timeline과 runbook | 단일 리포트가 아니라 사고 타임라인과 의사결정표 작성 |
| 8교시 | Kubernetes/운영 플랫폼 연결 + 배움일기 | 사고 사례별로 K8s/observability 필요성 도출 |

## Evidence Policy
Day 2에서는 evidence를 "정상 확인" 용도로 쓰지 않는다. evidence는 판단을 바꾸는 자료여야 한다.

| Evidence | Day 2에서의 역할 |
|---|---|
| HTTP status | client가 본 결과와 내부 상태가 일치하는지 비교 |
| `orders` table | 업무 상태가 실제로 생성/처리됐는지 확인 |
| `audit_logs` | 어떤 service가 어느 단계까지 수행했는지 확인 |
| Redis `LLEN` | backlog와 복구 drain 확인 |
| worker logs | 정상 처리보다 error/lost message/처리 지연 확인 |
| incident script output | 재현 가능한 사고 evidence bundle |

## End-Of-Day Checklist
- [ ] D1 정상 경로를 다시 설명하지 않고 사고 경로를 분석했다.
- [ ] client failure와 DB commit이 어긋나는 ghost pending order를 확인했다.
- [ ] worker backlog가 쌓이고 drain되는 과정을 queue length로 설명했다.
- [ ] poison message에서 DLQ가 왜 필요한지 설명했다.
- [ ] duplicate request에서 request id와 idempotency key의 차이를 설명했다.
- [ ] 사고 타임라인을 request id, DB, audit, log로 재구성했다.
- [ ] Kubernetes/observability 필요성을 사고 사례에서 끌어냈다.
