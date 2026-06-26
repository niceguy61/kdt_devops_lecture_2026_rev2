# 개요

- 주차 : 5주
- 일별 수업 시간 : 일 8시간, 50분 수업 10분 휴식, 매 정시 시작
- 1주차 1일차 과정별 OT는 운영 확정 일정에 따라 2026-06-10(수) 12:00~18:00, 점심시간 13:00~14:00, 총 5시간으로 진행한다.
- 수업 범위 : Devops, Cloud(AWS), Docker, Kubernetes, MSA, IaC, Observability, Kubernetes Known plugins
- 과목 명 : Cloud Native
- 대상자 : 전공 막학기 학생, 비전공 취업준비생, 전직 개발자 (클라우드 직군 이직 희망자)

## 5주 운영 구조
| 주차 | 핵심 주제 | 주차 학습 결과 |
|---|---|---|
| 1주차 | 컴퓨팅 펀더멘털, DevOps 마인드셋, 로컬 서비스 실행 | 미니 웹앱, README/runbook, RCA, 컴퓨팅 spine 매핑 |
| 2주차 | Docker, 이미지/컨테이너, Dockerfile, Compose | Dockerfile, compose.yaml, 이미지 실행 흐름, 컨테이너 장애 분석 |
| 3주차 | MSA 2일, GitHub/GitHub Actions 1일, Kubernetes 진입 2일 | MSA 장애 리포트, branch/merge/rebase/revert/tag 압축 실습, CI gate, Pod/Deployment/Service 첫 배포 |
| 4주차 | Kubernetes 운영 5일 | Helm 기반 add-on 설치, Ingress, metrics-server, Prometheus/Grafana, RBAC, Kyverno, Argo CD, Istio/Kiali preview |
| 5주차 | AWS 마무리 3일, Terraform/IaC 2일 | AWS 운영 runbook, 비용/관찰 흐름, Terraform 코드/plan/destroy 흐름 |

## 일차 운영 리듬
| 일차 | 공통 흐름 |
|---|---|
| 1일차 | 전주 핵심 10분 요약, 주차 핵심 개념, 환경 점검 |
| 2일차 | 전날 강의 10분 요약, 핵심 구성요소 실습 1 |
| 3일차 | 전날 강의 10분 요약, 핵심 구성요소 실습 2, 연결/관찰/장애 분석 |
| 4일차 | 운영 관점 확장, 장애 주입, 회사/현업 사례, 보충 실습 |
| 5일차 | 통합 실습, 다음 단계 연결, 배움일기 숙제 |

## 공통 수업 규칙
- 1교시는 전날 강의의 핵심을 약 10분 요약한 뒤 당일 주제로 들어간다. 주차가 바뀌는 날은 전주 핵심을 10분 요약한다.
- 1~7교시는 강의와 실습 내용만 둔다. 별도 산출 요구는 8교시 구름 EXP 배움일기에만 둔다.
- 8교시는 구름 EXP 배움일기를 안내한다. 당일 공부한 내용을 간단한 메모 형태로 남겨도 되고, 블로그 형태로 정리해도 좋다.
- 구름 EXP 배움일기에는 그날 이해한 개념, 막힌 지점, 다시 해볼 실습, 다음 수업 전 질문을 남긴다.
- 수업 계획에는 학습 내용과 배움일기 안내만 둔다.
- 강의 자료에서 같은 핵심 포인트, 주의사항, cleanup 원칙, 운영 해석을 교시마다 반복하지 않는다. 공통 원칙은 README나 hands-on lab 앞부분에 한 번만 두고, 각 lesson에는 그 교시 고유의 판단 기준과 위험만 남긴다.
- "핵심 포인트"와 "주의할 점"은 분량 채우기용 문단이 아니다. 이전 교시와 의미가 같은 문장은 삭제하고, 실제 시나리오 판단에 필요한 새 정보만 남긴다.
- 수업은 도구 나열보다 시나리오 해결 중심으로 구성한다. 학생이 "명령을 배웠다"가 아니라 "사건을 증거로 분석하고 복구했다"라고 느끼도록 범위와 실습 밀도를 높인다.
- Kubernetes add-on과 known plugin 설치는 Helm으로 통일한다. 공식 문서의 raw manifest 설치 예제가 있더라도 수업 설치 절차는 `helm repo add`, `helm repo update`, `helm upgrade --install`, `helm list`, `kubectl get pods`, `helm uninstall` 흐름으로 맞춘다.
- Kubernetes add-on 설정은 긴 `--set` 나열보다 수업용 `values.yaml`을 우선한다. 학생이 chart, release, namespace, values, rollback, uninstall의 공통 패턴을 반복해서 익히도록 한다.
- Kubernetes 상태 확인은 `kubectl`을 기본으로 가르치고, k9s 같은 TUI 도구는 보조 관찰 도구로 소개한다. TUI가 편해도 `get`, `describe`, `logs`, `events`, `exec`, `rollout`의 의미를 대체하지 않는다는 점을 명확히 한다.
- W3D4부터 이어지는 Kubernetes 7일 탐험의 imagegen 인포그래픽은 전문적인 클라우드 아키텍처 그래픽을 기본 톤으로 한다. 귀여운 너구리 캐릭터는 화면 한쪽에서 작은 설명자 역할만 하며, 바다/항해 요소는 나침반, 옅은 항로선, 작은 아이콘처럼 보조 장식으로만 사용한다. 아키텍처 그림에서는 박스, 연결선, 계층, traffic flow, 상태 흐름이 반드시 주인공이어야 한다.
- Kubernetes 이미지에는 긴 설명문을 넣지 않는다. 이미지는 구조를 보여주는 도식이어야 하며, 제목 1개, 핵심 노드 4~7개, 짧은 라벨 6~10개 정도만 허용한다. 문장형 설명, 긴 체크리스트, 표 형태의 세부 비교, 주의사항은 lesson 본문 표로 내린다.
- 이미지에 들어갈 텍스트는 `API Server`, `etcd`, `Pod`, `Service`, `Sync`, `Deny`, `Graph`처럼 짧은 명사/상태어 중심으로 둔다. "왜", "주의", "장단점", "운영 해석"은 그림 안에 쓰지 않고 본문 표에서 설명한다.
- 이미지 리팩토링 우선순위는 구조 이해가 중요한 그림부터 한다. 1순위는 control plane, node/runtime, Service/DNS/Ingress, NetworkPolicy, Argo CD sync, Istio/Kiali mesh graph다. 배움일기/요약 이미지는 텍스트가 많아지기 쉬우므로 아이콘형 evidence board 정도로 단순화한다.

# 1주차

## keyword
- overview, computing fundamentals, devops mindset, linux, network, http, process, observability, git, documentation, mini-project

## 1주차 목표
- Cloud Native를 배우기 전에 필요한 컴퓨팅 구성요소의 공통 언어를 만든다.
- compute, memory, storage, network, process lifecycle, configuration, identity/access, observability, cost/resource boundary를 구분한다.
- 로컬 컴퓨터에서 웹 서비스가 실행되고 접속되는 흐름을 명령, port, HTTP status, log 확인으로 설명한다.
- GitHub, VS Code, Git, CLI, README를 이용해 실습 흐름을 재현 가능한 형태로 이해한다.
- 작은 정적 웹 애플리케이션을 만들고, 장애/RCA 흐름을 이해한다.
- Docker, MSA, Kubernetes, AWS, Terraform, Observability가 Week 1 컴퓨팅 spine 위에서 어떤 문제를 확장해 해결하는지 설명한다.

## 1주차 운영 원칙
- 1주차는 overview 주간이지만 얕은 용어 소개가 아니다. 이후 기술을 해석할 컴퓨팅 좌표계를 만든다.
- Docker 명령 실습, AWS 리소스 생성, DORA 지표 수업, Well-Architected 독립 수업은 1주차에서 진행하지 않는다.
- Docker, Kubernetes, AWS, Terraform은 미래 anchor로만 언급하고, 모든 언급은 Week 1 컴퓨팅 spine에 연결한다.
- 모든 활동은 화면, 명령 출력, 브라우저 동작처럼 관찰 가능한 상태를 기준으로 다룬다.
- 비유는 최소화하고 공식 문서, 학술 기준, 현업 DevOps/SRE 기준, 실행 상태 확인을 우선한다.
- 1주차 4일차는 국내 IT 기업 사례로 현대 애플리케이션 구성요소를 설명하고 Docker 필요성을 빌드업한다. 7~8교시는 더 이상 면담 전용으로 비워두지 않으며, 환경/용어/자신감 회복이 필요한 학생의 첫 1:1 멘토링은 Day6로 이동한다.

