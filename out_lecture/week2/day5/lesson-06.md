# 6교시: 2주차 발표

## 수업 목표
- Docker 실행 방법을 기능 소개가 아니라 evidence 중심으로 발표한다.
- 겪은 장애, 해결 과정, 남은 위험을 짧고 명확하게 공유한다.
- peer feedback을 통해 README와 실행 절차를 개선한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | 발표 기준 안내 | 설명 15% | presentation rubric |
| 8-18분 | 발표 카드 작성 | 실행 20% | 3-minute card |
| 18-38분 | 학생 발표 | 발표 40% | peer feedback |
| 38-46분 | evidence gap 표시 | 실행 15% | patch list |
| 46-50분 | 다음 교시 Q&A 연결 | 설명 10% | question list |

### Visual 1: evidence 중심 발표 구조
![Presentation evidence structure](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/lesson-06-presentation-evidence.png)

이 visual은 발표가 기능 소개가 아니라 problem, run, evidence, failure, risk, next step으로 구성되어야 함을 보여준다.

## 핵심 설명
현업 발표는 "만든 것 자랑"이 아니라 의사결정자가 다음 행동을 할 수 있게 증거를 전달하는 일이다. Week 2 발표도 마찬가지다.

좋은 발표는 다음 질문에 답한다.

1. 무엇을 Docker로 실행했는가?
2. 어떤 명령으로 build/run/check하는가?
3. 정상 상태 evidence는 무엇인가?
4. 어떤 장애를 겪었고 어떻게 재확인했는가?
5. 남은 위험과 다음 주차 질문은 무엇인가?

## 3분 발표 카드
```markdown
## Week 2 Docker Presentation
- App:
- Build command:
- Run command:
- Compose command:
- HTTP evidence:
- Failure/RCA:
- Security note:
- Cleanup:
- Week 3 question:
```

## 발표 시간 배분
| 구간 | 내용 |
|---|---|
| 0:00-0:30 | 앱과 Docker화 목표 |
| 0:30-1:10 | build/run/compose 명령 |
| 1:10-1:50 | HTTP/log/status evidence |
| 1:50-2:30 | 장애/RCA |
| 2:30-3:00 | 보안/cleanup/Week 3 질문 |

## 좋은 발표와 약한 발표
| 유형 | 특징 |
|---|---|
| 약한 발표 | "Docker로 실행했습니다" 중심 |
| 중간 발표 | 명령은 있으나 expected output 부족 |
| 좋은 발표 | 명령, 상태, HTTP, RCA, risk, next step 포함 |

## peer feedback form
```markdown
## Peer Feedback
- 가장 재현 가능했던 설명:
- 누락된 evidence:
- 보안/cleanup 위험:
- README 개선 제안:
- Week 3 연결 질문:
```

## 학술 기준 연결
ABET의 커뮤니케이션 outcome과 AAC&U oral communication rubric 관점이 적용된다. 기술 발표는 청중이 이해하고 재현하고 판단할 수 있게 구성되어야 한다.

## 실무 insight
DevOps 회의에서 "성공했습니다"보다 중요한 것은 evidence와 residual risk다. 특히 배포 전 공유에서는 정상 확인 방법과 rollback/cleanup 방법이 빠지면 의사결정이 어렵다.

## 오해 점검
| 오해 | 교정 |
|---|---|
| 발표는 결과만 보여주면 된다 | 재현 가능한 과정과 증거가 필요하다 |
| 실패 이야기는 빼는 게 좋다 | RCA는 운영 성숙도의 증거다 |
| 시간이 짧으면 보안은 생략한다 | secret/cleanup 위험은 짧게라도 말한다 |
| 화면이 보이면 evidence다 | command/output/path가 같이 있어야 한다 |

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 구조 | 3분 카드 기준을 지켰다 |
| evidence | HTTP/status/log/tag를 제시했다 |
| RCA | 실패와 재확인을 설명했다 |
| 책임 | 보안/cleanup 위험을 언급했다 |
| 연결 | Week 3 질문을 제시했다 |

## 전이 과제
발표 후 받은 feedback 중 하나를 README에 반영하고 어떤 문장을 바꿨는지 기록한다.

### 공식 근거 링크
- AAC&U VALUE Rubrics: https://www.aacu.org/initiatives/value-initiative/value-rubrics
- Google SRE Postmortem Culture: https://sre.google/sre-book/postmortem-culture/

