# Week 2 Day 1: Docker 개념, 설치, 기본 실행 사이클

## Overview
Day 1은 Week 1의 로컬 실행 evidence를 Docker의 실행 환경 표준화 문제로 연결한다. 학생은 Docker Desktop을 설치하거나 상태를 확인하고, Docker가 image, container, registry, engine을 통해 어떤 실행 문제를 다루는지 학습한다.

오늘의 목표는 많은 명령을 외우는 것이 아니다. 컨테이너를 실행하고, 상태를 확인하고, 로그를 보고, 중지하고, 정리하는 기본 lifecycle을 하나의 운영 사이클로 익히는 것이다.

## 초보자 빠른 시작
Docker 수업은 설치 성공자만 따라가는 방식으로 운영하지 않는다. 설치가 되면 실행 evidence를 남기고, 설치가 막히면 blocker evidence를 남긴다.

- 설치 가이드: [필수 소프트웨어 설치 가이드](../../docs/software-installation-guide.md)
- macOS 기본 경로: Docker Desktop 설치, 실행, `docker version`, `docker run --rm hello-world`
- Linux 기본 경로: Docker Desktop 또는 Docker Engine 설치, daemon 실행, `docker compose version`
- blocker 기록: OS, CPU architecture, 설치 방식, 명령, 에러 메시지, 확인한 공식 문서 URL

## Learning Goals
- Week 1 미니 앱의 실행 조건을 Docker 학습 목표와 연결한다.
- Docker Desktop 설치 상태와 `docker version` 결과를 evidence로 남긴다.
- image, container, registry, Docker Engine, Docker Desktop의 역할을 구분한다.
- Docker와 local computer 실행 방식의 장점, 비용, 한계를 비교한다.
- `hello-world`, `nginx`, 표준 실습 앱 실행 결과를 command, status, URL, log로 확인한다.
- Docker 실행 실패를 숨기지 않고 OS, Docker 상태, command, error message 기준으로 기록한다.

## Lesson Index
- 1교시: 1주차 복습 및 Docker 학습 목표 - 로컬 실행 문제, 배포 문제, 환경 차이 문제 정리
- 2교시: Docker Desktop 설치 및 계정 확인 - macOS 기준 설치, Docker Hub 로그인, Windows 사용자의 WSL 2/가상화 예외 경로 기록
- 3교시: Docker의 컨셉과 작동 방식 - PC 부품과 연결해 image, container, registry, Docker Engine, Docker Desktop 이해
- 4교시: Docker vs Local Computer - 좋아지는 점, 나빠지는 점, 언제 Docker를 쓰지 말아야 하는지
- 5교시: Docker 기본 명령어 1 - `docker version`, `pull`, `images`, `run`, `ps`, `stop`, `rm`
- 6교시: Hello World, nginx, 표준 실습 앱 첫 실행 - container 실행, Docker Hub pull, browser 접속, `curl` 확인
- 7교시: 개인 면담 및 환경 점검 - Docker Desktop 실행, macOS 권한/실행 상태, Windows WSL 2/가상화 예외 경로, 로그인 문제 해결
- 8교시: 보충 실습 - 기본 명령어 재실습, 막힌 학생 진도 회복

## Official References
| Topic | Reference | 오늘 확인할 키워드 |
|---|---|---|
| Docker overview | https://docs.docker.com/engine/docker-overview/ | image, container, registry |
| Docker Desktop | https://docs.docker.com/desktop/ | install, run, GUI, Desktop |
| Mac install | https://docs.docker.com/desktop/setup/install/mac-install/ | Apple silicon, Intel, system requirements |
| Windows install | https://docs.docker.com/desktop/setup/install/windows-install/ | WSL 2, system requirements |
| Sign in | https://docs.docker.com/desktop/setup/sign-in/ | Docker account, sign in |
| Image concept | https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/ | immutable, layers |

## Key Terms
- Docker Desktop
- Docker Engine
- image
- container
- registry
- Docker Hub
- port binding
- container lifecycle
- logs
- cleanup

