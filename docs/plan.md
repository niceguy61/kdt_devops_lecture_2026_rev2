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
| 3주차 | MSA, 서비스 경계, API/데이터 의존성, 다중 서비스 운영 | MSA 실습 앱, 서비스 계약, 의존성/장애 전파 분석 |
| 4주차 | Kubernetes, manifest, rollout, service discovery, 운영 플러그인 | Kubernetes manifest, Helm/plugin 흐름, rollout/rollback, 클러스터 장애 분석 |
| 5주차 | AWS 서비스 매핑, FinOps, Observability, Terraform/IaC 기초 | AWS 아키텍처 다이어그램, 비용/관찰 흐름, Terraform 코드/plan/destroy 흐름 |

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
- Day 4는 environment/config, logs/inspect/exec/stats, failure drill, cleanup/security를 깊게 다룬다.
- Day 5는 Docker Compose 섹션으로 확정하고, 표준 코드와 compose.yaml로 유명한 로컬 아키텍처 패턴을 직접 실행/검증한다.
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
- 1교시 : Day4 강의 10분 요약 + Compose 기본과 검증 루프 - 제공 코드에서 `compose.yaml` 읽기, `config`, `up`, `ps`, `logs`, `down` 실행
- 2교시 : Architecture 1 - Web + PostgreSQL two-tier app, service name과 internal port로 DB 연결
- 3교시 : Architecture 2 - Web + PostgreSQL + Adminer/pgAdmin, DB 관리 UI와 host port 노출 기준
- 4교시 : Architecture 3 - Web + Redis cache, cache hit/miss와 container logs 확인
- 5교시 : Architecture 4 - Nginx reverse proxy + multiple web services, path/host routing과 upstream 장애 확인
- 6교시 : Architecture 5 - Queue + worker + database, 비동기 처리와 worker logs 확인
- 7교시 : Compose 장애 분석과 cleanup - missing env, wrong service name, wrong port, stale volume, `down` vs `down -v`
- 8교시 : 구름 EXP 배움일기 - Compose가 줄여준 명령, service boundary/API/DB/worker 연결, Week3 MSA에서 확인할 질문

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
- monolith
- api
- multi-service
- service communication
- database
- message queue
- failure
- docker-compose

## 3주차 목표
- Monolith와 MSA의 차이를 인프라 운영 관점에서 설명한다.
- 여러 서비스로 나뉜 시스템의 실행 단위, 배포 단위, 네트워크 경계, 데이터 의존성을 파악한다.
- 개발자가 만든 서비스를 인프라에서 실행하기 위해 필요한 정보와 요청사항을 파악할 수 있다.
- 서비스 간 HTTP 통신, DB 연결, 환경변수, 포트, 네트워크 구성을 운영 관점에서 해석한다.
- 여러 컨테이너가 함께 실행될 때 발생하는 실행 순서, 장애 전파, 로그 분산 문제를 체감한다.
- health check, timeout, retry, graceful degradation 같은 안정성 개념이 인프라 구성에 왜 필요한지 이해한다.
- "왜 Kubernetes 같은 오케스트레이션 도구가 필요한가"를 운영 사례 기반으로 설명할 수 있다.

## 3주차 운영 원칙
- 2주차 표준 실습 앱을 확장한 MSA 실습 애플리케이션을 사용한다.
- 실습 애플리케이션은 frontend, api, worker, database 구조를 기본으로 하고, 선택적으로 redis 또는 queue를 추가한다.
- MSA를 개발 방법론이 아니라 인프라가 운영해야 하는 서비스 토폴로지로 다룬다.
- 개발자 내부 구현보다 실행 조건, 네트워크 연결, 설정, 로그, 헬스체크, 배포 순서, 장애 영향 범위에 집중한다.
- MSA를 정답으로 가르치지 않고, 운영 복잡도를 감당할 이유가 있을 때 선택하는 아키텍처로 다룬다.
- 매 실습은 "인프라 관점에서 좋아진 점"과 "운영 관점에서 어려워진 점"을 함께 다룬다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## 1일차
- 1교시 : Week2 강의 10분 요약 + 3주차 학습 목표 - 단일 컨테이너 앱에서 여러 서비스 앱으로 확장되는 흐름
- 2교시 : Monolith vs MSA - 배포 단위, 장애 영향 범위, 네트워크 의존성, 운영 복잡도 비교
- 3교시 : 인프라 엔지니어가 MSA에서 알아야 할 것 - 서비스 목록, 포트, 프로토콜, 의존성, 설정, 헬스체크, 로그 위치
- 4교시 : 표준 MSA 실습 앱 토폴로지 소개 - frontend, api, worker, database 역할과 요청 흐름
- 5교시 : 실습 앱 다운로드 및 실행 준비 - GitHub clone 또는 압축 파일 다운로드, 운영 문서와 폴더 구조 확인
- 6교시 : Docker Compose로 전체 서비스 실행 - compose up, ps, logs, 브라우저 접속, 서비스 상태 확인
- 7교시 : 개인 면담 및 환경 점검 - Compose 실행, 포트 충돌, 이미지 pull/build 문제 해결
- 8교시 : 구름 EXP 배움일기 - Monolith와 MSA 차이, 표준 MSA 앱 토폴로지, Compose 실행에서 막힌 지점

