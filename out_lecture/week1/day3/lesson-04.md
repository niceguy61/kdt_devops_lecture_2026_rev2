# 4교시: 재현 가능성 - README, path, expected result, clean directory

## 수업 목표
- 재현 가능한 README의 최소 구조를 작성한다.
- clean directory에서 실행할 때 필요한 정보를 구분한다.
- start/check/stop/troubleshooting을 command와 expected result로 기록한다.

## 50분 흐름
| Time | Activity |
|---|---|
| 0-5분 | service execution contract 확인 |
| 5-15분 | 재현성의 의미와 README 역할 설명 |
| 15-30분 | README 실행 절차 작성 |
| 30-40분 | clean directory 관점으로 빠진 조건 점검 |
| 40-50분 | 실패 분석 RCA로 연결 |

## 0-5분 service execution contract 확인

- 진행: service execution contract 확인

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 상세 설명
재현 가능성은 "내가 다시 실행할 수 있다"보다 넓은 개념이다. 다른 사람이 새 directory에서 repository를 clone한 뒤 같은 명령으로 같은 결과를 얻을 수 있어야 한다. README는 이 과정을 사람이 읽을 수 있는 runbook으로 만든다.

좋은 README는 command만 나열하지 않는다. 어디에서 실행하는지, 어떤 version이 필요한지, 어떤 결과가 나와야 하는지, 실패하면 무엇을 확인해야 하는지까지 포함한다. expected result가 없으면 성공 여부를 판단할 수 없다.



### Visual 1: README runbook 흐름
![README는 실행 Runbook](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day3/assets/lesson-04-readme-runbook.png)

이 이미지는 README를 소개 문서가 아니라 재현 가능한 실행 절차로 읽게 한다. `Requirements`, `Start`, `Check`, `Expected`, `Stop`, `Troubleshooting` 순서가 빠지면 다른 사람이 같은 결과를 재현하기 어렵다.

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day3__lesson-04--diagram-01.png)

README는 설명문이 아니라 짧은 runbook이다. `Check`와 `Expected`가 함께 있어야 성공 여부를 같은 기준으로 판단할 수 있다.

## 5-15분 재현성의 의미와 README 역할 설명

- 진행: 재현성의 의미와 README 역할 설명

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### README 최소 항목
| 섹션 | 작성할 내용 | 예시 |
|---|---|---|
| Requirements | 실행 전 필요한 도구 | Python 3 |
| Start | 서비스를 시작하는 명령 | `python3 -m http.server 8000` |
| Check | 성공 여부를 확인하는 명령 | `curl -I http://localhost:8000` |
| Expected | 기대 결과 | HTTP status 200 |
| Stop | 서비스를 멈추는 방법 | server terminal에서 Ctrl+C |
| Data | 읽는 파일과 위치 | repository root의 `index.html` |
| Troubleshooting | 실패 증상별 첫 확인 | process, port, URL path |



### Visual 2: Clean directory 점검표
| 새로 clone한 사람이 묻는 질문 | README에 있어야 하는 답 |
|---|---|
| 어디에서 명령을 실행하나요? | repository root 또는 상대 path |
| 무엇이 설치되어 있어야 하나요? | Python 3 같은 requirement |
| 어떻게 시작하나요? | start command |
| 성공은 어떻게 확인하나요? | check command와 expected result |
| 어떻게 멈추나요? | stop command |
| 실패하면 무엇부터 보나요? | symptom별 troubleshooting |

개인 컴퓨터의 absolute path를 쓰면 다른 학생이 따라 하기 어렵다. repository 기준 상대 path로 적는 습관을 만든다.

## 15-30분 README 실행 절차 작성

- 진행: README 실행 절차 작성

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### README 최소 구조
| 항목 | 포함 여부 |
|---|---|
| Requirements | |
| Start command | |
| Check command | |
| Expected result | |
| Stop instruction | |
| Troubleshooting | |


### 명령 절차
README 작성 후 새 terminal에서 절차를 다시 따라 한다.

```bash
python3 --version
python3 -m http.server 8000
```

새 terminal:

```bash
curl -I http://localhost:8000
```

## 30-40분 clean directory 관점으로 빠진 조건 점검

- 진행: clean directory 관점으로 빠진 조건 점검

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 확인 질문
- clean directory에서 필요한 첫 명령은 무엇인가?
- README에 stop 절차가 없으면 어떤 운영 문제가 생기는가?
- expected result와 실제 result가 다르면 어떻게 기록해야 하는가?



### 다음 주차 매핑
컨테이너 실행 환경 정의는 README의 start 조건을 표준 실행 절차로 바꾸고, Kubernetes manifest는 실행 상태를 선언한다. Terraform은 환경 자체를 재현 가능한 코드로 만든다.



### 예상 결과
- README만 보고도 start/check/stop을 수행할 수 있어야 한다.
- expected status가 실제 status와 맞아야 한다.
- 실패 시 troubleshooting 표에서 첫 확인 대상을 고를 수 있어야 한다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| README는 설명문이라 명령 검증이 필요 없다. | README의 명령은 실행 절차이므로 검증해야 한다. |
| expected result는 없어도 된다. | expected result가 없으면 성공/실패 판단이 주관적이 된다. |
| 내 컴퓨터 path를 그대로 쓰면 좋다. | 개인 absolute path보다 repository root 기준 상대 경로가 재현성이 높다. |

## 40-50분 실패 분석 RCA로 연결

- 진행: 실패 분석 RCA로 연결

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 실습 Evidence
| Evidence | Value |
|---|---|
| start command | |
| check command | |
| expected status | |
| stop command | |
| known issue | |



### 학술 근거와 DevOps insight
재현성은 실험과 공학 모두의 기본 조건이다. 현업에서는 README, runbook, deployment guide가 같은 역할을 한다. 사람이 실행할 수 없는 README는 자동화로 옮겨도 실패 가능성이 높다.



### 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 50분 참여 | 시간 흐름에 맞춰 설명, 활동, 산출물 작성에 참여했다. |
| 증거 산출 | 수업에서 요구한 note, command, table, blocker 중 해당 산출물을 구체적으로 남겼다. |
| 전이 연결 | 오늘 개념이 Week2~6 기술 또는 자기 산출물과 어떻게 연결되는지 한 문장 이상 설명했다. |



### 공식/학술 근거 링크
- GitHub Docs: About READMEs, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes - README가 실행과 도움 경로를 제공해야 하는 기준이다.
- Pro Git: About Version Control, https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control - 실행 조건 변경을 version control evidence로 남기는 이유다.
- Monash Constructive Alignment, https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/learning-outcomes/how-to/constructive-alignment - 실행 활동과 평가 evidence를 정렬하는 기준이다.
