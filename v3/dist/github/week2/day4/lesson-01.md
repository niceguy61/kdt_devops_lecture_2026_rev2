# 1교시 · 컨테이너의 데이터는 어디에

> [!NOTE]
> **이번 시간에 할 일**
>
> - 어제 배운 이미지·Dockerfile을 5분 안에 손으로 복습합니다.
> - PostgreSQL 컨테이너를 처음 실행하고, `psql`로 표를 하나 만듭니다.
> - 볼륨 없이 컨테이너를 지우면 **데이터가 사라지는 것**을 직접 봅니다.
> - 사라진 줄 알았던 데이터가 사실은 **이름 없는 볼륨**에 버려져 있다는 것을 찾아냅니다.

## 어제 요약 — 5분 손 복습

어제는 내 앱을 이미지로 포장했습니다. 오늘 실습의 출발점인 이미지가 있는지 확인하고, 한 번 실행해 봅니다.

```bash
docker images devmart/catalog-api
docker run -d --name api -p 8000:8000 devmart/catalog-api:1.0.1
curl http://localhost:8000/api/products
docker rm -f api
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> REPOSITORY            TAG     IMAGE ID       ...
> devmart/catalog-api   1.0.1   …
> devmart/catalog-api   1.0.0   …
> {"items":[{"id":1,"name":"러닝화","price":59000},…,{"id":3,"name":"에코백","price":9900}],"source":"sample"}
> ```
> 마지막의 `"source":"sample"`에 주목하세요. 지금 API는 **코드 안에 적어 둔 샘플 3개**를 돌려줍니다. 오늘 이것을 `"source":"database"`로 바꾸는 것이 목표입니다.

| 어제 배운 것 | 한 줄 요약 |
|---|---|
| 레이어 | 이미지 = 읽기 전용 층들, 컨테이너 = 그 위의 **얇은 쓰기 가능한 층** |
| Dockerfile | `FROM` → 의존성 → 설치 → 코드 → `CMD` (자주 바뀌는 것을 뒤로) |
| `.dockerignore` | 비밀값과 쓰레기를 이미지에 넣지 않는다 |
| 태그·다이제스트 | 이름표와 지문. 운영에 `latest`는 쓰지 않는다 |

## 왜 데이터베이스가 문제인가

어제 1교시 그림을 다시 떠올려 보세요. 컨테이너가 파일을 쓰면, 그 내용은 이미지가 아니라 컨테이너마다 붙은 **얇은 쓰기 가능한 층**에 저장됩니다. 그리고 `docker rm`을 하면 그 층도 함께 사라집니다.

웹 서버나 상품 API처럼 **기억할 것이 없는** 프로그램은 이게 오히려 장점입니다. 고장 나면 지우고 새로 띄우면 그만이니까요(1주차 4일차 "애완동물이 아니라 가축"). 하지만 **데이터베이스**는 다릅니다. 주문, 회원, 상품 정보가 컨테이너와 함께 사라지면 회사가 문을 닫아야 합니다.

![컨테이너의 쓰기 가능한 층은 컨테이너와 함께 사라진다 — 데이터는 컨테이너 바깥의 볼륨에 둬야 한다](../../assets/week2/day4/w2d4-ephemeral.png)

> **🧩 비유 — 호텔 방과 개인 금고**
>
> 컨테이너는 **호텔 방**입니다. 체크아웃(`docker rm`)하면 청소부가 방을 깨끗이 비웁니다. 방에 두고 간 노트북은 돌아오지 않습니다. 소중한 물건은 방이 아니라 **호텔 바깥의 내 금고(볼륨)**에 넣어야, 다음에 어느 방에 묵든 다시 꺼낼 수 있습니다.

## 실습 1 · 볼륨 없이 DB를 지워 보기

> **🧪 실습: 실습 목표**
>
> PostgreSQL 18 컨테이너를 **볼륨 없이** 띄워 표를 만들고, 컨테이너를 지웠다가 다시 띄워서 표가 사라졌는지 확인합니다.

### 단계 1 — PostgreSQL 컨테이너 실행

```bash
docker run -d --name db-temp \
  -e POSTGRES_USER=devmart \
  -e POSTGRES_PASSWORD=devmart-pw \
  -e POSTGRES_DB=devmart \
  postgres:18
```