## 2일차
- 1교시 : Day1 강의 10분 요약 + 서비스 간 통신을 보는 법 - endpoint, protocol, status code, latency, dependency map
- 2교시 : frontend와 api 연결 운영 관점 - API URL, CORS 이슈를 개발팀과 협업해 확인하는 방법
- 3교시 : 컨테이너 네트워크 복습 - localhost 오해, service name DNS, 내부 포트와 외부 포트
- 4교시 : api와 database 연결 운영 관점 - connection string, credential, migration, 초기 데이터, 접근 권한
- 5교시 : 서비스 실행 순서 문제 - depends_on의 의미와 한계, DB readiness, 재시도 필요성
- 6교시 : health check 기본 - /health endpoint, liveness/readiness 차이, 장애 감지 기준
- 7교시 : 연결 실패 장애 분석 - 잘못된 API URL, DB host 오류, 포트 오류, 환경변수 누락 찾기
- 8교시 : 구름 EXP 배움일기 - 서비스 간 통신, API/DB 연결, health check, 연결 실패에서 먼저 볼 지점

## 3일차
- 1교시 : Day2 강의 10분 요약 + 서비스 분리와 데이터 의존성 - DB 공유의 위험, 서비스별 데이터 책임, 장애 영향 범위
- 2교시 : worker 서비스 운영 관점 - 비동기 처리, 배치 작업, 오래 걸리는 작업이 인프라에 주는 영향
- 3교시 : queue 또는 redis 운영 개념 - 동기 호출과 비동기 처리의 차이, 병목과 적체를 관찰하는 방법
- 4교시 : worker/queue 실습 - 요청 생성, 작업 처리, 로그와 상태로 처리 흐름 확인
- 5교시 : 장애 전파와 부분 장애 - api 장애, DB 장애, worker 장애가 사용자 경험과 운영 대응에 미치는 영향
- 6교시 : timeout과 retry 기본 - 무한 대기 방지, 재시도의 위험, 중복 처리 문제, 개발팀과 합의할 값
- 7교시 : 로그 분산 문제 - 여러 서비스 로그 보기, correlation id 또는 request id를 개발팀에 요구해야 하는 이유
- 8교시 : 구름 EXP 배움일기 - worker/queue가 필요한 상황, 장애 전파, timeout/retry, 로그 분산 문제

## 4일차
- 1교시 : Day3 강의 10분 요약 + MSA 설정 관리 - 환경변수, .env, config 분리, secret을 코드에 넣지 않는 이유
- 2교시 : MSA 로컬 개발 환경 - hot reload, bind mount, dev/prod compose 분리 개념
- 3교시 : API 계약과 운영 문서 - OpenAPI/Swagger 개념, 인프라가 알아야 할 endpoint, health, dependency 정보
- 4교시 : 버전 관리와 배포 협업 - 이미지 태그, 하위 호환, 배포 순서, rollback 가능성
- 5교시 : MSA 운영 비용 - 배포 단위 증가, 로그 증가, 네트워크 장애, 모니터링/알림 복잡도
- 6교시 : Kubernetes가 필요한 이유 - 여러 컨테이너를 수동으로 관리할 때의 한계, 선언적 운영의 필요성
- 7교시 : 개인 면담 및 환경 점검 - MSA 실습 앱 실행 상태, Compose 설정, 로그 분석 흐름 확인
- 8교시 : 구름 EXP 배움일기 - MSA 설정 관리, API 계약, 배포 협업, Kubernetes가 필요해지는 이유

