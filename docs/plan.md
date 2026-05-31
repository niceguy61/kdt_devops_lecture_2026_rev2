# 개요

- 주차 : 6주
- 일별 수업 시간 : 일 8시간, 50분 수업 10분 휴식, 매 정시 시작
- 수업 범위 : Devops, Cloud(AWS), Docker, Kubernetes, MSA, IaC, Observability, Kubernetes Known plugins
- 과목 명 : Cloud Native
- 대상자 : 전공 막학기 학생, 비전공 취업준비생, 전직 개발자 (클라우드 직군 이직 희망자)

# 1주차

## keyword
- overview, mindset, cloud, devops, linux, network, git, ai, mini-project

## 1주차 목표
- Cloud Native를 배우는 이유와 DevOps 엔지니어의 역할을 이해한다.
- 로컬 컴퓨터에서 웹 서비스가 실행되고 접속되는 기본 흐름을 설명할 수 있다.
- GitHub, VS Code, Docker, AI Coding Tool 계정 생성, 설치, 로그인, 기본 동작 확인을 완료한다.
- 간단한 웹 애플리케이션을 만들고, 로컬 또는 Docker 환경에서 실행할 수 있다.
- 로그, 포트, 프로세스, HTTP 요청을 이용해 기본적인 문제 원인 분석을 수행한다.
- 비용, 보안, 공식 문서, 운영 지표를 기술 선택의 일부로 바라보는 습관을 만든다.

## 1주차 운영 원칙
- 계정 생성, 프로그램 설치, 로그인, 버전 확인은 수업 시간 안에서 천천히 함께 진행한다.
- 설치 자체를 과제로 넘기지 않고, 설치 중 발생하는 오류를 문제 해결 훈련의 일부로 다룬다.
- 모든 설치형 도구는 설치 후 바로 버전 확인 또는 Hello World 수준의 동작 확인까지 진행한다.
- 매주 1일차와 4일차 7~8교시는 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 둔다.

## 1일차

- 1교시 : 오리엔테이션 - 학습 과정 안내, 최종 목표, 6주간 만들 산출물 소개
- 2교시 : Cloud Native 학습 마인드셋 - 문제 해결 프로세스, 도구 선택법, 도구를 이해한다는 것의 의미
- 3교시 : 클라우드란 무엇인가? - 로컬 컴퓨터, 데이터센터, 호스팅, 클라우드의 차이
- 4교시 : DevOps란 무엇인가? - 개발 라이프사이클, 배포, 운영, 피드백 루프, 협업 문화
- 5교시 : GitHub 계정 생성, Git SCM 설치 및 VS Code 설치 - 계정 생성, 이메일 인증, Git 설치, VS Code 설치, 터미널 열기
- 6교시 : Git/GitHub 기본 실습 - git 설치 확인, repository 생성, clone, commit, push, README 수정
- 7교시 : 개인 면담 및 환경 점검 - 설치 상태 확인, 배경 지식 파악, 개인 목표 정리
- 8교시 : 개인 면담 및 보충 실습 - GitHub, VS Code, Git 설정 문제 해결

## 2일차

- 1교시 : 컴퓨팅의 기본 - CPU, Memory, Disk, Network, Process가 애플리케이션과 만나는 방식
- 2교시 : Linux/CLI 기본 - pwd, ls, cd, cat, grep, curl, ps, kill, 환경변수, 권한
- 3교시 : 웹 서비스의 기본 흐름 - Browser, DNS, IP, TCP, HTTP, Server, Response
- 4교시 : 포트와 프로세스 - localhost, 0.0.0.0, port binding, listen 상태 확인
- 5교시 : 로컬 웹 서버 실행 준비 - 필요한 런타임 설치 여부 확인, 샘플 앱 내려받기, 실행 명령 확인
- 6교시 : 로컬 웹 서버 실행 실습 - 브라우저와 curl로 접속 확인, 포트 충돌 상황 관찰
- 7교시 : 로그와 설정의 기본 - stdout 로그, 에러 메시지 읽기, config, secret, .env 개념
- 8교시 : 원인 분석 기본 라이프사이클 - 재현, 관찰, 가설, 검증, 수정, 기록

## 3일차

- 1교시 : 배포란 무엇인가? - 내 컴퓨터에서만 되는 프로그램과 다른 사람이 접속 가능한 서비스의 차이
- 2교시 : 배포 사이클 - 개발, 빌드, 테스트, 패키징, 배포, 모니터링, 피드백
- 3교시 : 개발자가 보는 인프라 vs 인프라 엔지니어가 보는 인프라 - 안정성, 확장성, 비용, 보안 관점
- 4교시 : 재현 가능한 인프라의 필요성 - 문서, 스크립트, IaC의 개념과 설계도 작성의 중요성
- 5교시 : Docker가 필요한 이유 - 로컬 환경 차이, 의존성 충돌, 배포 단위, 실행 환경 표준화
- 6교시 : 프로젝트 구성요소와 3-tier 아키텍처 - 웹 애플리케이션, 데이터베이스, 캐시, 로드 밸런서, 관찰 지점 이해
- 7교시 : AI Coding Tool 학습/실습 준비 - 계정/설치 확인, 페르소나/Agent/Skill 활용, 단계별 개념 설명, 에러 메시지 기반 디버깅 요청, 공식 문서/전문가 크로스체크
- 8교시 : AI Coding Tool 실습 - 무료 범위의 싱글 프론트엔드 앱 제작, 더미 JSON 데이터, 생성 코드 구조와 운영성 점검

