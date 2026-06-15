# 7교시: AI Coding Tool 사용 원칙 - 공식 문서 확인, 실행 검증, 비밀값/cost/API 위험

## 수업 목표
- AI 답변을 실행 증거와 공식 문서로 검증한다.
- 비밀값, paid API, external 외부 의존성 위험을 식별한다.
- Day3 8교시 챌린지로 넘길 수 있는 작은 정적 웹사이트 제안과 제외해야 할 위험한 제안을 구분한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 기록 |
|---|---|---|---|
| AI 답변은 후보 | 실행 책임과 운영 책임은 사람에게 남는다. | 틀린 명령이나 위험한 제안을 그대로 실행한다. | 채택/수정/보류 기록 |
| 범위 통제 | Day3는 정적 파일, 로컬 실행, 검증에 집중한다. | backend/API/cloud까지 커져 재현성이 무너진다. | 제외 항목 표 |
| 공식 문서와 실행 검증 | 최신 명령과 실제 결과를 확인해야 한다. | 설명은 그럴듯하지만 실행되지 않는다. | 공식 URL, command/상태 코드 |
| 보안/비용/API 위험 | 비밀값과 유료 리소스는 작은 실습에서도 사고가 된다. | token 노출, 비용 발생, 계정 권한 문제가 생긴다. | 비밀값/cost/API yes/no |

### 챌린저 복구 기준
- AI가 큰 앱을 제안하면 먼저 파일 수, 외부 의존성, 비용, 인증을 줄인다.
- 오늘 받아들일 수 있는 제안은 8교시 챌린지로 넘길 수 있는 작은 정적 웹사이트 수준이다.
- 실행하지 않은 내용은 확인 기록으로 쓰지 말고, 보류 사유로 따로 남긴다.

## 50분 흐름
| Time | Activity |
|---|---|
| 0-5분 | 관찰 가능성 확인 기록 확인 |
| 5-15분 | AI Coding Tool의 장점과 검증 필요성 설명 |
| 15-30분 | AI 답변 위험 체크 표 작성 |
| 30-40분 | 공식 문서/실행 결과와 비교 |
| 40-50분 | spine mapping으로 연결 |

## 0-5분 관찰 가능성 확인 기록 확인

- 진행: 관찰 가능성 확인 기록 확인

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 상세 설명
AI Coding Tool은 빠른 초안과 설명을 제공할 수 있지만, 실행 조건을 빠뜨리거나, 최신 문서와 다른 명령을 제안하거나, 비밀값을 코드에 넣거나, 유료 API를 사용하게 만들 수 있다. 따라서 AI 답변은 "후보"일 뿐이고, 공식 문서와 실행 확인 기록으로 검증해야 한다.

Day3의 중요한 판단 기준은 scope control이다. AI가 "작은 앱을 만들어보자"고 제안하더라도 backend, database, paid API, authentication, cloud 배포까지 확장하지 않는다. 8교시 챌린지로 넘길 수 있는 것은 HTML/CSS/JS만 쓰는 작은 정적 웹사이트 초안이며, 제안에서 source, 실행 환경, command, 포트, data, 외부 의존성, 비밀값, cost, 관찰 가능성 항목이 빠졌는지 검토한다.



### Visual 1: AI 답변 검증 흐름
![AI 제안 위험 체크](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day3/assets/lesson-07-ai-risk-check.png)

이 이미지는 AI 제안이 공식 문서, 보안, 비용, 재현성 검토를 통과해야 실행 후보가 된다는 기준을 만든다. Day3 범위를 넘는 제안은 실행하지 않고 확인 기록과 보류 사유만 남긴다.

![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/lecture_mermaid_assets/week1__day3__lesson-07--diagram-01.png)

AI 답변은 후보일 뿐이다. 오늘 받아들일 수 있는 것은 Day3 범위 안에서 실행 확인 기록과 안전 기준을 통과한 부분이다.

## 5-15분 AI Coding Tool의 장점과 검증 필요성 설명

- 진행: AI Coding Tool의 장점과 검증 필요성 설명

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Visual 2: 제안 문장 위험 표시표
| 제안에 보이는 말 | 표시할 위험 | Day3 결정 |
|---|---|---|
| "API key를 넣고" | 비밀값 노출 | 제외 |
| "바로 배포" | 비용/계정/권한 | 보류 |
| "작은 정적 웹사이트" | 범위 관리 필요 | 8교시 챌린지 후보 |
| "backend/API 연동 앱 구현" | 범위 초과 | Day4 이후 또는 제외 |
| "공식 문서 없이" | 검증 부족 | 문서 확인 전 보류 |
| "curl로 확인" | 실행 확인 기록 가능 | 범위 안에서 사용 |