## 5일차
- 1교시 : Day4 강의 10분 요약 + 3주차 통합 실습 - MSA 실습 앱을 인프라 운영 관점으로 점검
- 2교시 : 배포 설정 변경 실습 - 이미지 태그, 환경변수, 포트, 서비스 개수 조정을 Compose 수준에서 확인
- 3교시 : 이미지 재빌드와 Compose 재실행 - 변경된 서비스만 build, up, logs로 확인
- 4교시 : 장애 주입 실습 - 일부 서비스 중지, 잘못된 환경변수 설정, DB 연결 실패 상황 만들기
- 5교시 : 장애 복구 실습 - 원인 분석, 설정 복구, 서비스 재시작, 개발팀 협업 지점
- 6교시 : Kubernetes가 필요해지는 지점 - 서비스 토폴로지, 실행 조건, 장애 대응, 선언적 운영
- 7교시 : 4주차 Kubernetes Preview - Pod, Deployment, Service, ConfigMap, Secret이 등장하는 이유
- 8교시 : 구름 EXP 배움일기 - MSA 통합 실습에서 이해한 운영 복잡도, Kubernetes로 넘겨 볼 질문

## 3주차 학습 결과
- MSA 실습 애플리케이션 실행 가능한 compose.yaml
- frontend, api, worker, database 요청 흐름과 의존성 설명 문서 또는 다이어그램
- 서비스별 실행 조건 - 이미지, 포트, 환경변수, 의존 서비스, health check
- 배포 설정 또는 환경 설정 변경 내역
- 장애 주입 및 복구 흐름 1개
- 개발팀에 전달할 장애 리포트 또는 운영 개선 요청 흐름 1개
- 인프라 관점에서 본 MSA의 장점과 운영 비용 회고
- 4주차 Kubernetes 학습 전 체크리스트

## 3주차 환경 준비 체크리스트
- MSA 실습 앱 소스코드 다운로드 가능
- `docker compose up`으로 전체 서비스 실행 가능
- frontend에서 api 요청 성공
- api에서 database 연결 성공
- worker 또는 queue 처리 로그 확인
- 서비스별 로그 확인 가능
- 일부 서비스 중지 후 장애 상황 재현 가능

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
- helm
- istio
- autoscaler
- grafana stack
- known plugins

## 4주차 목표
- 3주차 MSA 운영 문제를 Kubernetes가 어떤 방식으로 해결하려고 하는지 설명한다.
- Pod, Deployment, Service, ConfigMap, Secret, Ingress의 역할을 인프라 운영 관점에서 이해한다.
- Docker Compose 기반 MSA 실습 앱을 Kubernetes manifest로 옮겨 실행한다.
- 로컬 Kubernetes에서도 multi-node 클러스터를 구성해 여러 서버에 분산 실행되는 환경을 축소 실습한다.
- Helm을 이용해 Kubernetes 확장 컴포넌트를 설치하고 관리하는 기본 흐름을 이해한다.
- Istio, Ingress Controller, autoscaler, Grafana stack 같은 Kubernetes known plugin이 필요한 이유를 운영 관점에서 설명한다.
- kubectl로 리소스 상태, 로그, 이벤트, 네트워크 연결 문제를 확인한다.
- rollout, rollback, scaling, self-healing을 실습하고 운영 관점의 장단점을 이해한다.
- 5주차 AWS 서비스, 비용 관리, 관찰 가능성 수업으로 이어질 수 있도록 Kubernetes와 클라우드 서비스의 연결 지점을 이해한다.

