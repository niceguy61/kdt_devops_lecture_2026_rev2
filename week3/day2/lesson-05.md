# 5교시: Poison Message와 DLQ 필요성

![Week 3 Day 2 Lesson 5](./assets/lesson-05-startup-order-readiness.png)

## 수업 목표
- 잘못된 queue message가 worker에 어떤 영향을 주는지 확인한다.
- message가 소비된 뒤 실패하면 evidence가 어떻게 사라질 수 있는지 이해한다.
- retry, dead-letter queue, schema validation 필요성을 설명한다.
- 단순 worker log 확인을 넘어 실패 message 처리 정책을 논의한다.

## 사고 시나리오
정상 message:

```json
{"order_id": 12, "request_id": "day2-..."}
```

poison message:

```text
not-json-day2-poison
```

worker는 queue에서 message를 꺼내 JSON으로 파싱하려고 한다. 파싱에 실패하면 error log를 남긴다. 그런데 이 교육용 worker에는 DLQ가 없으므로 message가 별도로 보관되지 않는다.

## 실행
```bash
cd week3/day2/labs/incident-scenarios
./03_poison_message.sh
```

## 봐야 할 Evidence
| Evidence | 질문 |
|---|---|
| worker log | `worker_error`가 남았는가 |
| queue length | poison message가 남아 있는가 |
| audit_logs | 업무 event로 기록됐는가 |
| request id | 추적 가능한 id가 있는가 |

## 해석
| 관찰 | 의미 |
|---|---|
| `worker_error` | worker가 message 처리에 실패했다 |
| queue length 0 | message가 소비된 뒤 사라졌을 수 있다 |
| audit row 없음 | 업무 처리 단계까지 가지 못했다 |
| request id 없음 | 추적이 더 어렵다 |

이 시나리오는 현실적이다. 운영에서는 잘못된 payload, schema 변경, 배포 버전 불일치, 수동 queue 주입 실수로 poison message가 발생할 수 있다.

## 왜 위험한가
| 위험 | 설명 |
|---|---|
| silent loss | 실패 message가 사라져 재처리할 수 없다 |
| 반복 실패 | 같은 message가 계속 worker를 실패시킬 수 있다 |
| backlog blockage | queue 종류에 따라 뒤 message 처리가 막힐 수 있다 |
| 원인 추적 어려움 | request id와 payload metadata가 없으면 조사 어렵다 |

## 필요한 설계
| 설계 | 목적 |
|---|---|
| schema validation | worker 처리 전에 message 형태 검증 |
| retry metadata | 몇 번 실패했는지 기록 |
| DLQ | 반복 실패 message를 별도 queue로 격리 |
| error reason | 실패 원인 저장 |
| alert | DLQ 증가나 worker error rate 감지 |

## 실무형 Runbook
| 단계 | 명령/확인 | 판단 |
|---|---|---|
| 1 | worker error rate 확인 | poison message 가능성 |
| 2 | queue depth 확인 | backlog 동반 여부 |
| 3 | 실패 payload 샘플 확인 | schema mismatch 여부 |
| 4 | DLQ 확인 | 격리된 message 수 |
| 5 | 재처리 가능성 판단 | idempotency와 데이터 상태 확인 |

현재 실습에는 DLQ가 없다. 그래서 "없는 것" 자체가 학습 포인트다.

## 운영 리포트 문장
```text
Redis queue에 malformed payload를 주입하자 order-worker가 worker_error를 남겼다.
이후 order-events queue length는 0이 되었고, audit_logs에는 업무 event가 남지 않았다.
현재 worker에는 DLQ가 없어 실패 message를 별도로 추적하거나 재처리하기 어렵다.
```

## 핵심 포인트
queue를 쓴다고 자동으로 안정적인 것이 아니다.

```text
queue + worker
  needs retry policy
  needs DLQ
  needs schema validation
  needs idempotent processing
```

## Evidence Note
```markdown
# W3D2S5 Poison Message
- payload:
- worker error:
- queue length after consume:
- audit row:
- lost evidence:
- required design:
```