### 챌린지 룰
- 단순한 Hello World가 아닌 내가 실제로 필요하다고 느끼는 기능을 만든다.
- 이번 챌린지는 HTML/CSS/JavaScript 중심의 싱글 프론트엔드 앱으로 제한한다.
- 데이터베이스는 사용하지 않고, 데이터베이스나 외부 API에서 가져와야 할 데이터는 `data/*.json` 같은 더미 JSON으로 대체한다.
- 백엔드 서버 코드는 만들지 않고, 정적 파일을 `python3 -m http.server` 같은 방식으로 확인한다.
- 유료 AI 구독, 로컬 LLM, 유료 API, 비용 청구 서비스는 필수로 요구하지 않는다.
- 유료화 API 또는 비용 청구 가능성이 있는 서비스는 사용하지 않는다. 단, 본인이 이미 승인받았고 quota 내에서 비용이 청구되지 않는 경우는 선택적으로 허용한다.
- 외부 API가 반드시 필요한 아이디어는 이번 시간에는 더미 JSON으로 표현한다.
- 기본 기능 구조는 최대 2시간 안에 만들 수 있는 범위로 제한한다.
- GitHub 저장소에 코드와 README를 올린다.
- README에는 실행 방법, 사용한 AI 도구 또는 강사 제공 템플릿 여부, 주요 프롬프트, 더미 JSON 수정 방법, 제외한 기능, 막힌 점, 해결 과정을 적는다.
- 로컬 브라우저에서 실행 가능해야 하며, 가능하면 Docker로도 실행할 수 있게 만든다.
- 최소 1개의 에러 상황 또는 범위 조정 기록을 설명할 수 있어야 한다.
- 별도의 평가 점수는 없으며, 기본 프로젝트와 심화 프로젝트 아이디어 후보로 활용한다.

## 4일차

- 1교시 : 클라우드 기본 구성 요소 - Region, AZ, Compute, Storage, Network, IAM의 큰 그림
- 2교시 : 클라우드 서비스 모델 - IaaS, PaaS, SaaS, Managed Service, Shared Responsibility Model
- 3교시 : AWS 계정 생성 전 안내 - 과금 구조, Free Tier, 결제 수단, MFA, root 계정 주의사항
- 4교시 : AWS 계정 생성 및 보안 기본 설정 - 계정 생성, MFA 설정, Billing 알림 확인, 콘솔 로그인
- 5교시 : 클라우드 비용 관리 기본 - 데이터센터 비용과 클라우드 비용 비교, 사용량 기반 과금, 낭비 사례
- 6교시 : 보안 기본 원칙과 공식 Documentation 읽는 법 - 최소 권한, secret 관리, AI 답변 검증, 버전과 전제 조건 확인
- 7교시 : 개인 면담 및 환경 점검 - AWS 계정, MFA, Billing 알림, Docker 실행 상태 확인
- 8교시 : 프로젝트 아이디어 면담 - 만들고 싶은 서비스, 필요한 리소스, 예상 위험 요소 정리

## 5일차

- 1교시 : Devops Mindset 원칙 Remind
- 2교시 : 클라우드 아키텍처의 기본 원칙 - AWS Well-Architected Framework 소개
- 3교시 : DORA Metric 소개 - 배포 빈도, 변경 리드 타임, 변경 실패율, 복구 시간
- 4교시 : 미니 챌린지 진행 - 무료 범위의 싱글 프론트엔드 앱 기능 완성, 더미 JSON 수정, 로컬 실행 확인
- 5교시 : 1주차 통합 체크리스트 작성 - 실행 방법, 포트, 로그, 환경변수, README, 장애 분석 기록 점검
- 6교시 : 미니 챌린지 간이 발표 - 문제, 해결 아이디어, 구현 방식, 실행 방법, 막힌 점, 배운 점
- 7교시 : 발표 피드백 및 라이브 Q&A - 기술 피드백, 프로젝트 후보 아이디어 선별, 설치/계정 문제 잔여 해결
- 8교시 : 차주 수업내용 Overview (Docker)

## 1주차 산출물
- GitHub 저장소 1개
- README.md 1개
- 브라우저에서 실행 가능한 싱글 프론트엔드 미니 웹 애플리케이션 1개
- 3-tier 관점의 Architecture Note 1개
- AI 개념 학습 사다리와 디버깅 요청 예시 1개
- 더미 JSON 데이터 파일 1개 이상
- 로컬 정적 서버 실행 명령 또는 Docker 실행 명령
- 간단한 장애 분석 기록 1개
- 2주차 Docker 학습 전 개인 체크리스트

## 1주차 환경 준비 체크리스트
- GitHub 계정 생성, 이메일 인증, repository 생성
- Git 설치 및 `git --version` 확인
- VS Code 설치, 터미널 실행, 프로젝트 폴더 열기
- Docker Desktop 설치는 2주 1일차에 진행한다는 것을 안내하고, 1주차에는 설치를 요구하지 않음
- AI Coding Tool 계정 생성 또는 로그인, 간단한 프롬프트 실행 확인
- AWS 계정 생성, MFA 설정, Billing 알림 또는 비용 확인 화면 접근
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
- Docker가 해결하려는 문제와 컨테이너 실행 모델을 이해한다.
- 이미지와 컨테이너의 차이를 설명하고 기본 명령어로 컨테이너 생명주기를 다룬다.
- Dockerfile을 작성해 간단한 웹 애플리케이션 이미지를 직접 빌드한다.
- 포트 바인딩, 볼륨, 환경변수, 네트워크를 이용해 컨테이너 실행 방식을 제어한다.
- Docker Compose로 웹 애플리케이션과 데이터베이스를 함께 실행한다.
- 컨테이너 로그와 상태를 확인하고 기본적인 장애 원인을 분석한다.

## 2주차 운영 원칙
- 강사가 제공하는 표준 실습 애플리케이션을 Docker 실습의 기본 재료로 사용한다.
- 실습 애플리케이션은 GitHub 또는 압축 파일로 내려받을 수 있게 제공하고, 완성 이미지는 Docker Hub에 게시한다.
- 학생 개인의 1주차 미니 웹 애플리케이션은 추가 도전 과제 또는 보충 실습 재료로 활용한다.
- Docker 명령어는 암기보다 "무엇을 확인하려는 명령인지"를 기준으로 가르친다.
- 매 실습마다 실행, 확인, 중지, 정리까지 한 사이클로 진행한다.
- 매주 1일차와 4일차 7~8교시는 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 둔다.

