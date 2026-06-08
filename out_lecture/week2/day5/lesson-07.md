# 7교시: 발표 피드백 및 live Q&A

## 수업 목표
- 발표에서 발견된 Dockerfile/Compose/README 개선점을 즉시 분류한다.
- live Q&A를 통해 Week 2 개념 오해를 정리한다.
- 수정 가능한 항목은 작은 patch list로 남긴다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | feedback 수집 | 상담 15% | feedback board |
| 8-20분 | 개선점 분류 | 설명 25% | triage table |
| 20-35분 | README/Dockerfile quick patch | 실행 30% | patch list |
| 35-45분 | live Q&A | 설명 20% | Q&A note |
| 45-50분 | 최종 제출 기준 확인 | 실행 10% | final readiness |

### Visual 1: 피드백 수정 흐름
![Feedback loop](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/lesson-07-feedback-loop.png)

이 visual은 발표 feedback을 수집, 분류, 수정, 재확인하는 흐름을 보여준다.

## 핵심 설명
피드백은 평가가 끝났다는 신호가 아니라 개선할 수 있는 정보다. Day 5의 7교시는 발표에서 드러난 evidence gap을 실제 README나 Dockerfile 개선으로 연결한다.

## feedback 분류
| 분류 | 예 | 처리 |
|---|---|---|
| Critical | secret 노출, cleanup 위험 | 즉시 수정 |
| High | 실행 명령 누락 | README 보완 |
| Medium | expected output 부족 | evidence 추가 |
| Low | 표현 모호 | 문장 수정 |
| Future | Week 3 주제 | 다음 주 질문으로 이동 |

## quick patch 대상
| 파일 | 수정 예 |
|---|---|
| README | build/run/check/cleanup 보강 |
| Dockerfile | COPY 범위 확인 |
| `.dockerignore` | secret/불필요 파일 제외 |
| compose.yaml | port/env 설명 보완 |
| RCA note | recheck/prevention 추가 |

## live Q&A 핵심 질문
| 질문 | 답 방향 |
|---|---|
| container와 VM 차이는? | process isolation vs guest OS |
| EXPOSE와 ports 차이는? | metadata vs host publish |
| image와 container 차이는? | artifact vs running instance |
| tag는 왜 필요한가? | reproducibility와 handoff |
| down -v는 왜 위험한가? | volume data 삭제 |
| secret은 어디에 두는가? | image 밖, 공개 문서 밖 |

## 실무 insight
현업 review에서 좋은 태도는 방어가 아니라 evidence 업데이트다. "그건 제 PC에서는 됐습니다"보다 "README에 확인 명령과 expected output을 추가하겠습니다"가 더 좋다.

## Q&A 기록 템플릿
```markdown
## Day 5 Q&A
- Question:
- Answer:
- Related file:
- Action:
- Recheck:
```

## 학술 기준 연결
형성평가는 feedback과 revision action이 연결될 때 효과가 있다. 질문을 들었다는 사실보다, 그 질문이 어떤 문서 수정으로 이어졌는지가 중요하다.

## 오해 점검
| 오해 | 교정 |
|---|---|
| feedback은 발표 점수에만 영향 | 제출물 개선 입력이다 |
| 질문은 모르는 티를 낸다 | 좋은 질문은 risk를 드러낸다 |
| 모든 feedback을 반영해야 한다 | severity 기준으로 우선순위화한다 |
| README 수정은 부가 작업이다 | handoff 품질 자체다 |

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 분류 | feedback severity를 나눴다 |
| 수정 | 하나 이상 patch action을 기록했다 |
| Q&A | 질문과 답을 문서화했다 |
| 재확인 | 수정 후 check 명령을 적었다 |

## 전이 과제
Week 3 첫날에 가져갈 질문 하나를 다음 형식으로 작성한다.

```markdown
## Week 3 Question
- Docker/Compose에서 헷갈린 점:
- MSA에서 커질 것 같은 위험:
- 확인하고 싶은 evidence:
```

### 공식 근거 링크
- GitHub Docs About READMEs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- Monash Constructive Alignment: https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/learning-outcomes/how-to/constructive-alignment

## live patch log
```markdown
## Live Patch Log
- Feedback:
- Severity:
- File:
- Change:
- Recheck command:
- Result:
```

## Q&A를 산출물로 바꾸기
| 질문 | 문서 action |
|---|---|
| 어떤 port로 접속하나요 | README Check section 보강 |
| `down -v` 써도 되나요 | cleanup warning 추가 |
| image push했나요 | push decision record 추가 |
| secret은 어디 있나요 | security note 추가 |
| Week 3와 연결은? | readiness question 추가 |

## feedback severity 예시
| Severity | 예 | 처리 |
|---|---|---|
| Critical | real token 노출 | 즉시 제거/폐기 |
| High | 실행 명령 누락 | README 즉시 수정 |
| Medium | expected output 없음 | evidence 보강 |
| Low | 표현 모호 | 시간 남으면 수정 |
| Future | Kubernetes 질문 | Week 3 이후로 이동 |

## live Q&A 운영 규칙
- 질문은 짧게 받는다.
- 답은 evidence와 연결한다.
- 문서 수정이 필요한 질문은 action으로 바꾼다.
- scope 밖 질문은 Week 3/후속 질문으로 기록한다.
- secret, 계정, 개인 정보가 화면에 보이면 즉시 중단하고 가린다.

## Lesson 7 Exit Ticket
```markdown
## Exit Ticket
- 오늘 받은 가장 중요한 feedback:
- severity:
- 수정한 파일:
- 재확인 명령:
- Week 3로 넘길 질문:
```

## 피드백 마감 기준
피드백은 기록만 하고 끝내지 않는다. 최소 하나는 문서나 명령으로 반영한다. 수정할 시간이 부족하면 "수정 예정"이 아니라 owner, 파일, recheck 명령을 남긴다.

마감 확인:
- Critical/High feedback이 방치되지 않았는가?
- README 수정 후 명령을 다시 확인했는가?
- Week 3 질문과 Day 5 수정 항목을 구분했는가?

이 기준을 통과하면 feedback이 말로 끝나지 않고 handoff 품질 개선으로 연결된다.

## feedback 반영 예시
발표 feedback:

```text
HTTP 확인은 말했지만 body marker가 README에 없습니다.
```

수정 action:

```markdown
curl -s http://localhost:18085 | grep week2-day5-integration-v1
```

recheck:

```text
body marker 확인 성공
```

## live patch log
```markdown
## Live Patch Log
- Feedback:
- Severity:
- File:
- Change:
- Recheck command:
- Result:
```

## Q&A를 산출물로 바꾸기
| 질문 | 문서 action |
|---|---|
| 어떤 port로 접속하나요 | README Check section 보강 |
| `down -v` 써도 되나요 | cleanup warning 추가 |
| image push했나요 | push decision record 추가 |
| secret은 어디 있나요 | security note 추가 |
| Week 3와 연결은? | readiness question 추가 |

## feedback 우선순위 원칙
1. secret/security risk
2. 실행 불가능한 명령
3. 정상 확인 기준 누락
4. cleanup/data risk
5. 표현 개선
6. 선택적 polish