거절은 학습 실패가 아니다. 오늘 범위를 지키는 것은 나중에 구현을 안정적으로 시작하기 위한 준비다.

## 15-30분 AI 답변 위험 체크 표 작성

- 진행: AI 답변 위험 체크 표 작성

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 검증표
| Check | 확인 기록 |
|---|---|
| 공식 문서와 충돌하지 않는가 | URL |
| 실행했는가 | command/상태 코드 |
| 비밀값을 요구하는가 | yes/no |
| 비용이 생기는가 | yes/no |
| 외부 API/외부 의존성이 생기는가 | yes/no |
| Week 1 Day3 범위를 넘는가 | excluded note |
| log/상태 코드 확인 방법이 있는가 | 확인 기록 |



### 활동 절차
AI에게 받은 답변이나 가상의 제안을 다음 기준으로 평가한다.

"작은 웹앱을 만들고 API key를 넣어 배포해보세요."

검토:
- 앱 구현 시작: 8교시 챌린지 범위를 넘는지 확인 필요
- API key: 비밀값 위험
- 배포: 비용/계정/권한 위험
- 실행 조건: command, 포트, 외부 의존성 확인 필요
- 공식 문서: 사용 도구별 공식 문서 확인 필요

## 30-40분 공식 문서/실행 결과와 비교

- 진행: 공식 문서/실행 결과와 비교

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 확인 질문
- AI 답변에서 오늘 실행으로 검증한 부분은 무엇인가?
- 비밀값/cost/API 위험이 있는 부분은 무엇인가?
- Day3 범위를 넘는 작업을 어떻게 기록하고 보류할 것인가?



### 다음 주차 매핑
컨테이너 실행 환경 정의 제안, Kubernetes YAML 제안, cloud resource 제안, Terraform 코드 제안에도 같은 검증표를 적용한다. 특히 cloud credential과 비용 발생 resource는 AI가 제안해도 즉시 실행하지 않는다.



### 예상 결과
- 범위 안의 정적 웹사이트 제안은 "8교시 챌린지 후보"로, 범위를 넘는 구현 제안은 "Day4 이후 보류"로 기록한다.
- 비밀값이나 유료 API가 필요한 제안은 오늘 실습에서 제외한다.
- 실행한 명령만 확인 기록으로 남긴다.



### 흔한 오해
| 오해 | 교정 |
|---|---|
| AI가 만든 코드는 바로 쓰면 된다. | 실행, 공식 문서, 보안, 비용 검증 후 사용한다. |
| 작은 API key는 README에 넣어도 된다. | 모든 credential은 비밀값으로 다룬다. |
| 범위를 넘는 제안은 더 좋은 학습이다. | 기초 실행 조건을 고정하기 전 구현을 늘리면 재현성이 무너진다. |

## 40-50분 spine mapping으로 연결

- 진행: spine mapping으로 연결

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 실습 확인 기록
| 확인 항목 | 값 |
|---|---|
| AI suggestion summary | |
| official doc checked | |
| command verified | |
| 비밀값 risk | yes/no |
| cost/API risk | yes/no |
| scope decision | accept/reject/defer |



### 학술 근거와 현업 DevOps insight
AI 보조 개발 환경에서는 human-in-the-loop 검증이 필수다. 운영 책임은 도구가 아니라 배포하고 운영하는 팀에 남는다. DevOps 관점에서 AI 답변은 runbook, security review, cost review, 관찰 가능성 checklist를 통과해야 실제 변경 후보가 된다.



### 평가 기준
| 기준 | 2점 확인 기록 |
|---|---|
| 50분 참여 | 시간 흐름에 맞춰 설명, 활동, 산출물 작성에 참여했다. |
| 증거 산출 | 수업에서 요구한 note, command, table, blocker 중 해당 산출물을 구체적으로 남겼다. |
| 전이 연결 | 오늘 개념이 Week2~5 기술 또는 자기 산출물과 어떻게 연결되는지 한 문장 이상 설명했다. |



### 공식/학술 근거 링크
- NIST AI Risk Management Framework, https://www.nist.gov/itl/ai-risk-management-framework - AI agent 사용을 risk management 관점으로 검증하는 기준이다.
- OpenAI: Running Codex Safely, https://openai.com/index/running-codex-safely/ - coding agent의 access, approval, governance 통제가 필요한 이유다.
- CMU Eberly Center: Bloom's Taxonomy, https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html - AI가 만든 답을 이해, 적용, 평가 수준으로 구분하는 기준이다.
