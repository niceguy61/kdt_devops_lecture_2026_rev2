<sub>[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [2일차](README.md) › 3/7교시</sub>

# 3교시 · nginx를 백그라운드로 실행

> [!NOTE]
> **이번 시간에 할 일**
>
> - `docker pull`로 이미지를 미리 받고, 층(레이어) 단위로 내려받는 모습을 봅니다.
> - 컨테이너를 앞(foreground)에서 실행하고 `Ctrl` + `C`로 멈춥니다.
> - `-d`와 `--name`으로 백그라운드 컨테이너를 실행합니다.
> - 실행은 되는데 접속이 안 되는 이유를 1주차 3일차 지식으로 설명합니다.

## 웹 서버 nginx

**nginx**(엔진엑스)는 웹 페이지를 내주고, 1주차 3일차에 배운 **리버스 프록시**와 **로드밸런서** 역할도 하는 서버 프로그램입니다. 이번 주 5일차에 DevMart의 화면을 보여 주고 `/api` 요청을 상품 API로 넘기는 역할을 맡습니다. 오늘은 그 전에 nginx 컨테이너를 다루는 연습을 합니다.

## 실습 3 · 이미지 미리 받기

> **🧪 실습: 실습 목표**
>
> nginx 이미지를 받으면서 이미지가 **여러 층으로 나뉘어** 내려오는 것을 확인합니다.

### 단계 1 — pull

```bash
docker pull nginx:1.30-alpine
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 1.30-alpine: Pulling from library/nginx
> 7a2b6f1c4e3d: Pull complete
> 5c8e9a1b2d3f: Pull complete
> a4d3c2b1e0f9: Pull complete
> ...
> Digest: sha256:4f1c…
> Status: Downloaded newer image for nginx:1.30-alpine
> docker.io/library/nginx:1.30-alpine
> ```
> `Pull complete` 줄이 **여러 개**입니다. 이미지가 하나의 큰 파일이 아니라 **여러 층(레이어)**으로 되어 있기 때문입니다. 마지막 `Digest: sha256:…`은 어제 3교시 학술 노트의 그 **내용 지문**입니다. 3일차에 레이어와 다이제스트를 자세히 배웁니다.

### 단계 2 — 받은 이미지 확인

```bash
docker images
```

> **🟢 확인: 이렇게 나오면 성공**
>
> `alpine:3.24`, `hello-world:latest`, **`nginx:1.30-alpine`**이 보입니다. Alpine 기반이라 크기가 작습니다.

## 실습 4 · 앞에서 실행하고 멈추기

> **🧪 실습: 실습 목표**
>
> `-d` 없이 실행하면 터미널이 어떻게 되는지 보고, `Ctrl` + `C`로 멈춰 봅니다.

### 단계 1 — 앞에서 실행

```bash
docker run --rm nginx:1.30-alpine
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
> ...
> /docker-entrypoint.sh: Configuration complete; ready for start up
> 2026/11/30 01:10:12 [notice] 1#1: nginx/1.30.6
> 2026/11/30 01:10:12 [notice] 1#1: start worker processes
> ```
> 로그가 나오고 **프롬프트가 돌아오지 않습니다.** nginx는 hello-world와 달리 할 일을 끝내고 종료하는 프로그램이 아니라, 요청을 **계속 기다리는** 서버이기 때문입니다. `1#1`의 첫 1은 **PID 1**입니다(2교시).

### 단계 2 — 멈추기

`Ctrl` + `C`를 누릅니다. nginx가 종료되고 프롬프트가 돌아옵니다. `--rm`을 붙였으니 컨테이너도 사라졌습니다. 이렇게 앞에서 실행하면 터미널을 하나 차지하므로 불편합니다.

## 실습 5 · 백그라운드로 실행

> **🧪 실습: 실습 목표**
>
> `-d`로 nginx를 백그라운드에 띄우고, `docker ps`로 확인한 뒤, 접속을 시도해 봅니다.

### 단계 1 — 백그라운드 실행

```bash
docker run -d --name web nginx:1.30-alpine
```

| 옵션 | 뜻 |
|---|---|
| `-d` | **d**etached — 백그라운드에서 실행하고 터미널을 바로 돌려준다 |
| `--name web` | 컨테이너 이름을 `web`으로 정한다. 앞으로 ID 대신 이름으로 부른다 |

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 52ae767dfac9e4b1c0a3f8d27e65b9c1a4d8f02e7b3c6a915d04e2f8b7c1a3d6
> ```
> 긴 문자열(컨테이너 ID 전체) 한 줄이 나오고 프롬프트가 바로 돌아옵니다.

### 단계 2 — 실행 중인지 확인

```bash
docker ps
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS     NAMES
> 52ae767dfac9   nginx:1.30-alpine   "/docker-entrypoint.…"   5 seconds ago   Up 4 seconds   80/tcp    web
> ```
> STATUS가 **Up**, NAMES가 **web**입니다. PORTS에 **`80/tcp`**가 보입니다. 이 컨테이너 안에서 nginx가 80번 포트를 열고 기다린다는 뜻입니다.

### 단계 3 — 접속해 보기

```bash
curl http://localhost:80
```

> **🟢 확인: 예상되는 결과 — 실패**
>
> ```text
> curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server
> ```
> nginx는 분명 Up인데 접속이 안 됩니다. 왜일까요?

> [!IMPORTANT]
> **1주차 3일차로 설명하기**
>
> 컨테이너는 자기만의 **네트워크 네임스페이스**를 가집니다. 컨테이너 안의 80번 포트는 **컨테이너라는 건물 안의 80호실**일 뿐, 내 노트북이라는 건물의 80호실이 아닙니다. 지금 `localhost:80`은 내 노트북의 80호실에 노크한 것이고, 거기에는 아무도 없으니 1주차 3일차 에러 표의 **"닿았지만 받을 프로그램이 없다(refused)"**와 같은 상황입니다. PORTS의 `80/tcp`에 **화살표(`->`)가 없는 것**이 바로 그 증거입니다. 다음 시간에 두 건물을 잇는 통로를 뚫습니다.

> **🧹 정리: 정리**
>
> ```bash
> docker rm -f web
> ```
> `-f`(force)는 실행 중인 컨테이너를 **멈추고 지우는 것을 한 번에** 합니다. 6교시에 차근차근 나눠서 해 봅니다.

> **🎓 학술 노트 — 데몬과 '한 컨테이너, 한 프로세스'**
>
> nginx처럼 계속 떠서 요청을 기다리는 프로그램을 Unix에서는 **데몬(daemon)**이라고 부릅니다. 전통적인 서버에서는 데몬을 백그라운드로 돌리고, 죽으면 다시 살리는 일을 **init 시스템**(오늘날의 systemd)이 맡았습니다.
>
> 컨테이너에서는 이 구조가 바뀝니다. 컨테이너 안에는 보통 systemd가 없고, **우리가 실행한 프로그램 자체가 PID 1**입니다. 그래서 nginx 이미지는 nginx를 데몬 모드로 보내지 않고 **앞에서(`daemon off`) 실행**합니다. PID 1이 끝나면 컨테이너가 끝나기 때문입니다. 그리고 "죽으면 다시 살리기"는 컨테이너 바깥의 Docker(재시작 정책, 6교시)나 Kubernetes(3주차)가 맡습니다. 이 분업이 Docker가 권장하는 **"컨테이너 하나에 관심사 하나(one concern per container)"** 원칙의 바탕입니다. 웹 서버와 DB를 한 컨테이너에 넣지 않고 5일차처럼 따로 띄우는 이유입니다.
>
> - Docker Docs. *Building best practices — Decouple applications*. docs.docker.com/build/building/best-practices
> - Burns, B., & Oppenheimer, D. (2016). Design patterns for container-based distributed systems. *USENIX HotCloud '16*.

> **📈 트렌드 — nginx 1.30과 '버전을 적는' 습관**
>
> nginx는 전체 웹사이트의 약 3분의 1이 쓰는 가장 널리 쓰이는 웹 서버 중 하나입니다. 2026년 4월 새 안정 버전 **1.30**이 나오면서 1.28과 1.29는 지원이 끝났고, 이후에도 여러 차례 보안 패치(1.30.x)가 나왔습니다. 이것이 이 교재가 `nginx:latest` 대신 `nginx:1.30-alpine`처럼 **주 버전을 적고**, 패치 번호(1.30.6 등)는 이미지가 알아서 최신을 따라가게 하는 이유입니다. 너무 느슨하면(`latest`) 갑자기 큰 변화가 들어오고, 너무 빡빡하면(`1.30.0` 고정) 보안 패치를 놓칩니다. 이 균형을 정하는 것도 DevOps 엔지니어의 일입니다.

## 정리

- `docker pull`은 이미지를 **여러 층**으로 내려받고, 마지막에 **다이제스트(sha256)**를 보여 줍니다.
- `-d` 없이 실행한 서버는 터미널을 차지하고, `Ctrl` + `C`로 멈춥니다.
- `docker run -d --name 이름`으로 백그라운드에서 이름 붙여 실행합니다.
- 컨테이너 안의 포트는 컨테이너 건물 안의 호실입니다. **포트를 연결하지 않으면 바깥에서 들어갈 수 없습니다.**

> **✅ 확인 문제**
>
> 1. `docker pull` 출력에 `Pull complete`가 여러 줄 나오는 이유는?
> 2. nginx를 `-d` 없이 실행하면 프롬프트가 돌아오지 않는 이유는?
> 3. `-d`와 `--name`은 각각 무슨 옵션인가요?
> 4. `docker ps`의 PORTS가 `80/tcp`일 때 `localhost:80`으로 접속이 안 되는 이유는?
> 5. 실행 중인 컨테이너를 한 번에 멈추고 지우는 명령은?
>
> <details><summary>정답</summary>
>
> 1. 이미지가 여러 층(레이어)으로 되어 있어 층마다 내려받기 때문
> 2. nginx는 요청을 계속 기다리는 서버(데몬)라 끝나지 않기 때문
> 3. `-d`는 백그라운드 실행(detached), `--name`은 컨테이너 이름 지정
> 4. 컨테이너는 별도의 네트워크 네임스페이스를 가지므로, 포트를 호스트에 연결(publish)하지 않으면 바깥에서 닿을 수 없다
> 5. `docker rm -f 이름`
>
> </details>

## 참고 문헌

- Docker Hub. *nginx Docker Official Image*. hub.docker.com/_/nginx
- nginx. *nginx news*. nginx.org/en/news.html
- Docker Docs. *docker container run — detached mode (-d), --name*. docs.docker.com
- Burns, B., & Oppenheimer, D. (2016). Design patterns for container-based distributed systems. *HotCloud '16*.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [2교시 · 컨테이너 안에 들어가 보기](lesson-02.md) | [⬆️ 2일차 목차](README.md) | [4교시 · 포트 연결](lesson-04.md) ➡️ |
