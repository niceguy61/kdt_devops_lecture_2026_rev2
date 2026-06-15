# 3교시: Docker의 컨셉과 작동 방식

## 수업 목표
- Docker의 핵심 구성요소인 image, container, registry, Docker Engine, Docker Desktop의 역할을 구분한다.
- CPU, RAM, disk, network, OS kernel 같은 PC 부품/구성요소와 Docker 컴포넌트를 연결해 이해한다.
- VM 가상화와 Docker 컨테이너화의 OS/kernel 구조 차이를 설명한다.
- `docker run`이 단순 실행 명령이 아니라 image 확보, container 생성, process 시작, network 연결을 포함하는 흐름임을 이해한다.
- Week 1의 process/filesystem/network/config 개념이 Docker 안에서 어떻게 이름을 바꾸는지 설명한다.

## 선행 지식
| 이미 알고 있어야 할 것 | 오늘 새로 연결할 것 |
|---|---|
| process는 command로 시작되고 종료 상태를 가진다 | container는 image에서 시작된 격리된 process다 |
| OS kernel은 process, filesystem, network resource를 중재한다 | container는 host kernel을 공유하는 격리된 process 모델이다 |
| CPU, RAM, disk, network는 실제 PC 자원이다 | Docker는 새 하드웨어가 아니라 PC 자원을 나누어 쓰는 실행 계층이다 |
| file path와 app folder가 실행 재료가 된다 | image는 실행에 필요한 파일과 설정을 포함한다 |
| localhost와 port로 서비스에 접근한다 | port binding으로 host와 container port를 연결한다 |
| README가 실행 절차를 문서화한다 | Dockerfile과 Docker command가 실행 계약을 더 명확히 한다 |

## 50분 흐름
| 시간 | 활동 | 학습 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | Docker 설치 상태 재확인 | client/server 연결 상태를 다시 확인한다. | readiness status |
| 5-15분 | PC 부품과 Docker 컴포넌트 연결 | CPU/RAM/disk/network/kernel을 Docker 용어와 연결한다. | component mapping note |
| 15-25분 | image와 container, VM/컨테이너 구조 | 실행 패키지, 실행 상태, host kernel 공유를 구분한다. | OS/kernel 비교 note |
| 25-35분 | Docker Engine/Desktop 작동 흐름 | CLI, daemon, Desktop의 역할을 나눈다. | 작동 흐름도 |
| 35-45분 | `docker run` 내부 흐름 읽기 | pull/create/start/attach/check를 연결한다. | command 해석 |
| 45-50분 | 오해 점검과 다음 교시 연결 | Docker와 local 실행의 비교 기준을 준비한다. | 확인 질문 |

## 0-5분 Docker 설치 상태 재확인

이 교시는 설치 성공자만을 위한 개념 수업이 아니다. 설치가 막힌 학생도 Docker가 어떤 구성요소로 동작하는지 알아야 이후 blocker를 정확히 설명할 수 있다. `docker version`에서 server가 보이지 않는 경우는 image/container 개념을 이해하지 못해서가 아니라 Docker daemon 연결이 아직 성립하지 않은 상태일 수 있다.

### 빠른 확인 명령
```bash
docker version
```

기록할 것은 전체 출력 복사가 아니라 상태 요약이다. `Client visible`, `Server visible`, `Error summary` 세 가지로 충분하다.

### Visual 1: Docker 작동 구조
![Docker 작동 구조](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day1/assets/lesson-03-docker-architecture.png)

이 이미지는 CLI, Docker Engine, Registry, Image, Container, Network, Volume의 관계를 한 화면에 배치한다. 왼쪽의 `docker run` 요청이 Engine으로 들어가고, Engine이 registry에서 image layer를 받고 container, network, volume을 관리하는 흐름을 본다.

## 5-15분 PC 부품과 Docker 컴포넌트 연결

Docker를 처음 배울 때 가장 먼저 잡아야 할 기준은 Docker가 새로운 물리 하드웨어를 만드는 도구가 아니라는 점이다. 컨테이너가 실행될 때도 실제 연산은 PC의 CPU가 수행하고, 실행 중인 데이터는 RAM을 사용하며, image와 volume은 disk 공간을 차지한다. 외부 접속은 PC의 network stack과 port를 통해 들어오고, 격리와 resource 제어는 OS kernel 기능을 기반으로 동작한다.

