# 7교시: 제출물 점검 및 live Q&A

## 수업 목표
- Week 2 Docker 학습 정리 제출물의 evidence gap을 찾는다.
- live Q&A를 통해 Docker 개념 오해를 정리한다.
- 수정 가능한 항목은 README, Dockerfile, Compose, 학습 정리 카드에 작은 patch list로 남긴다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | 제출물 점검 기준 확인 | 상담 15% | review board |
| 8-20분 | evidence gap 분류 | 설명 25% | triage table |
| 20-35분 | README/Dockerfile/summary quick patch | 실행 30% | patch list |
| 35-45분 | live Q&A | 설명 20% | Q&A note |
| 45-50분 | 최종 제출 기준 확인 | 실행 10% | final readiness |

### Visual 1: 제출물 점검과 수정 흐름
![Feedback loop](./assets/lesson-07-feedback-loop.png)

이 visual은 제출물에서 빠진 evidence를 찾고, 분류하고, 수정하고, 재확인하는 흐름을 보여준다.

## 핵심 설명
점검은 감점 이벤트가 아니라 제출물을 실행 가능한 상태로 만드는 과정이다. Day 5의 7교시는 학습 정리에서 드러난 evidence gap을 실제 README, Dockerfile, Compose 또는 summary 문장 개선으로 연결한다.

## evidence gap 분류
| 분류 | 예 | 처리 |
|---|---|---|
| Critical | secret 노출, cleanup 위험 | 즉시 수정 |
| High | 실행 명령 누락 | README 또는 summary 보완 |
| Medium | expected output 부족 | evidence 추가 |
| Low | 표현 모호 | 문장 수정 |
| Future | Week 3 주제 | 다음 주 질문으로 이동 |

## quick patch 대상
| 파일/문서 | 수정 예 |
|---|---|
| README | build/run/check/cleanup 보강 |
| Dockerfile | COPY 범위 확인 |
| `.dockerignore` | secret/불필요 파일 제외 |
| compose.yaml | port/env 설명 보완 |
| RCA note | recheck/prevention 추가 |
| learning summary | hands-on 발전 내역, 인사이트, Week3 질문 추가 |

## live Q&A 핵심 질문
| 질문 | 답 방향 |
|---|---|
| container와 VM 차이는? | process isolation vs guest OS |
| EXPOSE와 ports 차이는? | metadata vs host publish |
| image와 container 차이는? | artifact vs running instance |
| tag는 왜 필요한가? | reproducibility와 handoff |
| down -v는 왜 위험한가? | volume data 삭제 |
| secret은 어디에 두는가? | image 밖, 공개 문서 밖 |
| 좋은 인사이트는 무엇인가? | 실행 evidence에서 나온 구조/위험/개선 판단 |

## 실무 insight
현업 review에서 좋은 태도는 방어가 아니라 evidence 업데이트다. "제 PC에서는 됐습니다"보다 "README에 확인 명령과 expected output을 추가하겠습니다"가 더 좋다.

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
형성평가는 점검과 revision action이 연결될 때 효과가 있다. 질문을 들었다는 사실보다, 그 질문이 어떤 문서 수정이나 재확인으로 이어졌는지가 중요하다.

## 오해 점검
| 오해 | 교정 |
|---|---|
| 점검은 점수 확인 시간이다 | 제출물 개선 입력이다 |
| 질문은 모르는 티를 낸다 | 좋은 질문은 risk를 드러낸다 |
| 모든 지적을 길게 반영해야 한다 | severity 기준으로 우선순위화한다 |
| README 수정은 부가 작업이다 | handoff 품질 자체다 |
| 인사이트는 거창해야 한다 | 작은 실패에서 나온 재현성/보안/구조 판단이면 충분하다 |

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 분류 | evidence gap severity를 나눴다 |
| 수정 | 하나 이상 patch action을 기록했다 |
| Q&A | 질문과 답을 문서화했다 |
| 재확인 | 수정 후 check 명령을 적었다 |
| 인사이트 | hands-on 발전 또는 Week3 구조 질문을 구체화했다 |

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
- Gap:
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
| hands-on 발전 내역이 약해요 | 변경한 점, 이유, evidence를 한 줄씩 추가 |

## evidence gap 우선순위 원칙
1. secret/security risk
2. 실행 불가능한 명령
3. 정상 확인 기준 누락
4. cleanup/data risk
5. 인사이트 또는 Week3 질문 부재
6. 표현 개선

## Lesson 7 Exit Ticket
```markdown
## Exit Ticket
- 오늘 찾은 가장 중요한 evidence gap:
- severity:
- 수정한 파일:
- 재확인 명령:
- Week 3로 넘길 질문:
```

## 제출물 점검 마감 기준
점검은 기록만 하고 끝내지 않는다. 최소 하나는 문서나 명령으로 반영한다. 수정할 시간이 부족하면 "수정 예정"이 아니라 owner, 파일, recheck 명령을 남긴다.

마감 확인:
- Critical/High gap이 방치되지 않았는가?
- README 수정 후 명령을 다시 확인했는가?
- Week 3 질문과 Day 5 수정 항목을 구분했는가?
- 제출물에 본인이 실행한 evidence와 본인 판단이 함께 있는가?