## 1일차
- 1교시 : 1주차 복습 및 Docker 학습 목표 - 로컬 실행 문제, 배포 문제, 환경 차이 문제 정리
- 2교시 : Docker Desktop 설치 및 계정 확인 - 공식 문서 기준 설치, Docker Hub 로그인, 권한/가상화 이슈 기록
- 3교시 : Docker의 컨셉과 작동 방식 - image, container, registry, Docker Engine, Docker Desktop
- 4교시 : Docker vs Local Computer - 좋아지는 점, 나빠지는 점, 언제 Docker를 쓰지 말아야 하는지
- 5교시 : Docker 기본 명령어 1 - docker version, pull, images, run, ps, stop, rm
- 6교시 : Hello World, nginx, 표준 실습 앱 첫 실행 - 컨테이너 실행, Docker Hub pull, 브라우저 접속, curl 확인
- 7교시 : 개인 면담 및 환경 점검 - Docker Desktop 실행, WSL/가상화, 권한, 로그인 문제 해결
- 8교시 : 보충 실습 - 기본 명령어 재실습, 막힌 학생 진도 회복

## 2일차
- 1교시 : 이미지와 레이어의 이해 - base image, layer, cache, tag, digest의 기본 개념
- 2교시 : Dockerfile 기본 문법 - FROM, WORKDIR, COPY, RUN, CMD, EXPOSE
- 3교시 : 표준 실습 앱 소스코드 다운로드 - GitHub clone 또는 압축 파일 다운로드, 로컬 실행 구조 확인
- 4교시 : 표준 실습 앱 이미지 만들기 - Dockerfile 작성, docker build, docker run
- 5교시 : 이미지 빌드 문제 해결 - build context, .dockerignore, 캐시, 경로 오류, 권한 오류
- 6교시 : 컨테이너 실행 검증 - 포트 접속, 로그 확인, 컨테이너 내부 파일 확인
- 7교시 : 이미지 태그와 Docker Hub - tag, login, push, pull, 공개 이미지 사용 시 주의사항
- 8교시 : 실습 정리 - README에 Docker build/run 명령 추가

## 3일차
- 1교시 : 컨테이너 네트워크 기본 - bridge network, localhost 오해, container name, DNS
- 2교시 : 포트 바인딩 실습 - host port와 container port, 포트 충돌, 여러 컨테이너 실행
- 3교시 : 환경변수와 설정 주입 - -e 옵션, .env 파일, secret을 이미지에 넣으면 안 되는 이유
- 4교시 : 볼륨과 데이터 보존 - bind mount, named volume, 컨테이너 삭제와 데이터의 관계
- 5교시 : 데이터베이스 컨테이너 실행 - PostgreSQL 또는 MySQL 실행, 환경변수, 볼륨 연결
- 6교시 : 웹 앱과 DB 연결 개념 - connection string, host, port, credential, 네트워크 확인
- 7교시 : 장애 분석 실습 - 접속 실패, 포트 충돌, 환경변수 누락, 로그 기반 원인 분석
- 8교시 : 장애 분석 기록 작성 - 재현, 관찰, 가설, 검증, 수정 내용을 README 또는 기록 파일에 정리

## 4일차
- 1교시 : Docker Compose가 필요한 이유 - 여러 컨테이너 실행 명령을 파일로 관리하는 방식
- 2교시 : compose.yaml 기본 구조 - services, image, build, ports, environment, volumes, networks
- 3교시 : 웹 애플리케이션 + DB Compose 실습 - compose up/down, logs, ps, exec
- 4교시 : Compose 네트워크와 서비스 이름 - 컨테이너 간 통신, depends_on의 의미와 한계
- 5교시 : 개발 환경용 Compose 구성 - bind mount, hot reload, env_file, local-only 설정
- 6교시 : Compose 장애 분석 - DB 준비 전 앱 실행, 잘못된 포트, 잘못된 환경변수, 볼륨 초기화 이슈
- 7교시 : 개인 면담 및 환경 점검 - Dockerfile, Compose, Docker Hub, 표준 실습 앱 실행 상태 확인
- 8교시 : 보충 실습 - Compose 실습 진도 회복, 개인 프로젝트 Docker 실행 문제 해결

## 5일차
- 1교시 : Docker 운영 관점 정리 - 컨테이너는 VM이 아니다, 상태 없는 앱, immutable image
- 2교시 : 좋은 Dockerfile 작성 원칙 - 작은 이미지, 명확한 실행 명령, .dockerignore, secret 제외
- 3교시 : 컨테이너 보안 기초 - root 실행 주의, 이미지 출처, 태그 고정, 취약 이미지, secret 관리
- 4교시 : 이미지 배포 흐름 - build, tag, push, pull, run으로 보는 배포 파이프라인
- 5교시 : 2주차 통합 실습 - 표준 실습 앱을 Dockerfile과 Compose로 실행 가능하게 정리
- 6교시 : 2주차 발표 - Docker로 실행하는 방법, 겪은 장애, 해결 과정, 남은 문제 공유
- 7교시 : 발표 피드백 및 라이브 Q&A - Dockerfile/Compose 개선점, 다음 주차 클라우드 배포 연결
- 8교시 : 차주 수업내용 Overview - AWS 기반 배포 또는 Kubernetes 진입 전 필요한 개념 정리

## 2주차 산출물
- 표준 실습 애플리케이션용 Dockerfile
- compose.yaml 1개
- Docker build/run/compose 실행 명령이 포함된 README.md
- Docker Hub에서 내려받아 실행한 표준 이미지 1개
- 직접 빌드한 로컬 이미지 태그 1개
- 포트, 로그, 환경변수, 볼륨 중 하나 이상을 포함한 장애 분석 기록 1개
- 3주차 학습 전 Docker 체크리스트

## 2주차 환경 준비 체크리스트
- Docker Desktop 정상 실행
- `docker version` 확인
- `docker run hello-world` 성공
- `docker run -p 8080:80 nginx` 실행 후 브라우저 접속 확인
- Docker Hub 로그인 또는 표준 실습 앱 이미지 pull 가능 상태 확인
- 표준 실습 앱 소스코드 다운로드 가능 상태 확인
- Dockerfile build 성공
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
- 개발자가 만든 서비스를 인프라에서 실행하기 위해 필요한 정보와 요청사항을 정리할 수 있다.
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
- 매 실습마다 "인프라 관점에서 좋아진 점"과 "운영 관점에서 어려워진 점"을 함께 기록한다.
- 매주 1일차와 4일차 7~8교시는 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 둔다.