그래서 Docker 컴포넌트를 PC 부품과 연결해 읽으면 추상 용어가 줄어든다. Docker Engine은 "컨테이너를 생성하고 실행하고 관리하는 관리자"에 가깝고, container는 "CPU/RAM을 사용해 실행 중인 격리된 process", image는 "disk에 저장된 실행 재료 묶음", volume은 "컨테이너 삭제와 분리해 disk에 남기는 데이터 공간", registry는 "image를 올리고 내려받는 원격 창고"로 이해할 수 있다.

### Visual 2: PC 부품과 Docker 컴포넌트 연결
![PC 부품과 Docker 컴포넌트 연결](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day1/assets/lesson-03-pc-parts-to-docker-components.png)

이 이미지는 CPU, RAM, SSD/disk, network, OS kernel이 Docker Engine, container, image, volume, port binding, registry와 어떻게 연결되는지 보여준다. 오른쪽 Docker 구성요소를 외울 때 왼쪽 PC 자원이 실제로 무엇을 제공하는지 함께 읽는다.

### PC 부품 기반 Docker 컴포넌트 표
| PC 구성요소 | Docker에서 연결되는 말 | 확인 질문 |
|---|---|---|
| CPU | container process 실행 | 어떤 process가 CPU를 쓰고 있는가 |
| RAM | running container memory | container가 너무 많은 memory를 쓰는가 |
| SSD/disk | image, layer, volume, build cache | image와 volume이 disk를 얼마나 차지하는가 |
| Network | port binding, Docker network | host port와 container port가 어떻게 연결되는가 |
| OS kernel | process 격리, filesystem/network/resource 제어 | container가 host kernel 기능에 의존한다는 점을 이해했는가 |
| Remote storage | registry, Docker Hub | image 출처와 tag를 신뢰할 수 있는가 |

## 15-25분 image와 container, VM/컨테이너 구조

image는 container를 만들기 위한 표준 실행 패키지다. Docker 공식 문서는 image를 container 실행에 필요한 files, binaries, libraries, configurations를 포함하는 package로 설명한다. image는 만들어진 뒤 직접 수정하는 대상이 아니라 새 image를 만들거나 layer를 추가해 변경한다.

container는 image에서 시작된 실행 상태다. Week 1에서 `python3 -m http.server` 같은 command가 process를 만들었던 것처럼, Docker에서는 image를 기준으로 container process를 시작한다. 같은 image에서 여러 container를 만들 수 있고, 각 container는 서로 다른 port, environment variable, volume을 가질 수 있다.

### Visual 3: image와 container의 차이
| 구분 | Image | Container |
|---|---|---|
| 상태 | 실행 전 package | 실행 중 또는 종료된 instance |
| 바뀌는가 | 보통 immutable로 다룸 | 실행 상태, log, writable layer가 생김 |
| 예시 | `nginx:latest` | `web-demo-1` container |
| 확인 명령 | `docker images` | `docker ps`, `docker ps -a` |
| 운영 질문 | 출처와 tag를 신뢰할 수 있는가 | 현재 running/exited 상태인가 |

### Visual 4: VM 가상화와 컨테이너화의 OS/kernel 구조
![VM 가상화와 컨테이너화의 OS/kernel 구조](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day1/assets/lesson-03-vm-vs-container-os-kernel.png)

Docker를 정확히 이해하려면 "컨테이너는 작은 VM인가?"라는 질문을 분리해야 한다. VM 가상화는 hypervisor 위에 여러 가상 머신을 만들고, 각 VM이 보통 자기 Guest OS와 kernel을 가진다. 그래서 OS 전체를 분리해 실행할 수 있지만, Guest OS까지 포함하므로 상대적으로 무겁다.

컨테이너화는 다른 모델이다. 컨테이너는 보통 host OS kernel을 공유하면서 서로 격리된 process로 실행된다. container image 안에는 애플리케이션 실행에 필요한 파일, library, binary, 설정이 들어가지만 OS 전체와 별도 kernel이 들어간다고 이해하면 안 된다. Linux container가 Linux kernel 기능을 사용하기 때문에, macOS에서 Docker Desktop으로 Linux container를 실행할 때는 Docker Desktop이 내부 Linux VM 계층을 관리한다. Windows 사용자는 별도 경로로 WSL 2 backend와 가상화 조건을 확인한다.

