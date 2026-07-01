# 7교시: CloudWatch Metrics와 Alarm

![CloudWatch Metrics and Alarm flow](./assets/lesson-07-cloudwatch-metrics-alarm.png)

## 수업 목표
- CloudWatch Metrics의 namespace, metric, dimension 개념을 이해한다.
- EC2/ECS/App Runner/ALB에서 볼 핵심 metric을 구분한다.
- Alarm의 threshold와 state를 preview한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Metric | 시간에 따른 수치형 관찰 데이터다 | 로그와 지표를 혼동한다 | CloudWatch Metrics |
| Dimension | metric을 resource별로 구분하는 label이다 | 어떤 service의 CPU인지 모른다 | dimension filter |
| Alarm | 조건을 만족하면 상태가 바뀌는 감시 규칙이다 | 장애 알림 기준이 없다 | threshold, state |
| ALB target metric | user traffic 관점의 장애 징후를 본다 | app task만 보고 외부 장애를 놓친다 | target response, unhealthy host |

## Logs와 Metrics 차이
| 구분 | Logs | Metrics |
|---|---|---|
| 형태 | event/text | number over time |
| 예시 | error stack, request log | CPUUtilization, 5xx count |
| 질문 | 무슨 일이 있었나 | 얼마나 자주/크게 일어났나 |
| 도구 | Log groups/streams | Metrics/graphs/alarms |

## 볼 수 있는 metric 예시
| 대상 | metric 예시 | 질문 |
|---|---|---|
| EC2 | CPUUtilization, NetworkIn/Out | instance가 과부하인가 |
| ECS | CPU/Memory utilization | service resource가 부족한가 |
| App Runner | request count, latency, 5xx 계열 | managed service가 응답하는가 |
| ALB | TargetResponseTime, HTTPCode_Target_5XX_Count, UnHealthyHostCount | user traffic이 정상인가 |

## Alarm preview
Alarm은 metric이 일정 조건을 만족하면 상태가 바뀌는 규칙이다. 오늘은 알림 채널까지 깊게 만들지 않아도 된다. 다만 threshold, period, evaluation, state 개념을 읽는다.

```text
Metric -> Threshold -> Evaluation -> Alarm State
```

| Alarm state | 의미 |
|---|---|
| OK | 조건 미충족, 정상 범위 |
| ALARM | 조건 충족 |
| INSUFFICIENT_DATA | 판단할 데이터 부족 |

## Evidence Note
```markdown
# W5D3S7 CloudWatch Metrics Alarm
- Service:
- Metric namespace:
- Metric name:
- Dimension:
- 그래프 시간 범위:
- Alarm 후보:
- threshold:
```

## 혼자 다시 따라오기
- 최소 재현 경로: CloudWatch Metrics에서 ALB 또는 ECS/App Runner 관련 metric 하나를 찾아 그래프 시간을 조정한다.
- 공식 문서 키워드: `CloudWatch Metrics`, `namespace`, `dimension`, `CloudWatch alarm`, `threshold`.
- 스스로 확인할 화면: CloudWatch Metrics, Graphed metrics, Alarms.
- 흔한 실패 3개: metric이 아직 안 쌓였는데 장애로 판단함, Region이 다름, 로그에서 봐야 할 error를 metric에서 찾음.
- 다음 준비 상태: log와 metric과 alarm의 역할을 구분할 수 있어야 한다.

## 한 줄 요약
```text
CloudWatch Metrics는 상태를 숫자로 보고, Alarm은 그 숫자에 운영 기준을 붙인다.
```