## Practice Files And Assets
| 자료 | 용도 |
|---|---|
| Week 1 README/runbook | 로컬 실행 조건을 Docker 학습 목표로 매핑 |
| 표준 실습 앱 repository 또는 압축 파일 | Day 1 6교시 첫 실행 확인, Day 2 Dockerfile 실습 재료 |
| `docker-evidence.md` | 설치, 실행, 실패, 복구 기록 |
| `screenshots/` | Docker Desktop 또는 browser evidence 파일명 기록 |
| `assets/lesson-01-week1-to-docker-evidence.png` | Week 1 evidence가 Docker 실행 조건으로 이동하는 흐름 |
| `assets/lesson-02-docker-desktop-triage.png` | Docker Desktop 설치/Client/Server/blocker triage |
| `assets/lesson-03-docker-architecture.png` | CLI, Engine, Registry, Image, Container, Network, Volume 관계 |
| `assets/lesson-03-pc-parts-to-docker-components.png` | CPU, RAM, disk, network, OS kernel과 Docker 컴포넌트 매핑 |
| `assets/lesson-03-vm-vs-container-os-kernel.png` | VM 가상화와 Docker 컨테이너화의 OS/kernel 구조 비교 |
| `assets/lesson-04-docker-vs-local.png` | Local 실행과 Docker 실행의 장점/새 책임 비교 |
| `assets/lesson-05-docker-command-cycle.png` | Docker 기본 명령 cycle과 실행 80% 원칙 |
| `assets/lesson-06-nginx-run-verification.png` | nginx 실행, port binding, HTTP 200, cleanup 검증 흐름 |
| `assets/lesson-07-docker-troubleshooting-lab.png` | blocker triage와 환경 점검 흐름 |
| `assets/lesson-08-supplemental-practice-board.png` | 보충 실습 evidence board와 Day 2 준비 |

## Visual Asset Review
| Asset | 검수 결과 | 수업 사용 기준 |
|---|---|---|
| `lesson-01-week1-to-docker-evidence.png` | nonblank, 큰 흐름 readable, Docker 실행 조건 매핑이 명확함 | 세부 용어는 본문 표와 함께 읽는다. |
| `lesson-02-docker-desktop-triage.png` | nonblank, 설치 triage와 secret masking 메시지가 명확함 | OS별 실제 요구사항은 공식 문서로 재확인한다. |
| `lesson-03-docker-architecture.png` | nonblank, CLI/Engine/Registry/Image/Container 관계가 명확함 | Docker 공식 로고 대체 그림이며 공식 architecture 용어는 본문으로 보정한다. |
| `lesson-03-pc-parts-to-docker-components.png` | nonblank, PC 부품과 Docker 컴포넌트 연결이 명확함 | Docker가 새 하드웨어를 만드는 것이 아니라 PC 자원을 OS kernel을 통해 나누어 쓴다는 점을 본문으로 보정한다. |
| `lesson-03-vm-vs-container-os-kernel.png` | nonblank, VM의 Guest OS 계층과 container의 host kernel 공유 구조가 명확함 | macOS는 Docker Desktop의 내부 Linux VM 계층, Windows는 WSL 2/가상화 예외 경로로 구분해 읽는다. |
| `lesson-04-docker-vs-local.png` | nonblank, local/Docker 비교와 새 책임 메시지가 명확함 | Docker 도입 판단은 본문 decision table로 보완한다. |
| `lesson-05-docker-command-cycle.png` | nonblank, 기본 명령 cycle과 evidence checklist가 명확함 | 본문 명령은 테스트 충돌을 피하기 위해 `18080:80` 기준으로 보정한다. |
| `lesson-06-nginx-run-verification.png` | nonblank, nginx 실행과 HTTP 검증 흐름이 명확함 | HTTP header 값은 실행 시점과 image version에 따라 달라질 수 있음을 본문에 명시한다. |
| `lesson-07-docker-troubleshooting-lab.png` | nonblank, 증상/증거/다음 행동 구조가 명확함 | blocker는 학생 책임이 아니라 환경과 출력 기반 진단으로 다룬다. |
| `lesson-08-supplemental-practice-board.png` | nonblank, 보충 실습 evidence 표와 Day 2 준비 흐름이 명확함 | cleanup 기준과 Dockerfile readiness note를 본문으로 보완한다. |