## 4주차 운영 원칙
- Kubernetes를 YAML 암기 수업으로 만들지 않고, MSA 운영 문제를 해결하는 선언적 운영 모델로 다룬다.
- 실습 환경은 multi-node 구성이 가능한 kind 또는 minikube를 우선 표준으로 정하고, Docker Desktop Kubernetes는 fallback으로 둔다.
- 처음에는 managed Kubernetes가 아니라 로컬 Kubernetes로 개념과 kubectl 사용법을 익힌다.
- 로컬 multi-node 클러스터가 실제 여러 서버 운영 환경을 완전히 대체하지는 않지만, Pod 배치, 노드 상태, 장애 영향 범위를 테스트할 수 있음을 명확히 설명한다.
- Kubernetes known plugin은 깊은 튜닝보다 설치 이유, 핵심 리소스, 운영 효과, 장애 확인 방법을 중심으로 다룬다.
- Helm은 플러그인 설치를 쉽게 하기 위한 패키지 매니저로 도입하고, chart 구조를 깊게 작성하는 것은 후순위로 둔다.
- 매 실습마다 manifest 작성, apply, 상태 확인, 로그 확인, 삭제 또는 복구까지 한 사이클로 진행한다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## 1일차
- 1교시 : Week3 강의 10분 요약 + Kubernetes가 필요한 이유 - 여러 컨테이너 운영, 장애 복구, 배포 자동화, 선언적 상태 관리
- 2교시 : Kubernetes 전체 그림 - cluster, node, control plane, worker node, kubelet, container runtime
- 3교시 : 로컬 Kubernetes 환경 준비 - kind 또는 minikube 설치, kubectl 연결, 단일 노드 클러스터 확인
- 4교시 : 로컬 multi-node 클러스터 구성 - control-plane/worker node 구성, `kubectl get nodes`로 여러 노드 확인
- 5교시 : kubectl 기본 - context, namespace, get, describe, logs, exec, apply, delete
- 6교시 : Helm 설치 및 기본 사용 - helm repo, search, install, upgrade, uninstall, release 개념
- 7교시 : 개인 면담 및 환경 점검 - Kubernetes 실행, kubectl context, Helm, multi-node 구성, 이미지 pull 문제 해결
- 8교시 : 구름 EXP 배움일기 - Kubernetes가 필요한 이유, cluster/node/control plane, kubectl/Helm에서 막힌 지점

## 2일차
- 1교시 : Day1 강의 10분 요약 + Deployment가 필요한 이유 - Pod 직접 실행의 한계, desired state, replica, self-healing
- 2교시 : Deployment manifest 구조 - apiVersion, kind, metadata, spec, selector, template
- 3교시 : 표준 MSA 앱의 api Deployment 배포 - 이미지 지정, replicas, labels, selector 확인
- 4교시 : Service가 필요한 이유 - Pod IP 변화, 안정적인 접근 주소, ClusterIP 개념
- 5교시 : Service manifest 구조와 연결 확인 - api Service 생성, exec/curl로 내부 통신 확인
- 6교시 : frontend와 api 연결 - service name DNS, container port, service port, targetPort 구분
- 7교시 : multi-node 배치 확인 - replica가 어떤 node에 배치되는지 확인, node 단위 장애 영향 범위 관찰
- 8교시 : 구름 EXP 배움일기 - Deployment/Service 역할, service name DNS, multi-node 배치, rollout/rollback 질문

## 3일차
- 1교시 : Day2 강의 10분 요약 + ConfigMap과 Secret이 필요한 이유 - 설정과 민감정보를 이미지에서 분리하는 운영 원칙
- 2교시 : ConfigMap 실습 - 환경변수 주입, 설정 변경, Pod 재시작 필요성 확인
- 3교시 : Secret 실습 - DB credential 주입, base64 오해, 저장소에 올리면 안 되는 정보
- 4교시 : Database를 Kubernetes에서 다루는 기본 관점 - Stateful workload의 어려움, local 실습과 운영 환경의 차이
- 5교시 : volume 기본 - emptyDir, hostPath 또는 local volume 개념, 데이터 보존과 삭제의 관계
- 6교시 : MSA 앱 전체 배포 - frontend, api, worker, database를 namespace 안에 배포
- 7교시 : Ingress Controller와 로드밸런싱 - Helm으로 ingress-nginx 설치, 외부 트래픽 진입점 구성
- 8교시 : 구름 EXP 배움일기 - ConfigMap/Secret 차이, Kubernetes에서 database를 다룰 때의 어려움, Ingress와 장애 분석 질문

