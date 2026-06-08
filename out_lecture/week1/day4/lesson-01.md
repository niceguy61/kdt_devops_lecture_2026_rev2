# 1교시: 미니 앱 요구사항과 범위 경계

## 수업 목표
- 1주차 안에서 완성 가능한 미니 앱의 포함/제외 범위를 정한다.
- backend, database, paid API, authentication을 제외하는 이유를 운영 관점으로 설명한다.
- 기능 욕심을 줄이고 실행 가능한 artifact 중심으로 요구사항을 쓴다.

## 50분 운영
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | Day4 목표 소개 | 완성 기준을 "작게 실행 가능"으로 고정한다. | 목표 확인 |
| 5-15분 | 포함/제외 예시 분석 | 범위 초과 사례를 잘라낸다. | include/exclude 표 |
| 15-30분 | 개인 앱 아이디어 작성 | 기능을 1개 사용자 흐름으로 축소한다. | one-flow 요구사항 |
| 30-40분 | 위험 관점 점검 | 비용/보안/재현성 질문을 던진다. | 제외 사유 |
| 40-50분 | 짝 검토 | 서로 실행 가능성을 검토한다. | 수정된 scope note |

## 0-5분 Day4 목표 소개

- 초점: 완성 기준을 "작게 실행 가능"으로 고정한다.

- 학생 산출: 목표 확인


### 핵심 설명
Day4의 미니 앱은 제품 완성이 아니라 "실행 가능한 작은 서비스"를 만드는 훈련이다. 앱은 HTML/CSS/JS, dummy JSON, 로컬 정적 서버, README 실행 증거만 포함한다. 서버, 데이터베이스, 유료 API, 로그인은 Week1 범위 밖이다. 제외 이유는 학생 역량 부족이 아니라 재현성, 비용, 보안, 디버깅 범위를 통제하기 위해서다.


### Visual 1: 구조 다이어그램
![Week1 computing spine](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-computing-spine.png)

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day4__lesson-01--diagram-01.png)

## 5-15분 포함/제외 예시 분석

- 초점: 범위 초과 사례를 잘라낸다.

- 학생 산출: include/exclude 표


### Scope Rule
| Include | Exclude | 제외 이유 |
|---|---|---|
| HTML/CSS/JS | backend server | 실행 경로가 늘어나면 실패 원인 분리가 어려워진다. |
| dummy JSON | database | Week1 평가는 persistence가 아니라 data rendering이다. |
| local static server | paid API | 비용과 key 관리 위험을 만들지 않는다. |
| README evidence | authentication | secret, session, 권한 모델은 Week1 이후에 다룬다. |


### Mini App Scope
- App name:
- User flow:
- Included files:
- Excluded features:
- Exclusion reasons:


### Visual 2: scope 결정 보드
| 결정 지점 | 남기는 것 | 잘라내는 것 |
|---|---|---|
| 사용자 흐름 | 한 가지 동작 | 여러 화면과 역할 |
| 데이터 | dummy JSON | DB, 외부 API |
| 실행 | local static server | 배포, 인증, 결제 |
| 증거 | command/path/status | "화면을 봤다"만 적는 기록 |

## 15-30분 개인 앱 아이디어 작성

- 초점: 기능을 1개 사용자 흐름으로 축소한다.

- 학생 산출: one-flow 요구사항


### Visual 3: 앱 범위 위험 삼각형
| 위험 | Week1에서 낮추는 방법 | 확인 증거 |
|---|---|---|
| 비용 | 로컬 실행과 dummy data | paid API 없음 |
| 보안 | secret 없는 샘플 데이터 | 가짜 데이터 |
| 재현성 | command/path/status 기록 | README evidence |


### 활동 절차
1. 앱 이름을 한 문장으로 쓴다.
2. 사용자가 하는 일을 하나의 동사로 제한한다. 예: 목록 보기, 항목 필터링, 상태 표시.
3. 필요한 파일을 `index.html`, `styles.css`, `app.js`, `data.json`, `README.md`로 제한한다.
4. 제외할 기능을 최소 3개 적고 제외 이유를 운영 위험과 연결한다.
5. 짝에게 "50분 안에 skeleton을 만들 수 있는가"를 기준으로 검토받는다.

## 30-40분 위험 관점 점검

- 초점: 비용/보안/재현성 질문을 던진다.

- 학생 산출: 제외 사유


### 흔한 오해
| 오해 | 교정 |
|---|---|
| 산출물이 있으면 evidence는 나중에 채워도 된다. | evidence는 산출물의 일부다. command, path, status, log, note가 함께 있어야 평가 가능하다. |
| Week1에서 모든 기술을 깊게 익혀야 한다. | Week1은 컴퓨팅 spine과 운영 증거를 만드는 주차이며, 깊은 hands-on은 각 기술 주차에서 진행한다. |
| 막힌 내용을 숨기는 것이 좋다. | blocker를 증상, 시도한 일, 다음 조치로 기록하는 것이 현업식 진행 관리다. |

## 40-50분 짝 검토

- 초점: 서로 실행 가능성을 검토한다.

- 학생 산출: 수정된 scope note


### 산출물
아래 양식 또는 표를 사용해 이 시간 블록의 산출물을 작성한다.

### 평가 기준
| 기준 | 충족 |
|---|---|
| 사용자 흐름이 1개로 제한되어 있다. | |
| 제외 기능과 이유가 명확하다. | |
| 유료 API, DB, 로그인, backend가 포함되지 않았다. | |
| 다음 교시에 파일 구조를 만들 수 있다. | |


### 현업 DevOps insight
작은 범위는 속도만을 위한 선택이 아니다. 운영팀은 실행 경로가 짧을수록 장애 원인, 비용 위험, 보안 노출을 빠르게 판단한다. Week1에서는 DORA나 Well-Architected를 별도 이론 수업으로 다루지 않고, "변경을 작게 만들고 증거를 남긴다"는 현업 습관으로만 연결한다.


### 학술 근거
- Bloom taxonomy의 create/evaluate 단계: 학생은 앱 범위를 만들고 운영 기준으로 평가한다.
- CS2023 software development practice: 요구사항을 제한 조건과 산출물로 변환한다.
- 인지부하 이론: backend와 인증을 제거해 초보자가 관찰해야 할 변수를 줄인다.


### 다음 주차 연결
Week2 Docker에서는 같은 미니 앱을 컨테이너로 감싼다. 오늘 정한 실행 범위가 명확해야 실행 환경 정의가 "무엇을 실행해야 하는지"를 설명할 수 있다.


### 다음 연결
다음 교시는 scope note를 실제 파일 tree와 skeleton으로 바꾼다.


### 공식/학술 근거 링크
- Pro Git: About Version Control, https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control - 변경 이력과 협업 증거가 필요한 이유다.
- GitHub Docs: About READMEs, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes - repository가 실행과 도움 경로를 설명해야 하는 기준이다.
- Google Cloud DevOps guidance, https://docs.cloud.google.com/architecture/devops - 작은 변경과 evidence가 delivery/operations 성과로 이어지는 근거다.