- `\` : 명령이 길어서 다음 줄에 이어 쓴다는 표시. 그대로 복사해 붙여 넣으면 됩니다.
- `-e POSTGRES_USER=…` : PostgreSQL 공식 이미지가 **처음 시작할 때** 읽는 환경 변수. 이 사용자와 비밀번호, DB를 만들어 줍니다.
- `devmart-pw` : 실습용 비밀번호입니다. **명령어에 비밀번호를 직접 쓰는 것은 나쁜 습관**인데, 왜 나쁜지와 고치는 법은 6교시에 다룹니다. 지금은 그대로 따라 합니다.

### 단계 2 — 준비될 때까지 기다리기

DB는 켜지는 데 몇 초가 걸립니다. 준비되었는지 물어봅니다.

```bash
docker exec db-temp pg_isready -U devmart
```

> **🟢 확인: 이렇게 나오면 준비 완료**
>
> ```text
> /var/run/postgresql:5432 - accepting connections
> ```
> `no response`가 나오면 3~5초 뒤에 다시 실행하세요. 처음 시작할 때는 DB 파일을 새로 만드느라 조금 더 걸립니다.

### 단계 3 — 표를 만들고 한 줄 넣기

`psql`은 PostgreSQL에 SQL을 보내는 명령줄 도구입니다. 컨테이너 **안에** 들어 있으므로 `docker exec`로 실행합니다.

```bash
docker exec db-temp psql -U devmart -d devmart \
  -c "CREATE TABLE memo(t TEXT); INSERT INTO memo VALUES ('지워질까?');"
docker exec db-temp psql -U devmart -d devmart -c "SELECT * FROM memo;"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> INSERT 0 1
>      t
> -----------
>  지워질까?
> (1 row)
> ```

### 단계 4 — 지우고, 같은 명령으로 다시 띄우기

```bash
docker rm -f db-temp
docker run -d --name db-temp \
  -e POSTGRES_USER=devmart -e POSTGRES_PASSWORD=devmart-pw -e POSTGRES_DB=devmart \
  postgres:18
