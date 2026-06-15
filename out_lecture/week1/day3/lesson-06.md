# 6교시: 관찰 가능성과 배포 미리보기 - logs/상태 코드 확인 기록, build, 산출물, 릴리스, 배포, 되돌리기

## 수업 목표
- log, 상태 코드, metric, trace의 역할을 구분한다.
- 배포 관련 기본 용어를 Week 1 수준으로 구분한다.
- 변경 전달에는 확인 기록이 필요하다는 점을 이해한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 기록 |
|---|---|---|---|
| 관찰 가능성 | 시스템 내부 상태를 외부 기록으로 추론하는 능력이다. | 화면만 보고 정상/비정상을 단정한다. | 상태 코드와 로그 비교 |
| Log/상태 코드/Metric/Trace | 관찰 신호마다 답하는 질문이 다르다. | 로그 하나만 있으면 충분하다고 오해한다. | 신호별 예시 표 |
| Build/산출물/릴리스/배포 | 변경이 전달되는 단계를 구분한다. | 만든 것, 배포한 것, 사용 가능한 변경을 섞는다. | 용어 매핑 표 |
| 되돌리기 | 사용자 영향을 줄이기 위해 이전 상태로 되돌리는 전략이다. | 실패 후 원인을 모른 채 계속 수정한다. | 이전 정상 파일/상태 기록 |

### 챌린저 복구 기준
- 오늘은 실제 배포를 하지 않는다. 로컬 상태 코드와 로그로 배포 전후 비교 사고만 연습한다.
- `산출물`은 지금 수준에서는 전달 가능한 `index.html`과 README 절차라고 보면 된다.
- 되돌리기는 실패가 아니라 사용자 영향을 줄이는 운영 선택지다.

## 50분 흐름
| Time | Activity |
|---|---|
| 0-5분 | RCA record 확인 |
| 5-15분 | 관찰 가능성 signal과 Deployment 용어 설명 |
| 15-30분 | local server log/상태 코드 확인 기록 수집 |
| 30-40분 | 산출물/릴리스/배포/되돌리기 미리보기 |
| 40-50분 | AI 검증 원칙으로 연결 |

## 0-5분 RCA record 확인

- 진행: RCA record 확인

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 상세 설명
관찰 가능성은 시스템 내부 상태를 외부 확인 기록으로 추론할 수 있게 하는 능력이다. Week 1에서는 전문 도구를 쓰지 않고 log와 HTTP 상태 코드만 사용한다. log는 사건 기록이고, 상태 코드는 요청 결과를 분류하는 신호다. metric은 수치화된 상태, trace는 요청이 여러 구성요소를 지나가는 경로를 뜻하지만 오늘은 개념 preview로만 다룬다.

배포 용어도 미리 구분한다. Build는 실행 가능한 산출물을 준비하는 과정, 산출물은 전달 가능한 결과물, 릴리스는 사용자에게 의미 있는 변경 묶음, 배포는 실행 환경에 반영하는 행위, 되돌리기는 이전 상태로 되돌리는 조치다. 오늘은 배포하지 않고, 이 용어가 local 확인 기록과 어떻게 연결되는지만 본다.



### Visual 1: 관찰 가능성 확인 기록 흐름
![서비스 확인 기록 흐름](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png)

오늘의 관찰 가능성은 전문 도구가 아니라 `curl` 상태 코드와 서버 로그에서 시작한다. 같은 요청에 대해 "사용자가 본 결과"와 "서버가 남긴 기록"을 나란히 남기는 것이 핵심이다.

## 5-15분 관찰 가능성 signal과 Deployment 용어 설명

- 진행: 관찰 가능성 signal과 Deployment 용어 설명

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Visual 2: 배포 미리보기 단어 지도
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/lecture_mermaid_assets/week1__day3__lesson-06--diagram-01.png)

Day3에서는 실제 배포를 하지 않는다. 다만 local 확인 기록을 통해 나중에 배포 전후에 무엇을 비교해야 하는지 미리 익힌다.

## 15-30분 local server log/상태 코드 확인 기록 수집

