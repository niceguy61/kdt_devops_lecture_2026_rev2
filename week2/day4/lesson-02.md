# 2교시 · 이름 있는 볼륨

> [!NOTE]
> **이번 시간에 할 일**
>
> - `docker volume create`로 **이름 있는 볼륨** `devmart-db`를 만듭니다.
> - 초기화 SQL로 DevMart 상품 5개를 DB에 넣습니다.
> - 컨테이너를 지우고 다시 띄워도 **데이터가 남는 것**을 확인합니다.
> - PostgreSQL 18 이미지의 **볼륨 경로 함정**을 알고 피합니다.
> - 볼륨을 `tar` 파일로 백업합니다.

## 볼륨 = Docker가 관리하는 바깥 금고

**볼륨(volume)**은 컨테이너 바깥, Docker가 관리하는 저장 공간입니다. 컨테이너의 한 폴더에 볼륨을 **붙이면(mount)**, 그 폴더에 쓰는 모든 것이 컨테이너가 아니라 볼륨에 저장됩니다. 컨테이너를 지워도 볼륨은 남고, 새 컨테이너에 **같은 이름으로** 다시 붙이면 데이터가 그대로 보입니다.

```text
-v  볼륨이름 : 컨테이너 안의 폴더
-v  devmart-db : /var/lib/postgresql
```

`-p 8080:80`이 "바깥:안" 순서였던 것처럼 `-v`도 **바깥(볼륨):안(폴더)** 순서입니다.

## 실습 2 · DevMart DB를 볼륨 위에 세우기

> **🧪 실습: 실습 목표**
>
> 이름 있는 볼륨에 DevMart 데이터베이스를 만들고, 처음 시작할 때 상품 5개가 자동으로 들어가게 합니다.

### 단계 1 — 초기화 SQL 파일 만들기

PostgreSQL 공식 이미지는 **데이터가 비어 있을 때 처음 한 번** `/docker-entrypoint-initdb.d/` 폴더의 `.sql` 파일을 실행해 줍니다. 여기에 표와 상품을 만드는 SQL을 둡니다.

```bash
cd ~/devops-lab/devmart
mkdir -p db/init
code db/init/01-schema.sql
```

VS Code에 아래를 붙여 넣고 저장합니다. (강의 저장소의 `labs/week2/devmart/db/init/01-schema.sql`과 같습니다.)

```sql
-- 컨테이너가 처음 만들어질 때(데이터가 비어 있을 때) 한 번만 실행된다.
CREATE TABLE IF NOT EXISTS products (
    id    SERIAL PRIMARY KEY,
    name  TEXT    NOT NULL,
    price INTEGER NOT NULL
);

INSERT INTO products (name, price) VALUES
    ('러닝화', 59000),
    ('후드 집업', 45000),
    ('에코백', 12000),
    ('텀블러', 18000),
    ('무선 이어폰', 89000);
```

- `SERIAL PRIMARY KEY` : 1, 2, 3… 번호를 자동으로 매기는 고유 번호
- `INSERT INTO … VALUES` : 상품 5개를 넣는다

> **📖 용어 — 시드 데이터(seed data)**
>
> 빈 DB를 처음 쓸 수 있는 상태로 만들기 위해 넣는 기본 데이터. 씨앗을 뿌린다는 뜻입니다. 개발·테스트 환경에서는 매번 같은 시드로 시작하면 누구나 같은 화면을 보게 되어 편합니다.

### 단계 2 — 볼륨 만들기

```bash
docker volume create devmart-db
docker volume ls
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> devmart-db
> DRIVER    VOLUME NAME
> local     devmart-db
> ```

### 단계 3 — 볼륨을 붙여 DB 실행

```bash
docker run -d --name db \
  -e POSTGRES_USER=devmart -e POSTGRES_PASSWORD=devmart-pw -e POSTGRES_DB=devmart \
  -v devmart-db:/var/lib/postgresql \
  -v "$PWD/db/init":/docker-entrypoint-initdb.d:ro \
  postgres:18
```

- `-v devmart-db:/var/lib/postgresql` : **이름 있는 볼륨**을 DB 데이터 폴더에 붙인다
- `-v "$PWD/db/init":/docker-entrypoint-initdb.d:ro` : **내 폴더**를 초기화 폴더에 붙인다. 이것은 3교시에 배울 **바인드 마운트**입니다. `$PWD`는 "지금 있는 폴더의 전체 경로", `:ro`는 읽기 전용(read-only)
- 이번 컨테이너 이름은 `db`입니다. 4교시부터 API가 이 이름으로 DB를 찾습니다.

