# Week 2 Day 1: Docker 컨셉, 설치, nginx 실행, PostgreSQL 컨테이너 실험

## Overview
Day 1은 Week 1의 로컬 실행 확인 지점을 짧게 복기한 뒤 Docker 공식 문서 기준으로 image, container, registry, Docker Engine, Docker Desktop의 역할을 잡는다. 개념을 길게 분리하지 않고 설치와 실행 확인으로 바로 연결한다.

오늘의 목표는 Docker가 실제로 잘 실행되는지 확인하는 것이다. macOS는 Docker Desktop GUI 설치/실행을 포함하고, Linux는 Docker Engine 설치와 daemon 실행을 공식 문서 기준으로 확인한다. Docker Desktop for Linux는 예외 경로로만 분리해 확인한다. nginx container로 HTTP 접속을 먼저 검증한 뒤, Week 1에서 설치한 로컬 PostgreSQL과 Docker PostgreSQL container의 port 충돌을 확인하고, 로컬 PostgreSQL 정리 후 Docker PostgreSQL을 다시 띄운다. 이후 PostgreSQL 16/18을 서로 다른 host port로 병렬 실행하고, SQL로 user/database/table/row를 만들어 query까지 확인한다. 7~8교시는 개인 면담과 환경 점검으로 사용한다.

## 초보자 빠른 시작
Docker 수업은 설치 성공자만 따라가는 방식으로 운영하지 않는다. 설치가 되면 실행 확인 지점을 남기고, 설치가 막히면 blocker를 확인한다.

- 설치 가이드: [필수 소프트웨어 설치 가이드](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/docs/software-installation-guide.md)
- macOS 기본 경로: Docker Desktop 설치, 실행, `docker version`, `docker compose version`, `docker run --rm hello-world`
- Linux 기본 경로: Docker Engine 설치, daemon 실행, `docker version`, `docker compose version`, `docker run --rm hello-world`
- 첫 실행 검증: `nginx` container를 host port에 publish하고 browser 또는 `curl`로 HTTP 응답 확인
- blocker 확인: OS, CPU architecture, 설치 방식, 명령, 에러 메시지, 확인한 공식 문서 URL

## Learning Goals
- Week 1 미니 앱과 로컬 PostgreSQL 설치 경험을 Docker 학습 목표와 연결한다.
- Docker Desktop GUI 설치 상태와 `docker version` 결과를 확인 지점으로 남긴다.
- image, container, registry, Docker Engine, Docker Desktop의 역할을 구분한다.
- nginx container를 실행하고 HTTP 응답으로 Docker 실행 가능 여부를 확인한다.
- Week 1에서 설치한 로컬 PostgreSQL과 Docker PostgreSQL container의 port 충돌 여부를 확인한다.
- macOS/Linux에서 로컬 PostgreSQL을 삭제/중지/보류 중 하나로 안전하게 처리하고 확인한다.
- `postgres:16`과 `postgres:18`을 서로 다른 host port로 실행하고 각 버전에 접속해 결과를 확인한다.
- 같은 host port로 두 컨테이너를 실행할 때 실패하는 이유를 port binding 관점으로 설명한다.
- PostgreSQL container에 user, database, table, row를 만들고 query로 정상 동작을 확인한다.
- Docker 실행 실패를 숨기지 않고 OS, Docker 상태, command, error message 기준으로 확인한다.

## Lesson Index
- 1교시: 짧은 Week 1 리뷰와 Docker 공식 컨셉 - Week 1 실행 조건을 Docker overview의 image/container/registry/client/daemon 개념으로 연결
- 2교시: Docker 설치와 nginx 실행 확인 - macOS Docker Desktop GUI, Linux Docker Engine, `hello-world`, nginx HTTP 확인
- 3교시: 로컬 PostgreSQL과 Docker PostgreSQL port 충돌 확인 - Week 1 로컬 PostgreSQL의 `5432` 사용 여부와 Docker PostgreSQL 같은 port 실행 실패 확인
- 4교시: 로컬 PostgreSQL 삭제/중지 후 Docker PostgreSQL 재실행 - macOS/Linux별 정리 절차와 Docker PostgreSQL 접속 확인
- 5교시: PostgreSQL 16/18 container 병렬 실행 - host port를 다르게 연결하고 일부러 port 충돌도 확인
- 6교시: SQL 기본 조작 검증 - user, database, table 생성, row insert, query 확인
- 7교시: 개인 면담 및 환경 점검 A - 설치 blocker, PostgreSQL 정리 위험, port 충돌, SQL 접속 문제
- 8교시: 개인 면담 및 환경 점검 B - Day 2 volume 실습 준비, 미완료 학생 보충 경로, 확인 지점 확인 상태

