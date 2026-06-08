# 3교시: 현업 DevOps handoff

## 수업 목표
- 다음 작업자가 실행, 확인, 위험 판단을 할 수 있는 handoff package를 만든다.
- 코드, 문서, 증거, 위험, 미해결 항목을 한 묶음으로 전달한다.
- 좋은 handoff와 나쁜 handoff의 차이를 설명한다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-10분 | handoff 예시 비교 | 모호한 문서와 실행 가능한 문서를 비교한다. | 차이점 메모 |
| 10-25분 | package 작성 | README에 필요한 섹션을 채우게 한다. | handoff draft |
| 25-35분 | 위험/제외 항목 정리 | "안 한 것"을 정리한다. | known gaps |
| 35-45분 | 교차 검토 | 짝이 handoff만 보고 실행 가능성을 판단한다. | peer feedback |
| 45-50분 | 수정 | 누락된 command/evidence를 보완한다. | final handoff |

## 0-10분 handoff 예시 비교

- 진행: handoff 예시 비교

- 초점: 모호한 문서와 실행 가능한 문서를 비교한다.

- 학생 산출: 차이점 메모

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 핵심 설명
Handoff는 "제가 만들었습니다"가 아니라 "당신이 이어서 할 수 있습니다"라는 문서다. 현업에서는 사람이 바뀌거나 시간이 지나도 실행 조건과 위험을 알 수 있어야 한다.



### 시각 자료 1: Handoff Evidence Flow
![Week1 service evidence flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png)

handoff 문서는 실행 증거, 확인 증거, 위험 증거를 한 묶음으로 전달하는 화면이다.

## 10-25분 package 작성

- 진행: package 작성

- 초점: README에 필요한 섹션을 채우게 한다.

- 학생 산출: handoff draft

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Handoff Package 구성
| Section | 내용 |
|---|---|
| Summary | 앱 목적과 사용자 흐름 1개 |
| How to run | path, command, port, URL |
| How to verify | expected screen, curl status, console check |
| Known risks | cost/security/reproducibility |
| Known gaps | 아직 못 한 것, 의도적으로 제외한 것 |
| Next step | Week2 Docker로 옮길 항목 |



### 시각 자료 2: 다음 작업자 관점
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day5__lesson-03--diagram-01.png)

## 25-35분 위험/제외 항목 정리

- 진행: 위험/제외 항목 정리

- 초점: "안 한 것"을 정리한다.

- 학생 산출: known gaps

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 시각 자료 3: Handoff 품질 비교
| 나쁜 handoff | 좋은 handoff |
|---|---|
| "서버 실행하면 됩니다." | path, command, port, URL이 있다. |
| "정상 작동합니다." | 정상 화면, HTTP 확인, 데이터 표시 기준이 있다. |
| "아직 미완성입니다." | known gaps와 의도적 제외가 분리되어 있다. |
| "다음에 Docker 합니다." | Week2로 옮길 app folder와 run step이 지정되어 있다. |



### 활동 절차
1. 앱 summary를 3문장 이하로 쓴다.
2. 실행 명령과 확인 절차를 순서대로 쓴다.
3. known risks와 known gaps를 분리한다.
4. Day4에서 제외한 backend, DB, API, auth를 다시 명시한다.
5. 짝이 README만 읽고 질문 없이 실행 가능한지 확인한다.

## 35-45분 교차 검토

- 진행: 교차 검토

- 초점: 짝이 handoff만 보고 실행 가능성을 판단한다.

- 학생 산출: peer feedback

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 45-50분 수정

- 진행: 수정

- 초점: 누락된 command/evidence를 보완한다.

- 학생 산출: final handoff

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 산출물
- handoff package section
- peer feedback note
- 수정된 README



### 평가 기준
| 기준 | 충족 |
|---|---|
| handoff에 실행 경로와 확인 경로가 모두 있다. | |
| known risks와 known gaps가 구분된다. | |
| 범위 밖 기능을 다시 추가하지 않았다. | |
| 짝 검토 후 모호한 표현을 수정했다. | |



### 현업 DevOps insight
좋은 handoff는 다음 사람의 질문 수를 줄인다. 운영 인수인계에서 "어디서 실행하나요", "정상인지 어떻게 아나요", "무엇이 위험한가요"가 바로 답해야 할 핵심 질문이다.



### 학술 근거
- Authentic workplace writing: 실제 팀 인수인계 문서 형식으로 작성한다.
- Peer review: 독자가 직접 문서 품질을 검증한다.
- ABET communication outcome: 기술 내용을 이해 가능한 문서로 전달한다.



### 다음 주차 연결
Week2에서는 handoff의 `How to run`이 Docker build/run 절차로 확장된다. 오늘의 문서가 Docker runbook의 초안이 된다.



### 다음 연결
다음 교시는 미니 앱 완성 실습으로 남은 구현과 문서 누락을 닫는다.



### 공식/학술 근거 링크
- RFC 9110: HTTP Semantics, https://datatracker.ietf.org/doc/html/rfc9110 - 실행 확인에서 status code와 resource를 evidence로 쓰는 기준이다.
- MDN HTTP Overview, https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview - browser 확인과 request/response 흐름을 연결하는 기준이다.
- Google SRE Book: Introduction, https://sre.google/sre-book/introduction/ - 상태 확인, monitoring, emergency response가 운영 readiness에 포함되는 근거다.
