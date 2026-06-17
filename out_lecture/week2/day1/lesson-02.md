# 2교시: Docker 설치 및 실행 확인 - macOS/Linux 경로 분리

## 수업 목표
- 공식 문서를 기준으로 Docker 설치 또는 상태 확인을 진행한다.
- `docker version`으로 client와 server 연결 상태를 구분한다.
- 기본 실습 환경은 macOS Docker Desktop과 Linux Docker Engine 경로를 나누어 안내한다.
- Docker Hub 로그인과 credential 보호 기준을 이해한다.
- 설치 실패를 OS 종류, Mac chip, Linux 배포판, 권한, daemon 상태, error message 기준으로 확인한다.

## 설치 가이드
Docker 설치 절차는 OS, CPU architecture, Linux 배포판, 조직 장비 정책에 따라 달라진다. 수업 중에는 아래 가이드를 먼저 열고, 자신의 환경에 맞는 macOS 또는 Linux 절차를 따른다.

- macOS/Linux 설치 가이드: [필수 소프트웨어 설치 가이드](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/docs/software-installation-guide.md)
- Docker Mac 공식 설치 문서: https://docs.docker.com/desktop/setup/install/mac-install/
- Docker Engine Ubuntu 공식 설치 문서: https://docs.docker.com/engine/install/ubuntu/
- Docker Engine Linux post-install 문서: https://docs.docker.com/engine/install/linux-postinstall/
- Docker Desktop for Linux 예외 경로 문서: https://docs.docker.com/desktop/setup/install/linux/

설치 완료 판단은 Docker Desktop 창이 열리는 것만으로 하지 않는다. `docker version`, `docker compose version`, `docker run --rm hello-world` 중 어디까지 성공했는지 확인한다.

## 강의 전개

이 교시는 설치 성공을 경쟁시키는 시간이 아니라, 실행 기반을 증거로 분리하는 시간이다. Docker 설치는 OS와 장비 정책의 영향을 많이 받는다. 같은 "Mac"이라고 해도 Apple silicon과 Intel Mac의 조건이 다를 수 있다. Linux에서는 Docker Engine을 기본 경로로 두고, Docker Desktop for Linux를 이미 쓰거나 조직 정책상 필요한 학생만 예외 경로로 표시한다.

강의는 먼저 공식 문서 확인으로 시작한다. 검색 결과나 AI 답변이 설치 단계를 알려줄 수는 있지만, 수업의 기준은 Docker 공식 문서다. 공식 문서에서 system requirement, 권한 조건, 설치 후 확인 명령, 알려진 제약을 직접 확인하도록 만든다. 학생이 설치에 막혔을 때도 "무엇을 따라 했는지"가 남아야 도움을 줄 수 있다.

그 다음은 GUI와 CLI를 분리한다. Docker Desktop 창이 열려도 Docker CLI가 daemon/server와 통신하지 못하면 container는 실행되지 않는다. 반대로 Linux Engine 경로에서는 Desktop GUI가 없어도 daemon과 CLI가 제대로 연결되어 있으면 실습을 진행할 수 있다. 그래서 `docker version`의 Client/Server 구분을 설치 확인의 중심에 둔다.

설치 실패자는 수업에서 제외하지 않는다. 설치 실패도 OS, chip, 배포판, 권한, daemon 상태, error message를 기준으로 정리하면 유효한 운영 확인 지점가 된다. 이 방식은 뒤에서 container 실행 실패를 분석할 때 그대로 반복된다. 즉, 설치 수업은 Docker 개념 수업이기도 하다. 학생들은 "실패를 확인하는 방식"을 여기서 배운다.

마지막에는 보안 기준을 명확히 한다. Docker Hub 로그인, token, MFA code, 개인 email, 조직 registry 주소는 screenshot이나 README에 그대로 남기면 안 된다. 설치와 로그인은 편의 기능이 아니라 credential을 다루는 작업이므로, public image pull 가능 여부와 credential 보호 기준을 함께 확인한다.

## 선행 지식
| 이미 알고 있어야 할 것 | 오늘 새로 확인할 것 |
|---|---|
| 공식 문서에서 prerequisite와 warning을 찾는 법 | Docker Desktop system requirements |
| CLI에서 version output을 확인하는 법 | Docker client/server version |
| OS와 kernel이 process 실행에 관여한다는 Week 1 개념 | Linux container 실행에 Linux kernel이 필요하다는 점 |
| secret을 공개 문서에 남기지 않는 법 | Docker Hub password/token/MFA 보호 |
| blocker를 증상 중심으로 쓰는 법 | 설치/daemon/login blocker |

## OS와 설치 상태 확인