## 1일차
- 1교시 : 2주차 복습 및 3주차 학습 목표 - 단일 컨테이너 앱에서 여러 서비스 앱으로 확장되는 흐름
- 2교시 : Monolith vs MSA - 배포 단위, 장애 영향 범위, 네트워크 의존성, 운영 복잡도 비교
- 3교시 : 인프라 엔지니어가 MSA에서 알아야 할 것 - 서비스 목록, 포트, 프로토콜, 의존성, 설정, 헬스체크, 로그 위치
- 4교시 : 표준 MSA 실습 앱 토폴로지 소개 - frontend, api, worker, database 역할과 요청 흐름
- 5교시 : 실습 앱 다운로드 및 실행 준비 - GitHub clone 또는 압축 파일 다운로드, 운영 문서와 폴더 구조 확인
- 6교시 : Docker Compose로 전체 서비스 실행 - compose up, ps, logs, 브라우저 접속, 서비스 상태 확인
- 7교시 : 개인 면담 및 환경 점검 - Compose 실행, 포트 충돌, 이미지 pull/build 문제 해결
- 8교시 : 보충 실습 - 전체 서비스 실행 실패 학생 진도 회복

## 2일차
- 1교시 : 서비스 간 통신을 보는 법 - endpoint, protocol, status code, latency, dependency map
- 2교시 : frontend와 api 연결 운영 관점 - API URL, CORS 이슈를 개발팀과 협업해 확인하는 방법
- 3교시 : 컨테이너 네트워크 복습 - localhost 오해, service name DNS, 내부 포트와 외부 포트
- 4교시 : api와 database 연결 운영 관점 - connection string, credential, migration, 초기 데이터, 접근 권한
- 5교시 : 서비스 실행 순서 문제 - depends_on의 의미와 한계, DB readiness, 재시도 필요성
- 6교시 : health check 기본 - /health endpoint, liveness/readiness 차이, 장애 감지 기준
- 7교시 : 연결 실패 장애 분석 - 잘못된 API URL, DB host 오류, 포트 오류, 환경변수 누락 찾기
- 8교시 : 개발팀에 전달할 장애 리포트 작성 - 재현 조건, 관찰 결과, 의심 지점, 필요한 수정 요청 정리

## 3일차
- 1교시 : 서비스 분리와 데이터 의존성 - DB 공유의 위험, 서비스별 데이터 책임, 장애 영향 범위
- 2교시 : worker 서비스 운영 관점 - 비동기 처리, 배치 작업, 오래 걸리는 작업이 인프라에 주는 영향
- 3교시 : queue 또는 redis 운영 개념 - 동기 호출과 비동기 처리의 차이, 병목과 적체를 관찰하는 방법
- 4교시 : worker/queue 실습 - 요청 생성, 작업 처리, 로그와 상태로 처리 흐름 확인
- 5교시 : 장애 전파와 부분 장애 - api 장애, DB 장애, worker 장애가 사용자 경험과 운영 대응에 미치는 영향
- 6교시 : timeout과 retry 기본 - 무한 대기 방지, 재시도의 위험, 중복 처리 문제, 개발팀과 합의할 값
- 7교시 : 로그 분산 문제 - 여러 서비스 로그 보기, correlation id 또는 request id를 개발팀에 요구해야 하는 이유
- 8교시 : 관찰 가능성 기초 실습 - compose logs, 서비스별 로그 필터링, 요청 흐름 추적

## 4일차
- 1교시 : MSA 설정 관리 - 환경변수, .env, config 분리, secret을 코드에 넣지 않는 이유
- 2교시 : MSA 로컬 개발 환경 - hot reload, bind mount, dev/prod compose 분리 개념
- 3교시 : API 계약과 운영 문서 - OpenAPI/Swagger 개념, 인프라가 알아야 할 endpoint, health, dependency 정보
- 4교시 : 버전 관리와 배포 협업 - 이미지 태그, 하위 호환, 배포 순서, rollback 가능성
- 5교시 : MSA 운영 비용 정리 - 배포 단위 증가, 로그 증가, 네트워크 장애, 모니터링/알림 복잡도
- 6교시 : Kubernetes가 필요한 이유 - 여러 컨테이너를 수동으로 관리할 때의 한계, 선언적 운영의 필요성
- 7교시 : 개인 면담 및 환경 점검 - MSA 실습 앱 실행 상태, Compose 설정, 로그 분석 기록 확인
- 8교시 : 보충 실습 - 서비스 연결 문제, DB 초기화 문제, worker 실행 문제 해결

## 5일차
- 1교시 : 3주차 통합 실습 안내 - MSA 실습 앱을 인프라 운영 문서 기준으로 점검
- 2교시 : 배포 설정 변경 실습 - 이미지 태그, 환경변수, 포트, 서비스 개수 조정을 Compose 수준에서 확인
- 3교시 : 이미지 재빌드와 Compose 재실행 - 변경된 서비스만 build, up, logs로 확인
- 4교시 : 장애 주입 실습 - 일부 서비스 중지, 잘못된 환경변수 설정, DB 연결 실패 상황 만들기
- 5교시 : 장애 복구 실습 - 원인 분석, 설정 복구, 서비스 재시작, 개발팀 전달사항 정리
- 6교시 : 3주차 발표 - 서비스 토폴로지, 실행 조건, 발생한 장애, 운영 대응, Kubernetes가 필요해지는 지점 설명
- 7교시 : 발표 피드백 및 라이브 Q&A - 인프라/개발 협업 요청사항, 운영 복잡도, 다음 주차 Kubernetes 연결
- 8교시 : 차주 수업내용 Overview - Kubernetes의 Pod, Deployment, Service, ConfigMap, Secret이 등장하는 이유