```

몇 초 기다렸다가(`pg_isready`로 확인) 표를 찾아봅니다.

```bash
docker exec db-temp psql -U devmart -d devmart -c "SELECT * FROM memo;"
```

> **🟢 확인: 보이는 것 — 사라졌다**
>
> ```text
> ERROR:  relation "memo" does not exist
> LINE 1: SELECT * FROM memo;
>                       ^
> ```
> **표가 없습니다.** 같은 이미지, 같은 이름, 같은 설정으로 다시 띄웠지만 새 컨테이너는 **새 빈 데이터**로 시작했습니다. 운영 중인 쇼핑몰이었다면 모든 주문이 사라진 것입니다.

## 진짜로 사라졌을까? — 이름 없는 볼륨

조금 이상한 점을 찾아봅시다.

```bash
docker volume ls
```

> **🟢 확인: 보이는 것**
>
> ```text
> DRIVER    VOLUME NAME
> local     1673955…(64자리 무작위 이름)
> local     5835936…(64자리 무작위 이름)
> ```
> 우리는 볼륨을 만든 적이 없는데 볼륨이 **두 개** 있습니다.

PostgreSQL 공식 이미지의 Dockerfile에는 `VOLUME /var/lib/postgresql`이라는 줄이 있습니다. "이 폴더는 데이터를 담는 곳이니 쓰기 가능한 층이 아니라 **볼륨에 두라**"는 표시입니다. 그래서 우리가 `-v`를 주지 않으면 Docker가 **무작위 이름의 볼륨**을 자동으로 만들어 붙입니다. 이것을 **이름 없는 볼륨(anonymous volume)**이라고 합니다.

- 첫 번째 `db-temp`의 데이터(`지워질까?`)는 사실 첫 번째 이름 없는 볼륨에 **남아 있습니다.**
- 하지만 두 번째 `db-temp`는 그 볼륨을 모르고 **새 이름 없는 볼륨**을 또 만들었습니다.
- 이름이 무작위라 **어느 것이 내 데이터인지 알 수 없고**, 다시 붙이기도 어렵습니다. 사실상 **버려진 데이터**이고, 디스크만 차지합니다.

```bash
docker system df -v | grep -A5 "VOLUME NAME"
```

> **🟢 확인: 보이는 것**
>
> ```text
> VOLUME NAME                                  LINKS     SIZE
> 5835936…                                     1         62.65MB
> 1673955…                                     0         87.72MB
> ```
> `LINKS 0`인 볼륨은 어느 컨테이너에도 연결되지 않은 **고아 볼륨**입니다. 크기가 수십 MB씩 됩니다. 실습을 여러 번 반복하면 금방 GB 단위로 쌓입니다.

> **❓ 오해 — '컨테이너를 지우면 디스크가 깨끗해진다'**
>
> `docker rm`은 **이름 없는 볼륨을 지우지 않습니다.** 컨테이너와 함께 지우려면 `docker rm -v`를, 이미 고아가 된 것은 `docker volume prune`을 씁니다. 반대로 말하면, Docker는 "혹시 소중한 데이터일지 모르니" 볼륨을 함부로 지우지 않는다는 뜻이기도 합니다.

## 정리 — 실습 1 뒷정리

> **🧹 정리: 정리**
>
> ```bash
> docker rm -f -v db-temp
> docker volume prune -a
> ```
> `prune`은 지워도 되는지 `[y/N]`으로 묻습니다. `y`를 입력합니다. `-a`는 이름 있는 볼륨까지 포함해 **연결되지 않은 모든 볼륨**을 지우므로, 실제 업무에서는 신중하게 씁니다. 지금은 실습용 데이터뿐이라 괜찮습니다.

> [!IMPORTANT]
> **1교시 핵심**
>
> | 상황 | 데이터 |
> |---|---|
> | 컨테이너 안(쓰기 가능한 층)에 쓴 파일 | `docker rm`과 함께 **사라짐** |
> | 이름 없는 볼륨 | 남지만 **찾을 수 없음** (고아) |
> | 이름 있는 볼륨 (2교시) | 남고, **이름으로 다시 붙일 수 있음** |

> **🎓 학술 노트 — 'D'를 지키는 일: 트랜잭션의 지속성**
>
> 데이터베이스 교과서에 빠지지 않는 단어가 **ACID**입니다. 1983년 독일의 테오 해더(Theo Härder)와 안드레아스 로이터(Andreas Reuter)가 논문 「트랜잭션 중심 데이터베이스 복구의 원칙」(ACM Computing Surveys)에서 정리한 네 가지 성질 — 원자성(Atomicity), 일관성(Consistency), 격리성(Isolation), **지속성(Durability)** — 의 머리글자입니다.
>
> 지속성은 "**한 번 완료되었다고 알린 데이터는 그 뒤에 전원이 나가도, 프로그램이 죽어도 사라지지 않는다**"는 약속입니다. PostgreSQL은 이 약속을 지키려고 데이터를 디스크에 쓰고 나서야 "저장 완료"라고 답합니다. 그런데 그 디스크가 **컨테이너의 쓰기 가능한 층**이라면, 컨테이너를 지우는 순간 약속이 깨집니다. DB 프로그램은 약속을 지켰는데 **그 아래 저장소가 사라진** 셈이지요. 그래서 컨테이너 시대에는 "데이터를 어디에 두느냐"가 DB 프로그램 바깥, 즉 **인프라의 책임**이 되었습니다. 오늘 배우는 볼륨이 그 답이고, 3주차 Kubernetes의 PersistentVolume, 5주차 AWS의 EBS가 같은 문제의 더 큰 답입니다.
>
> - Härder, T., & Reuter, A. (1983). Principles of transaction-oriented database recovery. *ACM Computing Surveys, 15*(4), 287–317.

> **📈 트렌드 — '데이터가 있는 것'은 컨테이너 밖으로**
>
> 1주차 1일차에 배운 관리형 서비스를 기억하나요? 실제 회사에서는 **운영 DB를 직접 컨테이너로 돌리기보다 Amazon RDS 같은 관리형 DB를 쓰는 경우가 많습니다.** 백업, 장애 조치, 패치를 클라우드가 대신해 주기 때문입니다. 컨테이너로 돌리는 DB는 주로 **개발·테스트용**이고, 오늘 우리가 하는 것도 그 용도입니다. 반면 Kubernetes 위에서 DB를 안전하게 운영하도록 돕는 **오퍼레이터(Operator)** 도구들도 꾸준히 발전하고 있어, "상태가 있는 앱을 어디에 둘 것인가"는 지금도 팀마다 고민하는 설계 결정입니다. 5주차 AWS에서 이 선택을 직접 해 봅니다.

## 정리

- 컨테이너 안에 쓴 데이터는 컨테이너와 함께 사라진다. 상품 API처럼 기억할 게 없는 앱에는 장점, **DB에는 치명적**이다.
- PostgreSQL 이미지는 `VOLUME` 지시어 때문에 `-v`를 안 줘도 **이름 없는 볼륨**을 만든다. 남긴 하지만 찾을 수 없다.
- `docker rm`은 볼륨을 지우지 않는다. `docker rm -v`, `docker volume prune`.
- 다음 시간: 이름을 붙인 볼륨으로 데이터를 지킨다.

> **✅ 확인 문제**
>
> 1. 볼륨 없이 띄운 DB 컨테이너를 지우고 같은 명령으로 다시 띄우면 표는 어떻게 되나요?
> 2. 우리가 만들지 않았는데 `docker volume ls`에 볼륨이 생긴 이유는?
> 3. `LINKS 0`인 볼륨은 무엇인가요?
> 4. ACID의 D는 무엇이고, 컨테이너와 어떤 관계가 있나요?
>
> <details><summary>정답</summary>
>
> 1. 없다. 새 컨테이너는 새 빈 데이터로 시작한다 (`relation "memo" does not exist`)
> 2. 이미지의 `VOLUME /var/lib/postgresql` 지시어 때문에 Docker가 이름 없는 볼륨을 자동으로 만들었다
> 3. 어느 컨테이너에도 연결되지 않은 고아 볼륨. 디스크만 차지한다
> 4. 지속성(Durability). 저장된 데이터는 사라지지 않아야 하는데, 쓰기 가능한 층은 컨테이너와 함께 사라지므로 볼륨이 필요하다
>
> </details>

## 참고 문헌

- Docker Docs. *Volumes*. docs.docker.com/engine/storage/volumes
- Docker Hub. *postgres Docker Official Image — PGDATA, Where to store data*. hub.docker.com/_/postgres
- Härder, T., & Reuter, A. (1983). Principles of transaction-oriented database recovery. *ACM Computing Surveys, 15*(4).
