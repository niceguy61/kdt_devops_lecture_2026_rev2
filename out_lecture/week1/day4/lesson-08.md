# 8교시: 개인 면담 및 보충 실습

## 수업 목표
- Day4 필수 산출물을 제출 가능한 상태로 마감한다.
- 미해결 blocker를 줄이고 다음 주차 전 보완 계획을 남긴다.
- 개인별 수준 차이를 고려해 최소 제출 기준과 확장 과제를 분리한다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | Day4 제출 기준 재확인 | 최소 제출 기준을 다시 말한다. | 체크리스트 |
| 5-30분 | 집중 보충 실습 | blocker 우선순위가 높은 항목부터 수정한다. | 수정된 앱/문서 |
| 30-40분 | 짝 실행 테스트 | README만 보고 서로 실행한다. | peer test note |
| 40-47분 | 제출 패키지 정리 | 파일 누락과 evidence 누락을 확인한다. | Day4 package |
| 47-50분 | Day5 연결 | 통합과 handoff로 이어지는 이월 메모를 작성한다. | 이월 메모 |

## 0-5분 Day4 제출 기준 재확인

- 초점: 최소 제출 기준을 다시 말한다.

- 학생 산출: 체크리스트


### 핵심 설명
8교시는 7교시에 이어 개인 면담과 보충 실습으로 운영한다. 새 강의 주제보다 Day4 산출물 회복과 제출 준비에 집중한다. 각자는 "필수 제출", "가능하면 보완", "다음 주차로 이월"을 구분한다.


### Visual 1: 구조 다이어그램
![Week1 service evidence flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png)

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day4__lesson-08--diagram-01.png)

## 5-30분 집중 보충 실습

- 초점: blocker 우선순위가 높은 항목부터 수정한다.

- 학생 산출: 수정된 앱/문서


### Visual 2: 마감 판단 표
| 마감 판단 | 기준 | 새 진도 여부 |
|---|---|---|
| 필수 제출 | 실행, data rendering, evidence, risk, README/runbook | 새 진도 아님 |
| 가능하면 보완 | 문서 표현 정리, 캡처 누락 보완 | 새 진도 아님 |
| 다음 주차 이월 | 오늘 해결 못 한 blocker와 다음 행동 | 새 진도 아님 |

## 30-40분 짝 실행 테스트

- 초점: README만 보고 서로 실행한다.

- 학생 산출: peer test note


### Visual 3: Day4 제출 패키지
| Package item | 최소 기준 |
|---|---|
| app | 정적 서버에서 열림 |
| data | 화면에 dummy JSON 표시 |
| evidence | command/path/port/status |
| handoff | blocker와 다음 행동 |


### 필수 제출 기준
| Artifact | Minimum |
|---|---|
| mini app | 정적 서버에서 열리는 `index.html` |
| data | 화면에 표시되는 dummy JSON |
| evidence | command, path, port, URL, 확인 결과 |
| risk | 비용/보안/재현성 위험 분류 |
| README/runbook | start/check/stop/troubleshoot |
| interview note | blocker와 다음 행동 |


### 보충 실습 절차
1. 필수 제출 기준에서 비어 있는 항목을 표시한다.
2. 가장 먼저 실행 실패를 해결한다.
3. 다음으로 data rendering을 확인한다.
4. 마지막으로 README/runbook과 risk table을 채운다.
5. 짝이 README만 보고 실행해 보고 누락을 적는다.

## 40-47분 제출 패키지 정리

- 초점: 파일 누락과 evidence 누락을 확인한다.

- 학생 산출: Day4 package


### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 47-50분 Day5 연결

- 초점: 통합과 handoff로 이어지는 이월 메모를 작성한다.

- 학생 산출: 이월 메모


### 산출물
- Day4 제출 패키지
- peer test note
- 남은 위험 또는 다음 행동 메모


### 평가 기준
| 기준 | 충족 |
|---|---|
| 앱이 정적 서버로 실행된다. | |
| README만 보고 시작/확인/중지할 수 있다. | |
| 위험 분류가 앱 범위와 연결된다. | |
| 개인 blocker와 보완 계획이 남아 있다. | |


### 현업 DevOps insight
완성은 기능 수가 아니라 handoff 가능성으로 판단한다. 동료가 README만 보고 실행할 수 있다면 작은 서비스라도 운영 가능한 산출물에 가까워진다.


### 학술 근거
- Peer instruction: 짝 실행 테스트가 문서의 모호함을 드러낸다.
- Mastery threshold: 다음 단계로 넘어가기 전 최소 역량 기준을 확인한다.
- Evidence-centered assessment: 제출물과 실행 증거가 평가의 중심이다.


### 다음 주차 연결
Week2 Docker preview에서 Day4 앱을 컨테이너로 실행한다. Day4 산출물이 불안정하면 container 문제가 아니라 기존 실행 계약 문제가 된다.


### 다음 연결
Day5는 Day1~4 산출물을 통합하고, spine 최종 매핑과 handoff package를 완성한다.


### 공식/학술 근거 링크
- CMU Eberly Center: Bloom's Taxonomy, https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html - 보강 활동을 이해, 적용, 분석 수준으로 구분하는 기준이다.
- MIT Missing Semester, https://missing.csail.mit.edu/ - shell/Git/debugging 보강이 기술 주차의 선행 역량인 근거다.
- Google SRE Book: Introduction, https://sre.google/sre-book/introduction/ - 운영자는 장애 대응과 change management를 학습 증거로 남겨야 한다는 기준이다.
