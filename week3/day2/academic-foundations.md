# Week 3 Day2 Academic Foundations

## 수업 기준
Day 2는 MSA 정상 경로 복습이 아니라 운영 사고 분석이다.

핵심 질문:

```text
API 응답과 내부 업무 상태가 어긋날 수 있는가?
queue message가 실패하면 어디에 남는가?
retry가 중복 업무를 만들 수 있는가?
Kubernetes가 도와주는 문제와 application 설계가 풀어야 하는 문제는 무엇인가?
```

## 주요 개념
| 개념 | 수업 연결 |
|---|---|
| Transaction boundary | DB commit과 Redis publish가 하나의 atomic transaction이 아님 |
| Outbox pattern | DB 상태와 event 발행 의도를 같은 transaction에 기록 |
| Idempotency | 같은 요청/event가 반복되어도 결과가 중복되지 않게 설계 |
| Dead Letter Queue | 반복 실패 message를 별도 보관해 조사/재처리 |
| Backlog | worker 처리량보다 유입량이 많을 때 queue에 쌓이는 작업 |
| Drain rate | 장애 복구 후 backlog가 줄어드는 속도 |
| Reconciliation | DB, queue, audit 상태를 대조해 어긋난 업무를 정리 |
| Readiness | traffic을 받을 준비 |
| Business consistency | 업무 상태가 모순 없이 남는 성질 |

## Kubernetes와 Application 책임 구분
| 문제 | Kubernetes/플랫폼 | Application/설계 |
|---|---|---|
| 죽은 worker 재시작 | Deployment, ReplicaSet | worker가 재시작 안전해야 함 |
| backlog 증가 감지 | metrics, HPA, alert | 처리 로직이 idempotent해야 함 |
| ready 아닌 pod 제외 | readinessProbe | readiness 기준을 app이 제공해야 함 |
| DB/queue publish 불일치 | 직접 해결하지 않음 | outbox/reconciliation 필요 |
| duplicate request | 직접 해결하지 않음 | idempotency key 필요 |
| poison message | 로그/메트릭 수집 가능 | DLQ/retry/schema validation 필요 |

## 참고 키워드
| Topic | 연결 |
|---|---|
| Google SRE Cascading Failures | dependency 장애 전파와 blast radius |
| Transactional Outbox | DB commit과 event publish 불일치 완화 |
| Idempotent Consumer | worker 재시도와 중복 event 처리 |
| Dead Letter Queue | poison message 격리 |
| Kubernetes Probes | readiness/liveness/startup 구분 |
| OpenTelemetry | request/trace 기반 evidence 연결 |

## 강의자가 강조할 경계
| 피해야 할 말 | 바꿔야 할 말 |
|---|---|
| Redis 장애라서 주문이 실패했다 | client failure와 DB pending row가 불일치한다 |
| worker 다시 켜면 끝 | queue drain과 pending 처리 완료를 확인해야 한다 |
| request id가 있으니 중복 방지된다 | request id는 추적용이고 idempotency key는 별도다 |
| Kubernetes 쓰면 해결된다 | 재시작/스케일은 도와주지만 일관성은 app 설계가 필요하다 |
| 로그에 error가 있다 | 어떤 message가 실패했고 재처리 가능한지 확인해야 한다 |
