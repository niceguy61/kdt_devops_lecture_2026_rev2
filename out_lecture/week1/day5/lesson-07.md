# 7교시: 발표 피드백 및 live Q&A

## 수업 목표
- 발표 중 드러난 공통 누락을 즉시 보완한다.
- 학생 질문을 실행, 문서, 위험, 다음 주차 연결로 분류한다.
- Week1 제출 전 마지막 수정 우선순위를 정한다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-10분 | 발표 피드백 요약 | 공통 누락을 3~5개로 묶는다. | issue list |
| 10-25분 | live Q&A | 질문을 유형별로 분류한다. | answer notes |
| 25-40분 | 즉시 보완 | README, risk, evidence를 수정한다. | patched package |
| 40-47분 | 재확인 | 수정 후 실행 또는 문서 확인을 한다. | recheck note |
| 47-50분 | Docker preview 연결 | 다음 교시 질문을 정리한다. | Docker question |

## 0-10분 발표 피드백 요약

- 진행: 발표 피드백 요약

- 초점: 공통 누락을 3~5개로 묶는다.

- 학생 산출: issue list

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 핵심 설명
Q&A는 새 강의가 아니라 제출물 품질을 높이는 피드백 시간이다. 질문은 가능한 한 README 또는 evidence 개선으로 연결한다.



### 시각 자료 1: 질문에서 수정까지
![질문, 수정, 재확인 흐름](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day5/assets/lesson-07-feedback-recheck.png)

이 이미지는 질문을 많이 받기 위한 장치가 아니라 들어온 질문을 개념, 실행, 문서 문제로 분류하고 수정 후 재확인 evidence를 남기는 절차다. 발표 후 변경 사항은 반드시 recheck note로 닫는다.

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day5__lesson-07--diagram-01.png)

## 10-25분 live Q&A

- 진행: live Q&A

- 초점: 질문을 유형별로 분류한다.

- 학생 산출: answer notes

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 시각 자료 2: Q&A 보드
| 질문 유형 | board에 적을 형식 | 즉시 보완 위치 |
|---|---|---|
| Execution | 실행 위치 또는 port가 모호함 | README start |
| Verification | 정상 기준이 보이지 않음 | evidence table |
| Risk | secret, API, 비용 질문 | risk note |
| Scope | backend/auth/DB 추가 요구 | known gaps |
| Next week | Docker로 무엇이 바뀌는가 | readiness question |

## 25-40분 즉시 보완

- 진행: 즉시 보완

- 초점: README, risk, evidence를 수정한다.

- 학생 산출: patched package

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 시각 자료 3: 수정 후 Recheck Capture
| 수정한 항목 | 다시 확인할 증거 | 기록 문장 |
|---|---|---|
| README command | 실제 실행 절차와 일치 | `README start updated and rechecked` |
| Evidence table | status 또는 화면 기준 있음 | `verification evidence added` |
| Risk note | 위험과 제외가 분리됨 | `scope gap documented` |
| Docker question | Week2 preview로 연결됨 | `question saved for Week2` |



### 질문 분류
| Type | 예시 | 연결 산출물 |
|---|---|---|
| Execution | 어디서 명령을 실행하나요? | README start |
| Verification | 정상인지 어떻게 확인하나요? | evidence table |
| Risk | API key를 써도 되나요? | risk/exclusion note |
| Scope | 로그인 기능을 넣어도 되나요? | known gaps |
| Next week | Docker가 왜 필요한가요? | Docker readiness note |



### 활동 절차
1. 발표에서 반복된 문제를 칠판 또는 공유 문서에 모은다.
2. 각 질문을 유형으로 분류한다.
3. 학생은 자기 README에서 같은 문제가 있는지 찾는다.
4. 수정 후 짧은 recheck note를 남긴다.
5. Docker preview에서 다룰 질문을 1개 적는다.

## 40-47분 재확인

- 진행: 재확인

- 초점: 수정 후 실행 또는 문서 확인을 한다.

- 학생 산출: recheck note

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 47-50분 Docker preview 연결

- 진행: Docker preview 연결

- 초점: 다음 교시 질문을 정리한다.

- 학생 산출: Docker question

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 산출물
- feedback issue list
- Q&A answer notes
- 수정된 README 또는 risk note
- Docker preview question



### 평가 기준
| 기준 | 충족 |
|---|---|
| 질문이 산출물 개선으로 이어졌다. | |
| 수정 후 recheck evidence가 있다. | |
| 공통 누락을 개인 제출물에 반영했다. | |
| Docker preview 질문이 준비되었다. | |



### 현업 DevOps insight
리뷰의 가치는 지적 자체가 아니라 수정된 artifact에 있다. 질문을 문서, 증거, 위험 표로 되돌려 놓으면 다음 사람이 같은 질문을 반복하지 않는다.



### 학술 근거
- Feedback loop: 피드백을 받은 뒤 즉시 산출물을 수정한다.
- Collaborative learning: 공통 질문을 공유해 개인별 누락을 줄인다.
- Assessment for learning: 평가는 제출 전 개선을 돕는 과정이다.



### 다음 주차 연결
학생 질문 중 "왜 Docker가 필요한가"는 다음 교시 preview와 Week2 시작 질문으로 이어진다.



### 다음 연결
다음 교시는 2주차 Docker preview를 통해 Week1 앱을 container 관점으로 바라본다.



### 공식/학술 근거 링크
- Monash Constructive Alignment, https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/learning-outcomes/how-to/constructive-alignment - feedback을 목표, 활동, 평가 evidence와 맞추는 기준이다.
- Google SRE Book: Postmortem Culture, https://sre.google/sre-book/postmortem-culture/ - feedback을 개인 비판이 아니라 개선 가능한 artifact로 바꾸는 기준이다.
- CMU Eberly Center: Bloom's Taxonomy, https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html - feedback을 이해/적용/평가 수준으로 구분하는 근거다.