## 1주차 컴퓨팅 spine
| Fundamental | Local computer | Docker로 확장 | Kubernetes로 확장 | AWS로 확장 | Terraform/IaC로 확장 |
|---|---|---|---|---|---|
| Compute | CPU가 process를 실행 | container process | Pod/container, replica | EC2, ECS task, Lambda, EKS node | compute resource |
| Memory | process가 RAM을 사용 | memory limit/usage | requests/limits, OOMKilled | instance/task memory | size variable |
| Storage | file/directory/data path | image layer, volume | Volume, PV, ConfigMap mount | EBS, EFS, S3, RDS | bucket/volume/db resource |
| Network | IP, localhost, port, protocol | port binding, bridge DNS | Service, Ingress, cluster DNS | VPC, subnet, SG, ALB, Route 53 | VPC/subnet/SG resource |
| Lifecycle | start, stop, crash, restart | run/stop/restart policy | rollout, probe, restart | Auto Scaling, ECS service | plan/apply/destroy |
| Configuration | env var, config file | `-e`, `.env`, Dockerfile default | ConfigMap, Secret | Parameter Store, Secrets Manager | variables, sensitive values |
| Identity/access | user, permission, token | registry auth, secret mount | ServiceAccount, RBAC | IAM, MFA, role, access key | provider/IAM resources |
| Observability | logs, status, exit code | logs, inspect, stats | logs, events, metrics, probes | CloudWatch, CloudTrail | outputs, drift signals |
| Cost/resource boundary | local resource limits | image size, running containers | node capacity, requests | billing, Free Tier, instance class | cost assumptions, destroy |

## 1일차

운영 확정: 2026-06-10(수) 12:00~18:00, 점심시간 13:00~14:00, ZEP 과정별 강의실, 총 5시간.

- 12:00~13:00 : 과정별 OT 개요 - 과정 구조, 소통 채널, 수업 참여 방식
- 13:00~14:00 : 점심시간
- 14:00~15:00 : 5주 커리큘럼 로드맵 - Week 1 컴퓨팅 spine과 Week 2~5 기술 연결
- 15:00~16:00 : AI coding agent 시대의 Cloud Native/DevOps 마인드셋 특강 - Claude Code/Codex로 작은 앱은 쉬워졌지만 비즈니스 서비스화에는 인프라, 보안, 배포, 관찰, 비용, 장애 대응 절차가 필요하다는 인사이트
- 16:00~17:00 : 데이터센터 vs 클라우드 - 운영 책임, 비용 구조, 변경 속도, 공유 책임 모델
- 17:00~18:00 : 데이터센터 vs 클라우드 확장 + Live QA - CAPEX/OPEX/TCO/Cloud Cost, 규모의 경제, 학생 질문

## 2일차

- 1교시 : Day1 강의 10분 요약 + 학습 작업공간 준비 - GitHub, Git, VS Code, 터미널 준비 흐름
- 2교시 : GitHub 계정, Git, Python3, VS Code 확인 - 계정/설치/터미널/민감정보 노출 주의
- 3교시 : Git/GitHub 기본 실습 - repository, clone, commit, push, README 확인
- 4교시 : 공식 문서 읽기와 AI 답변 검증 - 버전, 사전 조건, warning, support matrix 확인
- 5교시 : Linux/CLI 기본 - pwd, ls, cd, cat, grep, curl, ps, kill, env
- 6교시 : Compute와 process - CPU, process, thread, 명령, exit code
- 7교시 : Memory, storage, Network/HTTP 기본 - RAM, file system, 경로, persistence, permission, localhost, IP, DNS, TCP, port, request/response, status code
- 8교시 : 구름 EXP 배움일기 - 작업공간 준비, Git/GitHub 흐름, CLI 기본 명령, Network/HTTP에서 막힌 지점

## 3일차

- 1교시 : Day2 강의 10분 요약 + 로컬 정적 서버 실행 - `python3 -m http.server`, browser/curl 확인
- 2교시 : Log, config, secret - stdout/stderr, error message, env var, secret non-exposure
- 3교시 : 서비스 실행 조건 - source, runtime, command, port, data, dependency
- 4교시 : 재현 가능성 - README, script, path, expected result, clean directory
- 5교시 : 실패 분석 라이프사이클 - reproduce, observe, hypothesize, fix, recheck, prevent
- 6교시 : 관찰 가능성과 배포 preview - logs/status 확인, build, artifact, release, deploy, rollback
- 7교시 : AI Coding Tool 사용 원칙 - 공식 문서 확인, 실행 검증, secret/cost/API 위험 점검
- 8교시 : 구름 EXP 배움일기 - 로컬 서버 실행 흐름, log/config/secret 구분, AI 답변 검증에서 다시 확인할 질문

## 4일차

- 1교시 : Day3 강의 10분 요약 + 쿠팡으로 보는 현대 애플리케이션 전체 지도 - 상품, 가격, 재고, 이미지, 주문, 서빙 계층
- 2교시 : 토스로 보는 프론트엔드 플랫폼 - UI 복잡도, 공통 컴포넌트, 빌드 도구, 개발 생산성
- 3교시 : 당근으로 보는 백엔드와 서비스 경계 - 인증, 결제, 공통 의존성, MSA 경계
- 4교시 : 네이버로 보는 데이터베이스와 저장소 - 검색, 분산 저장, 서빙 지연시간, 데이터 최신성
- 5교시 : 카카오로 보는 메시지 스트리밍 - Kafka, 비동기 이벤트, producer/consumer 분리, 운영 결합도
- 6교시 : 우아한형제들로 보는 실시간 주문/배달 이벤트 - 주문 이벤트, 배달 이벤트, retry, observability
- 7교시 : 여기어때로 보는 폭주 트래픽 - 쿠폰, 예약, Redis, Kafka, 피크 트래픽 제어
- 8교시 : 구름 EXP 배움일기 - 현대 애플리케이션 구성요소, 서비스 경계, Docker가 필요해지는 지점

## 5일차

- 1교시 : Day4 강의 10분 요약 + 애플리케이션 실행 환경은 코드만이 아니다 - runtime, dependency, program, port, config, data, command
- 2교시 : DB를 두 개 설치해야 한다면 - 버전 차이, 중복 설치, 데이터 혼동, 삭제 어려움
- 3교시 : 포트 번호와 localhost 충돌 - 3306 충돌, 포트 변경의 연쇄 효과, port binding preview
- 4교시 : 환경변수와 설정 파일 지옥 - `.env`, dev/test/prod 차이, secret 노출 위험
- 5교시 : 삭제, 잔여 파일, 디스크 용량 문제 - 실행 파일, 서비스, 설정, 데이터 폴더, 캐시, 로그
- 6교시 : 빠르게 같은 환경을 만들고 싶다면 - 새 컴퓨터/다른 컴퓨터 환경 재현성, 설치 순서, 초기 데이터
- 7교시 : Docker가 등장하는 자리 - image, container, volume, port, env, compose, cleanup preview
- 8교시 : 구름 EXP 배움일기 - 실행 환경 구성요소, 포트/환경변수/삭제 문제, Docker 주차에서 확인하고 싶은 질문

## 6일차

- 1교시 : Day5 강의 10분 요약 + 첫 1:1 멘토링 A그룹 - 학습 배경, 환경 상태, 학습 불안, blocker type
- 2교시 : 첫 1:1 멘토링 B그룹 - Git, VS Code, terminal, Python, browser, repository 회복
- 3교시 : 용어 회복 - frontend, backend, database, cache, queue, port, environment variable
- 4교시 : 작은 성공 경험 - local app 하나 실행 후 command, URL, status, stop step 확인
- 5교시 : Docker 준비도 triage - 설치 위험, 로컬 자원 확인, 예상 blocker note
- 6교시 : 스터디 그룹 라우팅 - blocker type과 속도에 따라 학생을 묶기
- 7교시 : 개인 회복 계획 - 다음 행동 3개와 Week2 진입 전 확인 지점
- 8교시 : 구름 EXP 배움일기 - 이번 주 가장 어려웠던 용어, 다시 실행해볼 명령, Week2 Docker 시작 전 질문