```bash
docker exec db pg_isready -U devmart
docker exec db psql -U devmart -d devmart -c "SELECT * FROM products;"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> /var/run/postgresql:5432 - accepting connections
>  id |    name     | price
> ----+-------------+-------
>   1 | 러닝화      | 59000
>   2 | 후드 집업   | 45000
>   3 | 에코백      | 12000
>   4 | 텀블러      | 18000
>   5 | 무선 이어폰 | 89000
> (5 rows)
> ```

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인과 해결 |
> |---|---|
> | `relation "products" does not exist` | 초기화 SQL이 실행되지 않았다. `docker logs db`에서 `running /docker-entrypoint-initdb.d/01-schema.sql`이 있는지 본다. 없으면 `-v` 경로 오타. `ls db/init`으로 파일 확인 |
> | 초기화 SQL을 고쳤는데 반영이 안 된다 | **볼륨에 데이터가 이미 있으면 초기화는 다시 실행되지 않는다.** 아래 '처음부터 다시' 참고 |
> | `pg_isready`가 계속 `no response` | `docker logs db`로 오류 확인. 컨테이너가 꺼졌다면 `docker ps -a`에서 `Exited` |

## 실습 3 · 지우고 다시 띄워도 남는다

> **🧪 실습: 실습 목표**
>
> 1교시와 똑같이 컨테이너를 지우고 다시 띄웁니다. 이번에는 같은 볼륨을 붙입니다.

```bash
docker exec db psql -U devmart -d devmart \
  -c "INSERT INTO products (name, price) VALUES ('볼륨 테스트 양말', 7000);"
docker rm -f db
docker ps -a
```

컨테이너는 사라졌습니다. 이제 **같은 볼륨**을 붙여 새 컨테이너를 띄웁니다. 이번에는 초기화 폴더를 붙이지 않습니다.

```bash
docker run -d --name db \
  -e POSTGRES_USER=devmart -e POSTGRES_PASSWORD=devmart-pw -e POSTGRES_DB=devmart \
  -v devmart-db:/var/lib/postgresql \
  postgres:18
docker exec db pg_isready -U devmart
docker exec db psql -U devmart -d devmart -c "SELECT name, price FROM products;"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
>      name        | price
> -----------------+-------
>  러닝화          | 59000
>  후드 집업       | 45000
>  에코백          | 12000
>  텀블러          | 18000
>  무선 이어폰     | 89000
>  볼륨 테스트 양말 |  7000
> (6 rows)
> ```
> **새 컨테이너인데 6개가 모두 있습니다.** 방금 넣은 양말까지요. 컨테이너는 바뀌어도 데이터는 볼륨에 남았습니다. 호텔 방은 바뀌었지만 금고는 그대로인 것입니다.

양말은 지워 둡니다. 내일 화면에는 상품 5개만 나오게 합니다.

```bash
docker exec db psql -U devmart -d devmart -c "DELETE FROM products WHERE name='볼륨 테스트 양말';"
```

> [!TIP]
> **이제 DB 이미지를 바꾸는 것도 쉽다**
>
> 데이터가 볼륨에 있으므로, `postgres:18.1`을 `postgres:18.2`로 올릴 때도 **컨테이너만 새 이미지로 바꿔 띄우면** 됩니다. "이미지를 바꿔 끼우는 배포"가 DB에도 가능해진 것입니다. (단, 18 → 19처럼 **주 버전**이 바뀌면 데이터 형식이 달라 별도의 업그레이드 절차가 필요합니다.)

## PostgreSQL 18의 볼륨 경로 — 인터넷 예제를 조심

인터넷의 수많은 예제와 AI 도구가 아래처럼 씁니다.

```bash
-v devmart-db:/var/lib/postgresql/data     # 17 이하 버전의 경로
```

PostgreSQL **17 이하** 공식 이미지는 데이터를 `/var/lib/postgresql/data`에 두었습니다. 그런데 **18부터는** 주 버전 업그레이드(`pg_upgrade`)를 쉽게 하려고 데이터를 `/var/lib/postgresql/18/docker`처럼 **버전별 폴더**에 두도록 바뀌었고, 이미지의 `VOLUME`도 한 단계 위인 `/var/lib/postgresql`로 옮겨졌습니다.

```bash
docker exec db sh -c 'echo $PGDATA'
```

> **🟢 확인: 보이는 것**
>
> ```text
> /var/lib/postgresql/18/docker
> ```