Docker 설치 수업에서 가장 위험한 가정은 "모두 같은 장비 상태"라고 보는 것이다. 이번 수업은 macOS와 Linux 경로를 명확히 나눈다. macOS에서는 Apple silicon인지 Intel Mac인지에 따라 설치 파일과 요구사항이 달라질 수 있고, Docker Desktop 실행 권한이나 보안 설정이 영향을 줄 수 있다.

Linux 장비는 Docker Engine을 기본 경로로 둔다. Engine은 host Linux daemon을 직접 사용하므로 `systemctl status docker`, `docker version`, `docker compose version`, `docker run --rm hello-world`를 중심으로 확인한다. Docker Desktop for Linux는 자체 Linux VM과 전용 Docker context를 쓰는 예외 경로로만 다룬다.

Windows 장비를 사용하는 학생이 있을 수 있으므로 Windows 경로도 짧고 정확하게 남긴다. Windows에서는 Linux container 실행을 위해 WSL 2 backend, 가상화 설정, 조직 보안 정책, 관리자 권한이 영향을 줄 수 있다. 이 내용은 전체 수업의 기본 경로가 아니라 Windows 사용자를 위한 별도 점검 항목이다.

오늘은 설치 성공자와 실패자를 나누어 확인하지 않는다. 대신 각자의 장비 상태를 확인 지점으로 남기고, 해결 가능한 blocker를 분류한다. 현업에서도 배포 실패를 볼 때 "누가 잘못했는가"보다 "어느 환경에서 어떤 조건이 맞지 않았는가"를 먼저 확인한다.

### Visual 1: 설치 상태 triage 흐름
![Docker Desktop 설치 점검 triage](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day1/assets/lesson-02-docker-desktop-triage.png)

이 이미지는 설치 확인을 OS 요구사항, Desktop 실행, `docker version`의 Client/Server 증거, blocker 확인으로 나눈다. 설치가 실패했을 때도 개인 문제가 아니라 환경 차이와 증거 수집 문제로 분류하는 흐름을 본다.

### Visual 2: 설치 상태 Mermaid triage
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/lecture_mermaid_assets/week2__day1__lesson-02--diagram-01.png)

읽는 순서: 설치 실패를 하나의 큰 실패로 보지 않고, Desktop 실행, CLI 연결, daemon 응답, 공식 문서 확인 단계로 나누어 본다.

## 공식 설치 문서 읽기

공식 문서는 설치 파일 링크만 제공하는 곳이 아니다. system requirement, 권한 모델, 알려진 제약, 설치 후 확인 절차가 들어 있다. AI 답변이나 검색 결과가 설치 단계를 알려주더라도, 수업에서는 공식 문서에서 OS별 조건을 직접 확인한다.

macOS 수강생은 Docker Desktop Mac 설치 문서에서 Apple silicon/Intel 구분, system requirements, 설치 파일, 실행 권한을 확인한다. 수업 중 화면 예시는 macOS Docker Desktop 기준으로 진행할 수 있다.

Linux 수강생은 Docker Engine 공식 문서를 먼저 따른다. Ubuntu 기준으로는 apt repository 설정, package 설치, daemon 실행 상태, Compose plugin, post-install 권한 설정을 확인한다. Docker Desktop for Linux는 이미 해당 환경을 쓰고 있거나 조직 장비 정책상 필요한 경우에만 예외로 확인하며, Desktop이 자체 Linux VM과 Docker context를 만들고 host Engine과 port publish 충돌을 일으킬 수 있음을 분리해 설명한다.

Windows 수강생은 별도 예외 경로로 Docker Desktop Windows 설치 문서를 확인한다. Windows에서는 WSL 2 backend, virtualization, 관리자 권한, 조직 보안 정책이 blocker가 될 수 있다. Linux container는 Linux kernel 기능에 의존하므로 Windows에서 WSL 2 문제가 발생하면 단순 설치 문제가 아니라 container 실행 기반이 준비되지 않은 상태로 확인한다.

macOS에서도 Docker Desktop은 Linux container 실행을 위해 내부적으로 Linux VM 계층을 사용한다. 다만 학생이 직접 WSL 2를 설정하는 흐름은 아니다. 그래서 macOS 기본 경로에서는 Apple silicon/Intel 구분, Docker Desktop 실행 상태, `docker version`의 Client/Server 연결을 우선 확인한다.

