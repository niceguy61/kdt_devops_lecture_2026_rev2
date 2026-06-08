# 2세션: 6주 커리큘럼 로드맵 - Week 1 spine과 Week 2~6 기술 연결

## 수업 목표
- 6주 과정의 큰 흐름을 컴퓨팅 기본기에서 Cloud Native 운영까지 연결해 설명한다.
- Week 1의 process, file, port, log, README가 Week 2~6의 Docker, MSA, Kubernetes, AWS, Terraform으로 확장되는 방식을 분석한다.
- 학생이 각 주차의 기대 요소와 불안 요소를 기록하고, 자기 학습 전략으로 전환한다.

## 시간
14:00~15:00

## 오늘의 초점
- 6주 과정을 하나의 운영 문제 해결 흐름으로 이해한다.
- Week 1에서 배울 process, file, port, config, log, README가 이후 기술의 공통 언어가 됨을 확인한다.
- 학생별 기대와 불안을 학습 전략으로 정리한다.

## 50~60분 학습 흐름
| 시간 | 활동 | 내가 확인할 것 |
|---|---|---|
| 14:00~14:05 | 점심 이후 재집중, 오전 산출물 연결 | OT 기록이 로드맵 이해의 출발점임을 상기한다. |
| 14:05~14:15 | 6주 전체 그림 제시 | 각 기술이 따로 떨어진 과목이 아니라 운영 문제의 확장임을 보여준다. |
| 14:15~14:27 | Week 1 spine 설명 | process, file, port, config, log, README를 기준축으로 잡는다. |
| 14:27~14:40 | Week 2~6 기술 연결 | Docker/MSA/Kubernetes/AWS/Terraform을 "무엇을 표준화하는가"로 설명한다. |
| 14:40~14:48 | 기대/불안 매핑 활동 | 학생별 위험을 조기에 드러내고 대응 계획으로 바꾼다. |
| 14:48~14:50 | 현업 지표와 연결 | 운영 준비도와 재현성의 의미를 초급 수준으로 연결한다. |
| 14:50~15:00 | 휴식 및 다음 세션 전환 | 50분 수업 후 AI agent 마인드셋 세션으로 전환한다. |

## 14:00~14:05 점심 이후 재집중, 오전 산출물 연결

- 진행: 점심 이후 재집중, 오전 산출물 연결

- 초점: OT 기록이 로드맵 이해의 출발점임을 상기한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 공식 참고
- CNCF Cloud Native Definition: https://github.com/cncf/toc/blob/main/DEFINITION.md
- AWS: What is DevOps? https://aws.amazon.com/devops/what-is-devops/



### Visual 1: 6주 학습 로드맵
![Cloud Native 6-week roadmap](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day1/assets/lesson-02-roadmap.png)

이 이미지는 6주 과정의 큰 방향을 기억하기 위한 개념도다. 제품 로고나 세부 기능을 외우는 용도가 아니라, 각 주차가 어떤 운영 문제를 해결하는지 보는 자료다.

## 14:05~14:15 6주 전체 그림 제시

- 진행: 6주 전체 그림 제시

- 초점: 각 기술이 따로 떨어진 과목이 아니라 운영 문제의 확장임을 보여준다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 핵심 설명
> "Cloud Native를 Kubernetes부터 시작하면 초급자는 외워야 할 단어만 늘어납니다. 우리는 먼저 작은 서비스가 어떻게 실행되고, 어떤 파일을 읽고, 어떤 port를 열고, 어떤 log를 남기는지 봅니다. 그 다음 같은 질문을 container, cluster, cloud, IaC로 확장합니다."

> "Docker는 마법이 아니라 실행 조건을 포장하는 도구입니다. Kubernetes는 container를 많이 실행할 때 desired state와 복구를 관리하는 도구입니다. AWS는 compute, storage, network, identity를 서비스로 빌려 쓰는 환경입니다. Terraform은 그 인프라 선택을 코드와 state로 남기는 방식입니다."