## Official References
| Topic | Reference | 오늘 확인할 키워드 |
|---|---|---|
| Docker overview | https://docs.docker.com/get-started/docker-overview/ | client-server architecture, daemon, registry, images, containers |
| Docker Desktop | https://docs.docker.com/desktop/ | install, run, GUI, Desktop |
| Mac install | https://docs.docker.com/desktop/setup/install/mac-install/ | Apple silicon, Intel, system requirements |
| Ubuntu Engine install | https://docs.docker.com/engine/install/ubuntu/ | Docker Engine, apt repository |
| Linux post-install | https://docs.docker.com/engine/install/linux-postinstall/ | docker group, sudo 없이 실행, daemon 권한 |
| Linux Desktop exception | https://docs.docker.com/desktop/setup/install/linux/ | 예외 경로, Linux VM, Docker context, port conflict note |
| Sign in | https://docs.docker.com/desktop/setup/sign-in/ | Docker account, sign in |
| Container concept | https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/ | isolated process, VM comparison, port exposure |
| Image concept | https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/ | immutable, layers |
| Publishing ports | https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/ | host port, container port |
| PostgreSQL official image | https://github.com/docker-library/docs/blob/master/postgres/README.md | `POSTGRES_PASSWORD`, `PGDATA`, 16/18 tags |

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
- PostgreSQL official image
- host port / container port
- named volume
- cleanup

## Practice Files And Assets
| 자료 | 용도 |
|---|---|
| Week 1 README/runbook | 로컬 실행 조건을 Docker 학습 목표로 매핑 |
| 표준 실습 앱 repository 또는 압축 파일 | Day 1 6교시 첫 실행 확인, Day 2 Dockerfile 실습 재료 |
| `docker-확인 지점.md` | 설치, 실행, 실패, 복구 확인 |
| `screenshots/` | Docker Desktop 또는 browser 확인 지점 파일명 확인 |
| `assets/lesson-01-week1-to-docker-확인 지점.png` | Week 1 확인 지점가 Docker 실행 조건으로 이동하는 흐름 |
| `assets/lesson-01-pc-vm-docker-history.png` | imagegen으로 생성한 Multi PC -> VM -> Docker 역사/개념 인포그래픽 |
| `assets/lesson-02-docker-desktop-triage.png` | Docker Desktop 설치/Client/Server/blocker triage |
| `assets/lesson-03-docker-architecture.png` | CLI, Engine, Registry, Image, Container, Network, Volume 관계 |
| `assets/official-docker-architecture.webp` | Docker 공식 문서의 Docker Architecture diagram |
| `assets/official-docker-run-container.webp` | Docker 공식 문서의 Docker Desktop container run dialog 화면 |
| `assets/official-docker-access-frontend.webp` | Docker 공식 문서의 container port 접근 화면 |
| `assets/lesson-03-pc-parts-to-docker-components.png` | CPU, RAM, disk, network, OS kernel과 Docker 컴포넌트 매핑 |
| `assets/lesson-03-vm-vs-container-os-kernel.png` | VM 가상화와 Docker 컨테이너화의 OS/kernel 구조 비교 |
| `assets/lesson-04-docker-vs-local.png` | Local 실행과 Docker 실행의 장점/새 책임 비교 |
| `assets/lesson-05-docker-command-cycle.png` | Docker 기본 명령 cycle과 실행 80% 원칙 |
| `assets/lesson-06-nginx-run-verification.png` | 기본 container run/check/cleanup 흐름을 짧게 복습할 때 사용 |
| `assets/lesson-07-docker-troubleshooting-lab.png` | PostgreSQL 컨테이너 blocker triage에도 재사용 |
| `assets/lesson-08-supplemental-practice-board.png` | DB container cleanup/확인 지점 board로 재해석 |