- 진행: local server log/상태 코드 확인 기록 수집

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 관찰 signal
| Signal | Week 1 level | Later week |
|---|---|---|
| Log | request/error text | Docker/K8s/CloudWatch logs |
| 상태 코드 | HTTP 200/404/500 | health check/readiness |
| Metric | count/latency concept | CloudWatch/Prometheus |
| Trace | request 경로 concept | distributed tracing |



### 배포 미리보기 용어
| Term | Week 1 meaning |
|---|---|
| Build | 실행 가능한 산출물을 준비 |
| 산출물 | 전달 가능한 결과물 |
| 릴리스 | 사용 가능한 변경 묶음 |
| 배포 | 실행 환경에 반영 |
| 되돌리기 | 이전 상태로 되돌림 |

## 30-40분 산출물/릴리스/배포/되돌리기 미리보기

- 진행: 산출물/릴리스/배포/되돌리기 미리보기

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 명령 절차
```bash
curl -I http://localhost:8000
curl -I http://localhost:8000/no-such-file.html
```

서버 terminal에서 두 요청의 log를 비교한다.



### 확인 질문
- 오늘의 산출물은 무엇이라고 볼 수 있는가?
- 200과 404를 metric으로 바꾼다면 무엇을 셀 수 있는가?
- 되돌리기 판단에는 어떤 확인 기록이 필요할까?



### 예상 결과
- 정상 URL은 200 계열 상태 코드를 보여야 한다.
- 없는 URL은 404 상태 코드를 보여야 한다.
- 서버 로그는 두 요청 경로와 상태 코드 차이를 보여준다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| log가 있으면 관찰 가능성이 완성된다. | 필요한 질문에 답할 수 있는 log/상태 코드/metric/trace가 있어야 한다. |
| 배포는 build와 같은 말이다. | build는 산출물 준비, 배포는 실행 환경 반영이다. |
| 되돌리기는 실패 인정이라 나쁘다. | 되돌리기는 사용자 영향을 줄이는 정상 운영 전략이다. |

## 40-50분 AI 검증 원칙으로 연결

- 진행: AI 검증 원칙으로 연결

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 다음 주차 매핑
Docker image는 산출물이 되고, Kubernetes rollout은 배포/되돌리기를 제공한다. AWS CloudWatch는 log/metric을 모으고, Terraform은 배포 대상 infrastructure 변경을 plan/apply 확인 기록으로 남긴다.



### 실습 확인 기록
| 확인 항목 | 값 |
|---|---|
| successful 상태 코드 | |
| failed 상태 코드 | |
| log comparison | |
| 산출물 후보 | `index.html` and README instructions |
| 되돌리기 idea | previous known-good file/content |



### 학술 근거와 DevOps insight
Google SRE는 monitoring을 symptoms와 causes를 구분해 보는 활동으로 설명한다. DevOps 현업에서는 배포 전후 상태 코드와 log 확인 기록이 없으면 변경이 좋아졌는지 나빠졌는지 판단할 수 없다. 오늘의 단순 log 비교는 배포 관찰의 최소 형태다.



### 평가 기준
| 기준 | 2점 확인 기록 |
|---|---|
| 50분 참여 | 시간 흐름에 맞춰 설명, 활동, 산출물 작성에 참여했다. |
| 증거 산출 | 수업에서 요구한 note, command, table, blocker 중 해당 산출물을 구체적으로 남겼다. |
| 전이 연결 | 오늘 개념이 Week2~5 기술 또는 자기 산출물과 어떻게 연결되는지 한 문장 이상 설명했다. |



### 공식/학술 근거 링크
- Google Cloud DevOps guidance, https://docs.cloud.google.com/architecture/devops - 전달 확인 기록과 operational performance를 연결하는 기준이다.
- Google SRE Book: Introduction, https://sre.google/sre-book/introduction/ - monitoring과 change management가 운영 readiness에 포함되는 근거다.
- Pro Git: About Version Control, https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control - 배포 전후 변경 이력과 증거를 남기는 이유다.