이 이미지는 왼쪽 VM 구조에서 각 가상 머신이 Guest OS를 갖는 방식과, 오른쪽 컨테이너 구조에서 여러 container가 host OS kernel을 공유하는 방식을 비교한다. 아래쪽 OS별 경로는 macOS의 Docker Desktop 내부 Linux VM 계층과 Windows 사용자의 WSL 2 경로를 구분해 읽는다.

### 구조 비교 표
| 관점 | VM 가상화 | Docker 컨테이너화 |
|---|---|---|
| 실행 단위 | Guest OS를 포함한 가상 머신 | host kernel을 공유하는 격리된 process |
| OS/kernel | VM마다 Guest OS/kernel이 있을 수 있음 | container마다 별도 kernel을 갖지 않음 |
| 무게 | OS 전체가 포함되어 상대적으로 무거움 | app/library 중심이라 상대적으로 가벼움 |
| 격리 방식 | hypervisor 기반 가상 hardware/OS 격리 | namespace/cgroup 같은 kernel 기능 기반 격리 |
| macOS에서 Linux container | Linux VM 계층 필요 | Docker Desktop이 내부 Linux VM 계층을 관리 |
| Windows에서 Linux container | WSL 2 또는 Windows backend 조건 확인 필요 | Windows 사용자는 별도 설치 문서로 확인 |
| 운영 오해 | VM처럼 OS 전체를 복제한다고 생각함 | host kernel 의존성을 잊고 아무 OS나 실행 가능하다고 생각함 |

### 운영 판단
- container image에는 "실행에 필요한 사용자 공간 파일과 library"가 들어간다. kernel 자체를 image에 넣어 실행한다고 설명하지 않는다.
- Linux container는 Linux kernel 기능에 의존한다. macOS에서는 Docker Desktop이 내부 Linux VM 계층을 관리하고, Windows에서는 WSL 2와 virtualization 조건이 중요할 수 있다.
- container가 VM보다 가볍다는 말은 "항상 안전하다"는 뜻이 아니다. host kernel을 공유하므로 kernel 취약점, 권한, runtime 설정도 운영 책임에 포함된다.

## 25-35분 Docker Engine/Desktop 작동 흐름

Docker Desktop은 사용자가 containerized application을 local machine에서 build, share, run하기 쉽게 해준다. 하지만 Desktop 창이 Docker의 전부는 아니다. CLI 명령은 Docker Engine 또는 daemon에 전달되고, daemon이 image와 container lifecycle을 처리한다.

설치 문제를 분석할 때 이 구분이 중요하다. Desktop이 꺼져 있으면 CLI가 server에 연결하지 못할 수 있다. CLI가 설치되어 있어도 daemon이 실행 중이 아니면 container는 시작되지 않는다. registry 로그인 문제는 daemon 연결 문제와 다르다.

registry는 image를 저장하고 내려받는 곳이다. Docker Hub는 대표적인 public registry다. 학생은 image를 pull할 때 "이름이 익숙하다"보다 출처, tag, 공식 이미지 여부, 업데이트 책임을 확인해야 한다. `nginx` 같은 공식 이미지는 학습과 실습에 적합하지만, 실무에서는 아무 image나 그대로 가져오지 않는다. base image 선택은 보안, 크기, 유지보수, 취약점 대응에 영향을 준다.

### Visual 5: Docker 구성요소 관계
![Mermaid diagram 1](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/lecture_mermaid_assets/week2__day1__lesson-03--diagram-01.png)

읽는 순서: terminal의 Docker CLI는 Docker Engine에 요청을 보낸다. Engine은 local image, container, network, volume을 관리하고 필요한 image를 registry에서 가져온다. Docker Desktop은 이 과정을 GUI와 local runtime으로 보조한다.

### 판단 표: 어느 구성요소 문제인가
| 증상 | 가능성 | 확인할 것 |
|---|---|---|
| `docker: command not found` | CLI 설치/PATH 문제 | Docker Desktop 설치, terminal 재시작 |
| `Cannot connect to the Docker daemon` | daemon/Desktop 미실행 | Desktop running, service status |
| image pull 실패 | network, registry, auth 문제 | internet, Docker Hub, login |
| container 실행 후 접속 실패 | port binding 또는 app process 문제 | `docker ps`, `docker logs`, `curl` |
| container는 실행되지만 데이터 없음 | volume/config 문제 | volume mount, env var |