> "현업에서는 '배웠다'보다 '다른 사람이 재현할 수 있다'가 중요합니다. 이 과정의 로드맵도 재현성, 관찰 가능성, 인수인계 가능성을 계속 반복하도록 설계되어 있습니다."



### 6주 로드맵
| Week | Focus | Week 1 spine 연결 | 학생이 답해야 할 질문 |
|---|---|---|---|
| 1 | 컴퓨팅 펀더멘털과 운영 증거 | process, file, port, log, README | 이 서비스는 어디서 실행되고 무엇으로 정상 판단하는가? |
| 2 | Docker | process와 filesystem을 image/container로 표준화 | 같은 앱을 다른 환경에서 어떻게 재현할 것인가? |
| 3 | MSA | 여러 process/service의 network와 data boundary | 서비스 사이 책임과 통신 실패를 어떻게 설명할 것인가? |
| 4 | Kubernetes | container lifecycle, service discovery, desired state | 원하는 상태와 실제 상태가 다를 때 무엇을 볼 것인가? |
| 5 | AWS | compute, storage, network, identity, observability를 cloud service로 확장 | 비용, 권한, 보안, 가용성을 어떻게 관리할 것인가? |
| 6 | Terraform/IaC | infrastructure를 code와 state로 관리 | 인프라 변경을 어떻게 재현하고 검토할 것인가? |



### Week 1 spine 설명
| Component | 초급 정의 | 이후 확장 |
|---|---|---|
| Process | 실행 중인 프로그램 | container, pod, service lifecycle |
| File/System | 코드, 설정, 의존성이 놓이는 위치 | image layer, volume, object storage |
| Port/Network | 서비스가 요청을 받는 입구 | service discovery, ingress, load balancer |
| Configuration | 실행 환경을 바꾸는 값 | env var, secret, config map, IaC variable |
| Observability | 정상/비정상을 판단하는 증거 | log, metric, trace, alert, dashboard |
| Handoff | 다른 사람이 이어받을 수 있는 문서 | README, runbook, PR, postmortem |



### Visual 2: Week 1 spine에서 이후 기술로 확장
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/out_lecture/mermaid-assets/week1__day1__lesson-02--diagram-01.png)

읽는 순서: Week 1의 기초 개념이 오른쪽 기술로 이름을 바꾸어 확장된다. 다음 주차의 기술을 예고하되, 오늘은 공통 spine을 잡는 데 집중한다.

## 14:15~14:27 Week 1 spine 설명

- 진행: Week 1 spine 설명

- 초점: process, file, port, config, log, README를 기준축으로 잡는다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### Visual 3: 기대/불안 매핑 보드
| Week | 기대 | 불안 | 대응 전략 |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

이 표는 토론보다 개인 정리에 가깝다. 각 칸은 길게 쓰지 않고 단어 또는 짧은 문장으로 채운다.

## 14:27~14:40 Week 2~6 기술 연결

- 진행: Week 2~6 기술 연결

- 초점: Docker/MSA/Kubernetes/AWS/Terraform을 "무엇을 표준화하는가"로 설명한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 활동: 기대/불안 매핑
1. 학생은 6주 표를 보고 각 Week마다 `기대 1개`와 `불안 1개`를 적는다.
2. 불안 요소를 `개념`, `실습`, `환경`, `영어 문서`, `협업`, `평가` 중 하나로 분류한다.
3. 가장 큰 불안 1개를 고르고, 필요한 도움을 한 문장으로 쓴다.
4. 2~3명이 공유하되, 계정/개인정보/민감한 일정은 공개하지 않는다.

## 14:40~14:48 기대/불안 매핑 활동

- 진행: 기대/불안 매핑 활동

- 초점: 학생별 위험을 조기에 드러내고 대응 계획으로 바꾼다.

- 완료 조건: 이 시간 블록의 결과를 evidence note에 남긴다.

