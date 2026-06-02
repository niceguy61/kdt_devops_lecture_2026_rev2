# 1교시: Day1 OT 연결 및 학습 작업공간 준비

## 수업 목표
- Day1 OT에서 정한 개인 목표와 blocker를 실제 작업공간 준비로 연결한다.
- Week 1 산출물이 GitHub, README, command evidence로 누적된다는 점을 이해한다.
- "내 컴퓨터에서 어디에서 무엇을 실행했는가"를 path와 기록으로 설명한다.

## 50분 흐름
| Time | Activity |
|---|---|
| 0-5분 | Day1 목표와 blocker를 다시 읽는다. |
| 5-15분 | 작업공간, repository, evidence의 역할을 설명한다. |
| 15-30분 | 개인 작업 폴더를 만들고 현재 path를 기록한다. |
| 30-40분 | 공개 가능한 정보와 민감정보를 구분한다. |
| 40-50분 | evidence 표를 작성하고 다음 교시 준비 상태를 확인한다. |

## 0-5분 Day1 목표와 blocker를 다시 읽는다.

- 진행: Day1 목표와 blocker를 다시 읽는다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 상세 설명
작업공간은 단순한 폴더가 아니다. 현업에서는 장애나 배포 실패가 발생했을 때 "어떤 directory에서 어떤 command를 실행했는가"가 중요한 재현 조건이 된다. 같은 명령도 다른 path에서 실행하면 다른 파일을 읽거나, 다른 설정을 사용하거나, 아무 파일도 찾지 못할 수 있다.

Day1 OT에서 만든 목표는 추상적인 학습 의미였다. Day2부터는 그 의도를 실제 evidence로 바꾼다. evidence는 스크린샷만 의미하지 않는다. command, path, version, URL, status code, error message처럼 다른 사람이 다시 확인할 수 있는 자료를 말한다.



### Visual 1: 목표를 evidence로 바꾸는 흐름
![작업공간에서 서비스 evidence로 이어지는 흐름](../assets/week1-service-evidence-flow.png)

이 그림은 오늘 만드는 path 기록이 나중에 서비스 상태 evidence로 확장되는 흐름을 보여준다. 여러분은 먼저 "내가 어디에서 실행했는가"를 남기고, 이후 교시에서 command output과 README 기록을 붙여 간다.

```mermaid
flowchart LR
    A[Day1 개인 목표] --> B[작업 폴더 path]
    B --> C[실행 command]
    C --> D[확인 가능한 output]
    D --> E[README evidence]
```

## 5-15분 작업공간, repository, evidence의 역할을 설명한다.

- 진행: 작업공간, repository, evidence의 역할을 설명한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Visual 2: path 캡처 가이드
| 캡처할 장면 | 학생 기록 포인트 |
|---|---|
| 첫 번째 `pwd` 출력 | 수업 시작 위치를 그대로 적는다. |
| `cloud-native-week1` 이동 후 `pwd` | 끝 경로가 새 폴더인지 확인한다. |
| 민감정보 점검 | password, token, 인증코드는 캡처하거나 붙여 넣지 않는다. |

## 15-30분 개인 작업 폴더를 만들고 현재 path를 기록한다.

- 진행: 개인 작업 폴더를 만들고 현재 path를 기록한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Visual 3: 작업공간 판단 카드
| 판단 질문 | strong evidence | weak evidence |
|---|---|---|
| 어디에서 실행했는가? | full path와 command가 함께 있음 | 폴더 이름만 기억함 |
| 무엇을 남겼는가? | output을 README 또는 note에 요약 | 화면을 봤다고만 적음 |
| 공개 가능한가? | secret을 제거한 경로/출력 | token이나 인증코드가 섞인 캡처 |



### 명령 절차
```bash
pwd
mkdir -p cloud-native-week1
cd cloud-native-week1
pwd
```



### 확인 질문
- 현재 작업 폴더의 full path는 무엇인가?
- 오늘 만든 evidence 중 공유 가능한 것과 보호해야 할 것은 무엇인가?
- 다른 사람이 같은 폴더 구조를 만들려면 어떤 명령이 필요한가?

## 30-40분 공개 가능한 정보와 민감정보를 구분한다.

- 진행: 공개 가능한 정보와 민감정보를 구분한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 다음 주차 매핑
컨테이너 실행 환경의 작업 디렉터리, Kubernetes manifest의 mount path, Terraform module path는 모두 "어디에서 실행되는가"라는 질문으로 돌아온다. 오늘 기록한 path evidence가 그 기본 언어다.



### 예상 결과
- 첫 번째 `pwd`는 현재 위치를 보여준다.
- `mkdir -p cloud-native-week1`은 폴더가 없으면 만들고, 이미 있으면 오류 없이 지나간다.
- 두 번째 `pwd`는 끝이 `cloud-native-week1`인 path를 보여야 한다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| 폴더 이름은 아무래도 상관없다. | 이름은 자유지만 수업 evidence에서는 같은 이름을 쓰면 재현성이 좋아진다. |
| 스크린샷만 있으면 충분하다. | command와 output을 함께 기록해야 나중에 검색, 비교, 복구가 쉽다. |
| blocker는 실패 기록이라 감점이다. | blocker는 운영에서 중요한 상태 보고다. 단, 증상과 시도한 확인을 같이 써야 한다. |

## 40-50분 evidence 표를 작성하고 다음 교시 준비 상태를 확인한다.

- 진행: evidence 표를 작성하고 다음 교시 준비 상태를 확인한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 실습 Evidence
| 항목 | 기록 |
|---|---|
| Day1 개인 목표 | |
| 현재 blocker | |
| 작업 폴더 path | |
| 보호해야 할 정보 | password, token, MFA code, verification code |



### 학술 근거와 DevOps insight
ABET식 문제 해결 역량은 문제를 바로 고치는 능력보다 먼저 상황을 정확히 정의하는 능력을 요구한다. DevOps 현업에서도 "안 됩니다"보다 "어느 path에서 어떤 command를 실행했고 어떤 output이 나왔습니다"가 훨씬 좋은 보고다. 이 습관이 incident report, runbook, RCA의 출발점이다.



### 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 50분 참여 | 시간 흐름에 맞춰 설명, 활동, 산출물 작성에 참여했다. |
| 증거 산출 | 수업에서 요구한 note, command, table, blocker 중 해당 산출물을 구체적으로 남겼다. |
| 전이 연결 | 오늘 개념이 Week2~6 기술 또는 자기 산출물과 어떻게 연결되는지 한 문장 이상 설명했다. |



### 공식/학술 근거 링크
- OSTEP: Operating Systems: Three Easy Pieces, https://pages.cs.wisc.edu/~remzi/OSTEP/ - process, memory, filesystem, persistence를 운영체제 abstraction으로 설명하는 기준이다.
- CS:APP, https://csapp.cs.cmu.edu/ - 프로그램 실행과 메모리/스토리지/네트워크가 시스템 기초로 연결되는 근거다.
- MIT Missing Semester, https://missing.csail.mit.edu/ - shell, path, debugging을 실무형 컴퓨팅 문해력으로 다루는 대학 강의다.