## 1주차 학습 결과
- GitHub 저장소 1개
- README.md 1개
- 브라우저에서 실행 가능한 싱글 프론트엔드 미니 웹 애플리케이션 1개
- 컴퓨팅 spine mapping note 1개
- AI 답변 검증 note 1개
- 더미 JSON 데이터 파일 1개 이상
- 로컬 정적 서버 실행 명령
- 간단한 장애 분석 흐름 1개
- 2주차 Docker 학습 전 개인 체크리스트

## 1주차 환경 준비 체크리스트
- GitHub 계정 생성, 이메일 인증, repository 생성
- Git 설치 및 `git --version` 확인
- VS Code 설치, 터미널 실행, 프로젝트 폴더 열기
- Docker Desktop 설치는 2주 1일차에 진행한다는 것을 안내하고, 1주차에는 설치를 요구하지 않음
- AI Coding Tool 계정 생성 또는 로그인, 간단한 프롬프트 실행 확인
- AWS 계정 생성은 5주차에 진행한다. 1주차에는 cloud cost/security 개념만 future anchor로 확인한다.
- 브라우저 개발자 도구, curl, 로컬 서버 접속 확인

# 2주차
## Keyword
- docker
- overview
- disk
- network
- configuration
- multi application
- docker-compose

## 2주차 목표
- Docker가 등장한 역사적 배경과 실행 환경 표준화 문제를 설명한다.
- image와 container의 차이를 실행 패키지와 실행 중인 process 관점으로 구분한다.
- Docker 설치/실행 상태를 공식 문서와 CLI 출력 기준으로 확인한다.
- 기본 명령어로 container lifecycle을 실행, 확인, 관찰, 중지, 정리까지 다룬다.
- nginx container로 Docker 실행 가능 여부를 빠르게 검증한다.
- 로컬 PostgreSQL과 Docker PostgreSQL container의 port 충돌을 확인하고, OS별로 로컬 PostgreSQL 중지/삭제/보류 절차를 이해한다.
- PostgreSQL 16/18 container를 서로 다른 host port로 실행해 port binding과 version isolation을 검증한다.
- container 안의 PostgreSQL에 user, database, table, row를 만들고 query로 정상 동작을 확인한다.
- volume 없이 container를 재생성했을 때 데이터가 사라지는 이유를 확인하고, named volume으로 data lifecycle을 container lifecycle과 분리한다.
- Dockerfile을 작성해 표준 실습 애플리케이션 이미지를 직접 빌드한다.
- port binding, network, environment variable, bind mount, named volume을 이용해 runtime 실행 조건을 제어한다.
- Docker Compose로 웹 애플리케이션과 데이터베이스를 함께 실행하고 service name, network, volume을 설명한다.
- 컨테이너 로그와 상태를 확인하고 port/env/volume/network 장애 원인을 분석한다.

## 2주차 운영 원칙
- 표준 실습 애플리케이션을 Docker 실습의 기본 재료로 사용한다.
- 실습 애플리케이션은 GitHub 또는 압축 파일로 내려받을 수 있게 제공하고, 완성 이미지는 Docker Hub에 게시한다.
- 학생 개인의 1주차 미니 웹 애플리케이션은 추가 도전 과제 또는 보충 실습 재료로 활용한다.
- Docker 명령어는 암기보다 "무엇을 확인하려는 명령인지"를 기준으로 가르친다.
- 매 실습마다 실행, 확인, 중지, 정리까지 한 사이클로 진행한다.
- CLI로 실행할 명령은 반드시 fenced code block으로 제시하고, 바로 아래에 성공/실패 판정 기준과 cleanup 명령을 둔다.
- 강의에 넣는 Docker 실습 명령은 실제 실행 가능한 명령으로 구성하고, OS/Docker version 차이로 달라질 수 있는 출력은 expected pattern으로 둔다.
- 강의 본문은 개념 전개, 실습 절차, 오해 교정, cleanup 기준으로 구성한다.
- Day 1의 PostgreSQL 실습은 설치 검증, 로컬 PostgreSQL 충돌 확인, version별 port binding, SQL 기본 조작까지 다룬다.
- Day 2는 Day 1 DB container의 데이터가 사라지는 현상을 출발점으로 삼아 storage와 network를 깊게 다룬다.
- Day 3는 image, Dockerfile, layer/cache, tag/digest, registry를 깊게 다룬다.
- Day 4는 environment/config, logs/inspect/exec/stats, failure drill, cleanup/security를 도구별 소개가 아니라 운영 시나리오 기반 장애 대응으로 깊게 다룬다. 예: 환경변수 누락, 컨테이너는 Up인데 접속 실패, stale volume/data 혼동, container network DNS 오해, restart loop/resource 관찰, cleanup/data 삭제 위험.
- Day 4 자료는 강박적으로 반복되는 핵심 포인트와 주의사항을 삭제한다. 공통 보안/cleanup/관찰 원칙은 한 번만 선언하고, 각 교시는 해당 시나리오에서 새로 판단해야 하는 증거, 명령, 실패 원인, 복구 기준만 담는다.
- Day 5는 Docker Compose 섹션으로 확정하고, Week1 Day4의 회사형 서비스 아키텍처를 compose.yaml과 실제 동작하는 작은 API 앱으로 로컬 재현한다. 각 아키텍처에는 network area, 연결선, 서비스 아이콘이 있는 구조도를 포함한다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## 1일차
- 1교시 : Week1 강의 10분 요약 + Docker 공식 컨셉 - Week 1 실행 조건을 Docker 공식 overview의 image, container, registry, client, daemon 개념으로 연결
- 2교시 : Docker 설치와 nginx 실행 확인 - macOS Docker Desktop GUI 설치/실행, Linux Docker Engine 설치 확인, `docker version`, `hello-world`, nginx container 실행과 HTTP 확인
- 3교시 : 로컬 PostgreSQL과 Docker PostgreSQL port 충돌 확인 - Week 1 로컬 PostgreSQL이 `5432`를 쓰는지 확인하고 Docker PostgreSQL을 같은 port로 띄울 때 충돌이 나는지 관찰
- 4교시 : 로컬 PostgreSQL 삭제/중지 후 Docker PostgreSQL 재실행 - macOS/Linux별 로컬 PostgreSQL 중지/삭제/보류 절차, Docker PostgreSQL container 재실행과 접속 확인
- 5교시 : PostgreSQL version별 container 병렬 실행 - macOS/Linux에서 `postgres:16`, `postgres:18`을 서로 다른 host port로 실행하고 일부러 같은 host port 충돌도 확인
- 6교시 : SQL 기본 조작 검증 - 각 PostgreSQL container에 접속해 user, database, table을 만들고 row insert/query로 정상 동작 확인
- 7교시 : 개인 면담 및 환경 점검 A - Docker 설치 blocker, PostgreSQL 삭제 위험, 포트 충돌, SQL 접속 문제 확인
- 8교시 : 구름 EXP 배움일기 - Docker 설치 상태, nginx 실행 흐름, PostgreSQL 포트 충돌과 version isolation에서 다시 볼 지점

## 2일차
- 1교시 : Day1 강의 10분 요약 + DB container 재생성과 데이터 소실 확인 - volume 없이 만든 PostgreSQL container를 다시 만들면 user/database/table/row가 사라지는 이유 확인
- 2교시 : named volume과 database persistence - PostgreSQL volume을 만들고 container에 mount한 뒤 데이터 재입력, container 교체 후 보존 확인
- 3교시 : Docker volume 명령과 cleanup 위험 - `volume ls`, `inspect`, `rm`, dangling volume, bind mount와 named volume 비교
- 4교시 : bind mount와 host path 주의 - macOS/Linux path, read-only mount, host 파일 변경 반영 확인
- 5교시 : Docker network 기본 - default bridge, custom bridge, network ls/inspect, container attach/detach
- 6교시 : container name DNS와 DB client container - host port publish 없이 같은 network에서 PostgreSQL 접속
- 7교시 : port publish와 network의 차이 - host 접근과 container 간 접근을 분리해 실험, wrong host/port failure drill
- 8교시 : 구름 EXP 배움일기 - volume이 필요한 이유, host path 주의점, container name DNS와 port publish 차이