## 3주차 산출물
- MSA 실습 애플리케이션 실행 가능한 compose.yaml
- frontend, api, worker, database 요청 흐름과 의존성 설명 문서 또는 다이어그램
- 서비스별 실행 조건 정리 - 이미지, 포트, 환경변수, 의존 서비스, health check
- 배포 설정 또는 환경 설정 변경 내역
- 장애 주입 및 복구 기록 1개
- 개발팀에 전달할 장애 리포트 또는 운영 개선 요청서 1개
- 인프라 관점에서 본 MSA의 장점과 운영 비용을 정리한 회고 기록
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
- rollout, rollback, scaling, self-healing을 실습하고 운영 관점의 장단점을 정리한다.
- 5주차 AWS 서비스, 비용 관리, 관찰 가능성 수업으로 이어질 수 있도록 Kubernetes와 클라우드 서비스의 연결 지점을 이해한다.

## 4주차 운영 원칙
- Kubernetes를 YAML 암기 수업으로 만들지 않고, MSA 운영 문제를 해결하는 선언적 운영 모델로 다룬다.
- 실습 환경은 multi-node 구성이 가능한 kind 또는 minikube를 우선 표준으로 정하고, Docker Desktop Kubernetes는 fallback으로 둔다.
- 처음에는 managed Kubernetes가 아니라 로컬 Kubernetes로 개념과 kubectl 사용법을 익힌다.
- 로컬 multi-node 클러스터가 실제 여러 서버 운영 환경을 완전히 대체하지는 않지만, Pod 배치, 노드 상태, 장애 영향 범위를 테스트할 수 있음을 명확히 설명한다.
- Kubernetes known plugin은 깊은 튜닝보다 설치 이유, 핵심 리소스, 운영 효과, 장애 확인 방법을 중심으로 다룬다.
- Helm은 플러그인 설치를 쉽게 하기 위한 패키지 매니저로 도입하고, chart 구조를 깊게 작성하는 것은 후순위로 둔다.
- 매 실습마다 manifest 작성, apply, 상태 확인, 로그 확인, 삭제 또는 복구까지 한 사이클로 진행한다.
- 매주 1일차와 4일차 7~8교시는 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 둔다.

## 1일차
- 1교시 : 3주차 복습 및 Kubernetes가 필요한 이유 - 여러 컨테이너 운영, 장애 복구, 배포 자동화, 선언적 상태 관리
- 2교시 : Kubernetes 전체 그림 - cluster, node, control plane, worker node, kubelet, container runtime
- 3교시 : 로컬 Kubernetes 환경 준비 - kind 또는 minikube 설치, kubectl 연결, 단일 노드 클러스터 확인
- 4교시 : 로컬 multi-node 클러스터 구성 - control-plane/worker node 구성, `kubectl get nodes`로 여러 노드 확인
- 5교시 : kubectl 기본 - context, namespace, get, describe, logs, exec, apply, delete
- 6교시 : Helm 설치 및 기본 사용 - helm repo, search, install, upgrade, uninstall, release 개념
- 7교시 : 개인 면담 및 환경 점검 - Kubernetes 실행, kubectl context, Helm, multi-node 구성, 이미지 pull 문제 해결
- 8교시 : 보충 실습 - 로컬 클러스터 실행 실패 학생 진도 회복

## 2일차
- 1교시 : Deployment가 필요한 이유 - Pod 직접 실행의 한계, desired state, replica, self-healing
- 2교시 : Deployment manifest 작성 - apiVersion, kind, metadata, spec, selector, template
- 3교시 : 표준 MSA 앱의 api Deployment 배포 - 이미지 지정, replicas, labels, selector 확인
- 4교시 : Service가 필요한 이유 - Pod IP 변화, 안정적인 접근 주소, ClusterIP 개념
- 5교시 : Service manifest 작성 및 연결 확인 - api Service 생성, exec/curl로 내부 통신 확인
- 6교시 : frontend와 api 연결 - service name DNS, container port, service port, targetPort 구분
- 7교시 : multi-node 배치 확인 - replica가 어떤 node에 배치되는지 확인, node 단위 장애 영향 범위 관찰
- 8교시 : rollout과 rollback - 이미지 태그 변경, rollout status, history, undo 실습

## 3일차
- 1교시 : ConfigMap과 Secret이 필요한 이유 - 설정과 민감정보를 이미지에서 분리하는 운영 원칙
- 2교시 : ConfigMap 실습 - 환경변수 주입, 설정 변경, Pod 재시작 필요성 확인
- 3교시 : Secret 실습 - DB credential 주입, base64 오해, 저장소에 올리면 안 되는 정보 정리
- 4교시 : Database를 Kubernetes에서 다루는 기본 관점 - Stateful workload의 어려움, local 실습과 운영 환경의 차이
- 5교시 : volume 기본 - emptyDir, hostPath 또는 local volume 개념, 데이터 보존과 삭제의 관계
- 6교시 : MSA 앱 전체 배포 - frontend, api, worker, database를 namespace 안에 배포
- 7교시 : Ingress Controller와 로드밸런싱 - Helm으로 ingress-nginx 설치, 외부 트래픽 진입점 구성
- 8교시 : 장애 분석 실습 - selector 불일치, 이미지 태그 오류, 포트 오류, CrashLoopBackOff, node 배치 문제 확인

## 4일차
- 1교시 : health probe와 서비스 안정성 - livenessProbe, readinessProbe, 잘못된 probe가 장애를 만드는 사례
- 2교시 : 리소스 요청과 제한 - requests, limits, CPU/Memory 압박, OOMKilled 개념
- 3교시 : autoscaler 개념과 실습 - HPA, metrics-server, replicas 자동 조정, 부하와 비용의 관계
- 4교시 : Istio와 Service Mesh 개념 - mTLS, traffic routing, retry/timeout, sidecar, 보안/트래픽 제어가 필요한 이유
- 5교시 : Istio 기본 실습 - Helm 또는 공식 설치 도구로 설치, sidecar injection, 트래픽 흐름 확인
- 6교시 : Kubernetes 운영 비용과 복잡도 - 직접 운영 vs managed Kubernetes, 클러스터 비용, 노드 비용, 플러그인 운영 부담
- 7교시 : 개인 면담 및 환경 점검 - Helm, Ingress Controller, HPA, Istio, manifest 문제 확인
- 8교시 : 보충 실습 - 배포 실패, 네트워크 연결 실패, plugin 설치 실패, 이미지 pull 문제 해결