## 발표 평가 루브릭
| 항목 | 0점 | 1점 | 2점 |
|---|---|---|---|
| 문제/목표 | 없음 | 앱 설명만 | Docker화 목표 명확 |
| 실행 | 없음 | 명령 일부 | build/run/compose 명령 |
| 증거 | 없음 | 화면만 | HTTP/log/status/tag |
| 장애 | 없음 | 증상만 | RCA와 recheck |
| 보안 | 없음 | 주의만 | secret/push/cleanup 기준 |
| 다음 연결 | 없음 | 막연함 | Week 3 질문 구체 |

## 발표 후 기록
```markdown
## Presentation Result
- Presented by:
- Strongest evidence:
- Missing evidence:
- Peer question:
- Patch action:
- Recheck:
```

## 발표 금지 습관
| 습관 | 이유 |
|---|---|
| "아무튼 됐습니다" | 평가 가능한 evidence 없음 |
| token이 보이는 화면 공유 | credential leak |
| 실패를 생략 | 운영 학습 기회 상실 |
| README 없이 구두 설명만 | handoff 불가 |
| port와 path를 말하지 않음 | 재현 불가 |

## 좋은 발표 문장
```text
이 앱은 `paperclip/week2-day5-integration:local` tag로 build했고, `localhost:18085`에서 HTTP 200과 `week2-day5-integration-v1` body marker를 확인했습니다. wrong port 실패를 재현했고, README에 host port와 cleanup을 추가했습니다.
```

## peer 질문 예시
1. 이 image tag를 다른 사람이 어떻게 재현하나요?
2. README만 보고 cleanup할 수 있나요?
3. public push를 해도 안전한 상태인가요?
4. 장애가 다시 나면 어디를 먼저 보나요?
5. Week 3에서 service가 늘어나면 이 문서는 어떻게 바뀌나요?

## 발표 전 self-check
- [ ] 발표 시간이 3분을 넘지 않는다.
- [ ] build 명령을 말한다.
- [ ] run 또는 Compose 명령을 말한다.
- [ ] HTTP evidence를 말한다.
- [ ] 장애/RCA를 하나 말한다.
- [ ] secret/push/cleanup 위험을 말한다.
- [ ] Week 3 질문으로 마무리한다.

## Lesson 6 Exit Ticket
```markdown
## Exit Ticket
- 내 발표에서 가장 강한 evidence:
- 가장 약한 evidence:
- 받은 질문:
- README에 반영할 수정:
```

## 발표 마감 기준
발표가 끝났을 때 학생은 "무엇을 보여줬는가"보다 "무엇이 재현 가능한가"를 기준으로 자기 발표를 평가한다. 발표 중 보여준 화면과 README에 남은 명령이 서로 일치해야 한다.

마감 확인:
- 발표에서 말한 port가 README port와 같은가?
- 발표에서 말한 tag가 실제 image tag와 같은가?
- 발표에서 말한 cleanup 명령이 실제로 실행 가능한가?

## 발표 평가 루브릭
| 항목 | 0점 | 1점 | 2점 |
|---|---|---|---|
| 문제/목표 | 없음 | 앱 설명만 | Docker화 목표 명확 |
| 실행 | 없음 | 명령 일부 | build/run/compose 명령 |
| 증거 | 없음 | 화면만 | HTTP/log/status/tag |
| 장애 | 없음 | 증상만 | RCA와 recheck |
| 보안 | 없음 | 주의만 | secret/push/cleanup 기준 |
| 다음 연결 | 없음 | 막연함 | Week 3 질문 구체 |

## 발표 금지 습관
| 습관 | 이유 |
|---|---|
| "아무튼 됐습니다" | 평가 가능한 evidence 없음 |
| token이 보이는 화면 공유 | credential leak |
| 실패를 생략 | 운영 학습 기회 상실 |
| README 없이 구두 설명만 | handoff 불가 |
| port와 path를 말하지 않음 | 재현 불가 |

## 좋은 발표 문장
```text
이 앱은 `paperclip/week2-day5-integration:local` tag로 build했고, `localhost:18085`에서 HTTP 200과 `week2-day5-integration-v1` body marker를 확인했습니다. wrong port 실패를 재현했고, README에 host port와 cleanup을 추가했습니다.
```

## peer 질문 예시
1. 이 image tag를 다른 사람이 어떻게 재현하나요?
2. README만 보고 cleanup할 수 있나요?
3. public push를 해도 안전한 상태인가요?
4. 장애가 다시 나면 어디를 먼저 보나요?
5. Week 3에서 service가 늘어나면 이 문서는 어떻게 바뀌나요?
