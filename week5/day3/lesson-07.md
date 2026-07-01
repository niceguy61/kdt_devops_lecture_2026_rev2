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


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | logs vs metrics 구분 | comparison table |
| 10~20분 | metric namespace 찾기 | CloudWatch Metrics |
| 20~30분 | ALB/ECS/App Runner metric 확인 | graph |
| 30~40분 | alarm threshold preview | alarm draft |
| 40~50분 | 운영 지표 후보 정리 | metric note |

## metric을 고를 때의 기준
좋은 metric은 운영 행동으로 이어진다. CPU가 높으면 scale이나 instance size를 검토할 수 있고, 5xx가 늘면 app error를 조사하며, unhealthy host가 생기면 target health를 확인한다. 숫자를 보는 이유는 그래프를 예쁘게 만들기 위해서가 아니라 다음 행동을 빠르게 결정하기 위해서다.

## 주요 metric 후보
| 상황 | metric | 다음 행동 |
|---|---|---|
| task가 느림 | CPU/Memory utilization | resource/scale 확인 |
| 사용자가 오류 경험 | ALB 5xx, App Runner 5xx | logs와 deployment 확인 |
| target 장애 | UnHealthyHostCount | target health reason |
| traffic 증가 | RequestCount | scale/cost 확인 |

## Alarm을 너무 빨리 만들 때의 문제
threshold를 이해하지 못하고 alarm을 만들면 noise가 된다. 수업에서는 alarm 생성 자체보다 어떤 metric에 어떤 threshold를 걸면 어떤 운영 행동을 할지 설명하는 데 집중한다.

## 캡처 가이드
Metric graph는 time range, metric name, dimension이 보이게 캡처한다. alarm preview는 threshold와 state가 보이면 충분하다.

## 강사 보강 노트
이 교시는 `Metrics와 Alarm`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| metric dimension을 안 보고 전체 평균만 봄 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| 데이터 지연을 장애로 봄 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| noise alarm을 만들고 방치함 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

## 실습 중 멈춤 포인트
- 첫 번째 멈춤: 학생이 resource를 생성하기 전에 이름, Region, tag, 예상 비용 발생 지점을 말하게 한다.
- 두 번째 멈춤: 성공 화면이 나온 직후 resource ID와 상태값을 evidence note에 적게 한다.
- 세 번째 멈춤: 실패나 지연이 생기면 새로 클릭하기 전에 이전 단계의 화면과 명령을 다시 보게 한다.
- 네 번째 멈춤: 정리 단계에서 "삭제했다"가 아니라 "검색해도 남아 있지 않다"를 확인하게 한다.

## 확인 질문
1. 오늘 만든 resource가 어느 Region과 어느 계정 경계에 있는가?
2. 이 resource가 비용을 만들기 시작하는 시점은 언제인가?
3. 접속이 실패하면 app, network, permission 중 무엇을 먼저 확인할 것인가?
4. 수업이 끝난 뒤 남겨도 되는 resource와 지워야 하는 resource는 무엇인가?

## 제출 evidence 기준
| evidence | 좋은 예 | 부족한 예 |
|---|---|---|
| 화면 캡처 | metric namespace | 성공 toast만 보이는 캡처 |
| 설정 기록 | dimension | "기본값 사용"이라고만 적음 |
| 운영 판단 | threshold 후보 | "잘 됨", "안 됨"으로만 적음 |

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