## 5일차
- 1교시 : 4주차 통합 실습 안내 - 3주차 MSA 앱을 Kubernetes 리소스로 배포하고 상태를 설명
- 2교시 : Grafana stack 설치 - Helm으로 kube-prometheus-stack 또는 Grafana/Prometheus 설치, 대시보드 접속
- 3교시 : Observability 기본 실습 - Pod/Node 메트릭, 서비스 상태, 리소스 사용량, 알림 개념 확인
- 4교시 : 장애 주입과 관찰 - 잘못된 이미지 태그, readiness 실패, 부하 증가를 metrics/logs/events로 확인
- 5교시 : 운영 문서 작성 - 배포 방법, Helm release, 확인 명령, 장애 확인 명령, rollback 절차 정리
- 6교시 : 4주차 발표 - Kubernetes 리소스 구조, 플러그인 역할, 트래픽/보안/관찰 흐름, 장애 분석 설명
- 7교시 : 발표 피드백 및 라이브 Q&A - manifest와 Helm 개선점, 플러그인 운영 위험, 클라우드 이전 시 고려사항
- 8교시 : 차주 수업내용 Overview - 컴퓨팅 구성요소를 AWS 서비스로 확장하고 FinOps, Observability와 연결

## 4주차 산출물
- MSA 실습 앱을 배포할 Kubernetes manifest 세트
- namespace, deployment, service, configmap, secret, ingress 역할 설명 문서
- 로컬 multi-node 클러스터 구성 기록과 node/pod 배치 확인 결과
- Helm으로 설치한 known plugin 목록과 release 상태 기록
- Ingress Controller, autoscaler, Istio, Grafana stack 중 실습한 컴포넌트별 역할 정리
- kubectl 기반 상태 확인 및 장애 분석 명령 모음
- rollout 또는 rollback 실습 기록 1개
- Kubernetes 장애 주입, 관찰, 복구 기록 1개
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

## 5주차 목표
- 1주차에 배운 컴퓨팅 구성요소를 AWS 클라우드 서비스 이름과 역할로 확장한다.
- Compute, Network, Storage, Database, IAM, Observability, Billing 서비스를 인프라 관점에서 매핑한다.
- AWS Console을 이용해 직접 리소스를 만들고 연결하면서 수작업 구성의 흐름과 불편함을 체감한다.
- 비용이 발생하는 지점을 예측하고 Budget, Cost Explorer, 태그 기반 비용 관리의 필요성을 이해한다.
- CloudWatch Logs, Metrics, Alarm, Dashboard를 이용해 기본적인 관찰 가능성 실습을 수행한다.
- 6주차 Terraform IaC로 전환하기 위해 콘솔 작업 절차, 설정값, 의존 관계를 문서화한다.

## 5주차 운영 원칙
- 5주차 실습은 AWS Console 기준으로 진행한다.
- 모든 리소스는 정해진 리전과 공통 태그를 사용하고, 실습 종료 시 삭제 또는 중지 절차를 반드시 확인한다.
- FinOps와 Observability는 별도 이론으로 분리하지 않고, 리소스 선택과 운영 판단 안에 함께 다룬다.
- 복잡한 프로덕션 구성이 아니라 "AWS 서비스가 어떤 컴퓨팅 구성요소를 대체하거나 확장하는가"에 집중한다.
- 콘솔 수작업의 반복성, 누락 위험, 재현 어려움을 기록해 6주차 IaC 전환의 근거로 사용한다.
- 매주 1일차와 4일차 7~8교시는 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 둔다.

## 1일차
- 1교시 : 4주차 복습 및 AWS 학습 목표 - 로컬 클러스터/컨테이너 운영 모델을 클라우드 서비스로 확장
- 2교시 : AWS 계정 및 리전 운영 점검 - 로그인, MFA, region, IAM 사용자/권한, Billing 접근 확인
- 3교시 : 컴퓨팅 구성요소와 AWS 서비스 매핑 - EC2, VPC, EBS, S3, RDS, ECS/EKS, CloudWatch 큰 그림
- 4교시 : FinOps 사전 안전장치 - Free Tier, Pricing Calculator, Budget, Cost Explorer, 태그 정책
- 5교시 : VPC와 네트워크 기본 - VPC, subnet, route table, internet gateway, security group, NACL 개념
- 6교시 : Console 기반 네트워크 실습 - 기본 VPC 확인 또는 실습 VPC 생성, subnet/security group 구성
- 7교시 : 개인 면담 및 환경 점검 - AWS 계정, 권한, Billing, Budget, 리전 설정 문제 해결
- 8교시 : 보충 실습 - 콘솔 접근, MFA, 예산 알림, 네트워크 구성 진도 회복

## 2일차
- 1교시 : Compute 서비스 선택 기준 - EC2, ECS, EKS, Lambda의 역할과 운영 부담 비교
- 2교시 : EC2 Console 실습 - AMI, instance type, key pair, security group, user data, public IP
- 3교시 : EC2에 간단한 웹 서비스 실행 - 접속 확인, security group 포트, 로그 확인
- 4교시 : Load Balancing 개념 - ALB, target group, health check, listener, public/private 경계
- 5교시 : ALB Console 실습 - target group 생성, health check 확인, ALB로 웹 서비스 접속
- 6교시 : 컨테이너 실행 서비스 매핑 - Docker/Kubernetes 관점에서 ECS와 EKS가 해결하는 문제 비교
- 7교시 : ECS 또는 ECR 맛보기 - ECR repository, 이미지 push/pull 흐름 또는 ECS task/service 개념 확인
- 8교시 : 운영 문서 작성 - EC2/ALB 구성값, 접속 경로, health check, 보안 그룹 규칙 기록

