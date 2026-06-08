# 6교시: 운영 위험 분류와 README/runbook 기초

## 수업 목표
- 미니 앱의 비용, 보안, 재현성 위험을 분류한다.
- README와 runbook의 차이를 설명한다.
- 장애나 인수인계 상황에서 필요한 운영 정보를 작성한다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-10분 | 위험 유형 소개 | 위험을 겁주는 말이 아니라 판단 기준으로 설명한다. | risk type 이해 |
| 10-25분 | 개인 앱 위험 찾기 | 앱별 비용/보안/재현성 위험을 질문한다. | risk table |
| 25-35분 | README/runbook 구분 | start/check와 troubleshoot를 분리한다. | 문서 구조 |
| 35-45분 | runbook 작성 | 흔한 실패 3개와 확인 절차를 직접 적는다. | runbook 초안 |
| 45-50분 | 제출 전 점검 | evidence 누락을 표시한다. | 보완 목록 |

## 0-10분 위험 유형 소개

- 초점: 위험을 겁주는 말이 아니라 판단 기준으로 설명한다.

- 학생 산출: risk type 이해


### 핵심 설명
README는 새 환경에서 실행하는 사람을 위한 문서이고, runbook은 문제가 생겼을 때 확인할 절차다. Week1에서는 둘을 한 파일에 작성해도 되지만, 목적은 구분해야 한다.


### Visual 1: 구조 다이어그램
![위험 분류와 Runbook 대응](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-06-risk-runbook.png)

이 이미지는 위험을 막연한 불안이 아니라 비용, 보안, 재현성, 운영 범주로 분류하게 한다. 각 범주는 README나 runbook에 남길 대응 행동과 evidence로 이어져야 한다.

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day4__lesson-06--diagram-01.png)

## 10-25분 개인 앱 위험 찾기

- 초점: 앱별 비용/보안/재현성 위험을 질문한다.

- 학생 산출: risk table


### Visual 2: README/runbook 질문 카드
| 문서 영역 | 답해야 하는 질문 | 대표 evidence |
|---|---|---|
| README Start | 새 환경에서 실행하려면 무엇을 입력하는가? | command, working directory |
| README Check | 정상 실행은 어떻게 확인하는가? | URL, HTTP status, browser result |
| Runbook Symptom | 어떤 증상이 보이는가? | page not open, data missing |
| Runbook Fix | 어떤 순서로 복구하는가? | check command, path, port, JSON |

## 25-35분 README/runbook 구분

- 초점: start/check와 troubleshoot를 분리한다.

- 학생 산출: 문서 구조


### Visual 3: 위험 분류
| Risk Type | Week1 예시 | 대응 |
|---|---|---|
| Cost | 유료 API 호출, 클라우드 리소스 사용 | dummy JSON 사용, 로컬 실행 |
| Security | API key 노출, 개인정보 샘플 데이터 | secret 금지, 가짜 데이터 사용 |
| Reproducibility | 경로 누락, port 미기록, 브라우저만 확인 | command/URL/status 기록 |
| Operational | port 충돌, JSON 오류, 파일명 불일치 | troubleshoot 절차 작성 |


### 활동 절차
1. 자신의 앱에서 외부 의존성이 있는지 표시한다.
2. secret, 개인정보, 비용 발생 가능성을 찾아 제거한다.
3. 실행 재현성을 깨는 요소를 찾는다.
4. README에 정상 실행 절차를 쓴다.
5. runbook에 실패 증상, 확인 명령, 해결 방법을 쓴다.


### Runbook 템플릿

## 35-45분 runbook 작성

- 초점: 흔한 실패 3개와 확인 절차를 직접 적는다.

- 학생 산출: runbook 초안


### Runbook
#### Symptom: page does not open
- Check: server terminal is still running.
- Check: URL and port match the start command.
- Fix: restart the server or choose another port.

#### Symptom: data does not appear
- Check: data.json is in the same directory as index.html.
- Check: browser console for fetch or JSON errors.
- Fix: correct the path or JSON syntax.


### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 45-50분 제출 전 점검

- 초점: evidence 누락을 표시한다.

- 학생 산출: 보완 목록


### 산출물
- risk classification table
- README/runbook 초안
- 보완해야 할 evidence 목록


### 평가 기준
| 기준 | 충족 |
|---|---|
| 비용/보안/재현성 위험이 각각 1개 이상 검토되었다. | |
| 위험마다 대응이 있다. | |
| README와 runbook 목적이 구분된다. | |
| 흔한 장애 증상과 확인 절차가 있다. | |


### 현업 DevOps insight
현업의 운영 품질은 거창한 도구보다 "누가 봐도 같은 판단을 할 수 있는 기록"에서 시작한다. DORA와 Well-Architected는 나중에 더 체계적으로 다루지만, Week1에서는 변경 증거, 재현성, 위험 인식이라는 실무 습관만 사용한다.


### 학술 근거
- Metacognition: 학생이 자신의 산출물 위험을 스스로 점검한다.
- Authentic assessment: 실제 인수인계와 장애 대응에 가까운 문서를 평가한다.
- NIST NICE-style task: 민감정보와 접근 위험을 식별하고 줄인다.


### 다음 주차 연결
Week2 컨테이너 실행에서는 port mapping, image tag, container logs가 runbook 항목으로 추가된다. 오늘의 위험 분류가 그 틀이 된다.


### 다음 연결
다음 7~8교시는 새 진도를 나가지 않고 개인 면담과 보충 실습으로 blocker를 해결한다.


### 공식/학술 근거 링크
- Google SRE Book: Postmortem Culture, https://sre.google/sre-book/postmortem-culture/ - runbook과 incident note를 학습 가능한 운영 기록으로 다루는 근거다.
- GitHub Docs: About READMEs, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes - README가 실행, 도움 경로, maintainer 정보를 제공해야 하는 기준이다.
- OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html - runbook과 README에서 보호할 정보를 분리하는 기준이다.
