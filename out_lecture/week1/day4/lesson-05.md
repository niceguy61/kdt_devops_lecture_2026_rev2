# 5교시: 실행 증거 작성 - command, port, URL, curl/browser evidence

## 수업 목표
- 실행 명령, 작업 경로, port, URL, HTTP status를 증거로 남긴다.
- browser 확인과 `curl` 확인의 차이를 설명한다.
- README에 재현 가능한 실행 절차를 작성한다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | 실행 증거 기준 소개 | "봤다"와 "재현 가능하다"를 구분한다. | evidence 기준 |
| 5-15분 | 서버 실행 | 경로와 port 충돌을 점검한다. | 실행 command |
| 15-25분 | curl 확인 | HTTP status와 header를 읽게 한다. | curl 결과 |
| 25-35분 | browser 확인 | 화면과 console을 확인한다. | browser evidence |
| 35-50분 | README 작성 | start/check/stop/troubleshoot를 채운다. | README 초안 |

## 0-5분 실행 증거 기준 소개

- 초점: "봤다"와 "재현 가능하다"를 구분한다.

- 학생 산출: evidence 기준


### 핵심 설명
실행 증거는 스크린샷 하나가 아니라 다른 사람이 같은 결과를 재현할 수 있게 하는 기록이다. 최소 증거는 command, working directory, port, URL, expected result, observed result다.


### Visual 1: 구조 다이어그램
![Week1 service evidence flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png)

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day4__lesson-05--diagram-01.png)

## 5-15분 서버 실행

- 초점: 경로와 port 충돌을 점검한다.

- 학생 산출: 실행 command


### README 섹션 예시


### Start
Run from the mini-app directory:

python3 -m http.server 8000


### Check
Open http://localhost:8000 and confirm the item list appears.
Run curl -I http://localhost:8000 and confirm HTTP 200.


### Stop
Press Ctrl+C in the server terminal.


### Troubleshoot
- Port already in use: use another port and update the URL.
- Data does not load: check data.json path and JSON syntax.


### Visual 2: 실행 증거 quartet
| 캡처 항목 | 기록 예시 | 빠지면 생기는 문제 |
|---|---|---|
| command/path | `python3 -m http.server 8000` in `mini-app` | 재현 시작점이 불명확하다. |
| port/URL | `8000`, `http://localhost:8000` | 다른 주소를 확인할 수 있다. |
| HTTP/browser | `HTTP 200`, item list visible | 실행 여부가 주장으로만 남는다. |
| stop/troubleshoot | `Ctrl+C`, port conflict note | 다음 실행자가 막혔을 때 복구하기 어렵다. |

## 15-25분 curl 확인

- 초점: HTTP status와 header를 읽게 한다.

- 학생 산출: curl 결과


### Visual 3: README evidence table
| README section | 반드시 들어갈 값 |
|---|---|
| Start | working directory와 command |
| Check | URL, HTTP status, browser result |
| Stop | 종료 방법 |
| Troubleshoot | port/path/data 실패 대응 |


### 활동 절차
1. `mini-app` 폴더에서 정적 서버를 실행한다.
2. `curl -I http://localhost:8000`로 status를 확인한다.
3. browser에서 앱 화면과 data rendering을 확인한다.
4. 서버 중지 방법을 기록한다.
5. port 충돌, 파일 경로 오류, JSON syntax error의 해결 방법을 README에 적는다.


### 실행 증거 표
| Evidence | Value |
|---|---|
| working directory | |
| start command | `python3 -m http.server 8000` |
| port | `8000` |
| URL | `http://localhost:8000` |
| HTTP status | |
| browser result | |
| console result | |
| stop method | `Ctrl+C` |

## 25-35분 browser 확인

- 초점: 화면과 console을 확인한다.

- 학생 산출: browser evidence


### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 35-50분 README 작성

- 초점: start/check/stop/troubleshoot를 채운다.

- 학생 산출: README 초안


### 산출물
- README start/check/stop/troubleshoot
- execution evidence table
- curl 또는 browser 확인 결과


### 평가 기준
| 기준 | 충족 |
|---|---|
| 다른 학생이 README만 보고 실행할 수 있다. | |
| command, path, port, URL이 모두 있다. | |
| HTTP status 또는 browser evidence가 있다. | |
| 중지와 문제 해결 절차가 있다. | |


### 현업 DevOps insight
운영 문서는 장애가 난 뒤에 쓰면 늦다. 앱 실행 시점부터 실행 계약을 기록해야 다음 사람이 환경 차이를 빠르게 찾을 수 있다.


### 학술 근거
- Reproducible learning: 같은 절차로 같은 결과를 얻는 기록을 평가한다.
- Evidence-centered design: 학습 여부를 관찰 가능한 산출물로 판단한다.
- Professional communication: 명령과 결과를 모호하지 않게 전달한다.


### 다음 주차 연결
Week2 Docker에서는 start command가 container 실행 절차로 바뀐다. 오늘 만든 README 구조는 그대로 container 실행 runbook으로 확장된다.


### 다음 연결
다음 교시는 운영 위험 분류와 README/runbook을 완성한다.


### 공식/학술 근거 링크
- MDN HTTP Overview, https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview - browser와 HTTP 확인을 서비스 evidence로 연결하는 기준이다.
- RFC 9110: HTTP Semantics, https://datatracker.ietf.org/doc/html/rfc9110 - HTTP status와 resource 확인의 공식 기준이다.
- Google SRE Book: Introduction, https://sre.google/sre-book/introduction/ - 정상 확인과 관찰 가능성을 운영 readiness로 보는 근거다.
