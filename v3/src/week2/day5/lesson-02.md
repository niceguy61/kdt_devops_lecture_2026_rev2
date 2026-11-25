# 2교시 · up · ps · logs · down과 헬스 체크

!!! goal "이번 시간에 할 일"
    - `docker compose up -d` 한 줄로 DevMart 세 서비스를 띄웁니다.
    - 출력에서 **시작 순서와 헬스 체크**를 읽습니다.
    - `ps` · `logs` · `exec`로 상태를 봅니다.
    - Compose가 만든 이름(컨테이너 · 네트워크 · 볼륨)의 규칙을 압니다.
    - `down`과 `down -v`의 차이를 확인합니다.

## 실습 2 · 한 줄로 띄우기

!!! lab "실습 목표"
    어제 6개 명령으로 하던 일을 `docker compose up` 한 줄로 합니다.

```bash
cd ~/devops-lab/devmart
docker compose up -d --build
```

- `up` : `compose.yaml`에 적힌 상태로 **맞춘다** (없으면 만들고, 있으면 그대로)
- `-d` : 백그라운드로 실행 (2일차의 `docker run -d`와 같은 뜻)
- `--build` : `build:`가 있는 서비스의 이미지를 **다시 빌드**한다 (어제 이후 코드가 바뀌었을 수 있으니)

!!! check "이렇게 나오면 성공 (순서에 주목)"
    ```text
     ✔ Network devmart_default          Created
     ✔ Volume devmart_db-data           Created
     ✔ Container devmart-db-1           Started
     ⠿ Container devmart-db-1           Waiting
     ✔ Container devmart-db-1           Healthy
     ✔ Container devmart-catalog-api-1  Started
     ✔ Container devmart-web-1          Started
    ```
    1. **네트워크와 볼륨**을 먼저 만들었습니다 (어제 명령 1·2).
    2. **db**를 시작하고 **`Waiting` → `Healthy`**가 될 때까지 기다렸습니다 (어제 `until pg_isready`).
    3. 그다음 **catalog-api**, 마지막으로 **web** (어제 배운 의존 순서).

    순서를 적은 적이 없는데, `depends_on`을 보고 Compose가 스스로 순서를 정했습니다.

브라우저에서 **http://localhost:8080** 을 엽니다.

!!! check "이렇게 보이면 성공"
    - 머리말: `catalog-api v1.0.1 · compose · 컨테이너 c2022e9bc2d7`
    - 배지: **데이터베이스에서 불러옴**, 카드 5개
    - 환경이 `docker`가 아니라 **`compose`**인 것은 `compose.yaml`의 `APP_ENV: compose` 때문입니다.
    - 에코백이 **12,000원**입니다. 어제 9,900원으로 바꾼 것은 어제의 볼륨 `devmart-db`에 있고, 오늘은 Compose가 **새 볼륨** `devmart_db-data`를 만들어 초기화 SQL부터 다시 시작했기 때문입니다.

## Compose가 붙이는 이름

```bash
docker compose ps
docker network ls | grep devmart
docker volume ls | grep devmart
```

!!! check "보이는 것"
    ```text
    NAME                    IMAGE                     SERVICE       STATUS                   PORTS
    devmart-catalog-api-1   devmart/catalog-api:dev   catalog-api   Up 2 minutes             8000/tcp
    devmart-db-1            postgres:18               db            Up 2 minutes (healthy)   5432/tcp
    devmart-web-1           nginx:1.30-alpine         web           Up 2 minutes             0.0.0.0:8080->80/tcp
    45c592f14287   devmart_default   bridge    local
    local     devmart-db
    local     devmart_db-data
    ```

| 대상 | 규칙 | 예 |
|---|---|---|
| 컨테이너 | `프로젝트-서비스-번호` | `devmart-db-1` |
| 네트워크 | `프로젝트_default` | `devmart_default` |
| 볼륨 | `프로젝트_볼륨` | `devmart_db-data` |
| 이미지 (`build:`) | `image:`에 적은 이름 | `devmart/catalog-api:dev` |

**프로젝트 이름**은 `compose.yaml` 첫 줄의 `name: devmart`입니다(없으면 폴더 이름). 이름 앞에 프로젝트가 붙기 때문에, 다른 폴더의 다른 Compose 프로젝트와 **이름이 겹치지 않습니다.** `devmart-db`(어제, 손으로 만든 것)와 `devmart_db-data`(오늘, Compose가 만든 것)가 나란히 있는 것도 이 때문입니다.

