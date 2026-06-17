# 5교시: Docker 기본 명령어 1 - 실행 80% 사이클

## 수업 목표
- Docker 기본 명령어를 암기 목록이 아니라 상태 확인과 lifecycle 제어 도구로 사용한다.
- `version`, `pull`, `images`, `run`, `ps`, `logs`, `stop`, `rm`을 실행 목적과 확인 지점 기준으로 연결한다.
- 실행 후 중지와 정리까지 포함한 하나의 hands-on cycle을 완성한다.

## 강의 전개

이 교시는 Docker 명령어를 많이 소개하는 시간이 아니라, 하나의 container lifecycle을 끝까지 닫는 시간이다. 학생이 `docker run`만 성공시키고 넘어가면 이후 port 충돌, 이름 충돌, disk 누적을 스스로 만든다. 그래서 실행, 확인, 관찰, 중지, 삭제를 하나의 묶음으로 반복한다.

실습 image는 `nginx:latest`를 사용한다. PostgreSQL을 바로 시작하지 않는 이유는 web server가 port publishing을 눈으로 확인하기 쉽고, DB password와 readiness 같은 변수를 잠시 미룰 수 있기 때문이다. 여기서 `18080:80` mapping을 이해하면 다음 교시의 `15432:5432`, `15433:5432` mapping을 더 자연스럽게 받아들인다.

명령은 상태 질문과 함께 읽는다. `docker version`은 CLI와 daemon이 연결됐는지 묻는다. `docker pull`은 registry에서 image를 가져올 수 있는지 묻는다. `docker images`는 local disk에 어떤 실행 재료가 있는지 묻는다. `docker ps`는 현재 실행 중인 container와 port binding을 묻는다. `docker logs`는 process가 남긴 관찰 확인 지점을 묻는다. `docker stop`과 `docker rm`은 운영자가 lifecycle을 끝까지 책임졌는지 묻는다.

출력 차이도 정상 범위로 설명한다. 처음 pull하는 학생은 layer download가 보이고, 이미 받은 학생은 up to date가 보일 수 있다. container ID는 장비마다 다르다. Docker version도 다를 수 있다. 수업에서 고정해야 하는 것은 전체 문자열이 아니라 image name, container name, port binding, status, log의 의미다.

마지막에는 cleanup을 강하게 확인한다. container가 남아 있으면 다음 실습에서 이름 충돌이나 port 충돌이 난다. 특히 교육 환경에서는 "실습이 끝났다"의 기준을 browser 확인이 아니라 `stop`, `rm`, `ps` 재확인까지로 잡아야 한다.

## 실습 전 기준

오늘 명령은 모두 로컬 Docker와 Docker Hub public image를 사용한다. cloud resource는 만들지 않는다. container 이름은 충돌을 피하기 위해 `paperclip-day1-nginx`를 사용한다. 기존에 같은 이름의 container가 있으면 먼저 정리해야 한다.

```bash
docker ps -a --filter name=paperclip-day1-nginx
```

출력이 비어 있으면 바로 진행한다. 같은 이름의 container가 보이면 6교시 정리 절차에 따라 `stop`과 `rm`을 수행한다.

## 기본 명령 목적표
| 명령 | 실행 목적 | 정상 확인 지점 | 흔한 실패 |
|---|---|---|---|
| `docker version` | CLI와 daemon 연결 확인 | Client/Server 정보가 보임 | daemon 미실행, 권한 문제 |
| `docker pull nginx:latest` | registry에서 image 확보 | digest와 status 출력 | network/auth/image name 문제 |
| `docker images` | local image 목록 확인 | `nginx`, `hello-world` 등 표시 | socket 권한 문제 |
| `docker run` | image에서 container 시작 | container ID 또는 output | port 충돌, image 없음 |
| `docker ps` | running container 확인 | STATUS, PORTS, NAMES 확인 | 필터/이름 오타 |
| `docker logs` | process log 확인 | entrypoint/start log | container 이름 오타 |
| `docker stop` | running container 정상 중지 | container 이름 반환 | 이미 종료됨 |
| `docker rm` | stopped container 삭제 | container 이름 반환 | 실행 중이라 삭제 실패 |

## Hands-on 1: Docker 연결과 image 준비

```bash
docker version
docker pull nginx:latest
docker images
```

### Linux 사전 테스트 결과
환경: Ubuntu 24.04.3 LTS, Linux `6.6.87.2-microsoft-standard-WSL2`, Docker Client `29.0.2`, Docker Server `29.3.1`.