## Visual Asset Review
| Asset | 검수 결과 | 수업 사용 기준 |
|---|---|---|
| `lesson-01-pc-vm-docker-history.png` | imagegen generated asset, nonblank, 큰 글자 readable, Multi PC/VM/Docker 전환 흐름이 명확함 | 공식 문서 그림이 아니라 강의용 재구성 인포그래픽임을 본문에 명시한다. |
| `lesson-01-week1-to-docker-확인 지점.png` | nonblank, 큰 흐름 readable, Docker 실행 조건 매핑이 명확함 | 세부 용어는 본문 표와 함께 읽는다. |
| `lesson-02-docker-desktop-triage.png` | nonblank, 설치 triage와 secret masking 메시지가 명확함 | OS별 실제 요구사항은 공식 문서로 재확인한다. |
| `official-docker-architecture.webp` | Docker Docs 원본 이미지, nonblank | 출처 URL과 함께 사용하고, 용어는 Docker overview 본문 기준으로 읽는다. |
| `official-docker-run-container.webp` | Docker Docs 원본 이미지, nonblank | GUI 예시이며 실제 수업 명령은 CLI 확인 지점과 함께 확인한다. |
| `official-docker-access-frontend.webp` | Docker Docs 원본 이미지, nonblank | port exposure 예시이며 Day 1 후반 DB 실습에서는 `5432` container port를 host port로 매핑해 확장한다. |
| `lesson-03-docker-architecture.png` | nonblank, CLI/Engine/Registry/Image/Container 관계가 명확함 | Docker 공식 로고 대체 그림이며 공식 architecture 용어는 본문으로 보정한다. |
| `lesson-03-pc-parts-to-docker-components.png` | nonblank, PC 부품과 Docker 컴포넌트 연결이 명확함 | Docker가 새 하드웨어를 만드는 것이 아니라 PC 자원을 OS kernel을 통해 나누어 쓴다는 점을 본문으로 보정한다. |
| `lesson-03-vm-vs-container-os-kernel.png` | nonblank, VM의 Guest OS 계층과 container의 host kernel 공유 구조가 명확함 | macOS는 Docker Desktop의 내부 Linux VM 계층, Windows는 WSL 2/가상화 예외 경로로 구분해 읽는다. |
| `lesson-04-docker-vs-local.png` | nonblank, local/Docker 비교와 새 책임 메시지가 명확함 | Docker 도입 판단은 본문 decision table로 보완한다. |
| `lesson-05-docker-command-cycle.png` | nonblank, 기본 명령 cycle과 확인 지점 checklist가 명확함 | 본문 명령은 테스트 충돌을 피하기 위해 `18080:80` 기준으로 보정한다. |
| `lesson-06-nginx-run-verification.png` | nonblank, nginx 실행과 HTTP 검증 흐름이 명확함 | HTTP header 값은 실행 시점과 image version에 따라 달라질 수 있음을 본문에 명시한다. |
| `lesson-07-docker-troubleshooting-lab.png` | nonblank, 증상/증거/다음 행동 구조가 명확함 | blocker는 학생 책임이 아니라 환경과 출력 기반 진단으로 다룬다. |
| `lesson-08-supplemental-practice-board.png` | nonblank, 보충 실습 확인 지점 표와 Day 2 준비 흐름이 명확함 | cleanup 기준과 Dockerfile readiness note를 본문으로 보완한다. |

## Linux 사전 확인 지점
Day 1 기본 Docker 명령 cycle은 Linux 환경에서 사전 테스트했다. 6~8교시 PostgreSQL 16/18 실습은 수업용 절차로 추가했으며, image pull과 version query는 교육장 네트워크와 Docker Hub 상태에 따라 성공/실패 확인 지점을 모두 인정한다.

| 항목 | 결과 |
|---|---|
| Test OS | Ubuntu 24.04.3 LTS, Linux `6.6.87.2-microsoft-standard-WSL2`, `linux/amd64` |
| Docker version | Client `29.0.2`, Server `29.3.1` |
| `docker run --rm hello-world` | `Hello from Docker!` 출력 성공 |
| `docker pull nginx:latest` | 기본 명령 cycle 예시로 digest 확인 |
| `docker run -d --name paperclip-day1-nginx -p 18080:80 nginx:latest` | 기본 port binding 예시로 실행 성공 |
| `curl -I http://localhost:18080` | `HTTP/1.1 200 OK` |
| `docker stop` / `docker rm` | container 정리 성공 |
| PostgreSQL 16/18 planned check | `postgres:16`은 host `15432`, `postgres:18`은 host `15433`으로 실행하고 `SELECT version();`으로 확인 |

컨테이너 시작 직후 첫 요청은 아주 짧은 startup timing 때문에 connection reset/refused가 날 수 있다. PostgreSQL에서도 초기화가 끝나기 전에는 접속 실패가 날 수 있으므로 `docker logs`에서 ready message를 확인하고 짧게 재시도한다.

```bash
for i in 1 2 3 4 5; do
  docker exec paperclip-pg16 pg_isready -U postgres && break
  sleep 1
done
```

