# 3교시: 서비스 실행 조건 - source, runtime, command, port, data, dependency

## 수업 목표
- 서비스 실행에 필요한 조건을 6개 항목으로 분류한다.
- 실행 조건 누락이 Docker/Kubernetes/AWS에서 더 큰 장애가 되는 이유를 설명한다.
- local static server를 service execution contract로 기록한다.

## 50분 흐름
| Time | Activity |
|---|---|
| 0-5분 | log/config/secret evidence 확인 |
| 5-15분 | 실행 조건 6가지 정의 |
| 15-30분 | local server contract 작성 |
| 30-40분 | 누락 조건별 실패 증상 정리 |
| 40-50분 | README 재현성 구조로 연결 |

## 0-5분 log/config/secret evidence 확인

- 진행: log/config/secret evidence 확인

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 상세 설명
서비스가 실행되려면 코드만 있으면 되는 것이 아니다. source가 어디 있는지, 어떤 runtime이 필요한지, 어떤 command로 시작하는지, 어느 port에서 응답하는지, 어떤 data file이 필요한지, 외부 dependency가 있는지 알아야 한다. 이 6가지가 빠지면 다른 사람이 같은 결과를 만들 수 없다.

오늘의 정적 서버는 단순하지만 실행 조건을 모두 가진다. source는 `index.html`, runtime은 Python 3, command는 `python3 -m http.server 8000`, port는 8000, data는 현재 directory의 정적 파일, dependency는 외부 서비스 없음이다.



### Visual 1: 실행 조건이 Docker로 이어지는 위치
![Docker preview mapping](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-docker-preview-mapping.png)

이 그림은 구현을 시작하자는 뜻이 아니다. 오늘은 local 실행 조건을 먼저 말로 고정하고, 다음 주 Docker에서 같은 조건이 image, command, port publish로 바뀐다는 연결만 확인한다.

## 5-15분 실행 조건 6가지 정의

- 진행: 실행 조건 6가지 정의

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Visual 2: Service execution contract
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day3__lesson-03--diagram-01.png)

화살표 하나가 끊기면 실행 조건이 빠진 것이다. 특히 "dependency 없음"도 기록해야 나중에 외부 API나 데이터베이스가 생겼을 때 차이를 볼 수 있다.

## 15-30분 local server contract 작성

- 진행: local server contract 작성

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 실행 조건 표
| Condition | 질문 | Evidence |
|---|---|---|
| Source | 코드는 어디에 있는가? | repo/path |
| Runtime | 무엇으로 실행하는가? | `python3 --version` |
| Command | 어떻게 시작하는가? | command |
| Port | 어디로 접속하는가? | URL/status |
| Data | 어떤 파일/데이터가 필요한가? | `index.html` path |
| Dependency | 외부 의존성이 있는가? | dependency note |



### 명령 절차
```bash
pwd
python3 --version
ls -la index.html
curl -I http://localhost:8000
```

## 30-40분 누락 조건별 실패 증상 정리

- 진행: 누락 조건별 실패 증상 정리

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 실패 증상 매핑
| 누락 조건 | 흔한 증상 | 확인 |
|---|---|---|
| Source 없음 | 404 또는 directory listing | `ls`, URL path |
| Runtime 없음 | command not found | `python3 --version` |
| Command 틀림 | server 미실행 | terminal output |
| Port 충돌 | address already in use | server error |
| Data 누락 | expected content 없음 | `cat index.html` |
| Dependency 누락 | external call 실패 | dependency note |



### 확인 질문
- local static server의 runtime은 무엇인가?
- port가 빠진 README는 어떤 문제를 만들 수 있는가?
- dependency가 없다는 것도 왜 기록해야 하는가?



### 예상 결과
- `python3 --version`은 Python 3 version을 출력한다.
- `ls -la index.html`은 파일 권한과 크기를 보여준다.
- `curl -I`은 server가 실행 중이면 status를 보여주고, 실행 중이 아니면 connection 실패를 보여준다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| 실행 조건은 복잡한 앱에서만 필요하다. | 정적 서버도 source, runtime, command, port, data, dependency를 모두 가진다. |
| dependency가 없으면 표에서 빼도 된다. | "외부 dependency 없음"도 중요한 재현 조건이다. |
| port만 맞으면 서비스가 정상이다. | port 응답, file content, log, expected status를 함께 확인해야 한다. |

## 40-50분 README 재현성 구조로 연결

- 진행: README 재현성 구조로 연결

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 다음 주차 매핑
컨테이너 실행 환경 정의는 source/runtime/command를 표준 실행 단위로 묶고, Kubernetes manifest는 port와 runtime 상태를 선언한다. AWS와 Terraform은 dependency와 실행 환경을 더 큰 범위에서 관리한다.



### 실습 Evidence
| Condition | Value |
|---|---|
| Source | |
| Runtime | |
| Command | |
| Port | |
| Data | |
| Dependency | |



### 학술 근거와 DevOps insight
재현 가능한 시스템은 실행 조건이 명시되어 있어야 한다. DevOps 현업에서 컨테이너 실행 환경 정의와 Kubernetes manifest는 이 조건을 기계가 읽을 수 있는 형태로 바꾼 것이다. 사람이 먼저 조건을 정리하지 못하면 자동화도 불안정해진다.



### 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 50분 참여 | 시간 흐름에 맞춰 설명, 활동, 산출물 작성에 참여했다. |
| 증거 산출 | 수업에서 요구한 note, command, table, blocker 중 해당 산출물을 구체적으로 남겼다. |
| 전이 연결 | 오늘 개념이 Week2~6 기술 또는 자기 산출물과 어떻게 연결되는지 한 문장 이상 설명했다. |



### 공식/학술 근거 링크
- CS:APP, https://csapp.cs.cmu.edu/ - 프로그램 실행, 메모리, 네트워크가 systems 기초로 연결되는 근거다.
- OSTEP: Operating Systems: Three Easy Pieces, https://pages.cs.wisc.edu/~remzi/OSTEP/ - process와 filesystem을 실행 evidence로 관찰하는 기준이다.
- MDN HTTP Overview, https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview - local service 응답을 HTTP evidence로 설명하는 기준이다.
