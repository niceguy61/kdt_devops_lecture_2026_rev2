# 8교시: 운영 플랫폼 연결과 구름 EXP 배움일기

![Week 3 Day 2 Lesson 8](./assets/lesson-08-developer-incident-report.png)

## 수업 목표
- Day 2 사고 사례를 Kubernetes와 observability 필요성으로 연결한다.
- "Kubernetes가 해결하는 문제"와 "application이 해결해야 하는 문제"를 구분한다.
- 구름 EXP 배움일기를 사고 evidence 중심으로 작성한다.

## 오늘 본 사고와 연결 개념
| 사고 | 운영 플랫폼이 도와주는 것 | application이 해결해야 하는 것 |
|---|---|---|
| Ghost pending order | job 실행, metrics, alert | outbox, 보상 transaction |
| Worker backlog | replica scale, HPA | idempotent worker, 처리량 설계 |
| Poison message | logs/metrics alert | DLQ, schema validation, retry policy |
| Duplicate request | traffic routing은 가능 | idempotency key, unique constraint |
| Readiness gap | readinessProbe | business consistency |

Kubernetes는 중요하지만 모든 것을 해결하지 않는다.

```text
Kubernetes solves scheduling/restart/discovery/scaling primitives.
Application design solves consistency/idempotency/business recovery.
```

## 사고별 Kubernetes 연결
| Day 2 evidence | Kubernetes/운영 개념 |
|---|---|
| worker가 멈춤 | Deployment, ReplicaSet |
| queue backlog 증가 | metrics, HPA, alert |
| ready 아닌 service | readinessProbe |
| process hang | livenessProbe |
| service name 통신 | Service DNS |
| 환경별 설정 | ConfigMap, Secret |
| 사고 로그 분산 | centralized logging, tracing |
| audit timeline | observability + business audit |

## 하지만 K8s만으로 안 되는 것
| 문제 | 이유 |
|---|---|
| DB commit 후 Redis publish 실패 | transaction boundary 문제 |
| 중복 주문 | idempotency 설계 필요 |
| poison message 유실 | DLQ/retry metadata 필요 |
| 업무 상태 reconciliation | application/job 설계 필요 |
| 결제/주문 보상 처리 | domain policy 필요 |

이 구분을 못 하면 Kubernetes를 배우고도 운영 사고를 제대로 해결하지 못한다.

## 구름 EXP 배움일기 가이드
감상이 아니라 사고 분석 중심으로 쓴다.

| 항목 | 작성 가이드 |
|---|---|
| 선택한 사고 | ghost pending, backlog, poison, duplicate 중 하나 |
| 재현 명령 | 실행한 script |
| client symptom | 사용자가 봤을 결과 |
| internal evidence | DB/queue/log/audit 중 핵심 |
| mismatch | 외부 결과와 내부 상태가 어떻게 달랐는가 |
| immediate action | 당장 할 조치 |
| long-term fix | 설계 보완 |
| Kubernetes question | 어떤 K8s 개념이 도움 되는가 |
| application question | K8s로 해결 안 되는 것은 무엇인가 |

## 배움일기 예시
```markdown
# W3D2 배움일기

오늘은 ghost pending order 사고가 가장 인상적이었다.
`01_ghost_pending_order.sh`를 실행하자 client는 실패 응답을 봤지만,
DB `orders` table에는 pending 주문이 남아 있었다.
Redis queue에는 처리 event가 없어서 order-worker가 이 주문을 자동 처리할 수 없었다.

이 사고는 단순히 Redis를 다시 켠다고 해결되는 문제가 아니라,
DB commit과 queue publish 사이의 transaction boundary 문제라는 점을 알게 되었다.
Kubernetes readinessProbe는 준비 안 된 pod로 traffic을 보내지 않는 데 도움을 주지만,
outbox pattern이나 idempotency는 application에서 설계해야 한다.
```

## 다음 수업으로 넘길 질문
| 질문 | 다음 연결 |
|---|---|
| worker replica를 늘리면 backlog가 줄어드는가 | Deployment scale |
| readinessProbe는 어디까지 확인해야 하는가 | probe 설계 |
| Secret과 ConfigMap은 사고를 줄이는가 | 설정 관리 |
| logs만으로 충분한가 | metrics/tracing |
| Kubernetes Job으로 ghost pending을 보정할 수 있나 | batch/reconciliation |

## 핵심 포인트
Day 2의 결론:

```text
D1: MSA 정상 경로를 실행했다.
D2: 정상 경로가 깨질 때 내부 상태가 어떻게 어긋나는지 봤다.
K8s: 이 운영 문제 중 일부를 플랫폼 수준에서 다루기 시작한다.
```

## Evidence Note
```markdown
# W3D2S8 Learning Journal
- selected incident:
- script:
- client symptom:
- internal evidence:
- mismatch:
- Kubernetes helps with:
- application must solve:
```