## Linux Preflight Test Evidence
Day 1 5~8교시 hands-on 명령은 Linux 환경에서 사전 테스트했다.

| 항목 | 결과 |
|---|---|
| Test OS | Ubuntu 24.04.3 LTS, Linux `6.6.87.2-microsoft-standard-WSL2`, `linux/amd64` |
| Docker version | Client `29.0.2`, Server `29.3.1` |
| `docker run --rm hello-world` | `Hello from Docker!` 출력 성공 |
| `docker pull nginx:latest` | digest `sha256:5aca...69f6`, 최신 상태 확인 |
| `docker run -d --name paperclip-day1-nginx -p 18080:80 nginx:latest` | container ID 출력, 실행 성공 |
| `curl -I http://localhost:18080` | `HTTP/1.1 200 OK`, `Server: nginx/1.31.1` |
| `docker logs paperclip-day1-nginx` | nginx startup log 확인 |
| bind mount source edit | `labs/nginx-html/index.html` v1 응답 확인, host file 수정 후 v2 응답 확인 |
| `docker stop` / `docker rm` | 각각 `paperclip-day1-nginx` 출력 |
| cleanup recheck | `docker ps --filter name=paperclip-day1-nginx` 헤더만 출력 |

## Preparation Notes
- Docker Desktop 설치는 macOS 기준으로 진행한다. Apple silicon과 Intel Mac은 설치 파일과 요구사항이 다를 수 있으므로 공식 Mac 설치 문서를 확인한다.
- Windows 장비를 사용하는 학생이 있을 경우 별도 예외 경로로 Windows 설치 문서를 확인한다. 이때 WSL 2, 가상화 설정, 관리자 권한, 조직 보안 정책이 blocker가 될 수 있다.
- 설치 실패 자체는 감점이 아니며, 실패 증거와 요청 경로를 남기는 것이 중요하다.
- Week 2 Day 1은 cloud resource를 만들지 않는다. 비용 발생 가능성이 있는 외부 cloud service, paid database, paid API는 사용하지 않는다.
- Docker Hub 로그인 정보, password, token, MFA code는 화면 공유와 README에 남기지 않는다.

## Required Evidence
| Evidence | 제출 기준 |
|---|---|
| Docker version | `docker version` 또는 실패 시 error message 요약 |
| Docker Desktop status | running 상태 또는 blocker 기록 |
| OS/install note | macOS Apple silicon/Intel 여부, Windows 사용 시 WSL 2/가상화/권한 이슈 |
| `hello-world` result | 성공 output 요약 또는 실패 증상 |
| `nginx` result | `http://localhost:8080` 또는 `curl` 확인 |
| cleanup note | 실행한 container를 중지/정리했는지 기록 |
| blocker note | 막힌 지점, 시도한 확인, 필요한 도움 |

## End-Of-Day Checklist
- [ ] Docker Desktop 설치 또는 blocker를 기록했다.
- [ ] `docker version` 출력 또는 실패 원인을 기록했다.
- [ ] Docker image와 container의 차이를 한 문장으로 설명했다.
- [ ] `docker run hello-world`를 실행하거나 실패 증상을 기록했다.
- [ ] `nginx` container를 port binding으로 실행하고 browser/curl evidence를 남겼다.
- [ ] 실행한 container를 중지하고 정리했다.
- [ ] Day 2 Dockerfile 실습에 사용할 표준 실습 앱을 받을 준비가 되었다.

## Next Connection
Day 2는 오늘 실행해 본 container를 직접 만들 수 있도록 Dockerfile과 image build를 다룬다. 오늘의 핵심 evidence인 command, image name, port, log, cleanup 기록이 Dockerfile 작성의 기준이 된다.