`STATUS`의 **`(healthy)`**도 보세요. 헬스 체크를 정의한 서비스는 상태 옆에 결과가 붙습니다. 시작 직후에는 `(health: starting)`, 실패가 이어지면 `(unhealthy)`가 됩니다.

## 로그와 안쪽

```bash
docker compose logs --tail 5
docker compose logs -f catalog-api
```

- 서비스 이름 없이 쓰면 **모든 서비스의 로그**가 한 화면에, 줄 앞에 서비스 이름이 붙어서 나옵니다
- `-f` : 계속 따라가며 보기. 브라우저를 새로 고침하면 API 로그가 올라옵니다. `Ctrl + C`로 빠져나옵니다

!!! check "보이는 것"
    ```text
    catalog-api-1  | … "GET /api/info HTTP/1.0" 200 110 "-" "Mozilla/5.0 …"
    catalog-api-1  | … "GET /api/products HTTP/1.0" 200 253 "-" "Mozilla/5.0 …"
    ```
    요청이 `HTTP/1.0`인 것은 브라우저가 아니라 **nginx가 대신 요청**했기 때문입니다(어제 배운 리버스 프록시).

```bash
docker compose exec db psql -U devmart -d devmart -c "SELECT count(*) FROM products;"
```

`docker compose exec 서비스이름 …` — 컨테이너 이름(`devmart-db-1`)을 몰라도 **서비스 이름**으로 들어갑니다.

## 실습 3 · 헬스 체크가 하는 일

!!! lab "실습 목표"
    DB를 멈추고 다시 켜며 헬스 체크 상태를 관찰합니다.

```bash
docker compose stop db
docker compose ps
curl -s http://localhost:8080/api/products; echo
docker compose start db
docker compose ps
```

!!! check "보이는 것"
    ```text
    NAME                    ...   STATUS
    devmart-catalog-api-1   ...   Up 5 minutes
    devmart-web-1           ...   Up 5 minutes
    {"detail":"OperationalError","error":"database unavailable"}
    ...
    devmart-db-1            ...   Up 2 seconds (health: starting)
    ```
    `stop db`를 하면 db만 목록에서 빠지고(멈춘 것은 `ps -a`에서 보임) API는 어제 5교시처럼 503을 돌려줍니다. `start db` 직후에는 **`(health: starting)`**, 몇 초 뒤 **`(healthy)`**가 됩니다. API는 스스로 회복합니다.

!!! myth "오해 — '`depends_on`이 있으니 db가 죽으면 API도 멈춘다'"
    `depends_on`은 **시작할 때의 순서**만 정합니다. 실행 중에 db가 멈춰도 API는 계속 돌아갑니다. 그래서 어제 배운 것처럼 **API가 스스로 503을 돌려주고 회복하는 능력**이 여전히 필요합니다. "누가 누구를 지켜보다가 다시 살린다"는 일은 3주차 Kubernetes가 본격적으로 해 줍니다.

## 실습 4 · down과 down -v

```bash
docker compose down
docker compose ps -a
docker volume ls | grep devmart
```

!!! check "보이는 것"
    ```text
     ✔ Container devmart-web-1          Removed
     ✔ Container devmart-catalog-api-1  Removed
     ✔ Container devmart-db-1           Removed
     ✔ Network devmart_default          Removed
    NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS
    local     devmart-db
    local     devmart_db-data
    ```
    **컨테이너와 네트워크는 지웠지만 볼륨은 남겼습니다.** 지우는 순서도 web → api → db, 띄울 때의 **거꾸로**입니다.

다시 `up` 하면 같은 볼륨이 붙어 데이터가 그대로입니다. 이번에는 `--build` 없이 해 봅니다. 이미지가 이미 있으므로 빌드하지 않습니다.

```bash
docker compose up -d
docker compose exec db psql -U devmart -d devmart -c "SELECT count(*) FROM products;"
```

| 명령 | 컨테이너 | 네트워크 | 볼륨(데이터) | 언제 |
|---|---|---|---|---|
| `docker compose stop` | 멈춤 (남음) | 남음 | 남음 | 잠깐 쉴 때 |
| `docker compose down` | 지움 | 지움 | **남음** | 하루 일을 마칠 때 (기본) |
| `docker compose down -v` | 지움 | 지움 | **지움** | 데이터까지 처음부터 다시 |

!!! warn "`down -v`는 어제의 `docker volume rm`"
    `-v` 한 글자로 DB 데이터가 사라집니다. 개발 중에 "초기화 SQL을 고쳤으니 처음부터"처럼 **의도할 때만** 씁니다. 습관적으로 `down -v`를 치는 사람이 많은데, 운영 비슷한 환경에서 한 번 하면 큰 사고가 됩니다.

