# 4교시: 미니 앱 완성 실습

## 수업 목표
- Day4 미니 앱의 남은 구현, evidence, 문서 누락을 완성한다.
- 새 기능 추가보다 제출 기준 충족을 우선한다.
- 최종 제출 전 regression check를 수행한다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | 완성 기준 확인 | 새 기능 금지와 evidence 우선 원칙을 확인한다. | 기준 확인 |
| 5-20분 | 앱 수정 | data rendering, error state, CSS 문제를 고친다. | 수정된 앱 |
| 20-30분 | 실행 재검증 | 서버 재시작 후 URL과 status를 확인한다. | 재검증 evidence |
| 30-40분 | README 보완 | handoff와 runbook 누락을 채운다. | README final |
| 40-50분 | 제출 전 freeze | 더 바꾸지 않을 상태를 정한다. | final checklist |

## 0-5분 완성 기준 확인

- 진행: 완성 기준 확인

- 초점: 새 기능 금지와 evidence 우선 원칙을 확인한다.

- 학생 산출: 기준 확인

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 핵심 설명
완성 실습의 원칙은 "기능을 더 넣기 전에 실행을 다시 증명한다"이다. 오늘 추가할 수 있는 것은 작은 UI polish나 문서 보완뿐이며, backend, DB, 유료 API, 인증은 여전히 제외한다.



### 시각 자료 1: 수정 전 우선순위
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day5__lesson-04--diagram-01.png)

## 5-20분 앱 수정

- 진행: 앱 수정

- 초점: data rendering, error state, CSS 문제를 고친다.

- 학생 산출: 수정된 앱

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 시각 자료 2: Fresh Run 캡처 가이드
| 단계 | 봐야 할 화면/기록 | 실패 시 먼저 확인할 것 |
|---|---|---|
| 서버 시작 | 터미널에 서비스 상태가 보임 | 실행 위치와 파일 경로 |
| 브라우저 접속 | expected screen이 보임 | URL, port, index 파일 |
| 데이터 표시 | dummy JSON 값이 렌더링됨 | data path, fetch 경로 |
| README 일치 | 문서의 명령과 실제 실행이 같음 | 오래된 command 또는 port |

## 20-30분 실행 재검증

- 진행: 실행 재검증

- 초점: 서버 재시작 후 URL과 status를 확인한다.

- 학생 산출: 재검증 evidence

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 시각 자료 3: Preview Mapping
![Week1 Docker preview mapping](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-docker-preview-mapping.png)

오늘은 fresh run evidence가 Week2 Docker preview의 입력이 된다는 점을 확인한다. 실제 container 실행은 다음 주차의 단계별 실습에서 다룬다.



### 활동 절차
1. 통합 체크리스트에서 `missing` 항목만 고른다.
2. 실행이 깨진 학생은 구현보다 서버와 경로를 먼저 고친다.
3. 실행이 되는 학생은 error state 또는 README를 보완한다.
4. 서버를 새로 시작해 evidence를 다시 기록한다.
5. 제출 직전 변경 내용을 요약한다.

## 30-40분 README 보완

- 진행: README 보완

- 초점: handoff와 runbook 누락을 채운다.

- 학생 산출: README final

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 40-50분 제출 전 freeze

- 진행: 제출 전 freeze

- 초점: 더 바꾸지 않을 상태를 정한다.

- 학생 산출: final checklist

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 산출물
- final mini app
- final README/runbook
- 재검증 evidence
- final checklist



### 평가 기준
| 기준 | 충족 |
|---|---|
| 앱이 fresh server start 후 실행된다. | |
| data rendering이 확인된다. | |
| README/runbook이 최종 상태와 일치한다. | |
| 새 범위 초과 기능을 추가하지 않았다. | |



### 현업 DevOps insight
마감 직전 가장 위험한 행동은 검증되지 않은 큰 변경이다. 작은 수정 후 실행 증거를 다시 남기는 습관은 배포 전 change discipline의 출발점이다.



### 학술 근거
- Deliberate practice: 명확한 기준에 맞춰 부족한 부분만 반복 개선한다.
- Regression thinking: 수정 후 기존 실행 조건이 유지되는지 확인한다.
- Mastery learning: 제출 최소 기준을 충족한 뒤 확장한다.



### 다음 주차 연결
Week2 Docker 실습에서는 "fresh run"이 더 중요해진다. container는 이전 터미널 상태에 기대지 않고 실행되어야 하기 때문이다.



### 다음 연결
다음 교시는 통합 체크리스트, 평가 증거, 2~6주차 기술 매핑을 완성한다.



### 공식/학술 근거 링크
- Google SRE Book: Postmortem Culture, https://sre.google/sre-book/postmortem-culture/ - 수정 전후 evidence와 timeline을 학습 기록으로 남기는 기준이다.
- CMU Eberly Center: Bloom's Taxonomy, https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html - 보완을 단순 반복이 아니라 적용/분석/평가 단계로 보는 기준이다.
- Monash Constructive Alignment, https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/learning-outcomes/how-to/constructive-alignment - 보완 활동과 평가 evidence를 정렬하는 기준이다.