## 3일차
- 1교시 : Storage와 Database 서비스 선택 기준 - EBS, EFS, S3, RDS의 용도와 운영 책임 비교
- 2교시 : S3 Console 실습 - bucket 생성, 객체 업로드, public access block, 정적 파일 호스팅 개념
- 3교시 : RDS 개념과 비용 주의사항 - subnet group, security group, backup, Multi-AZ, storage 비용
- 4교시 : RDS Console 실습 또는 시뮬레이션 - DB 생성 흐름, 연결 정보, 보안 그룹, 삭제 보호 옵션 확인
- 5교시 : 애플리케이션 연결 관점 - connection string, secret 관리, private subnet, 접근 경로 정리
- 6교시 : CloudWatch Logs 기본 - 로그 그룹, 로그 스트림, EC2/app 로그 수집 개념
- 7교시 : CloudWatch Metrics와 Alarm - CPU, network, ALB target health, threshold, notification 개념
- 8교시 : Observability 기록 작성 - 어떤 지표와 로그를 봐야 장애를 빨리 찾을 수 있는지 정리

## 4일차
- 1교시 : 운영 대시보드 기본 - CloudWatch Dashboard, 서비스별 핵심 지표, 장애 확인 순서
- 2교시 : FinOps 실습 - Cost Explorer, Budget 알림, 태그별 비용 추적, 리소스별 비용 발생 지점 확인
- 3교시 : 보안 운영 기본 - IAM 최소 권한, security group 검토, secret 노출 위험, public resource 점검
- 4교시 : 장애 주입과 관찰 - security group 포트 차단, target health 실패, 인스턴스 중지 후 CloudWatch/ALB 확인
- 5교시 : 콘솔 작업의 한계 정리 - 클릭 순서 누락, 설정값 불일치, 재현 어려움, 리뷰 불가능성
- 6교시 : IaC가 필요한 이유 - 5주차 콘솔 구성을 Terraform으로 옮길 때의 이점과 주의점
- 7교시 : 개인 면담 및 환경 점검 - AWS 리소스 상태, 비용 알림, CloudWatch, 삭제 대상 확인
- 8교시 : 보충 실습 - 리소스 연결 실패, 알림 설정, 비용 확인, 보안 그룹 문제 해결

## 5일차
- 1교시 : 5주차 통합 실습 안내 - 콘솔로 구성한 AWS 아키텍처를 운영 관점에서 점검
- 2교시 : 아키텍처 다이어그램 작성 - VPC, subnet, EC2/ECS, ALB, S3/RDS, CloudWatch, 비용 경계 표시
- 3교시 : 운영 Runbook 작성 - 배포 확인, 장애 확인, 로그/메트릭 확인, 비용 확인, 정리 절차
- 4교시 : 리소스 정리 실습 - 비용 발생 리소스 삭제/중지, 삭제 보호, snapshot, EIP, NAT 등 잔여 비용 확인
- 5교시 : Terraform 전환 준비 - 콘솔 설정값 목록화, 리소스 의존성, 변수화할 값, 민감정보 분리
- 6교시 : 5주차 발표 - AWS 서비스 매핑, 구성 절차, 비용/관찰 지점, 콘솔 수작업의 불편함 설명
- 7교시 : 발표 피드백 및 라이브 Q&A - 서비스 선택, 비용 위험, 관찰 가능성, IaC 전환 범위 점검
- 8교시 : 차주 수업내용 Overview - Terraform으로 동일한 AWS 구성을 재현하고 변경/삭제까지 관리

## 5주차 산출물
- AWS Console로 구성한 실습 아키텍처 다이어그램
- AWS 서비스 매핑 표 - compute, network, storage, database, observability, billing
- Budget 또는 비용 알림 설정 기록
- CloudWatch Logs/Metrics/Alarm/Dashboard 실습 기록
- 장애 주입 및 관찰 기록 1개
- 콘솔 구성 절차와 설정값 목록
- 6주차 Terraform 전환 대상 리소스 목록
- 비용 발생 리소스 정리 체크리스트

## 5주차 환경 준비 체크리스트
- AWS Console 로그인 가능
- MFA 설정 확인
- 실습 리전 확정
- Billing, Budget, Cost Explorer 접근 가능
- 공통 태그 규칙 확인
- VPC, security group, EC2 또는 ECS 리소스 생성 가능
- CloudWatch Logs/Metrics/Alarm 접근 가능
- 실습 종료 후 삭제/중지할 리소스 목록 확인

# 6주차
## Keyword
- terraform
- iac
- aws
- state
- plan
- apply
- destroy
- module
- variables
- drift

## 6주차 목표
- 5주차 AWS Console 구성에서 느낀 반복성, 누락 위험, 재현 어려움을 IaC로 해결한다.
- Terraform의 provider, resource, variable, output, state, plan/apply/destroy 흐름을 이해한다.
- 5주차에 만든 AWS 네트워크, compute, security, observability 구성 일부를 Terraform으로 재현한다.
- Terraform plan을 통해 변경 전 검토하고, apply/destroy로 생성과 정리를 통제한다.
- state 관리, drift, secret 처리, 비용 위험 등 IaC 운영 시 주의할 점을 이해한다.
- 최종적으로 Console과 IaC 방식의 차이, FinOps/Observability를 코드에 반영하는 방법을 설명한다.

## 6주차 운영 원칙
- 6주차는 새로운 아키텍처를 만드는 주차가 아니라 5주차 콘솔 구성을 코드로 재현하는 주차로 운영한다.
- Terraform 실습 범위는 비용과 위험을 통제할 수 있는 작은 AWS 구성으로 제한한다.
- 모든 apply 전 plan을 읽고, 모든 실습 후 destroy 또는 정리 상태를 확인한다.
- 민감정보는 코드에 직접 넣지 않고 변수, 환경변수, AWS 관리 기능으로 분리하는 원칙을 지킨다.
- IaC 코드에는 비용 추적을 위한 태그와 관찰 가능성을 위한 로그/알림 설정을 가능한 범위에서 포함한다.
- 매주 1일차와 4일차 7~8교시는 개인 면담, 환경 점검, 보충 실습, 진도 회복 시간으로 둔다.

