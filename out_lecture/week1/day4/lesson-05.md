# 5교시: 카카오 - 메시지 스트리밍과 비동기 이벤트

## 수업 목표
- queue와 stream을 서비스 간 결합도를 낮추는 도구로 이해한다.
- synchronous call과 asynchronous event processing을 구분한다.
- producer, topic/queue, consumer, retry, monitoring을 설명한다.
- 메시지 시스템이 로컬 의존성과 실행 순서 문제를 만든다는 점을 Docker와 연결한다.

## 참고 자료
- Kakao Tech: https://tech.kakao.com/
- 카카오 개발자를 위한 공용 Message Streaming Platform: https://tech.kakao.com/posts/485
- Kakao Tech Kafka tag: https://tech.kakao.com/tag/kafka

## 50분 운영
| 시간 | 활동 | 강사 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | 메신저/알림 hook | 같은 이벤트를 여러 서비스가 필요로 한다. | event example |
| 5-15분 | sync vs async | 직접 API 호출과 queue를 비교한다. | comparison table |
| 15-25분 | 카카오 사례 읽기 | 공용 플랫폼이 반복 설정을 줄인다. | source note |
| 25-35분 | 이벤트 흐름 스케치 | producer, topic, consumer, failure path | event diagram |
| 35-45분 | 로컬 의존성 매핑 | queue는 port, data, startup order, log를 가진다. | queue contract |
| 45-50분 | Docker 연결 | multi-container runtime이 자연스러워진다. | Docker 필요성 |

## 핵심 설명
한 서비스가 다른 서비스를 직접 호출하면 caller는 receiver의 응답을 기다린다. 단순하지만 결합도가 높다. receiver가 느리거나 죽으면 caller도 영향을 받는다. Queue나 event stream은 이벤트를 남겨 두고 다른 service가 나중에 처리하게 만든다.

## 시각 자료
![메시지 스트리밍과 AI 알림 요약](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-05-message-streaming-ai-alert.png)

![메시지 스트리밍 아키텍처 모델](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-05-streaming-architecture.png)

![메시지 스트리밍 최적화 포인트](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-05-streaming-optimization.png)

## 서비스 특장점과 채용 동기 연결
- 카카오형 플랫폼 서비스의 강점은 여러 서비스가 공통 이벤트와 메시지 흐름을 공유한다는 점이다.
- 학생 입장에서는 메시징이 단순 "대기열"이 아니라 서비스 간 결합도를 낮추고 장애를 흡수하는 운영 장치라는 것을 볼 수 있다.
- 서비스 수가 늘수록 topic 설계, consumer lag, 재처리, 권한 관리가 중요해진다.

## AI 엔지니어링 연결
- AI 기능은 이벤트 기반으로 붙는 경우가 많다. 예를 들어 문의가 들어오면 분류 worker가 돌고, 장애 이벤트가 생기면 AI가 요약한다.
- 이벤트가 많아질수록 AI 요약, 이상 탐지, 자동 알림도 queue/stream 위에서 동작한다.
- AI worker는 일반 API보다 느릴 수 있으므로 비동기 처리, retry, DLQ 설계가 더 중요해진다.

## Sync vs Async
| 방식 | 형태 | 좋은 점 | 위험 |
|---|---|---|---|
| Synchronous API | 요청이 응답을 기다림 | 즉시 결과 필요 | 장애 전파가 빠름 |
| Queue | producer가 task를 넣고 worker가 처리 | background 작업 | 지연 처리와 retry 설계 필요 |
| Event stream | 여러 consumer가 event를 구독 | 여러 서비스 확장 | ordering, lag, monitoring 필요 |

## Event flow 실습
```text
User action:
Producer service:
Message name:
Queue or topic:
Consumer service:
What can run later:
What must be retried:
What log proves it worked:
```

## 체크포인트
- producer, queue/topic, consumer를 설명한다.
- async 처리가 결합도를 낮추는 이유 1개를 말한다.
- queue가 새로 만드는 운영 부담 1개를 말한다.

## 다음 연결
6교시는 이 흐름을 주문/배달 실시간 이벤트에 적용한다.