### Visual 3: 공식 문서 reading note
| 확인 항목 | 확인할 내용 | 이유 |
|---|---|---|
| 문서 URL | Docker Desktop Mac 설치 문서, Windows 사용자는 Windows 설치 문서 | AI 답변 검증 기준 |
| Mac chip | Apple silicon 또는 Intel | 설치 파일과 요구사항 차이 |
| 권한 조건 | 앱 실행 권한, 보안 설정, 관리자 권한 필요 여부 | 개인 장비 blocker 분류 |
| Linux 경로 | Docker Engine 기본, Docker Desktop for Linux는 예외 | host daemon, docker group, Desktop VM/context 차이 |
| Windows 예외 | WSL 2, virtualization, 관리자 권한 | Windows에서 Linux container runtime 제공 여부 |
| 설치 후 확인 | `docker version`, macOS Desktop 또는 Linux daemon running | 성공 기준을 command로 확인 |

## Docker 설치 또는 실행 확인

Docker Desktop은 local machine에서 containerized application을 build, share, run하도록 돕는 데스크톱 앱이다. 학생은 GUI를 보는 데서 멈추지 않고 CLI가 Docker daemon과 통신하는지 확인해야 한다. Linux Engine 경로를 선택한 학생은 Desktop GUI 대신 daemon/service와 CLI 연결을 확인한다.

설치가 이미 되어 있으면 update를 강제로 진행하지 않는다. 수업 시간에는 running 상태와 CLI 연결 상태를 확인 지점으로 남기는 것이 우선이다. 설치가 필요한 경우 공식 문서 기준으로 설치하되, 권한 요청이나 재부팅이 필요한 상황은 운영 지침에 따라 처리한다.

### 실습 절차
1. 본인 OS에 맞는 Docker 공식 설치 문서를 연다.
2. macOS는 Docker Desktop을 설치했거나 이미 설치된 상태인지 확인한다.
3. Linux는 Docker Engine 설치 상태와 daemon 실행 상태를 확인한다.
4. macOS는 Desktop이, Linux Engine 경로는 daemon/service가 running 상태가 될 때까지 기다린다.
5. terminal을 열고 다음 명령을 실행한다.

```bash
docker version
docker compose version
docker run --rm hello-world
```

### 예상 결과
- `Client` 정보만 보이고 `Server` 연결 error가 나오면 Docker CLI는 있지만 daemon에 연결되지 않은 상태일 수 있다.
- `Client`와 `Server` 정보가 모두 나오면 Docker daemon이 실행 중이고 CLI가 연결된 상태다.
- command 자체를 찾지 못하면 Docker CLI가 설치되지 않았거나 PATH에 잡히지 않은 상태다.

## `docker version` 확인

`docker version`은 "Docker가 설치되었다"는 주장보다 강한 확인 지점이다. 특히 client와 server를 나누어 읽어야 한다. Docker CLI client가 있어도 Docker daemon/server가 실행 중이 아니면 container를 실행할 수 없다.

### Visual 4: version output 읽는 방법
| 출력 위치 | 의미 | 흔한 실패 |
|---|---|---|
| `Client` | terminal에서 실행한 Docker CLI | command not found, old CLI |
| `Server` | container를 실제로 관리하는 Docker daemon | daemon not running, permission denied |
| Version 숫자 | 설치된 Docker component version | 문서/실습 예제와 차이가 날 수 있음 |
| Error message | 연결 실패나 권한 문제 | Desktop 미실행, Linux daemon/권한 문제, Windows WSL 2 문제 |

`docker compose version`은 Week 2 Day 4 전까지 계속 사용할 기본 확인 명령이다. Docker Desktop에는 Docker Compose가 포함되지만, Linux Engine 경로에서는 Compose plugin 설치 여부를 별도로 확인해야 할 수 있다.

### Docker version 주의점
- `Client`만 보이고 `Server`가 없으면 Docker CLI는 있지만 daemon이 준비되지 않은 상태다. Docker Desktop 실행 상태나 Linux daemon 권한을 먼저 확인한다.
- `permission denied`는 Docker 설치 실패가 아니라 Linux user 권한 문제일 수 있다. `sudo docker ...`로 되는지와 post-install 설정 여부를 구분한다.
- Docker version 숫자는 학생마다 조금 다를 수 있다. 수업에서는 숫자를 외우지 말고 client/server가 모두 보이는지, compose plugin이 있는지를 본다.
- 오류 화면을 공유할 때 token, username, 개인 경로가 보이면 가린다.

## Docker Hub 계정/로그인/보안 확인

Docker Hub는 image를 저장하고 내려받을 수 있는 대표 registry다. Day 1에서는 로그인 성공 자체보다 image pull이 가능한 상태인지, credential을 안전하게 다루는지 확인한다.