## 4일차
- 1교시 : Day3 강의 10분 요약 + health probe와 서비스 안정성 - livenessProbe, readinessProbe, 잘못된 probe가 장애를 만드는 사례
- 2교시 : 리소스 요청과 제한 - requests, limits, CPU/Memory 압박, OOMKilled 개념
- 3교시 : autoscaler 개념과 실습 - HPA, metrics-server, replicas 자동 조정, 부하와 비용의 관계
- 4교시 : Istio와 Service Mesh 개념 - mTLS, traffic routing, retry/timeout, sidecar, 보안/트래픽 제어가 필요한 이유
- 5교시 : Istio 기본 실습 - Helm 또는 공식 설치 도구로 설치, sidecar injection, 트래픽 흐름 확인
- 6교시 : Kubernetes 운영 비용과 복잡도 - 직접 운영 vs managed Kubernetes, 클러스터 비용, 노드 비용, 플러그인 운영 부담
- 7교시 : 개인 면담 및 환경 점검 - Helm, Ingress Controller, HPA, Istio, manifest 문제 확인
- 8교시 : 구름 EXP 배움일기 - probe/resource/autoscaler/service mesh가 필요한 상황, plugin 설치에서 막힌 지점

## 5일차
- 1교시 : Day4 강의 10분 요약 + 4주차 통합 실습 - 3주차 MSA 앱을 Kubernetes 리소스로 배포하고 상태를 확인
- 2교시 : Grafana stack 설치 - Helm으로 kube-prometheus-stack 또는 Grafana/Prometheus 설치, 대시보드 접속
- 3교시 : Observability 기본 실습 - Pod/Node 메트릭, 서비스 상태, 리소스 사용량, 알림 개념 확인
- 4교시 : 장애 주입과 관찰 - 잘못된 이미지 태그, readiness 실패, 부하 증가를 metrics/logs/events로 확인
- 5교시 : 운영 Runbook 관점 - 배포 방법, Helm release, 확인 명령, 장애 확인 명령, rollback 절차
- 6교시 : Kubernetes 리소스 구조 - 플러그인 역할, 트래픽/보안/관찰 흐름, 장애 분석
- 7교시 : 5주차 AWS/Terraform Preview - 컴퓨팅 구성요소를 AWS 서비스로 확장하고 FinOps, Observability, IaC와 연결
- 8교시 : 구름 EXP 배움일기 - Kubernetes 리소스 구조, 플러그인 역할, AWS/Terraform으로 이어질 질문

## 4주차 학습 결과
- MSA 실습 앱을 배포할 Kubernetes manifest 세트
- namespace, deployment, service, configmap, secret, ingress 역할 설명 문서
- 로컬 multi-node 클러스터 구성과 node/pod 배치 확인 결과
- Helm으로 설치한 known plugin 목록과 release 상태
- Ingress Controller, autoscaler, Istio, Grafana stack 중 실습한 컴포넌트별 역할
- kubectl 기반 상태 확인 및 장애 분석 명령 모음
- rollout 또는 rollback 실습 흐름 1개
- Kubernetes 장애 주입, 관찰, 복구 흐름 1개
- 5주차 클라우드 서비스 매핑 학습 전 체크리스트

## 4주차 환경 준비 체크리스트
- 로컬 Kubernetes 클러스터 실행 가능
- kind 또는 minikube 기반 multi-node 클러스터 구성 가능
- `kubectl config current-context` 확인
- `kubectl get nodes`에서 여러 node 확인
- Helm 설치 및 chart install/uninstall 가능
- namespace 생성 가능
- Pod, Deployment, Service 생성 가능
- Pod가 어느 node에 배치됐는지 확인 가능
- `kubectl logs`, `kubectl describe`, `kubectl exec` 사용 가능
- MSA 실습 앱을 Kubernetes에서 실행 가능
- Service 또는 Ingress를 통해 frontend 접속 가능
- Ingress Controller 설치 및 라우팅 확인 가능
- metrics-server 또는 HPA 실습 가능
- Grafana/Prometheus 대시보드 접속 가능

# 5주차
## Keyword
- aws
- cloud service mapping
- compute
- network
- storage
- database
- finops
- observability
- managed service
- console
- cloudwatch
- cost explorer
- terraform
- iac
- state
- drift

## 5주차 목표
- 1주차에 배운 컴퓨팅 구성요소를 AWS 클라우드 서비스 이름과 역할로 확장한다.
- Compute, Network, Storage, Database, IAM, Observability, Billing 서비스를 인프라 관점에서 매핑한다.
- AWS Console을 이용해 직접 리소스를 만들고 연결하면서 수작업 구성의 흐름과 불편함을 체감한다.
- 비용이 발생하는 지점을 예측하고 Budget, Cost Explorer, 태그 기반 비용 관리의 필요성을 이해한다.
- CloudWatch Logs, Metrics, Alarm, Dashboard를 이용해 기본적인 관찰 가능성 실습을 수행한다.
- Terraform의 provider, resource, variable, output, state, plan/apply/destroy 흐름을 이해한다.
- AWS Console 구성 일부를 Terraform 코드로 재현하고, 변경 검토와 cleanup 절차를 이해한다.