`docker version` 핵심 출력:

```text
Client: Docker Engine - Community
 Version:           29.0.2
 OS/Arch:           linux/amd64

Server:
 Engine:
  Version:          29.3.1
  OS/Arch:          linux/amd64
```

`docker pull nginx:latest` 재실행 시 출력:

```text
latest: Pulling from library/nginx
Digest: sha256:5aca99593157f4ae539a5dec1092a0ad8762f8e2eb1789085a13a0f5622369f6
Status: Image is up to date for nginx:latest
docker.io/library/nginx:latest
```

처음 실행하는 학생은 `Downloaded newer image`가 보일 수 있다. 이미 받은 학생은 `Image is up to date`가 보일 수 있다. 둘 다 정상이다.

## Hands-on 2: container 시작과 상태 확인

```bash
docker run -d --name paperclip-day1-nginx -p 18080:80 nginx:latest
docker ps --filter name=paperclip-day1-nginx
```

### 기대 결과
`docker run -d`는 긴 container ID를 출력한다. `docker ps`는 다음과 비슷하게 보인다.

```text
CONTAINER ID   IMAGE          COMMAND                  STATUS          PORTS                                       NAMES
ce1d01f8a780   nginx:latest   "/docker-entrypoint.…"   Up 44 seconds   0.0.0.0:18080->80/tcp, [::]:18080->80/tcp   paperclip-day1-nginx
```

`PORTS`에서 `18080->80/tcp`가 핵심이다. host의 `18080` port로 들어온 요청이 container 내부의 `80` port로 전달된다.

## Hands-on 3: log 확인과 정리

```bash
docker logs paperclip-day1-nginx
docker stop paperclip-day1-nginx
docker rm paperclip-day1-nginx
docker ps --filter name=paperclip-day1-nginx
```

### Linux 사전 테스트 결과
`docker logs` 핵심 출력:

```text
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/06/04 04:07:14 [notice] 1#1: nginx/1.31.1
2026/06/04 04:07:14 [notice] 1#1: start worker processes
```

`docker stop`과 `docker rm` 출력:

```text
paperclip-day1-nginx
paperclip-day1-nginx
```

정리 후 `docker ps --filter name=paperclip-day1-nginx` 출력:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

헤더만 보이면 running container가 남아 있지 않은 상태다.

## 주의할 점 메모
| 항목 | 학생 확인 |
|---|---|
| `docker version` Client/Server 확인 | |
| `nginx:latest` pull 결과 | |
| container name | `paperclip-day1-nginx` |
| port binding | `18080:80` |
| `docker ps` STATUS/PORTS | |
| `docker logs` 핵심 1줄 | |
| stop/rm 완료 여부 | |
| screenshot filename | |

## 흔한 오해
| 오해 | 바로잡기 |
|---|---|
| `docker run`만 성공하면 끝이다. | `ps`, `logs`, `stop`, `rm`까지 해야 운영 cycle이 닫힌다. |
| `docker images`에 기존 이미지가 많으면 문제다. | 기존 실습 이력이 있을 수 있다. 오늘 image인 `nginx`, `hello-world`를 구분해 확인한다. |
| `Image is up to date`는 실패다. | 이미 최신 image가 local에 있다는 뜻이다. |
| `rm`을 먼저 하면 된다. | running container는 보통 먼저 `stop`한 뒤 `rm`한다. |

## 확인 기준
| 기준 | 확인 지점 |
|---|---|
| 실행 비중 | 직접 명령을 실행하고 결과를 확인했다. |
| 상태 확인 | `version`, `images`, `ps`, `logs` 중 3개 이상의 출력 의미를 설명했다. |
| 정리 | `stop`과 `rm` 후 남은 container가 없음을 확인했다. |
| 재현성 | container name, port, image tag를 정확히 확인했다. |
| 보안/비용 | cloud resource를 만들지 않고 local 실습만 수행했다. |

### 공식 근거 링크
- Docker Docs: Docker run reference, https://docs.docker.com/reference/cli/docker/container/run/
- Docker Docs: docker container ls, https://docs.docker.com/reference/cli/docker/container/ls/
- Docker Docs: docker container logs, https://docs.docker.com/reference/cli/docker/container/logs/

### 다음 연결
다음 교시는 같은 명령 사이클을 PostgreSQL 공식 image에 적용한다. 핵심은 "container가 떠 있다"가 아니라 port, log, query result, cleanup으로 DB 실행 상태를 검증하는 것이다.