18 이미지에 옛날 경로(`…/data`)로 볼륨을 붙이면, 이미지가 실수를 알아채고 **경고 메시지를 출력하며 시작을 멈춥니다.** 메시지는 버전에 따라 조금씩 다르지만 "18 이상에서는 데이터 형식과 위치가 바뀌었으니 `/var/lib/postgresql`에 붙이라"는 내용입니다. 오늘 우리가 쓴 `-v devmart-db:/var/lib/postgresql`이 18의 올바른 방법입니다.

> [!WARNING]
> **예제를 복사하기 전에 버전부터 확인**
>
> 이 함정은 "인터넷 예제 = 정답"이 아니라는 좋은 예입니다. 예제가 **언제, 어떤 버전**으로 쓰였는지 확인하고, 막히면 **공식 이미지 문서(Docker Hub의 이미지 설명 페이지)**를 먼저 읽습니다. AI 도구가 알려 준 명령도 마찬가지입니다.

## 볼륨은 어디에 있나 — 그리고 백업

```bash
docker volume inspect devmart-db
```

> **🟢 확인: 보이는 것**
>
> ```json
> [
>     {
>         "CreatedAt": "2026-11-26T10:12:03+09:00",
>         "Driver": "local",
>         "Mountpoint": "/var/lib/docker/volumes/devmart-db/_data",
>         "Name": "devmart-db",
>         "Scope": "local"
>     }
> ]
> ```

`Mountpoint`가 실제 저장 위치입니다. Linux 엔진이라면 이 폴더에 파일이 있지만, **Docker Desktop(Windows·Mac)**에서는 Docker가 돌아가는 숨은 Linux 가상 머신 **안**에 있어서 내 탐색기에서 바로 보이지 않습니다. 볼륨 안을 직접 만지기보다 **컨테이너를 통해 다루는 것**이 원칙입니다. Docker Desktop 화면의 **Volumes** 메뉴에서 목록과 크기를 볼 수 있습니다.

### 실습 4 · 볼륨 백업 파일 만들기

볼륨 안의 파일을 꺼내려면 **임시 컨테이너**를 하나 띄워서, 한쪽에는 볼륨을, 한쪽에는 내 폴더를 붙이고 `tar`로 묶습니다.

```bash
mkdir -p ~/devops-lab/backup
docker run --rm \
  -v devmart-db:/data:ro \
  -v ~/devops-lab/backup:/backup \
  alpine:3.24 \
  tar czf /backup/devmart-db.tgz -C /data .
ls -lh ~/devops-lab/backup
```