## 35-45분 `docker run` 내부 흐름 읽기

처음 보는 학생에게 `docker run nginx`는 한 줄 명령처럼 보이지만, 실제로는 여러 단계가 합쳐진다. local에 image가 없으면 registry에서 pull하고, image를 기준으로 container를 만들고, container 내부 process를 시작한다. port를 지정하지 않으면 container 안의 web server가 떠 있어도 host browser에서 바로 접근할 수 없을 수 있다.

### Visual 6: `docker run`이 하는 일
![Mermaid diagram 2](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/lecture_mermaid_assets/week2__day1__lesson-03--diagram-02.png)

읽는 순서: `run`은 image 확보와 container 시작을 함께 수행할 수 있다. 그래서 실패 메시지도 pull 실패, container 생성 실패, process 실패, port 충돌 등으로 나누어 읽어야 한다.

## 45-50분 오해 점검과 다음 교시 연결

### 흔한 오해
| 오해 | 바로잡기 |
|---|---|
| image를 실행하면 image가 바뀐다. | 실행으로 생기는 상태는 container 쪽에서 다룬다. image는 재사용 가능한 package로 본다. |
| container는 작은 VM이다. | container는 보통 host kernel을 공유하는 격리된 process 모델이다. Guest OS 전체를 매번 실행하는 VM 모델과 다르다. |
| container image 안에는 완전한 OS와 kernel이 들어 있다. | image에는 사용자 공간 파일과 library가 들어갈 수 있지만, container는 host kernel을 사용한다. |
| macOS에서 Docker를 쓰면 WSL 2가 필요하다. | macOS는 WSL 2를 쓰지 않는다. Docker Desktop이 내부 Linux VM 계층을 관리한다. |
| Windows에서 Linux container를 바로 실행한다. | Windows 사용자는 Docker Desktop의 WSL 2 backend 또는 관련 가상화 조건을 공식 문서로 확인해야 한다. |
| Docker Hub의 모든 image는 안전하다. | 출처, 공식 이미지 여부, tag, update 상태를 확인해야 한다. |
| Docker Desktop만 배우면 Docker를 이해한 것이다. | Desktop은 도구 표면이고, 운영 판단은 image/container/network/volume evidence에서 나온다. |

### 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 개념 구분 | image와 container를 실행 전 package와 실행 상태로 구분했다. |
| PC 부품 매핑 | CPU/RAM/disk/network/kernel을 container/image/volume/port binding과 연결했다. |
| OS/kernel 구조 | VM의 Guest OS 모델과 container의 host kernel 공유 모델을 비교했다. |
| 구성요소 이해 | CLI, Engine, Desktop, registry의 역할을 설명했다. |
| 실패 분류 | pull, daemon, port, process 중 하나 이상의 실패 위치를 구분했다. |
| 보안/출처 인식 | image 출처와 tag 확인 필요성을 설명했다. |
| Week 1 연결 | process/filesystem/network/config 중 2개 이상을 Docker 표현과 연결했다. |

### 공식/학술 근거 링크
- Docker Docs: Docker overview, https://docs.docker.com/engine/docker-overview/ - Docker architecture와 image/container/registry 개념의 공식 기준이다.
- Docker Docs: What is an image?, https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/ - image가 immutable하고 layer로 구성된다는 기준이다.
- Docker Docs: Docker Desktop, https://docs.docker.com/desktop/ - Docker Desktop의 local build/share/run 역할을 확인하는 기준이다.
- Docker Docs: Install Docker Desktop on Mac, https://docs.docker.com/desktop/setup/install/mac-install/ - macOS 기본 설치 경로와 chip별 설치 조건을 확인하는 공식 기준이다.
- Docker Docs: Install Docker Desktop on Windows, https://docs.docker.com/desktop/setup/install/windows-install/ - Windows 사용자의 WSL 2와 가상화 조건을 별도로 확인하는 공식 기준이다.

### 다음 연결
다음 교시는 Docker와 local computer 실행 방식을 비교한다. Docker가 좋아지는 지점뿐 아니라 host resource 사용, image 관리, secret 노출, cleanup 책임 같은 비용과 한계를 함께 판단한다.
