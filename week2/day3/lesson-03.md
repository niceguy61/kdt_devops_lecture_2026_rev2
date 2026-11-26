[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [3일차](README.md)

# 3교시 · 첫 빌드와 실행

> [!NOTE]
> **이번 시간에 할 일**
>
> - `docker build`로 DevMart 상품 API 이미지를 만듭니다.
> - 빌드 출력에서 각 단계(층)를 읽습니다.
> - 만든 이미지를 컨테이너로 실행하고 `curl`로 세 주소를 확인합니다.
> - 같은 이미지를 **환경 변수만 바꿔** 다르게 실행해 봅니다.

## 실습 4 · 첫 빌드

> **🧪 실습: 실습 목표**
>
> Dockerfile로 `devmart/catalog-api:1.0.0` 이미지를 만듭니다.

### 단계 1 — 빌드

```bash
cd ~/devops-lab/devmart/catalog-api
docker build -t devmart/catalog-api:1.0.0 .
```

| 부분 | 뜻 |
|---|---|
| `docker build` | Dockerfile을 읽어 이미지를 만든다 |
| `-t devmart/catalog-api:1.0.0` | 만든 이미지에 **이름:태그**를 붙인다 (tag) |
| `.` | **빌드 컨텍스트** — 지금 폴더의 파일들을 빌드 재료로 쓴다 (4교시) |

> [!WARNING]
> **마지막 점(`.`)을 빼먹지 마세요**
>
> `docker build -t devmart/catalog-api:1.0.0`처럼 점을 빼면 `requires 1 argument` 에러가 납니다. 초보자가 가장 많이 하는 실수입니다.

> **🟢 확인: 이렇게 나오면 성공 (처음 빌드)**
>
> ```text
> [+] Building 38.2s (11/11) FINISHED
>  => [internal] load build definition from Dockerfile                       0.0s
>  => [internal] load metadata for docker.io/library/python:3.14-slim        1.8s
>  => [internal] load .dockerignore                                          0.0s
>  => [1/6] FROM docker.io/library/python:3.14-slim@sha256:…                 9.4s
>  => [internal] load build context                                          0.0s
>  => [2/6] WORKDIR /app                                                      0.2s
>  => [3/6] RUN useradd --create-home --uid 10001 appuser                    0.4s
>  => [4/6] COPY requirements.txt .                                           0.0s
>  => [5/6] RUN pip install --no-cache-dir -r requirements.txt              24.6s
>  => [6/6] COPY app.py .                                                     0.0s
>  => exporting to image                                                      1.1s
>  => => naming to docker.io/devmart/catalog-api:1.0.0                       0.0s
> ```
> `[1/6]`부터 `[6/6]`까지가 **파일을 바꾸는 명령**(FROM, WORKDIR, RUN, COPY)입니다. Dockerfile에서 쓴 순서 그대로입니다. 가장 오래 걸린 것은 `pip install`이고, 시간은 네트워크에 따라 다릅니다.

### 단계 2 — 만든 이미지 확인

```bash
docker images devmart/catalog-api
docker image history devmart/catalog-api:1.0.0
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> IMAGE                       ID             DISK USAGE   CONTENT SIZE   EXTRA
> devmart/catalog-api:1.0.0   b5965886b8ee        …MB          …MB
>
> CREATED BY                                      SIZE
> CMD ["gunicorn" "--bind" "0.0.0.0:8000" "--a…   0B
> EXPOSE [8000/tcp]                               0B
> ENV APP_VERSION=1.0.0                           0B
> USER appuser                                    0B
> COPY app.py . # buildkit                        …kB
> RUN /bin/sh -c pip install --no-cache-dir -r…   …MB
> COPY requirements.txt . # buildkit              …B
> RUN /bin/sh -c useradd --create-home --uid 1…   …kB
> WORKDIR /app                                    0B
> ...
> ```
> 1교시에서 nginx로 본 것과 같은 구조가 **내가 쓴 Dockerfile**로 만들어졌습니다. 내 코드(`app.py`)는 겨우 몇 kB이고, 대부분은 파이썬과 라이브러리입니다.

## 실습 5 · 실행하고 확인하기

> **🧪 실습: 실습 목표**
>
> 만든 이미지를 실행하고 `/health`, `/api/info`, `/api/products`를 차례로 확인합니다.

### 단계 1 — 실행

```bash
docker run -d --name api -p 8000:8000 devmart/catalog-api:1.0.0
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> NAMES     IMAGE                       PORTS                                         STATUS
> api       devmart/catalog-api:1.0.0   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   Up 3 seconds
> ```

### 단계 2 — 세 주소 확인

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/info
curl http://localhost:8000/api/products
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> {"status":"ok"}
> {"database":"not configured (sample data)","env":"local","hostname":"03e4a973b22a","service":"catalog-api","version":"1.0.0"}
> {"items":[{"id":1,"name":"러닝화","price":59000},{"id":2,"name":"후드 집업","price":45000},{"id":3,"name":"에코백","price":12000}],"source":"sample"}
> ```
> 브라우저에서 `http://localhost:8000/api/products`를 열어도 됩니다. **내 노트북에 파이썬을 설치하지 않았는데** 파이썬 앱이 돌아가고 있습니다. `hostname`은 어제 2교시에서 본 것처럼 **컨테이너 ID**입니다.

### 단계 3 — 로그와 사용자 확인

```bash
docker logs api
docker exec api whoami
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> [2026-11-30 03:02:41 +0000] [1] [INFO] Starting gunicorn 27.0.1
> [2026-11-30 03:02:41 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
> [2026-11-30 03:02:41 +0000] [7] [INFO] Booting worker with pid: 7
> 172.17.0.1 - - [30/Nov/2026:03:02:48 +0000] "GET /health HTTP/1.1" 200 16 "-" "curl/8.5.0"
> ...
> appuser
> ```
> - `Listening at: http://0.0.0.0:8000 (1)` — **0.0.0.0**에서, **PID 1**로 기다린다.
> - 요청 기록이 표준 출력으로 나와 `docker logs`로 보인다 (`--access-logfile -`).
> - `whoami`가 **appuser** — root가 아니다 (Dockerfile의 `USER`).

## 실습 6 · 같은 이미지, 다른 설정

> **🧪 실습: 실습 목표**
>
> 이미지를 다시 빌드하지 않고 **환경 변수만 바꿔** 다른 환경처럼 실행합니다.

### 단계 1 — 개발 환경처럼 하나 더

```bash
docker run -d --name api-dev -p 8001:8000 \
  -e APP_ENV=dev \
  -e APP_VERSION=1.0.0-dev \
  devmart/catalog-api:1.0.0
```

- `-e 이름=값` : 컨테이너에 환경 변수를 넣는다. Dockerfile의 `ENV` 기본값을 **덮어쓴다**.

### 단계 2 — 비교

```bash
curl http://localhost:8000/api/info
curl http://localhost:8001/api/info
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> {"database":"not configured (sample data)","env":"local","hostname":"03e4a973b22a","service":"catalog-api","version":"1.0.0"}
> {"database":"not configured (sample data)","env":"dev","hostname":"c23dd62235b0","service":"catalog-api","version":"1.0.0-dev"}
> ```
> **같은 이미지**인데 `env`와 `version`이 다르고, 서로 다른 컨테이너라 `hostname`도 다릅니다.

> [!IMPORTANT]
> **이미지는 하나, 설정은 환경마다 — 12-Factor III**
>
> 1주차 4일차 6교시 **12-Factor App의 III. 설정 — "설정은 코드가 아니라 환경 변수에"**를 직접 확인했습니다. 개발·테스트·운영 환경마다 이미지를 따로 만들면, "테스트한 이미지"와 "운영에 나간 이미지"가 달라져 테스트가 의미 없어집니다. 그래서 현업은 **이미지는 한 번만 빌드**하고, 환경마다 **설정만 다르게** 넣어 실행합니다. 1주차 5일차 2교시 CI/CD 파이프라인의 "⑤ 이미지 저장 → ⑥ 배포"에서 같은 이미지가 스테이징과 운영으로 차례로 나가는 이유입니다. 내일 DB 주소와 비밀번호도 이렇게 넣습니다.

> **🧹 정리: 정리와 커밋**
>
> ```bash
> docker rm -f api api-dev
> cd ~/devops-lab
> git add devmart/
> git status
> git commit -m "3일차: DevMart 상품 API와 Dockerfile 추가"
> git push
> ```
> 이미지(`devmart/catalog-api:1.0.0`)는 지우지 않습니다. 오늘 계속 씁니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인 | 해결 |
> |---|---|---|
> | `docker build requires 1 argument` | 마지막 `.`을 빠뜨림 | `docker build -t 이름:태그 .` |
> | `failed to read dockerfile: open Dockerfile: no such file` | 다른 폴더에서 실행했거나 파일 이름이 다름 (`dockerfile`, `Dockerfile.txt`) | `pwd`와 `ls`로 확인, 이름은 정확히 `Dockerfile` |
> | `ERROR: No matching distribution found for flask==…` | 버전 오타 또는 인터넷 연결 문제 | requirements.txt 철자 확인, 네트워크 확인 |
> | `COPY failed: … app.py: not found` | 파일 이름 오타 또는 저장 안 함 | VS Code 탭의 저장 표시(●) 확인 |
> | 컨테이너가 바로 Exited (1) | 코드 붙여 넣기 중 들여쓰기 깨짐 등 | `docker logs api`로 파이썬 에러 확인 |
> | `curl: (7) Failed to connect` | `-p` 빠뜨림 / 포트 순서 | 어제 4교시, 7교시 실패 5 |

> **🎓 학술 노트 — '빌드는 한 번, 배포는 여러 번'**
>
> 제즈 험블과 데이비드 팔리는 『Continuous Delivery』(2010)에서 배포 파이프라인의 핵심 원칙으로 **"바이너리는 한 번만 빌드하라(Only build your binaries once)"**를 꼽았습니다. 환경마다 다시 빌드하면, 그 사이에 컴파일러나 라이브러리 버전이 달라져 **테스트한 것과 다른 것**이 운영에 나갈 위험이 생기기 때문입니다. 대신 한 번 만든 결과물을 저장소에 보관하고, **환경별 설정만 바꿔** 같은 결과물을 차례로 배포합니다.
>
> 컨테이너 이미지는 이 원칙을 지키기에 아주 좋은 형태입니다. 오늘 실습 6이 그 축소판입니다. 6교시에서 이미지를 Docker Hub(결과물 저장소)에 올리면, 1주차 5일차 2교시의 파이프라인 그림이 완성됩니다. 3주차 GitHub Actions에서 이 과정을 자동화합니다.
>
> - Humble, J., & Farley, D. (2010). *Continuous Delivery*, Ch. 5 Anatomy of the Deployment Pipeline. Addison-Wesley.

> **📈 트렌드 — 빌드 결과에 '출생 증명서'를 붙인다**
>
> 빌드 출력 끝에 `exporting attestation manifest`라는 줄이 보일 수 있습니다. 최신 Docker(BuildKit)는 이미지를 만들 때 **어떤 재료로, 어떤 과정으로 만들었는지**를 기록한 증명서(provenance attestation)를 함께 붙일 수 있습니다. 1주차 5일차 2교시 트렌드에서 본 **SBOM**과 **SLSA**가 바로 이것입니다. 누가 만든 이미지인지, 중간에 바뀌지 않았는지를 나중에 검증할 수 있게 해 주어, 공급망 공격을 막는 기본 장치가 되어 가고 있습니다.

## 정리

- `docker build -t 이름:태그 .` — 마지막 `.`은 빌드 컨텍스트입니다.
- 빌드 출력의 `[n/6]`은 Dockerfile의 층 순서이고, `docker image history`로 결과를 확인합니다.
- 내 노트북에 파이썬 없이 파이썬 앱이 **0.0.0.0, PID 1, appuser**로 실행됩니다.
- **이미지는 한 번 빌드하고, 설정은 `-e`로 환경마다** 다르게 넣습니다.

> **✅ 확인 문제**
>
> 1. `docker build`에서 `-t`의 역할은?
> 2. 빌드 중 가장 오래 걸린 단계는 무엇이었나요? 왜일까요?
> 3. `/api/info`의 hostname 값은 무엇인가요?
> 4. 이미지를 다시 빌드하지 않고 `APP_ENV`를 바꾸는 방법은?
> 5. "이미지는 한 번만 빌드한다"는 원칙이 중요한 이유는?
>
> <details><summary>정답</summary>
>
> 1. 만든 이미지에 이름과 태그를 붙인다
> 2. `pip install` — 인터넷에서 라이브러리를 내려받아 설치하기 때문
> 3. 그 컨테이너의 ID
> 4. `docker run -e APP_ENV=값 …`
> 5. 환경마다 다시 빌드하면 테스트한 것과 다른 것이 운영에 나갈 수 있기 때문
>
> </details>

## 참고 문헌

- Docker Docs. *docker buildx build*, *Build context*. docs.docker.com
- Gunicorn Docs. *Settings — bind, accesslog*. docs.gunicorn.org
- Wiggins, A. (2011). *The Twelve-Factor App — III. Config*. 12factor.net/config
- Humble, J., & Farley, D. (2010). *Continuous Delivery*. Addison-Wesley.
- Docker Docs. *Build attestations*. docs.docker.com/build/metadata/attestations

---

⬅️ 이전: [2교시 · DevMart API와 Dockerfile 문법](lesson-02.md) &nbsp;|&nbsp; [⬆️ 3일차 목차](README.md) &nbsp;|&nbsp; 다음: [4교시 · 빌드 컨텍스트와 .dockerignore](lesson-04.md) ➡️