- `--rm` : 일이 끝나면 임시 컨테이너를 자동으로 지운다
- `-v devmart-db:/data:ro` : 볼륨을 **읽기 전용**으로 붙인다 (백업하다가 실수로 망가뜨리지 않게)
- `tar czf 파일 -C 폴더 .` : 폴더 안의 모든 것을 압축 파일 하나로 묶는다

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> -rw-r--r-- 1 root root 11M … devmart-db.tgz
> ```

> [!WARNING]
> **실행 중인 DB의 파일을 복사하는 백업은 연습용**
>
> DB가 켜진 채로 파일을 복사하면, 복사하는 순간에도 DB가 쓰고 있어서 **어긋난 백업**이 될 수 있습니다. 실제 업무에서는 PostgreSQL의 `pg_dump`(DB가 일관된 사본을 만들어 줌)나 관리형 DB의 **자동 백업·스냅샷**을 씁니다. 오늘 실습은 "볼륨도 결국 파일이고, 컨테이너로 꺼낼 수 있다"를 보는 것이 목적입니다. `backup/` 폴더는 Git에 올리지 않도록 `~/devops-lab/.gitignore`에 `backup/`을 한 줄 추가합니다.

## 처음부터 다시 시작하고 싶을 때

초기화 SQL을 고쳤거나 데이터를 완전히 처음 상태로 돌리고 싶으면 **볼륨을 지우고** 다시 만듭니다.

```bash
docker rm -f db
docker volume rm devmart-db          # 데이터가 영원히 사라진다!
docker volume create devmart-db
# 실습 2의 단계 3 명령을 다시 실행
```

> [!WARNING]
> **`docker volume rm`은 되돌릴 수 없다**
>
> 볼륨 삭제는 휴지통이 없습니다. 실습에서는 괜찮지만, 업무에서는 **지우기 전에 백업이 있는지** 먼저 확인하는 습관을 들입니다. "되돌릴 수 없는 작업 앞에서는 한 번 멈춘다"는 클라우드 작업 전체에 통하는 원칙입니다.

> **🎓 학술 노트 — 로그를 먼저 쓴다 (Write-Ahead Logging)**
>
> DB가 "저장 완료"라고 답한 뒤 전원이 나가도 데이터가 남는 비결은 **선행 기록(WAL, Write-Ahead Logging)**입니다. IBM의 모한(C. Mohan) 등이 1992년 ACM TODS 논문에서 정리한 **ARIES** 알고리즘이 대표적입니다. 아이디어는 단순합니다. 실제 표를 고치기 **전에**, "무엇을 어떻게 바꿀지"를 **로그 파일 끝에 먼저 덧붙여 디스크에 기록**합니다. 중간에 죽으면 다시 켜질 때 로그를 읽어 끝내지 못한 일을 마저 하거나 되돌립니다.
>
> PostgreSQL도 같은 방식이고, 볼륨 안을 보면 `pg_wal`이라는 폴더가 있습니다. 실습 4의 경고가 이 때문입니다. 실행 중인 DB의 파일을 단순 복사하면 **표 파일과 WAL 파일의 시점이 어긋날** 수 있습니다. 그래서 DB 백업은 DB가 직접 만들어 주는 방법(`pg_dump`, 스냅샷)을 써야 합니다. 이 원리는 5주차 RDS의 "특정 시점 복구(PITR)"로 이어집니다.
>
> - Mohan, C., Haderle, D., Lindsay, B., Pirahesh, H., & Schwarz, P. (1992). ARIES: A transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging. *ACM TODS, 17*(1), 94–162.

> **📈 트렌드 — 볼륨은 '플러그인'이 되었다**
>
> 오늘 쓴 볼륨의 `Driver`는 `local`(내 컴퓨터 디스크)이었습니다. 볼륨 드라이버를 바꾸면 같은 `-v` 문법으로 **네트워크 저장소나 클라우드 디스크**를 붙일 수도 있습니다. Kubernetes에서는 이것이 **CSI(Container Storage Interface)**라는 표준으로 정리되어, AWS EBS·EFS 같은 클라우드 저장소가 모두 같은 방식으로 붙습니다. 3주차에 PersistentVolume, 5주차에 EBS CSI 드라이버로 다시 만납니다. 이름과 규모는 커지지만 **"컨테이너 바깥에 데이터를 두고, 이름으로 붙인다"**는 오늘의 생각은 그대로입니다.

## 정리

- **이름 있는 볼륨** = Docker가 관리하는 바깥 금고. `docker volume create`, `-v 이름:경로`.
- 컨테이너를 지워도 볼륨은 남고, 같은 이름으로 다시 붙이면 데이터가 보인다.
- 공식 PostgreSQL 이미지는 `/docker-entrypoint-initdb.d/`의 SQL을 **빈 DB일 때 한 번만** 실행한다.
- PostgreSQL **18은 `/var/lib/postgresql`**에 붙인다. 옛 예제의 `…/data`는 17 이하용.
- 볼륨 백업은 임시 컨테이너 + `tar`로 할 수 있지만, 실제 DB 백업은 `pg_dump`나 스냅샷.

> **✅ 확인 문제**
>
> 1. `-v devmart-db:/var/lib/postgresql`에서 왼쪽과 오른쪽은 각각 무엇인가요?
> 2. 초기화 SQL을 고치고 컨테이너를 다시 띄웠는데 반영되지 않았습니다. 왜일까요?
> 3. PostgreSQL 18 이미지에서 볼륨을 붙일 경로는?
> 4. 실행 중인 DB 볼륨을 `tar`로 복사하는 백업이 위험한 이유는?
>
> <details><summary>정답</summary>
>
> 1. 왼쪽 = 볼륨 이름(바깥), 오른쪽 = 컨테이너 안의 폴더
> 2. 볼륨에 데이터가 이미 있어서 초기화가 다시 실행되지 않는다. 볼륨을 지우고 새로 시작해야 한다
> 3. `/var/lib/postgresql` (실제 데이터는 그 아래 `18/docker`)
> 4. 복사하는 동안 DB가 계속 써서 표 파일과 WAL의 시점이 어긋난 백업이 될 수 있다
>
> </details>

## 참고 문헌

- Docker Docs. *Volumes — Back up, restore, or migrate data volumes*. docs.docker.com/engine/storage/volumes
- Docker Hub. *postgres — Initialization scripts, PGDATA*. hub.docker.com/_/postgres
- docker-library/postgres. *Official PostgreSQL image repository — 18+ PGDATA change*. github.com/docker-library/postgres
- Mohan, C. et al. (1992). ARIES. *ACM TODS, 17*(1).
- Kubernetes Docs. *Container Storage Interface (CSI)*. kubernetes.io/docs/concepts/storage/volumes