!!! academic "학술 노트 — 실패는 빠르게, 의존은 조심스럽게 (Nygard, 2007)"
    마이클 나이가드(Michael T. Nygard)의 책 『Release It!』(2007, 2판 2018)은 실제 운영 장애 사례를 모아 **안정성 패턴**을 정리한 고전입니다. 그는 장애가 퍼지는 가장 흔한 길로 **"통합 지점(integration point)"**, 즉 다른 시스템을 부르는 곳을 꼽았습니다. 오늘의 API → DB가 바로 그곳입니다.

    책이 권하는 처방 중 오늘과 이어지는 것이 두 가지입니다. 첫째, **빠른 실패(Fail Fast)** — 일을 못 할 것이 분명하면 오래 붙잡고 있지 말고 바로 알린다. 우리 API가 DB가 없을 때 바로 503을 돌려주는 것, Compose가 `.env`에 비밀번호가 없으면 아예 시작하지 않는 것(`:?`)이 그 예입니다. 둘째, **타임아웃** — 상대가 답하지 않을 때 영원히 기다리지 않는다. 헬스 체크의 `timeout: 3s`가 작은 예입니다. 4주차 MSA와 Istio에서 서킷 브레이커와 재시도로 이 패턴들을 본격적으로 다룹니다.

    - Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.

!!! trend "트렌드 — 노트북에서 쓰는 Compose, 클라우드로 가는 다리"
    Compose는 "개발자 노트북에서 여러 컨테이너를 한 번에" 띄우는 도구로 사실상 표준이 되었습니다. 많은 오픈소스 프로젝트가 저장소에 `compose.yaml`을 넣어 두고 "`docker compose up` 한 줄로 체험하세요"라고 안내합니다. 동시에 Compose 파일을 Kubernetes 설정으로 바꿔 주는 도구들(Docker의 Compose Bridge, 오픈소스 Kompose 등)도 나와 있습니다. 다만 자동 변환 결과를 그대로 운영에 쓰기보다는, 3주차처럼 **Kubernetes의 방식으로 다시 이해하고 쓰는 것**이 보통입니다. 오늘 익힌 서비스 · 볼륨 · 환경 변수 · 헬스 체크가 거의 그대로 Kubernetes의 Deployment · PersistentVolume · ConfigMap/Secret · Probe에 대응합니다.

## 정리

- `docker compose up -d --build` — 네트워크 · 볼륨 → db(healthy까지 대기) → api → web.
- 이름 규칙: 컨테이너 `프로젝트-서비스-번호`, 네트워크 `프로젝트_default`, 볼륨 `프로젝트_볼륨`.
- `ps`(상태 + 헬스), `logs [-f] [서비스]`, `exec 서비스 …`는 **서비스 이름**으로.
- `depends_on`은 **시작 순서**만. 실행 중 장애는 앱의 회복력이 필요하다.
- `down`은 데이터를 남기고, `down -v`는 데이터까지 지운다.

!!! quiz "확인 문제"
    1. `up` 출력에서 `Waiting` → `Healthy`는 무엇을 기다린 것인가요?
    2. 오늘 화면의 에코백이 어제처럼 9,900원이 아니라 12,000원인 이유는?
    3. Compose가 만든 볼륨의 이름은? 그 이름은 어떻게 정해지나요?
    4. `docker compose down`과 `down -v`의 차이는?
    5. 실행 중에 db가 멈추면 `depends_on` 때문에 API도 멈추나요?

    ??? answer "정답"
        1. db 서비스의 헬스 체크(`pg_isready`)가 통과하기를 기다렸다 (`depends_on … service_healthy`)
        2. Compose가 새 볼륨 `devmart_db-data`를 만들어 초기화 SQL로 새로 시작했기 때문 (어제 값은 `devmart-db` 볼륨에 있다)
        3. `devmart_db-data` — 프로젝트 이름 + `_` + compose.yaml의 볼륨 이름
        4. `down`은 컨테이너·네트워크만 지우고 볼륨은 남긴다. `down -v`는 볼륨(데이터)까지 지운다
        5. 아니다. `depends_on`은 시작 순서만 정한다

## 참고 문헌

- Docker Docs. *docker compose up / ps / logs / exec / down*. docs.docker.com/reference/cli/docker/compose
- Docker Docs. *Control startup order in Compose*. docs.docker.com/compose/how-tos/startup-order
- Nygard, M. T. (2018). *Release It!* (2nd ed.). Pragmatic Bookshelf.
- Kompose. kompose.io