공개 image를 pull하는 기본 실습은 로그인 없이도 가능한 경우가 많다. 다만 push, private repository, rate limit, 조직 정책에 따라 로그인이 필요할 수 있다. 로그인 과정에서 password, token, MFA code가 terminal output, screenshot, README에 남지 않도록 주의한다.

### 보안 판단 표
| 항목 | 공개 가능 | 공개 금지 |
|---|---|---|
| Docker Hub username | 수업 정책에 따라 가능 | 개인 식별 우려가 있으면 마스킹 |
| image name/tag | 가능 | private naming 정책이 있으면 확인 |
| password/token/MFA | 불가능 | 어떤 경우에도 README/screenshot에 남기지 않음 |
| error message | secret 제거 후 가능 | token 일부가 포함되면 마스킹 |
| login success 여부 | 가능 | credential 값은 확인하지 않음 |

## blocker triage와 다음 교시 준비

설치가 막힌 경우에는 다음 순서로 blocker를 구분한다.

- OS와 설치 경로를 먼저 구분한다. macOS Docker Desktop, Linux Docker Engine, Windows WSL 2는 확인할 지점이 다르다.
- 실패 단계가 다운로드, 설치, 앱 실행, daemon 연결, 권한 문제 중 어디인지 나눈다.
- 에러 메시지는 전체를 복사하지 말고 핵심 문장만 본다. token, 개인 경로, 계정 정보가 섞이면 공유하지 않는다.
- 이미 시도한 해결책을 반복하지 않도록 공식 문서에서 확인한 조건과 다음 확인 지점을 정한다.

### 흔한 오해
| 오해 | 바로잡기 |
|---|---|
| Docker Desktop 창이 열리면 실습 준비가 끝났다. | CLI에서 `docker version`으로 daemon 연결까지 확인해야 한다. |
| `Client` 정보가 보이면 container 실행이 가능하다. | `Server` 연결이 안 되면 container 실행은 실패할 수 있다. |
| 로그인 실패는 Docker 설치 실패와 같다. | 설치/daemon 연결과 Docker Hub 인증은 다른 문제다. |
| error screenshot은 그대로 공유해도 된다. | token, email, 인증코드, 개인 경로가 포함되어 있으면 마스킹해야 한다. |

### 확인 기준
| 기준 | 확인 지점 |
|---|---|
| 공식 문서 사용 | 본인 OS용 Docker 설치 문서 URL과 확인한 requirement를 확인했다. |
| 설치 상태 확인 | macOS Desktop running 또는 Linux Engine daemon 상태/blocker를 구체적으로 확인했다. |
| CLI 연결 확인 | `docker version`의 Client/Server 상태를 구분했다. |
| 보안 책임 | password/token/MFA code를 확인하지 않는다고 명시했다. |
| 도움 요청 품질 | 실패 시 OS, 단계, error summary, 시도한 조치를 남겼다. |

### 공식/학술 근거 링크
- Docker Docs: Docker Desktop, https://docs.docker.com/desktop/ - Docker Desktop이 local에서 containerized application을 build/share/run하는 도구라는 공식 기준이다.
- Docker Docs: Install Docker Desktop on Mac, https://docs.docker.com/desktop/setup/install/mac-install/ - macOS 기본 설치 경로와 Apple silicon/Intel 차이를 확인하는 기준이다.
- Docker Docs: Install Docker Engine on Ubuntu, https://docs.docker.com/engine/install/ubuntu/ - Linux Engine 설치 경로의 공식 기준이다.
- Docker Docs: Linux post-installation steps for Docker Engine, https://docs.docker.com/engine/install/linux-postinstall/ - Linux Engine 권한과 docker group 설정의 공식 기준이다.
- Docker Docs: Install Docker Desktop on Linux, https://docs.docker.com/desktop/setup/install/linux/ - Linux Desktop 예외 경로의 VM/context와 host Engine 차이를 확인하는 기준이다.
- Docker Docs: Install Docker Desktop on Windows, https://docs.docker.com/desktop/setup/install/windows-install/ - Windows 사용자의 WSL 2, 가상화, 권한 조건을 별도 확인하는 기준이다.
- Docker Docs: Sign in to Docker Desktop, https://docs.docker.com/desktop/setup/sign-in/ - Docker Desktop 로그인과 credential 관련 확인 기준이다.
- OWASP Secrets Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html - password, token, credential을 공개 문서와 screenshot에 남기지 않는 보안 기준이다.

### 다음 연결
다음 교시에는 Docker의 핵심 구성요소를 다룬다. `docker version`으로 준비 상태가 확인된 학생은 image와 container 개념을 실제 명령으로 연결하고, blocker가 있는 학생은 설치 단계, OS, error message를 계속 보완해 후반 DB 실습 참여 가능 여부를 분류한다.