## 1일차
- 1교시 : 5주차 복습 및 IaC가 필요한 이유 - 콘솔 수작업의 문제, 재현성, 리뷰, 변경 이력
- 2교시 : Terraform 기본 개념 - provider, resource, data source, variable, output, state
- 3교시 : Terraform 설치 및 AWS 인증 준비 - terraform version, AWS CLI 또는 환경변수, 권한 확인
- 4교시 : 첫 Terraform 실습 - provider 설정, 간단한 resource 작성, init, fmt, validate
- 5교시 : plan/apply/destroy 흐름 - 변경 미리보기, 생성, 삭제, 실패 시 확인 방법
- 6교시 : state 파일 이해 - local state, remote state 개념, state에 민감정보가 남을 수 있는 위험
- 7교시 : 개인 면담 및 환경 점검 - Terraform 설치, AWS 인증, 권한, provider init 문제 해결
- 8교시 : 보충 실습 - init/plan/apply 실패 학생 진도 회복

## 2일차
- 1교시 : 5주차 네트워크 구성을 Terraform으로 옮기기 - VPC, subnet, route table, internet gateway
- 2교시 : security group 코드화 - ingress/egress, 최소 오픈 포트, 이름과 태그 규칙
- 3교시 : 변수와 출력값 - region, project name, CIDR, port, tags를 variable/output으로 분리
- 4교시 : EC2 구성 코드화 - AMI, instance type, key pair 또는 user data, 태그
- 5교시 : user data와 부트스트랩 - 간단한 웹 서비스 실행, 로그 확인, 재생성 시 동작 확인
- 6교시 : Terraform으로 생성한 리소스 검증 - Console, curl, CloudWatch, terraform state 비교
- 7교시 : 변경 실습 - instance type, tag, security group rule 변경 후 plan 차이 읽기
- 8교시 : 정리 실습 - destroy 전 비용 영향 확인, destroy 후 잔여 리소스 확인

## 3일차
- 1교시 : ALB 또는 ECS 구성 코드화 전략 - 어떤 리소스부터 IaC로 옮길지 범위 결정
- 2교시 : ALB 기본 구성 - target group, listener, health check, security group 관계
- 3교시 : S3 또는 RDS 구성 코드화 - 비용과 삭제 위험을 고려한 실습 범위 선택
- 4교시 : CloudWatch 코드화 - log group, alarm, dashboard 또는 metric alarm 기본 구성
- 5교시 : FinOps를 IaC에 반영하기 - 필수 태그, Budget은 Console/API 한계 설명, 비용 알림 운영 기준
- 6교시 : drift 개념 실습 - Console에서 수동 변경 후 terraform plan으로 차이 확인
- 7교시 : drift 대응 - 되돌릴지, 코드에 반영할지, 운영 변경 절차를 어떻게 둘지 정리
- 8교시 : IaC 운영 기록 작성 - plan 결과, apply 결과, drift 확인 내용을 문서화

## 4일차
- 1교시 : Terraform 코드 구조화 - main.tf, variables.tf, outputs.tf, locals, naming 규칙
- 2교시 : module 개념 - 반복되는 네트워크/컴퓨트 구성을 묶는 이유와 과도한 추상화의 위험
- 3교시 : 환경 분리 전략 - dev/stage/prod 디렉터리, workspace 개념, 변수 파일
- 4교시 : state 관리 전략 - local state의 한계, S3 backend와 DynamoDB lock 개념 소개
- 5교시 : 보안과 secret 관리 - tfvars 주의, Git에 올리면 안 되는 파일, IAM 권한 최소화
- 6교시 : IaC 리뷰 관점 - plan 리뷰, 비용 리뷰, 보안 리뷰, observability 누락 리뷰
- 7교시 : 개인 면담 및 환경 점검 - 코드 구조, state, drift, destroy, 권한 문제 확인
- 8교시 : 보충 실습 - Terraform 코드 정리, plan 실패, destroy 실패, 잔여 리소스 확인

## 5일차
- 1교시 : 최종 통합 실습 안내 - 5주차 콘솔 구성을 Terraform으로 재현하고 운영 관점으로 설명
- 2교시 : 최종 Terraform apply - 네트워크, compute, 보안 그룹, 관찰 가능성 일부 구성 생성
- 3교시 : 서비스 검증 - 접속 확인, 로그/메트릭/알람 확인, 태그/비용 추적 기준 확인
- 4교시 : 장애 또는 변경 실습 - 포트 변경, instance type 변경, alarm threshold 변경 후 plan/apply 확인
- 5교시 : 최종 정리 - destroy, 잔여 리소스 점검, 비용 발생 가능성 확인
- 6교시 : 최종 발표 - Console vs Terraform 비교, 재현성, 비용 관리, 관찰 가능성, 남은 리스크 설명
- 7교시 : 전체 과정 회고 및 Q&A - Docker, MSA, Kubernetes, AWS, Terraform이 연결되는 흐름 정리
- 8교시 : 수료 전 개인 피드백 - 포트폴리오 정리 방향, 면접에서 설명할 수 있는 운영 사례 정리

## 6주차 산출물
- 5주차 AWS 콘솔 구성을 재현하는 Terraform 코드
- `terraform init/fmt/validate/plan/apply/destroy` 실행 기록
- 변수, 출력값, 태그, 보안 그룹 규칙 설명 문서
- CloudWatch 또는 비용 추적 관련 IaC 구성 기록
- drift 확인 및 대응 기록 1개
- Console 수작업과 Terraform 방식 비교 회고
- 최종 리소스 삭제/정리 체크리스트

## 6주차 환경 준비 체크리스트
- Terraform 설치 및 `terraform version` 확인
- AWS 인증 설정 가능
- `terraform init` 성공
- `terraform fmt`와 `terraform validate` 성공
- `terraform plan` 결과를 읽고 변경 내용을 설명 가능
- `terraform apply`로 작은 AWS 구성 생성 가능
- `terraform destroy` 후 잔여 리소스 확인 가능
- state 파일과 민감정보 취급 주의사항 이해