## 5주차 운영 원칙
- 5주차 전반은 AWS Console 기준으로 진행하고, 후반은 동일한 구성을 Terraform/IaC 관점으로 전환한다.
- 모든 리소스는 정해진 리전과 공통 태그를 사용하고, 실습 종료 시 삭제 또는 중지 절차를 반드시 확인한다.
- FinOps와 Observability는 별도 이론으로 분리하지 않고, 리소스 선택과 운영 판단 안에 함께 다룬다.
- 복잡한 프로덕션 구성이 아니라 "AWS 서비스가 어떤 컴퓨팅 구성요소를 대체하거나 확장하는가"에 집중한다.
- 콘솔 수작업의 반복성, 누락 위험, 재현 어려움을 Terraform plan/state/drift 개념과 연결한다.
- 모든 Terraform apply 전 plan을 읽고, 실습 후 destroy 또는 잔여 리소스 확인을 수행한다.
- 1주차 첫 멘토링은 Day6로 이동한다. 2주차 이후에는 주차 상황에 따라 1일차 또는 4일차 후반을 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 사용할 수 있다.

## 1일차
- 1교시 : Week4 강의 10분 요약 + AWS 학습 목표 - 로컬 클러스터/컨테이너 운영 모델을 클라우드 서비스로 확장
- 2교시 : AWS 계정 및 리전 운영 점검 - 로그인, MFA, region, IAM 사용자/권한, Billing 접근 확인
- 3교시 : 컴퓨팅 구성요소와 AWS 서비스 매핑 - EC2, VPC, EBS, S3, RDS, ECS/EKS, CloudWatch 큰 그림
- 4교시 : FinOps 사전 안전장치 - Free Tier, Pricing Calculator, Budget, Cost Explorer, 태그 정책
- 5교시 : VPC와 네트워크 기본 - VPC, subnet, route table, internet gateway, security group, NACL 개념
- 6교시 : Console 기반 네트워크 실습 - 기본 VPC 확인 또는 실습 VPC 생성, subnet/security group 구성
- 7교시 : 개인 면담 및 환경 점검 - AWS 계정, 권한, Billing, Budget, 리전 설정 문제 해결
- 8교시 : 구름 EXP 배움일기 - AWS 서비스 매핑, 계정/리전/IAM/Billing, VPC와 security group 질문

## 2일차
- 1교시 : Day1 강의 10분 요약 + Compute 서비스 선택 기준 - EC2, ECS, EKS, Lambda의 역할과 운영 부담 비교
- 2교시 : EC2 Console 실습 - AMI, instance type, key pair, security group, user data, public IP
- 3교시 : EC2에 간단한 웹 서비스 실행 - 접속 확인, security group 포트, 로그 확인
- 4교시 : Load Balancing 개념 - ALB, target group, health check, listener, public/private 경계
- 5교시 : ALB Console 실습 - target group 생성, health check 확인, ALB로 웹 서비스 접속
- 6교시 : 컨테이너 실행 서비스 매핑 - Docker/Kubernetes 관점에서 ECS와 EKS가 해결하는 문제 비교
- 7교시 : ECS 또는 ECR 맛보기 - ECR repository, 이미지 push/pull 흐름 또는 ECS task/service 개념 확인
- 8교시 : 구름 EXP 배움일기 - EC2/ALB 구성 흐름, security group과 health check, ECS/ECR에서 다시 볼 질문

