<sub>[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [5일차](README.md) › 7/8교시</sub>

# 7교시 · Compose 심화 — 덧씌우기 파일과 환경별 설정

> [!NOTE]
> **이번 시간에 할 일**
>
> - `compose.yaml`은 그대로 두고, **덧씌우기(override) 파일**로 개발용 설정만 더합니다.
> - `docker compose config`로 **실제로 적용될 최종 모습**을 확인합니다.
> - 필요할 때만 켜는 도구를 **프로필(profile)**로 분리합니다.
> - 같은 `compose.yaml`에 **운영용 파일**을 겹쳐 자원 제한 · 재시작 정책을 더합니다.
> - 변수 기본값으로 **한 노트북에 DevMart를 두 벌** 띄웁니다.

> [!IMPORTANT]
> **왜 파일을 나누나**
>
> 개발할 때는 DB 포트를 열어 도구로 들여다보고 싶고, 운영에서는 절대 열면 안 됩니다. 이 차이를 `compose.yaml` 하나에 `if`처럼 섞으면 금방 엉킵니다. 대신 **모두가 같이 쓰는 바탕 파일 하나 + 환경마다 다른 점만 적은 얇은 파일**로 나눕니다. 3주차 5일차의 Kustomize 오버레이, 5주차 4일차의 `eks/` 오버레이가 같은 생각입니다.

## 실습 14 · 덧씌우기 파일 — `compose.override.yaml`

> **🧪 실습: 실습 목표**
>
> 개발할 때만 필요한 설정(DB 포트 열기, 앱 환경 이름 바꾸기)을 별도 파일에 적고, Compose가 이것을 **자동으로 합치는** 것을 확인합니다.

### 단계 1 — 지금 상태 확인

```bash
cd ~/devops-lab/devmart
git switch main && git pull
docker compose up -d
docker compose ps --format 'table {{.Service}}\t{{.Ports}}'
```

> **🟢 확인: 보이는 것**
>
> ```text
> SERVICE       PORTS
> catalog-api   8000/tcp
> db            5432/tcp
> web           0.0.0.0:8080->80/tcp
> ```
> 밖으로 열린 문은 `web`의 8080 하나입니다(4일차 7교시의 최소 노출).

### 단계 2 — 덧씌우기 파일 만들기

```bash
code compose.override.yaml
```

```yaml
# 개발용 덧씌우기 — compose.yaml과 같은 폴더에 두면 자동으로 합쳐진다
services:
  db:
    ports:
      - "127.0.0.1:5432:5432"     # 내 노트북에서만 DB에 접속 (DB 도구용)
  catalog-api:
    environment:
      APP_ENV: dev                 # 바탕 파일의 compose를 dev로 바꿔 씀
```

- `127.0.0.1:5432:5432` : 3교시 `0.0.0.0`과 반대. **내 컴퓨터 자신만** 접속할 수 있게 연다 — 같은 와이파이의 다른 사람은 못 들어온다
- 바탕 파일에 있는 항목(`environment`)은 **덮어쓰고**, 없는 항목(`ports`)은 **더합니다**

### 단계 3 — 합쳐진 결과 보기

```bash
docker compose config | sed -n '/^  catalog-api:/,/^  db:/p' | grep -A1 APP_ENV
docker compose config | grep -A4 "^  db:" | head -5
docker compose config --services
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
>       APP_ENV: dev
> ```
> `docker compose config`는 파일들을 합치고 변수(`${DB_PASSWORD}`)까지 채운 **최종 모습**을 보여 줍니다. 설정이 이상할 때 가장 먼저 치는 명령입니다. (`DB_PASSWORD` 값도 그대로 찍히므로 **화면 공유 중에는 조심**합니다.)

### 단계 4 — 적용하고 확인

```bash
docker compose up -d
docker compose ps --format 'table {{.Service}}\t{{.Ports}}'
curl -s http://localhost:8080/api/info; echo
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> SERVICE       PORTS
> catalog-api   8000/tcp
> db            127.0.0.1:5432->5432/tcp
> web           0.0.0.0:8080->80/tcp
> {"database":"configured","env":"dev","hostname":"…", …}
> ```
> `up`은 **바뀐 서비스만** 다시 만듭니다(2교시의 "맞춘다"). `web`은 그대로입니다.

> [!TIP]
> **덧씌우기 파일은 커밋할까?**
>
> `compose.override.yaml`은 **사람마다 다를 수 있는** 개발 설정이라, 팀에 따라 `.gitignore`에 넣고 예시 파일(`compose.override.example.yaml`)만 커밋하기도 합니다. 오늘은 팀 공통 개발 설정으로 보고 커밋합니다. **비밀값은 어느 쪽이든 넣지 않습니다** — 비밀값은 계속 `.env`에.

## 실습 15 · 필요할 때만 켜는 도구 — 프로필

DB 내용을 브라우저로 보는 도구 **Adminer**를 붙이되, 평소에는 켜지지 않게 합니다.

`compose.override.yaml`의 `services:` 아래에 추가합니다.

```yaml
  adminer:
    image: adminer:5
    profiles: ["tools"]            # --profile tools를 줄 때만 켜진다
    ports:
      - "127.0.0.1:8088:8080"
    depends_on:
      - db
```

```bash
docker compose up -d
docker compose ps --services
docker compose --profile tools up -d
docker compose ps --services
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> catalog-api
> db
> web
> adminer
> catalog-api
> db
> web
> ```
> 처음 `up`에는 `adminer`가 없고, `--profile tools`를 준 뒤에 생겼습니다. 브라우저에서 `http://localhost:8088` → 시스템 **PostgreSQL**, 서버 `db`, 사용자 `devmart`, 비밀번호는 `.env`의 값, DB `devmart`로 로그인하면 `products` 표가 보입니다.

```bash
docker compose --profile tools stop adminer
docker compose --profile tools rm -f adminer
```

## 실습 16 · 운영용 파일을 겹치기

> **🧪 실습: 실습 목표**
>
> `compose.prod.yaml`에 2일차 8교시의 자원 제한과 재시작 정책을 적고, `-f`로 **명시적으로** 겹칩니다.

```bash
code compose.prod.yaml
```

```yaml
# 운영용 덧씌우기 — 자동으로 합쳐지지 않는다. -f로 직접 지정할 때만
services:
  web:
    restart: unless-stopped
    read_only: true
    tmpfs: ["/var/cache/nginx", "/run"]
    mem_limit: 128m
    cpus: 0.5
  catalog-api:
    restart: unless-stopped
    mem_limit: 256m
    cpus: 1.0
  db:
    restart: unless-stopped
    mem_limit: 512m
```

```bash
docker compose -f compose.yaml -f compose.prod.yaml config | grep -E "mem_limit|restart|read_only"
docker compose -f compose.yaml -f compose.prod.yaml up -d
docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> NAME                    MEM USAGE / LIMIT
> devmart-web-1           3.4MiB / 128MiB
> devmart-catalog-api-1   62.1MiB / 256MiB
> devmart-db-1            38.5MiB / 512MiB
> ```
> `-f`를 직접 주면 **자동 덧씌우기(`compose.override.yaml`)는 읽지 않습니다.** 그래서 DB 포트도 다시 닫혔습니다(`docker compose ps`로 확인). 이 규칙 덕분에 개발 설정이 운영에 섞여 들어가지 않습니다.

| 명령 | 읽는 파일 |
|---|---|
| `docker compose up` | `compose.yaml` + `compose.override.yaml`(있으면) |
| `docker compose -f compose.yaml -f compose.prod.yaml up` | 적은 두 파일만, **뒤의 것이 앞의 것을 덮음** |

## 실습 17 · 한 노트북에 두 벌 — 변수 기본값

`compose.yaml`의 `web` 포트를 변수로 바꿉니다.

```yaml
    ports:
      - "${WEB_PORT:-8080}:80"
```

1일차 8교시의 `${변수:-기본값}`과 같은 문법입니다. 이제 프로젝트 이름(`-p`)과 포트를 바꿔 **두 번째 DevMart**를 띄웁니다.

```bash
docker compose -f compose.yaml -p devmart-review up -d
WEB_PORT=8081 docker compose -f compose.yaml -p devmart-review up -d
docker compose ls
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8081/
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> NAME             STATUS       CONFIG FILES
> devmart          running(3)   …/compose.yaml,…/compose.prod.yaml
> devmart-review   running(3)   …/compose.yaml
> 200
> ```
> 첫 줄은 `8080`이 이미 쓰이고 있어 **실패**합니다(`port is already allocated`). 두 번째 줄에서 포트를 바꾸자 같은 파일로 두 벌이 떴습니다. 프로젝트 이름이 다르면 컨테이너 · 네트워크 · **볼륨까지 따로** 만들어집니다(`devmart-review_db-data`). 동료의 PR을 내 작업과 섞지 않고 띄워 볼 때 씁니다.

> **🧹 정리: 정리와 커밋**
>
> ```bash
> docker compose -p devmart-review down -v          # 리뷰용은 볼륨까지 지움
> docker compose -f compose.yaml -f compose.prod.yaml down
> docker compose up -d                              # 평소 개발 상태로
> git switch -c feat/compose-env
> git add compose.yaml compose.override.yaml compose.prod.yaml
> git commit -m "Compose: 개발 덧씌우기, 도구 프로필, 운영 파일, 포트 변수"
> git push -u origin feat/compose-env
> gh pr create --fill
> ```
> 5교시처럼 PR로 올리고, 짝에게 리뷰를 받은 뒤 병합합니다.

> **🎓 학술 노트 — 한 번 만들고, 모든 환경에 같은 방식으로 (Humble & Farley, 2010)**
>
> 『Continuous Delivery』(Humble & Farley, 2010)는 배포 사고의 큰 원인으로 **환경마다 다른 방식으로 만들고 배포하는 것**을 꼽습니다. 책의 원칙은 두 가지입니다. ① **이미지(바이너리)는 한 번만 만들고** 모든 환경에 같은 것을 쓴다. ② 환경마다 다른 것은 **설정뿐**이며, 그 설정도 **버전 관리**한다. 오늘 `compose.yaml`(같은 이미지 · 같은 구조)에 얇은 파일만 바꿔 끼운 것이 이 원칙의 작은 모형입니다. 3주차 CI는 이미지를 한 번 만들어 GHCR에 올리고, 4주차 GitOps는 환경별 설정을 Git으로 관리하며, 5주차에는 **같은 커밋을 두 클러스터에** 배포합니다.
>
> - Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.

> **📈 트렌드 — Compose가 개발 루프 전체로**
>
> Compose는 "여러 컨테이너 띄우기"를 넘어 개발 흐름 전체를 맡는 쪽으로 넓어지고 있습니다. `develop.watch`를 적어 두고 `docker compose watch`를 실행하면 코드를 저장할 때마다 **컨테이너 안으로 자동 동기화하거나 다시 빌드**합니다. `include:`로 다른 팀의 Compose 파일을 통째로 가져와 붙일 수 있어, 큰 시스템을 서비스별 파일로 나눠 관리합니다. 운영에서는 이 역할을 Kubernetes가 넘겨받지만, **"바탕 + 환경별 차이"**라는 설계는 그대로 가져갑니다.

## 정리

- `compose.override.yaml`은 **자동으로** 합쳐지는 개발용 덧씌우기입니다. 없는 항목은 더하고, 있는 항목은 덮습니다.
- `docker compose config`로 **최종 모습**을 먼저 확인합니다.
- `profiles:`로 필요할 때만 켜는 서비스를 분리합니다(`--profile tools`).
- 운영 파일은 `-f compose.yaml -f compose.prod.yaml`로 **명시적으로** 겹칩니다. 이때 자동 덧씌우기는 읽지 않습니다.
- `${WEB_PORT:-8080}` + `-p 다른이름`으로 같은 파일을 한 노트북에 여러 벌 띄웁니다.

> **✅ 확인 문제**
>
> 1. 개발 중에만 DB 포트를 열고 싶습니다. `compose.yaml`을 고치지 않고 어떻게 하나요?
> 2. 설정이 생각대로 적용되지 않습니다. 가장 먼저 칠 명령은?
> 3. `docker compose -f compose.yaml -f compose.prod.yaml up`에 `compose.override.yaml`의 내용이 들어가나요?
> 4. `profiles: ["tools"]`가 붙은 서비스는 언제 켜지나요?
> 5. 같은 `compose.yaml`로 두 벌을 띄울 때 바꿔야 하는 두 가지는?
>
> <details><summary>정답</summary>
>
> 1. `compose.override.yaml`에 `db`의 `ports`를 적습니다(`127.0.0.1:5432:5432`).
> 2. `docker compose config`
> 3. 아닙니다. `-f`를 직접 주면 적은 파일만 읽습니다.
> 4. `--profile tools`를 줬을 때만
> 5. 프로젝트 이름(`-p`)과 겹치는 바깥 포트
>
> </details>

## 참고 문헌

- Humble, J., & Farley, D. (2010). *Continuous Delivery*. Addison-Wesley.
- Docker Docs. *Merge Compose files*; *Use profiles with Compose*; *Interpolation*; *Specify a project name*; *Use Compose Watch*; *include*.
- Compose Specification. *The Compose file — services.profiles, mem_limit, cpus, read_only, tmpfs, restart*. compose-spec.io
- Adminer. *Docker Official Image: adminer*. hub.docker.com/_/adminer

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · 충돌 해결](lesson-06.md) | [⬆️ 5일차 목차](README.md) | [8교시 · 2주차 회고와 정리](lesson-08.md) ➡️ |