## 3일차
- 1교시 : Day2 강의 10분 요약 + image와 layer, tag, digest - pull한 image를 `images`, `history`, `inspect`로 읽기
- 2교시 : Dockerfile 기본 문법 - `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `EXPOSE`
- 3교시 : build context와 `.dockerignore` - source tree, secret 제외, context size 확인
- 4교시 : 표준 앱 image build/run - 제공 코드로 image build, container run, HTTP 확인
- 5교시 : build cache와 layer 최적화 - source 변경, cache hit/miss, image size 비교
- 6교시 : registry와 image provenance - Docker Hub official image, tag 전략, digest pinning, pull policy
- 7교시 : tag/push/pull 흐름 - local tag, Docker Hub push는 선택, credential/secret gate 필수
- 8교시 : 구름 EXP 배움일기 - image/layer/tag/digest 차이, Dockerfile 명령, build 실패 시 먼저 볼 지점

## 4일차
- 1교시 : Day3 강의 10분 요약 + environment variable과 runtime config - `-e`, `--env-file`, `.env.example`, image 밖 config
- 2교시 : secret 비노출과 설정 파일 위험 - README/screenshot/history에 password/token을 남기지 않는 기준
- 3교시 : logs 기반 정상/장애 확인 - `docker logs`, app stdout/stderr, DB readiness log
- 4교시 : inspect/exec 기반 내부 확인 - filesystem, env, network, mount, process 확인
- 5교시 : stats/resource/restart policy - CPU/memory 관찰, restart 옵션, crash loop 맛보기
- 6교시 : 통합 failure drill - missing env, wrong port, wrong network, stale volume, bad image tag
- 7교시 : cleanup/security audit - container/image/network/volume 삭제 기준, 삭제하면 안 되는 data 구분
- 8교시 : 구름 EXP 배움일기 - env/config/secret 구분, logs/inspect/exec/stats 사용 위치, compose.yaml로 옮기고 싶은 명령

## 5일차
- 1교시 : Day4 강의 10분 요약 + Compose 기본 개념과 편의성 - 긴 `docker run`을 `compose.yaml` template으로 바꾸는 이유, `config/up/ps/logs/down` 공통 검증 루프
- 2교시 : 쿠팡형 커머스 카탈로그 - frontend, catalog API, PostgreSQL products table, `curl /products`와 DB query 확인
- 3교시 : 당근형 백엔드 서비스 경계 - gateway, identity API, payment API, Adminer, service name `db` 확인
- 4교시 : 토스형 프론트엔드 플랫폼 - frontend preview, config API, feature flag, Redis cache 확인
- 5교시 : Gateway routing template - Nginx reverse proxy, 내부 upstream service, `/a/`, `/b/` routing과 upstream 장애 확인
- 6교시 : 카카오형 메시징/worker - HTTP producer, Redis queue, worker logs, DB 확인
- 7교시 : API + PostgreSQL - PostgREST API 응답과 DB init/query 로그 확인
- 8교시 : Frontend + gateway + API + DB - Week3 MSA service boundary/dependency/failure propagation 질문 정리 + 구름 EXP 배움일기

## 2주차 학습 결과
- 표준 실습 애플리케이션용 Dockerfile
- compose.yaml 1개
- Docker build/run/compose 실행 명령이 포함된 README.md
- Docker Hub에서 내려받아 실행한 표준 이미지 1개
- 직접 빌드한 로컬 이미지 태그 1개 또는 Day 3~4 확정 전까지는 optional
- PostgreSQL 16/18 port binding 실험 흐름
- SQL user/database/table/insert/query 흐름
- storage/network 확인 흐름
- image/Dockerfile/registry 확인 흐름
- env/logs/inspect/exec failure drill 흐름
- Compose architecture 실행 흐름
- 포트, 로그, 환경변수, 볼륨, 네트워크 중 하나 이상을 포함한 장애 분석 흐름
- 3주차 학습 전 Docker 체크리스트

## 2주차 환경 준비 체크리스트
- Docker Desktop 정상 실행
- `docker version` 확인
- `docker run hello-world` 성공
- Week 1 로컬 PostgreSQL 삭제/중지/보류 결정
- `postgres:16`, `postgres:18`을 서로 다른 host port로 실행하거나 실패 증상 확인
- 같은 host port 충돌을 재현하고 port binding 관점으로 설명
- PostgreSQL container에서 user/database/table/row 생성과 query 성공
- volume 없는 container 재생성 후 데이터 소실 확인
- named volume 연결 후 container 교체에도 데이터 보존 확인
- custom network에서 container name으로 통신 확인
- official image tag/digest 또는 image inspect 확인
- env/config 주입과 secret 비노출 확인
- Docker Hub 로그인 또는 표준 실습 앱 이미지 pull 가능 상태 확인
- 표준 실습 앱 소스코드 확인과 build context 점검
- Dockerfile build 성공 또는 Day 3~4 확정 후 보충
- compose.yaml 실행 성공

# 3주차
## Keyword
- msa
- service boundary
- api
- database
- message queue
- failure
- github
- branch strategy
- pull request
- github actions
- runner
- ci gate
- kubernetes
- pod
- deployment
- service

## 3주차 목표
- MSA를 개발 방법론이 아니라 인프라가 운영해야 하는 서비스 토폴로지로 해석한다.
- frontend, api, worker, database, queue/cache 구조의 실행 조건과 장애 전파를 설명한다.
- 서비스 간 HTTP 통신, DB 연결, 환경변수, 포트, 네트워크, 로그, health check를 운영 증거로 확인한다.
- GitHub Flow 중심의 branch/PR/merge/rebase/revert/tag 흐름을 배포 사고 예방 관점으로 압축해 설명한다.
- GitHub Actions workflow, event, job, step, runner, secret의 기본 역할을 설명하고 PR CI gate를 구성한다.
- tag와 app version, Docker image tag의 연결 기준을 설명한다.
- Kubernetes가 MSA와 CI 이후 왜 필요한지 설명하고, Pod/Deployment/Service의 첫 실행 흐름으로 진입한다.

## 3주차 운영 원칙
- MSA는 2일로 압축한다. 개념 설명을 오래 끌지 않고 운영 시나리오와 장애 분석 중심으로 진행한다.
- GitHub는 1일로 압축한다. branch 전략, PR 운영, merge/rebase/revert/tag, GitHub Actions CI gate를 한 흐름으로 묶되 배포 전략의 깊은 내용은 Kubernetes rollout 주차로 넘긴다.
- GitHub Actions는 릴리스 전 검문소(CI gate)로 다룬다. Docker image build와 tag 기준은 맛보기로 연결하고, environment approval과 고급 CD는 이후 주차에서 확장한다.
- 학생이 직접 실행하는 shell script는 macOS BSD 기본 도구와 Linux GNU 도구 차이를 피한다. 특히 `sed -i`처럼 OS별 문법이 다른 명령은 쓰지 않고, 임시 파일을 만든 뒤 교체하는 portable 방식으로 작성한다.
- 3주차 후반 2일은 Kubernetes 입문에 사용한다. 학생 기대가 큰 영역이므로 cluster/node/kubectl/Pod/Deployment/Service를 실제 손으로 확인한다.
- 3주차 4~5일차는 W4D1~W4D5까지 이어지는 7일 Kubernetes 탐험의 시작이다. W3D4는 기본 요소와 설치, W3D5는 Pod/Deployment/Service 첫 실행에 집중하고, known plugin은 Week4에서 Helm 기반으로 단계적으로 심는다.
- 각 lesson에는 중복 주의사항을 반복하지 않고, 해당 시나리오에서 새로 판단해야 하는 증거와 실패 기준만 둔다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## 1일차
- 1교시 : Week2 강의 10분 요약 + MSA를 운영 토폴로지로 보기 - 단일 컨테이너 앱에서 frontend/api/worker/database 구조로 확장되는 흐름
- 2교시 : Monolith vs MSA - 배포 단위, 장애 영향 범위, 네트워크 의존성, 운영 복잡도 비교
- 3교시 : 인프라 엔지니어가 MSA에서 알아야 할 것 - 서비스 목록, 포트, 프로토콜, 의존성, 설정, 헬스체크, 로그 위치
- 4교시 : 표준 MSA 실습 앱 토폴로지 - frontend, api, worker, database, queue/cache 역할과 요청 흐름
- 5교시 : Compose로 전체 서비스 실행 - compose up, ps, logs, 브라우저 접속, 서비스 상태 확인
- 6교시 : 서비스 간 통신 확인 - frontend to api, api to database, worker to queue 흐름을 로그와 상태로 추적
- 7교시 : 장애 시나리오 1 - API URL 오류, DB host 오류, 환경변수 누락을 logs/inspect/exec로 분리
- 8교시 : 구름 EXP 배움일기 - MSA 토폴로지, 서비스별 실행 조건, 연결 실패에서 먼저 볼 증거

## 2일차
- 1교시 : Day1 강의 10분 요약 + 장애 전파와 부분 장애 - api 장애, DB 장애, worker 장애가 사용자 경험에 미치는 영향
- 2교시 : health check와 readiness - /health endpoint, DB readiness, depends_on의 한계, 재시도 필요성
- 3교시 : timeout과 retry - 무한 대기 방지, 재시도의 위험, 중복 처리 문제, 개발팀과 합의할 값
- 4교시 : queue/worker 운영 시나리오 - 작업 적체, worker 중지, 재처리 로그, 비동기 장애 확인
- 5교시 : 로그 분산과 correlation id - 여러 서비스 로그를 이어서 보는 방법과 개발팀에 요구할 정보
- 6교시 : 배포 설정 변경 - 이미지 태그, 환경변수, replica 수, 포트 변경이 장애로 이어지는 사례
- 7교시 : MSA 운영 리포트 작성 - 증상, 영향 범위, 원인 후보, 복구, 예방, 개발팀 전달사항
- 8교시 : 구름 EXP 배움일기 - 장애 전파, health check, timeout/retry, MSA 운영 비용과 Kubernetes 필요성

## 3일차
- 1교시 : Day2 강의 10분 요약 + GitHub 협업 모델 - local branch, remote branch, origin, pull request 흐름
- 2교시 : branch 전략 압축 - GitHub Flow 중심, trunk-based/Git Flow는 선택 기준만 비교
- 3교시 : PR 운영 기준 - 작은 PR, reviewer, status check, protected branch, merge 조건
- 4교시 : merge/rebase/conflict - merge commit, squash, rebase merge 차이와 conflict 재검증
- 5교시 : revert와 rollback - `git revert`, PR revert, 배포 rollback의 차이와 공유 commit 되돌리기 기준
- 6교시 : tag와 version 기준 - app version, Git tag, Docker image tag, latest 사용 주의
- 7교시 : GitHub Actions CI gate - `pull_request` event, checkout, lint/test/build, runner, secret 맛보기
- 8교시 : 구름 EXP 배움일기 - branch 전략, PR gate, merge/rebase/revert/tag, CI 실패 증거

## 4일차
- 1교시 : Day3 강의 10분 요약 + Kubernetes가 등장한 배경 - 컨테이너 수 증가, 배포 반복, 장애 복구, 스케줄링 문제
- 2교시 : Kubernetes 핵심 컨셉 - cluster, node, control plane, worker node, kubelet, container runtime
- 3교시 : Kubernetes가 많이 쓰이는 이유 - 선언적 운영, self-healing, service discovery, rollout/rollback, 확장성
- 4교시 : 장점과 단점 - 표준화/자동화/이식성 vs 러닝커브/YAML/관찰/비용/운영 부담
- 5교시 : 많이 쓰이는 분야와 참고 사례 - MSA, SaaS, 플랫폼 엔지니어링, CI/CD, managed Kubernetes, edge/cloud 사례
- 6교시 : 실습 도구 선택 - kind를 과정 표준으로 고정하고 학습/테스트용 cluster의 한계 설명
- 7교시 : WSL/macOS kind 설치 - Docker, kubectl, kind, k9s 선택 설치와 버전 확인
- 8교시 : kind cluster 생성과 확인 - `kind create cluster`, context, node, cluster-info 확인, k9s로 현재 context/resource 탐색 preview

## 5일차
- 1교시 : Day4 강의 10분 요약 + kubectl 기본과 k9s preview - context, namespace, get, describe, logs, exec, apply, delete, TUI 상태 탐색
- 2교시 : 첫 Pod 실행 - image, command, port, logs, exec, delete 흐름
- 3교시 : Pod 장애 확인 - ImagePullBackOff, CrashLoopBackOff, pending 상태를 describe/events/logs로 확인
- 4교시 : Deployment가 필요한 이유 - Pod 직접 실행의 한계, desired state, replica, self-healing
- 5교시 : Deployment manifest 구조와 배포 - apiVersion, kind, metadata, spec, selector, template
- 6교시 : Service가 필요한 이유 - Pod IP 변화, 안정적인 접근 주소, ClusterIP, endpoint 확인
- 7교시 : 샘플앱 내부 통신과 rollout 맛보기 - service DNS, curlbox, image tag 변경, rollout status/undo
- 8교시 : 구름 EXP 배움일기 - kind 설치, Pod/Deployment/Service 역할, Week4 Kubernetes 질문

## 3주차 학습 결과
- MSA 실습 애플리케이션 실행 가능한 compose.yaml
- frontend, api, worker, database 요청 흐름과 의존성 설명 문서 또는 다이어그램
- MSA 장애 주입 및 복구 리포트 1개
- GitHub branch 전략과 PR 운영 기준 메모
- merge/rebase/revert/tag 압축 실습 로그
- GitHub Actions CI workflow 1개
- GitHub Actions runner, secret, 실패 로그 확인 흐름
- 로컬 Kubernetes 클러스터와 kubectl 기본 확인 결과
- Pod, Deployment, Service 첫 배포 흐름
- Week4 Kubernetes로 확장할 MSA 앱과 image/tag 기준

## 3주차 환경 준비 체크리스트
- MSA 실습 앱 소스코드 다운로드 가능
- `docker compose up`으로 전체 서비스 실행 가능
- frontend/api/database/worker 또는 queue 로그 확인 가능
- GitHub repository push와 pull request 생성 가능
- GitHub Actions workflow 실행 가능
- GitHub Secrets 등록 가능
- branch protection 또는 status check 설정 가능
- Docker Hub 또는 GHCR credential 준비 가능
- Git tag와 GitHub Release 생성 가능
- kind 설치 가능
- `kubectl config current-context` 확인 가능
- Pod, Deployment, Service 생성 가능

# 4주차
## Keyword
- kubernetes
- orchestration
- pod
- deployment
- service
- configmap
- secret
- ingress
- namespace
- rollout
- rollback
- probes
- resources
- helm
- metrics-server
- observability
- prometheus
- grafana
- rbac
- kyverno
- argocd
- istio
- kiali
- runbook
- troubleshooting

## 4주차 목표
- Week3 Day4~Day5에서 잡은 Kubernetes 기본 요소를 실제 운영 시나리오로 확장한다.
- Helm의 chart, repository, release, values, upgrade, rollback, uninstall 흐름을 Kubernetes add-on 설치 표준으로 사용한다.
- Pod, Deployment, Service, ConfigMap, Secret, probe, resource request/limit, Ingress를 MSA 운영 맥락에서 연결한다.
- metrics-server로 Pod/node resource 사용량을 확인하고 requests/limits, HPA preview와 연결한다.
- PV/PVC, StorageClass, volume binding, zonal disk 제약을 Pod 재배치와 scheduling 관점에서 preview하고 AWS EBS/EFS/RDS 판단으로 연결한다.
- Gateway API와 Envoy Gateway를 Helm으로 설치하고 frontend/API 외부 진입 경로를 Gateway/HTTPRoute 기준으로 확인한다. ingress-nginx는 널리 쓰인 기존 Ingress Controller로 언급만 하고, 실습 표준은 Envoy Gateway/Gateway API로 잡는다.
- External Secrets Operator를 Kubernetes Secret과 cloud secret store를 연결하는 도구로 소개하고 AWS Secrets Manager, SSM Parameter Store 연동으로 확장한다.
- Cilium과 Hubble을 NetworkPolicy, CNI, eBPF 기반 network observability 후보로 소개하고 기존 Kubernetes NetworkPolicy와 비교한다.
- kube-prometheus-stack을 Helm으로 설치하고 Prometheus target, Grafana dashboard, Pod/node metric을 확인한다.
- ServiceAccount, Role, RoleBinding, RBAC 최소 권한을 실습하고 Kyverno로 admission policy가 배포를 차단하는 흐름을 확인한다.
- Argo CD로 Git repository의 Kubernetes manifest를 sync하고 drift, OutOfSync, manual sync 흐름을 확인한다.
- Istio와 Kiali는 service mesh의 sidecar, traffic graph, traffic split/fault injection을 preview 수준으로 체험한다.
- Kubernetes runbook을 배포, 확인, 장애 분석, rollback, policy 위반, observability, cleanup 기준으로 정리한다.

## 4주차 운영 원칙
- 4주차는 W3D4~W3D5에서 시작한 7일 Kubernetes 탐험의 후반 5일로 운영한다.
- Week3에서 정리한 MSA 앱, branch/tag/release 기준, CI/CD 증거를 Kubernetes 배포 대상으로 사용한다.
- Kubernetes를 YAML 암기 수업으로 만들지 않고, MSA 운영 문제를 해결하는 선언적 운영 모델로 다룬다.
- Kubernetes known plugin은 한 날에 몰아 소개하지 않는다. workload, traffic, observability, security, GitOps, mesh 주제 안에 하나씩 심어서 실제 운영 문제 해결 도구로 사용한다.
- Kubernetes add-on 설치는 Helm으로 통일한다. `kubectl apply -f <remote-url>` 방식은 설치 표준으로 쓰지 않고, 필요할 때만 왜 혼란을 만드는지 비교 설명한다.
- 모든 Helm 설치는 `helm upgrade --install`을 기본으로 하고 namespace, release name, chart repo, values file, 검증 명령, uninstall 명령을 함께 제공한다.
- Helm values는 수업 repo 안의 파일로 관리한다. 긴 `--set` 명령은 빠른 데모나 공식 문서 비교가 아닌 이상 사용하지 않는다.
- NGINX Ingress Controller는 기존 Ingress 생태계의 대표 사례로만 언급한다. 새 실습은 Gateway API/Envoy Gateway를 기준으로 구성하고, Ingress와 Gateway API의 API shape 차이를 비교한다.
- system namespace에 설치되는 add-on은 통신/권한 원리를 반드시 설명한다. `kube-system`, `monitoring`, `argocd`, `istio-system` 등에 설치된 Pod가 다른 namespace를 보는 이유를 Service DNS, APIService, ServiceAccount, Role/ClusterRole, RoleBinding/ClusterRoleBinding 기준으로 나눠 설명한다.
- "namespace가 다르지만 통신된다"는 표현은 HTTP/Service 통신인지 Kubernetes API 조회/변경인지 구분한다. Service 통신은 DNS/Service/Endpoint/NetworkPolicy를 보고, API 접근은 ServiceAccount token과 RBAC을 본다.
- Pod 재배치 설명에서는 compute scheduling과 storage scheduling을 분리한다. Deployment/ReplicaSet은 replica 수를 맞추고, Scheduler는 node를 고르며, PVC/PV/StorageClass와 PV `nodeAffinity` 또는 topology constraint는 volume이 붙을 수 있는 node/zone을 제한할 수 있다.
- AWS EBS는 zonal block storage이므로 EBS-backed PVC를 사용하는 Pod가 다른 AZ node로 마음대로 이동할 수 없다는 점을 명확히 설명한다. 여러 node/AZ에서 공유가 필요한 경우 EFS, 애플리케이션 레벨 복제, RDS 같은 managed database 선택지를 비교한다.
- add-on별 목표는 깊은 튜닝이 아니라 설치 이유, 핵심 리소스, 운영 효과, 장애 확인 방법이다.
- AWS 계정, 네트워크, 비용 안전장치, EC2/RDS 등 클라우드 인프라 실습은 5주차로 넘긴다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## W3D4~W4D5 Kubernetes 7일 흐름
| 일차 | 본 주제 | 함께 심는 add-on/plugin | 설치 기준 |
|---|---|---|---|
| W3D4 | Kubernetes 기본 요소와 kind 설치 | 없음 | kind/kubectl 자체 설치와 cluster 확인 |
| W3D5 | Pod, Deployment, Service 첫 실행 | 없음 | 기본 object manifest 직접 작성 |
| W4D1 | 운영 가능한 workload와 resource/storage scheduling 관찰 | Helm, metrics-server, External Secrets Operator preview | Helm으로 metrics-server 설치, PV/PVC와 ESO는 개념 preview |
| W4D2 | Service, DNS, Gateway API, 외부 traffic | Envoy Gateway, Gateway API, cert-manager preview | Helm으로 Envoy Gateway 설치, NGINX Ingress는 비교 언급 |
| W4D3 | 장애와 성능/네트워크 관찰 | kube-prometheus-stack, K9s, Cilium/Hubble preview | Helm으로 Prometheus/Grafana 설치, Cilium/Hubble은 network observability preview |
| W4D4 | 권한, 정책, secret 연동 | RBAC, Kyverno, External Secrets Operator | RBAC은 기본 object, Kyverno/ESO는 Helm 설치 또는 preview |
| W4D5 | GitOps와 mesh preview | Argo CD, Istio, Kiali, Cilium 비교 | 모두 Helm 설치, Cilium은 mesh/CNI 비교 축 |

## Kubernetes known plugin/add-on 배치 기준
| plugin/add-on | 넣을 세션 | 수업 역할 | 설치/실습 기준 |
|---|---|---|---|
| Helm | W4D1S2~S3 | add-on 설치 표준 | 모든 add-on 설치 패턴의 기준 |
| metrics-server | W4D1S7 | `kubectl top`, HPA preview | Helm 설치 |
| External Secrets Operator | W4D1S4 preview, W4D4S3~S4, W5D2 연결 | Kubernetes Secret과 외부 secret store 연동 | Helm 설치 또는 provider manifest preview |
| AWS Secrets Manager | W4D4/W5D2 연결 | 운영 secret 저장소 | ESO provider로 연결 설명 |
| AWS SSM Parameter Store | W4D4/W5D2 연결 | 저비용 parameter/secret 저장소 | ESO provider로 연결 설명 |
| Gateway API | W4D2S3~S4 | Ingress 이후 세대 L4/L7 routing API | Gateway/HTTPRoute 작성 |
| Envoy Gateway | W4D2S3~S5 | Gateway API controller | Helm 설치 |
| cert-manager | W4D2S6 preview, W5 AWS 연결 | TLS certificate 자동화 | preview 또는 Helm 설치 선택 |
| NGINX Ingress Controller | W4D2S1~S2 비교 언급 | 기존 Ingress 생태계 이해 | 설치하지 않고 비교만 |
| kube-prometheus-stack | W4D3S2~S6 | Prometheus/Grafana/Alertmanager | Helm 설치 |
| K9s | W4D3S1/S7 | TUI 기반 cluster 상태 확인 | 로컬 도구 소개 |
| Cilium | W4D2S6, W4D3S5, W4D5S5 | CNI, NetworkPolicy, eBPF visibility, mesh와 비교 | kind에서는 preview 중심, 설치 가능 환경이면 Helm |
| Hubble | W4D3S5 | service dependency/flow observability | Cilium과 함께 preview |
| Kyverno | W4D4S4~S7 | admission policy, Policy as Code | Helm 설치 |
| Argo CD | W4D5S1~S4 | GitOps sync/drift/self-heal | Helm 설치 |
| Istio | W4D5S5~S7 | Service Mesh, traffic policy, mTLS preview | Helm 설치 |
| Kiali | W4D5S6~S7 | mesh traffic graph | Helm 설치 |

## 1일차
- 1교시 : Week3 Kubernetes 2일 요약 + 운영 가능한 workload 기준 - Pod/Deployment/Service 복습, 설정/상태/자원/관찰이 필요한 이유
- 2교시 : Helm 기본 개념 - chart, repository, release, namespace, values, upgrade, rollback, uninstall
- 3교시 : Helm 공통 설치 루프 - `repo add/update`, `upgrade --install`, `helm list`, `kubectl get pods`, `helm uninstall`
- 4교시 : ConfigMap과 Secret - image 밖 runtime config, 민감정보 주입, `.env`와 Kubernetes object 연결
- 5교시 : probe와 readiness - liveness/readiness/startup probe, 잘못된 probe가 traffic과 restart에 미치는 영향
- 6교시 : resource requests/limits와 storage scheduling preview - CPU/memory 요청과 제한, OOMKilled, node capacity, PV/PVC, StorageClass, WaitForFirstConsumer, PV nodeAffinity, zonal volume 제약
- 7교시 : metrics-server 설치와 관찰 - Helm으로 metrics-server 설치, `kubectl top node/pod`, HPA preview
- 8교시 : 구름 EXP 배움일기 - Helm 설치 패턴, ConfigMap/Secret, probe/resource에서 막힌 지점

## 2일차
- 1교시 : Day1 강의 10분 요약 + Kubernetes networking 다시 잡기 - Pod IP, Service, Endpoint, DNS, selector
- 2교시 : MSA 앱 내부 통신 - frontend/api/database 또는 cache 연결, service name DNS와 targetPort 구분
- 3교시 : Gateway API와 Envoy Gateway 설치 - Helm으로 Envoy Gateway 설치, GatewayClass/Gateway/HTTPRoute 구조 확인, NGINX Ingress는 기존 방식으로 비교만 언급
- 4교시 : HTTPRoute rule 작성 - host/path routing, frontend와 API routing, curl/browser 확인
- 5교시 : Gateway/HTTPRoute 장애 분석 - GatewayClass 누락, HTTPRoute parentRefs 오류, Service selector 오류, backend port 오류, 404/502/connection refused 분리
- 6교시 : NetworkPolicy와 Cilium preview - namespace는 기본 network 격리벽이 아니라는 점을 명확히 설명하고, frontend -> backend, backend -> database 허용/차단 기준, podSelector/namespaceSelector 차이, DNS egress, CiliumNetworkPolicy/Hubble preview를 다룬다
- 7교시 : rollout과 external traffic - image tag 변경, rollout status/history/undo, Gateway 경로로 사용자 영향 확인
- 8교시 : 구름 EXP 배움일기 - Service/Gateway API/DNS 차이, Envoy Gateway Helm 설치, traffic 장애에서 먼저 볼 증거

## 3일차
- 1교시 : Day2 강의 10분 요약 + Kubernetes observability 기준 - logs/events/metrics/traces 차이, Docker stats와의 차이
- 2교시 : kube-prometheus-stack 설치 - Helm으로 Prometheus, Grafana, Alertmanager, exporter 구성 확인
- 3교시 : Prometheus target 확인 - scrape target, ServiceMonitor/PodMonitor 개념, target down 원인
- 4교시 : Grafana dashboard 확인 - node/pod CPU/memory/restart, namespace별 resource 사용량
- 5교시 : 장애와 metric/network flow 연결 - bad rollout, readiness 실패, restart 증가, CPU/memory 압박을 dashboard로 확인하고 Cilium/Hubble이 있다면 service dependency와 flow 관찰을 preview
- 6교시 : alert preview - alert rule과 silence 개념, threshold를 너무 낮게 잡을 때 생기는 noise
- 7교시 : 관찰 runbook 작성 - K9s로 상태를 빠르게 훑고, 증상, 관련 metric, 확인 명령, dashboard 위치, 개발팀 전달 정보를 정리
- 8교시 : 구름 EXP 배움일기 - Prometheus/Grafana에서 본 지표, target down 원인, 운영 dashboard 질문

## 4일차
- 1교시 : Day3 강의 10분 요약 + Kubernetes 권한 모델 - user, group, ServiceAccount, Role, ClusterRole, RoleBinding
- 2교시 : RBAC 최소 권한 실습 - 읽기 전용 ServiceAccount, namespace scope 권한, forbidden error 확인
- 3교시 : app Pod와 ServiceAccount, external secret 권한 - default ServiceAccount 위험, token mount, workload identity preview, External Secrets Operator가 AWS Secrets Manager/SSM Parameter Store를 읽는 권한 모델
- 4교시 : Kyverno와 External Secrets Operator 설치/preview - Helm으로 Kyverno 설치, ESO 설치 또는 manifest preview, admission controller와 operator reconciliation 차이
- 5교시 : Kyverno policy 실습 1 - `latest` tag 금지, required label, Audit/Enforce 차이
- 6교시 : Kyverno policy 실습 2 - privileged container 또는 hostPath 제한, policy violation 결과 확인
- 7교시 : 권한과 정책 장애 분석 - RBAC forbidden과 Kyverno admission deny를 구분하고 복구 기준 정리
- 8교시 : 구름 EXP 배움일기 - RBAC과 Kyverno 차이, 보안 정책이 배포를 막을 때 확인할 증거

## 5일차
- 1교시 : Day4 강의 10분 요약 + GitOps 개념 - GitHub Actions와 Argo CD 차이, CI와 CD 책임 분리
- 2교시 : Argo CD 설치 - Helm으로 Argo CD 설치, admin secret, port-forward 또는 Ingress 접속 기준
- 3교시 : Argo CD Application 생성 - Git repository의 manifest path를 Application으로 등록하고 sync 상태 확인
- 4교시 : drift와 sync - manifest 변경, OutOfSync, manual sync, prune/self-heal preview, rollback 기준
- 5교시 : Istio 개념 preview와 Cilium 비교 - sidecar, Envoy, mTLS, traffic policy, mesh가 필요한 시나리오, CNI/eBPF 계열 Cilium과 mesh 역할 차이
- 6교시 : Istio/Kiali 설치 - Helm으로 istio-base, istiod, gateway, Kiali 설치, namespace injection 확인
- 7교시 : mesh traffic 확인 - sample app sidecar injection, traffic split 또는 fault injection, Kiali graph 확인
- 8교시 : 구름 EXP 배움일기 - Argo CD/GitOps, Istio mesh preview, Kubernetes 7일 탐험에서 남은 질문

## 4주차 학습 결과
- MSA 실습 앱을 배포할 Kubernetes manifest 세트
- namespace, deployment, service, configmap, secret, ingress, probe, resource 역할 설명 문서
- Helm chart/repository/release/values/uninstall 공통 설치 패턴 evidence
- Helm으로 설치한 metrics-server, ingress-nginx, kube-prometheus-stack, Kyverno, Argo CD, Istio/Kiali release 상태
- kubectl 기반 상태 확인 및 장애 분석 명령 모음
- rollout 또는 rollback 실습 흐름 1개
- Prometheus/Grafana dashboard와 target 확인 evidence
- RBAC forbidden과 Kyverno admission deny를 구분한 보안 장애 note
- Argo CD Application sync/drift evidence
- Istio/Kiali mesh preview evidence
- Kubernetes 운영 runbook 초안
- Week3 image tag/release 기준과 Kubernetes rollout 연결 메모
- AWS로 넘길 계정/네트워크/비용 질문 목록

## 4주차 환경 준비 체크리스트
- 로컬 Kubernetes 클러스터 실행 가능
- `kubectl get nodes`에서 node 확인 가능
- Helm 설치 및 chart install/uninstall 가능
- MSA 실습 앱을 Kubernetes에서 실행 가능
- Service 또는 Ingress를 통해 frontend 접속 가능
- `kubectl logs`, `kubectl describe`, `kubectl exec` 사용 가능
- Week3에서 생성한 image tag 또는 로컬 빌드 이미지 사용 가능
- rollout/rollback 실습용 정상 이미지와 실패 이미지 준비 가능
- Helm chart 다운로드가 가능한 네트워크 상태 확인
- Grafana, Argo CD, Kiali UI 접속을 위한 port-forward 또는 Ingress 접근 가능

# 5주차
## Keyword
- aws
- load balancer
- ecr
- ecs
- s3
- rds
- cloudwatch
- finops
- observability
- managed service
- terraform
- iac
- state
- drift
- plan
- destroy

## 5주차 목표
- AWS compute, network, storage, database, container, observability, billing 서비스를 운영 관점에서 연결한다.
- EC2/ALB, ECR/ECS 또는 컨테이너 실행 서비스, S3, RDS, CloudWatch를 실습 시나리오로 확인한다.
- 비용이 발생하는 지점을 예측하고 Budget, Cost Explorer, 태그 기반 비용 관리의 필요성을 이해한다.
- Terraform의 provider, resource, variable, output, state, plan/apply/destroy 흐름을 이해한다.
- AWS Console 구성 일부를 Terraform 코드로 재현하고, 변경 검토와 cleanup 절차를 이해한다.
- 수작업 콘솔 구성의 반복성, 누락 위험, 리뷰 불가능성을 IaC와 연결한다.

## 5주차 운영 원칙
- 5주차 1~3일차는 AWS 계정 안전장치, 네트워크, 컴퓨팅, 컨테이너/관찰 흐름을 압축해서 다룬다.
- 5주차 4~5일차는 남은 시간을 Terraform/IaC에 집중한다.
- AWS 실습은 비용 통제가 가능한 리소스를 우선 사용하고, RDS/ECS/EKS는 계정/비용 상태에 따라 생성 또는 시뮬레이션 경로를 둔다.
- FinOps와 Observability는 별도 이론으로 분리하지 않고, 리소스 선택과 운영 판단 안에 함께 다룬다.
- Terraform은 거대한 모듈 작성보다 plan을 읽고 변경/비용/보안/cleanup을 검토하는 능력에 집중한다.
- 모든 Terraform apply 전 plan을 읽고, 실습 후 destroy 또는 잔여 리소스 확인을 수행한다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## 1일차
- 1교시 : Week4 강의 10분 요약 + Load Balancing 개념 - ALB, target group, health check, listener, public/private 경계
- 2교시 : ALB Console 실습 - target group 생성, health check 확인, ALB로 웹 서비스 접속
- 3교시 : 컨테이너 실행 서비스 매핑 - Docker/Kubernetes 관점에서 ECR, ECS, EKS가 해결하는 문제 비교
- 4교시 : ECR 실습 - repository 생성, image tag 규칙, push/pull 흐름, credential 주의
- 5교시 : ECS 또는 App Runner 맛보기 - task/service 개념, image 실행, logs와 health 확인
- 6교시 : CloudWatch Logs 기본 - 로그 그룹, 로그 스트림, EC2/ECS/app 로그 수집 개념
- 7교시 : CloudWatch Metrics와 Alarm - CPU, network, ALB target health, threshold, notification 개념
- 8교시 : 구름 EXP 배움일기 - ALB/ECR/ECS/CloudWatch 연결 흐름과 장애 확인 지점

## 2일차
- 1교시 : Day1 강의 10분 요약 + Storage와 Database 서비스 선택 기준 - EBS, EFS, S3, RDS의 용도와 운영 책임, Kubernetes PV/PVC와 EBS zonal 제약 연결
- 2교시 : S3 Console 실습 - bucket 생성, 객체 업로드, public access block, 정적 파일 호스팅 개념
- 3교시 : S3 보안/비용 시나리오 - public access, lifecycle, storage class, 삭제 확인
- 4교시 : RDS 개념과 비용 주의사항 - subnet group, security group, backup, Multi-AZ, storage 비용
- 5교시 : RDS Console 실습 또는 시뮬레이션 - DB 생성 흐름, 연결 정보, 보안 그룹, 삭제 보호 옵션 확인
- 6교시 : 애플리케이션 연결 관점 - connection string, secret 관리, private subnet, 접근 경로
- 7교시 : 장애/보안 점검 - DB port 노출, credential 노출, backup/delete protection, 비용 잔여 리소스
- 8교시 : 구름 EXP 배움일기 - S3/RDS 선택 기준, connection string과 secret, 비용 위험 질문

## 3일차
- 1교시 : Day2 강의 10분 요약 + 운영 대시보드 기본 - CloudWatch Dashboard, 서비스별 핵심 지표, 장애 확인 순서
- 2교시 : FinOps 실습 - Cost Explorer, Budget 알림, 태그별 비용 추적, 리소스별 비용 발생 지점 확인
- 3교시 : 보안 운영 기본 - IAM 최소 권한, security group 검토, secret 노출 위험, public resource 점검
- 4교시 : AWS 통합 장애 시나리오 - EC2/ALB/S3/RDS/CloudWatch 중 하나의 실패를 증거로 분석
- 5교시 : AWS 운영 Runbook - 배포, 확인, 로그/지표, 비용, cleanup 절차 정리
- 6교시 : 콘솔 작업의 한계 - 클릭 순서 누락, 설정값 불일치, 재현 어려움, 리뷰 불가능성
- 7교시 : Terraform 전환 Preview - 어떤 설정을 코드로 옮길지, 변수화/민감정보/상태 관리 기준
- 8교시 : 구름 EXP 배움일기 - AWS 5일 요약, 운영 runbook, Terraform으로 옮길 후보

## 4일차
- 1교시 : Day3 강의 10분 요약 + Terraform 기본 개념 - provider, resource, variable, output, state, plan/apply/destroy
- 2교시 : Terraform 설치 및 인증 준비 - terraform version, AWS 인증, provider init, fmt, validate
- 3교시 : 작은 AWS 구성 코드화 - region, tag, security group, EC2 또는 S3 등 비용 통제 가능한 리소스
- 4교시 : variable/output/sensitive - 반복 설정 제거, output 확인, secret을 코드와 state에 남기는 위험
- 5교시 : Terraform plan 검토 - 변경 전 미리보기, 비용/보안/태그/관찰 가능성 누락 확인
- 6교시 : Terraform apply 및 검증 - Console, curl, CloudWatch, terraform state 비교
- 7교시 : 개인 면담 및 환경 점검 - Terraform init/provider 인증/state/backend 문제 확인
- 8교시 : 구름 EXP 배움일기 - Terraform plan을 읽는 법, provider 인증, sensitive/state에서 주의할 점

## 5일차
- 1교시 : Day4 강의 10분 요약 + 변경/drift 실습 - Console에서 tag 또는 rule 변경 후 plan 차이 확인
- 2교시 : Terraform import 개념과 한계 - 이미 만든 리소스와 코드의 관계, state 관리 위험
- 3교시 : 모듈화 맛보기 - 반복 리소스 정리, module input/output, 과한 추상화의 위험
- 4교시 : destroy와 cleanup audit - destroy 전 plan 확인, 잔여 리소스, 비용 알림, state 파일 처리
- 5교시 : 최종 통합 정리 - Docker, MSA, GitHub Actions, Kubernetes, AWS, Terraform이 하나의 운영 흐름으로 연결되는 방식
- 6교시 : 운영 포트폴리오 패킷 - 아키텍처 다이어그램, runbook, CI workflow, manifest, Terraform plan, cleanup evidence
- 7교시 : 다음 학습 로드맵 - EKS/ECS 심화, Observability, Security, Terraform module/backend, GitOps
- 8교시 : 구름 EXP 배움일기 - 전체 과정에서 연결된 개념, Terraform으로 이해한 재현성, 이후 더 공부할 질문

## 5주차 학습 결과
- AWS Console로 구성한 실습 아키텍처 다이어그램
- AWS 서비스 매핑 표 - compute, network, storage, database, observability, billing
- Budget 또는 비용 알림 설정 흐름
- CloudWatch Logs/Metrics/Alarm/Dashboard 실습 흐름
- EC2/ALB, ECR/ECS 또는 App Runner, S3/RDS 중 선택 실습 결과
- AWS 운영 runbook과 cleanup 체크리스트
- Terraform 전환 대상 리소스 목록과 최소 Terraform 코드
- `terraform init/fmt/validate/plan/apply/destroy` 실행 흐름
- state, drift, secret, 비용 위험에 대한 운영 note
- 전체 과정 포트폴리오 패킷 초안

## 5주차 환경 준비 체크리스트
- AWS Console 로그인 가능
- MFA 설정 확인
- 실습 리전 확정
- Billing, Budget, Cost Explorer 접근 가능
- 공통 태그 규칙 확인
- VPC, security group, EC2, ALB 또는 컨테이너 실행 서비스 생성 가능
- S3, RDS 생성 또는 시뮬레이션 흐름 확인 가능
- CloudWatch Logs/Metrics/Alarm 접근 가능
- Terraform 설치 및 `terraform version` 확인
- AWS 인증을 Terraform provider에서 사용할 수 있음
- `terraform init`, `terraform fmt`, `terraform validate` 실행 가능
- `terraform plan` 결과를 읽고 변경 내용을 설명 가능
- 실습 종료 후 삭제/중지할 리소스 목록 확인