## 14:48~14:50 현업 지표와 연결

- 진행: 현업 지표와 연결

- 초점: 운영 준비도와 재현성의 의미를 초급 수준으로 연결한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 오해 점검
| 오해 | 바로잡기 |
|---|---|
| Kubernetes를 빨리 배우면 Cloud Native를 이해한 것이다. | 실행, 네트워크, 설정, 관찰 가능성의 기초 없이는 cluster 문제를 해석하기 어렵다. |
| Docker는 앱을 자동으로 좋은 서비스로 만든다. | Docker는 실행 조건을 표준화하지만 보안, 비용, 장애 대응은 별도 설계가 필요하다. |
| AWS는 클릭해서 만들면 끝이다. | 권한, 비용, region, network, cleanup, 문서화가 운영 품질을 좌우한다. |
| Terraform은 인프라를 만드는 명령어다. | Terraform은 변경 의도와 state를 관리하는 방식까지 포함한다. |

## 14:50~15:00 휴식 및 다음 세션 전환

- 진행: 휴식 및 다음 세션 전환

- 초점: 50분 수업 후 AI agent 마인드셋 세션으로 전환한다.

- 완료 조건: 아래 자료를 사용해 이 시간 블록의 산출물을 만든다.



### 안내 프롬프트
- 공개 질문: "6주 과정에서 가장 먼저 안정화해야 할 내 학습 위험은 무엇인가?"
- 개인 작성: 기대 1개, 불안 1개, 약한 spine component 1개를 적는다.



### 산출물
- 6주 기대/불안 note
- Week 1 spine에서 본인이 약하다고 느끼는 component 1개
- 가장 큰 학습 위험 1개와 필요한 도움 1문장



### 학술/현업 근거
- CNCF Cloud Native Definition은 resilient, manageable, observable system을 강조한다. 따라서 Day 1부터 관찰 가능성과 관리 가능성을 학습 언어로 둔다.
- AWS DevOps 설명은 문화, 자동화, 통합, 측정의 결합을 강조한다. 이 로드맵은 도구보다 운영 문제를 먼저 확인한다.
- Google Cloud DevOps guidance는 delivery와 operational performance를 개선하는 역량을 강조한다. 초급 과정에서는 이를 "증거를 남기고 빠르게 복구하는 습관"으로 낮춰 적용한다.
- Bloom analyze/evaluate 수준: 학생은 단순 암기가 아니라 주차별 기술이 해결하는 문제를 분류하고 자기 위험을 평가한다.



### AI coding agent 시대 인사이트
- agent는 컨테이너 실행 환경 정의, Kubernetes manifest, Terraform 초안을 생성할 수 있지만, 어떤 운영 문제를 해결하려는지 모르면 그럴듯한 파일만 만든다.
- 사람은 "이 앱의 실행 조건은 무엇인가", "정상 상태 증거는 무엇인가", "비용과 권한 위험은 무엇인가"를 agent에게 요구해야 한다.
- 6주 로드맵은 agent가 만든 결과물을 검토하는 기준을 단계적으로 쌓는 과정이다.



### 세션 체크리스트
- [ ] 학생이 Week 1 spine과 Week 2~6 기술의 연결을 말할 수 있다.
- [ ] 학생이 기대/불안을 최소 1개씩 작성했다.
 - [ ] 학생이 약한 spine component와 대응 전략을 적었다.



### 다음 연결
다음 세션은 AI coding agent 시대의 Cloud Native/DevOps 학습 마인드셋을 다룬다.



### 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 50분 참여 | 시간 흐름에 맞춰 설명, 활동, 산출물 작성에 참여했다. |
| 증거 산출 | 수업에서 요구한 note, command, table, blocker 중 해당 산출물을 구체적으로 남겼다. |
| 전이 연결 | 오늘 개념이 Week2~6 기술 또는 자기 산출물과 어떻게 연결되는지 한 문장 이상 설명했다. |