## Preparation Notes
- Docker Desktop 설치는 macOS 기준으로 진행한다. Apple silicon과 Intel Mac은 설치 파일과 요구사항이 다를 수 있으므로 공식 Mac 설치 문서를 확인한다.
- Linux 장비를 사용하는 학생은 Docker Engine 설치 경로를 기본으로 따른다. Desktop for Linux를 이미 쓰거나 조직 정책상 필요하면 예외 경로로 표시하고, Desktop의 자체 Linux VM/context와 host Engine daemon의 차이를 확인한다.
- Windows 장비를 사용하는 학생이 있을 경우 별도 예외 경로로 Windows 설치 문서를 확인한다. 이때 WSL 2, 가상화 설정, 관리자 권한, 조직 보안 정책이 blocker가 될 수 있다.
- 설치 실패 자체는 감점이 아니며, 실패 증거와 요청 경로를 남기는 것이 중요하다.
- Week 1에서 설치한 로컬 PostgreSQL은 OS별 절차로 중지/삭제하거나 수업 중 최소한 비활성화한다. 기존 데이터 삭제가 위험하면 삭제하지 말고 running service와 port 사용 여부만 확인 지점으로 남긴다.
- Week 2 Day 1은 cloud resource를 만들지 않는다. 비용 발생 가능성이 있는 외부 cloud service, paid database, paid API는 사용하지 않는다.
- Docker Hub 로그인 정보, password, token, MFA code는 화면 공유와 README에 남기지 않는다.

## 주의할 점
| 상황 | 실수를 줄이는 확인 지점 |
|---|---|
| Docker version | `docker version` 또는 실패 시 error message 요약 |
| Docker runtime status | macOS Desktop running 또는 Linux Engine daemon 상태/blocker 확인 |
| OS/install note | macOS Apple silicon/Intel 여부, Linux Engine 설치/권한 상태, Linux Desktop 예외 여부, Windows 사용 시 WSL 2/가상화/권한 이슈 |
| `hello-world` result | 성공 output 요약 또는 실패 증상 |
| nginx HTTP result | container name, host port, browser/curl result |
| local PostgreSQL conflict | `5432` 사용 여부, Docker PostgreSQL 같은 host port 실행 결과 |
| 로컬 PostgreSQL 정리 | stop/delete/disable 중 어떤 조치를 했는지, 기존 데이터 보존 여부 |
| PostgreSQL 16 result | container name, host port, 접속 버전 |
| PostgreSQL 18 result | container name, host port, 접속 버전 |
| port conflict result | 같은 host port를 쓰면 실패한다는 error summary |
| SQL result | user, database, table, insert, query result |
| interview note | 남은 blocker와 Day 2 준비 상태 |
| cleanup note | 실행한 container를 중지/정리했는지 확인. Day 2 데이터 소실 실험을 위해 volume은 만들지 않는다. |
| blocker note | 막힌 지점, 시도한 확인, 필요한 도움 |

## End-Of-Day Checklist
- [ ] macOS Docker Desktop 또는 Linux Docker Engine 설치/blocker를 확인했다.
- [ ] `docker version` 출력 또는 실패 원인을 확인했다.
- [ ] Docker image와 container의 차이를 한 문장으로 설명했다.
- [ ] `docker run hello-world`를 실행하거나 실패 증상을 확인했다.
- [ ] nginx container를 실행하고 HTTP 응답을 확인했다.
- [ ] 로컬 PostgreSQL과 Docker PostgreSQL의 `5432` port 충돌 여부를 확인했다.
- [ ] Week 1 로컬 PostgreSQL을 삭제/중지/보류 중 하나로 처리하고 이유를 확인했다.
- [ ] `postgres:16`과 `postgres:18`을 서로 다른 host port로 실행하거나 실패 증상을 확인했다.
- [ ] 같은 host port 충돌 실험을 통해 왜 동시에 실행이 안 되는지 설명했다.
- [ ] PostgreSQL container에서 user/database/table/row/query를 확인했다.
- [ ] 7~8교시 면담에서 남은 blocker와 Day 2 volume 실습 준비 상태를 확인했다.

## Next Connection
Day 2는 오늘 만든 PostgreSQL container의 데이터가 container lifecycle과 함께 사라지는지 확인하면서 volume으로 넘어간다. Day 1에서는 일부러 volume을 붙이지 않고, Day 2에서 named volume을 연결한 뒤 container를 교체해도 데이터가 유지되는지 검증한다.