## 3일차
- 1교시 : Day2 강의 10분 요약 + Storage와 Database 서비스 선택 기준 - EBS, EFS, S3, RDS의 용도와 운영 책임 비교
- 2교시 : S3 Console 실습 - bucket 생성, 객체 업로드, public access block, 정적 파일 호스팅 개념
- 3교시 : RDS 개념과 비용 주의사항 - subnet group, security group, backup, Multi-AZ, storage 비용
- 4교시 : RDS Console 실습 또는 시뮬레이션 - DB 생성 흐름, 연결 정보, 보안 그룹, 삭제 보호 옵션 확인
- 5교시 : 애플리케이션 연결 관점 - connection string, secret 관리, private subnet, 접근 경로
- 6교시 : CloudWatch Logs 기본 - 로그 그룹, 로그 스트림, EC2/app 로그 수집 개념
- 7교시 : CloudWatch Metrics와 Alarm - CPU, network, ALB target health, threshold, notification 개념
- 8교시 : 구름 EXP 배움일기 - S3/RDS 선택 기준, connection string과 secret, CloudWatch 로그/지표 질문

## 4일차
- 1교시 : Day3 강의 10분 요약 + 운영 대시보드 기본 - CloudWatch Dashboard, 서비스별 핵심 지표, 장애 확인 순서
- 2교시 : FinOps 실습 - Cost Explorer, Budget 알림, 태그별 비용 추적, 리소스별 비용 발생 지점 확인
- 3교시 : 보안 운영 기본 - IAM 최소 권한, security group 검토, secret 노출 위험, public resource 점검
- 4교시 : 콘솔 작업의 한계 - 클릭 순서 누락, 설정값 불일치, 재현 어려움, 리뷰 불가능성
- 5교시 : Terraform 기본 개념 - provider, resource, variable, output, state, plan/apply/destroy
- 6교시 : Terraform 설치 및 인증 준비 - terraform version, AWS 인증, provider init, fmt, validate
- 7교시 : 개인 면담 및 환경 점검 - AWS 리소스 상태, 비용 알림, CloudWatch, Terraform init 문제 확인
- 8교시 : 구름 EXP 배움일기 - Dashboard/FinOps/IAM/Terraform 기본 개념, provider 인증에서 막힌 지점

## 5일차
- 1교시 : Day4 강의 10분 요약 + Terraform 전환 범위 결정 - 콘솔 설정값 목록화, 리소스 의존성, 변수화할 값, 민감정보 분리
- 2교시 : 작은 AWS 구성 코드화 - region, tag, security group, EC2 또는 S3 등 비용 통제 가능한 리소스
- 3교시 : Terraform plan 검토 - 변경 전 미리보기, 비용/보안/태그/관찰 가능성 누락 확인
- 4교시 : Terraform apply 및 검증 - Console, curl, CloudWatch, terraform state 비교
- 5교시 : 변경/drift/cleanup 실습 - tag 또는 rule 변경, plan 차이 확인, destroy 후 잔여 리소스 점검
- 6교시 : AWS 서비스 매핑 - 구성 절차, 비용/관찰 지점, Console vs Terraform 비교
- 7교시 : 전체 과정 연결 - Docker, MSA, Kubernetes, AWS, Terraform이 하나의 운영 흐름으로 연결되는 방식
- 8교시 : 구름 EXP 배움일기 - 전체 과정에서 연결된 개념, Terraform으로 이해한 재현성, 이후 더 공부할 질문

## 5주차 학습 결과
- AWS Console로 구성한 실습 아키텍처 다이어그램
- AWS 서비스 매핑 표 - compute, network, storage, database, observability, billing
- Budget 또는 비용 알림 설정 흐름
- CloudWatch Logs/Metrics/Alarm/Dashboard 실습 흐름
- 장애 주입 및 관찰 흐름 1개
- 콘솔 구성 절차와 설정값 목록
- Terraform 전환 대상 리소스 목록과 최소 Terraform 코드
- `terraform init/fmt/validate/plan/apply/destroy` 실행 흐름
- state, drift, secret, 비용 위험에 대한 운영 note
- 비용 발생 리소스 cleanup 체크리스트

## 5주차 환경 준비 체크리스트
- AWS Console 로그인 가능
- MFA 설정 확인
- 실습 리전 확정
- Billing, Budget, Cost Explorer 접근 가능
- 공통 태그 규칙 확인
- VPC, security group, EC2 또는 ECS 리소스 생성 가능
- CloudWatch Logs/Metrics/Alarm 접근 가능
- Terraform 설치 및 `terraform version` 확인
- AWS 인증을 Terraform provider에서 사용할 수 있음
- `terraform init`, `terraform fmt`, `terraform validate` 실행 가능
- `terraform plan` 결과를 읽고 변경 내용을 설명 가능
- 실습 종료 후 삭제/중지할 리소스 목록 확인
