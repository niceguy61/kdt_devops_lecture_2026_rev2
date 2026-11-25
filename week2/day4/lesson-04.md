# 4교시 · Docker 네트워크와 이름 찾기

> [!NOTE]
> **이번 시간에 할 일**
>
> - 컨테이너마다 IP 주소가 있지만 **IP는 믿을 수 없다**는 것을 확인합니다.
> - 기본 네트워크(`bridge`)에서는 **이름으로 서로를 찾을 수 없다**는 것을 봅니다.
> - 사용자 정의 네트워크 `devmart-net`을 만들고 **컨테이너 이름 = 주소**가 되는 것을 확인합니다.
> - `-p`(바깥 ↔ 컨테이너)와 네트워크(컨테이너 ↔ 컨테이너)의 차이를 정리합니다.

## 문제 — API는 DB를 어떻게 찾을까

2교시에 DB(`db`)를 띄웠습니다. 이제 상품 API가 이 DB에 접속해야 합니다. API의 코드는 환경 변수 `DB_HOST`에 적힌 주소로 접속합니다. 그럼 `DB_HOST`에 무엇을 적어야 할까요?

- `localhost`? — **안 됩니다.** 2일차 7교시 실패 4에서 `127.0.0.1`(나 자신)을 봤듯이, 컨테이너 안의 `localhost`는 **그 컨테이너 자신**입니다. API 컨테이너 안에는 DB가 없습니다.
- DB 컨테이너의 IP 주소? — 될 것 같지만 **곧 깨집니다.** 아래에서 확인합니다.
- **DB 컨테이너의 이름(`db`)** — 이것이 정답입니다. 단, **조건이 하나** 있습니다.

## 실습 6 · 기본 네트워크에서는 이름이 통하지 않는다

> **🧪 실습: 실습 목표**
>
> 네트워크를 따로 지정하지 않은 컨테이너 두 개가 서로를 이름으로 찾을 수 있는지 확인합니다.

### 단계 1 — 컨테이너 두 개 띄우기

```bash
docker run -d --name api-a devmart/catalog-api:1.0.1
docker run -d --name api-b devmart/catalog-api:1.0.1
docker network ls
```

> **🟢 확인: 보이는 것**
>
> ```text
> NETWORK ID     NAME      DRIVER    SCOPE
> 4a74b0bf64c2   bridge    bridge    local
> 3c22633b6e9e   host      host      local
> 63d7017b5865   none      null      local
> ```
> Docker는 처음부터 네트워크 세 개를 갖고 있습니다. `--network`를 주지 않은 컨테이너는 모두 **`bridge`**(기본 네트워크)에 연결됩니다. `host`는 컨테이너가 노트북의 네트워크를 그대로 쓰는 것, `none`은 네트워크가 아예 없는 것입니다.

### 단계 2 — IP 주소 보기

```bash
docker inspect api-b --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

> **🟢 확인: 보이는 것**
>
> ```text
> 172.17.0.3
> ```
> 컨테이너마다 `172.17.0.x` 같은 **사설 IP**가 붙습니다. 숫자는 사람마다 다릅니다.

### 단계 3 — 이름으로 찾아보기

`getent hosts 이름`은 "이 이름의 IP 주소가 뭐지?"를 물어보는 명령입니다. 찾으면 IP를 출력하고, 못 찾으면 **아무것도 출력하지 않습니다.**

```bash
docker exec api-a getent hosts api-b
echo "결과 코드: $?"
```

> **🟢 확인: 보이는 것 — 못 찾는다**
>
> ```text
> 결과 코드: 2
> ```
> 아무것도 나오지 않고 결과 코드가 `2`(찾지 못함)입니다. 같은 `bridge` 네트워크에 있어서 **IP로는 통하지만, 이름으로는 서로를 모릅니다.** 기본 네트워크는 옛날 Docker와의 호환을 위해 **이름 찾기(DNS) 기능이 꺼져** 있습니다.

### 단계 4 — IP는 왜 믿을 수 없나

```bash
docker rm -f api-b
docker run -d --name api-c devmart/catalog-api:1.0.1
docker run -d --name api-b devmart/catalog-api:1.0.1
docker inspect api-b --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

> **🟢 확인: 보이는 것**
>
> ```text
> 172.17.0.4
> ```
> 같은 이름 `api-b`로 다시 띄웠는데 **IP가 바뀌었습니다.** 그 사이 `api-c`가 먼저 빈 번호를 가져갔기 때문입니다. 컨테이너는 고장 나면 지우고 새로 띄우는 **가축**이라, 띄울 때마다 IP가 달라질 수 있습니다. API 설정에 DB의 IP를 적어 두면 DB 컨테이너를 한 번 다시 띄우는 순간 API가 엉뚱한 곳에 접속합니다.

> **🧹 정리: 정리**
>
> ```bash
> docker rm -f api-a api-b api-c
> ```

## 사용자 정의 네트워크 — 이름이 곧 주소

해결책은 **내가 만든 네트워크(사용자 정의 브리지 네트워크)**입니다. 여기에 연결된 컨테이너들은 Docker에 내장된 **DNS 서버**가 서로의 이름을 IP로 바꿔 줍니다. 컨테이너가 다시 떠서 IP가 바뀌어도 DNS가 새 IP를 알려 주므로, 이름만 쓰면 항상 맞는 곳을 찾아갑니다.

![기본 bridge 네트워크에서는 이름 찾기가 안 되고, 사용자 정의 네트워크에서는 Docker 내장 DNS가 컨테이너 이름을 IP로 바꿔 준다](../../assets/week2/day4/w2d4-bridge-dns.png)

> **🧩 비유 — 회사 내선 전화번호부**
>
> 컨테이너 IP는 **자리 번호**입니다. 자리 배치가 바뀌면 번호도 바뀝니다. 사용자 정의 네트워크는 **사내 전화번호부**가 있는 회사입니다. "DB팀 연결해 주세요"라고 하면 교환원(내장 DNS)이 오늘 DB팀이 앉은 자리로 연결해 줍니다. 기본 `bridge`는 전화번호부가 없는 회사라 자리 번호를 외워야 합니다.

## 실습 7 · `devmart-net` 만들기

> **🧪 실습: 실습 목표**
>
> DevMart 전용 네트워크를 만들고, 2교시의 `db` 컨테이너를 연결한 뒤 이름으로 찾아봅니다.

### 단계 1 — 네트워크 만들기

```bash
docker network create devmart-net
docker network ls
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> f4d734abf972…
> NETWORK ID     NAME          DRIVER    SCOPE
> 4a74b0bf64c2   bridge        bridge    local
> f4d734abf972   devmart-net   bridge    local
> ...
> ```
> `DRIVER`가 `bridge`인 것은 같지만, **내가 만든** 브리지라 이름 찾기가 켜져 있습니다.

### 단계 2 — 실행 중인 DB를 네트워크에 연결

2교시에 띄운 `db`는 기본 `bridge`에 있습니다. 지우지 않고 **실행 중인 채로** 새 네트워크에 연결할 수 있습니다.

```bash
docker network connect devmart-net db
```

다음부터는 처음 띄울 때 `--network devmart-net`을 주면 됩니다(5교시).

### 단계 3 — 같은 네트워크에서 이름 찾기

같은 네트워크에 임시 컨테이너를 하나 띄워 `db`를 찾아봅니다.

```bash
docker run --rm --network devmart-net devmart/catalog-api:1.0.1 getent hosts db
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 172.18.0.2      db
> ```
> 이번에는 이름 `db`가 IP로 바뀌었습니다. `172.18.…`로 시작하는 것은 `devmart-net`이 **별도의 주소 대역**을 쓰기 때문입니다.

### 단계 4 — 네트워크 안 들여다보기

```bash
docker network inspect devmart-net \
  --format '{{range .Containers}}{{.Name}}  {{.IPv4Address}}{{"\n"}}{{end}}'
```

> **🟢 확인: 보이는 것**
>
> ```text
> db  172.18.0.2/16
> ```
> 지금 `devmart-net`에는 `db` 하나만 있습니다. 5교시에 `catalog-api`, 7교시에 `web`이 들어옵니다.

## `-p`와 네트워크는 다른 문

헷갈리기 쉬운 두 가지를 정리합니다.

| | `-p 8000:8000` (포트 공개) | `--network devmart-net` |
|---|---|---|
| 누가 들어오나 | **노트북 바깥**(브라우저, `curl`) → 컨테이너 | **컨테이너 ↔ 컨테이너** |
| 주소 | `localhost:8000` | `컨테이너이름:컨테이너포트` (예: `db:5432`) |
| 포트 번호 | 바깥:안 (바깥 번호는 바꿀 수 있음) | 컨테이너가 실제로 듣는 포트 그대로 |
| 오늘의 예 | `web`의 8080, (확인용) API의 8000 | API → `db:5432`, 웹 → `catalog-api:8000` |

> [!IMPORTANT]
> **DB에는 `-p`를 주지 않는다**
>
> 2교시의 `db`는 `-p 5432:5432`를 주지 않았습니다. 그래서 **노트북 바깥에서는 DB에 접속할 수 없고**, 같은 네트워크의 컨테이너만 접속할 수 있습니다. 1주차 3일차에 배운 "바깥에 노출하면 안 되는 서버는 사설 서브넷에"와 같은 원리입니다. 꼭 필요한 문만 바깥으로 연다 — **최소 노출**입니다. 5주차 AWS의 보안 그룹, 4주차 Kubernetes의 NetworkPolicy가 같은 생각을 더 정교하게 표현합니다.

> **❓ 오해 — '같은 노트북에 있으니 컨테이너끼리 `localhost`로 부르면 된다'**
>
> 각 컨테이너는 **자기만의 네트워크 공간**(네트워크 네임스페이스)을 갖습니다. 그래서 컨테이너마다 `localhost`가 다르고, 각자 자기 자신을 가리킵니다. 같은 노트북에 있어도 컨테이너끼리는 **서로 다른 컴퓨터처럼** 이름이나 IP로 불러야 합니다. (예외: `--network host`를 쓰면 노트북의 네트워크를 공유하지만, Docker Desktop에서는 동작이 다르고 격리가 깨지므로 이 과정에서는 쓰지 않습니다.)

> **🎓 학술 노트 — 이름과 주소를 나누는 발명, DNS**
>
> "사람은 이름으로 부르고, 기계는 숫자로 찾는다"는 문제는 인터넷 초창기에도 있었습니다. 1980년대 초까지는 모든 컴퓨터의 이름과 주소를 적은 **`HOSTS.TXT` 파일 하나**를 중앙에서 관리하고 모두가 내려받아 썼습니다. 컴퓨터가 늘자 파일은 매일 바뀌고 커져서 감당할 수 없게 되었습니다.
>
> 1983년 폴 모카페트리스(Paul Mockapetris)가 이 문제를 풀려고 **DNS(Domain Name System)**를 설계했고, 1987년 RFC 1034·1035로 표준이 되었습니다. 핵심은 **"이름과 주소를 분리하고, 주소는 바뀌어도 이름으로 언제든 다시 찾을 수 있게"**입니다. Docker의 내장 DNS는 이 40년 된 아이디어를 컨테이너 규모로 옮긴 것입니다. 3주차 Kubernetes에서는 **CoreDNS**가 `catalog-api.default.svc.cluster.local` 같은 이름을 같은 방식으로 풀어 주고, 4주차 Istio는 그 위에서 "어느 이름으로 보낼지"까지 조절합니다.
>
> - Mockapetris, P. (1987). *Domain names — concepts and facilities* (RFC 1034) / *implementation and specification* (RFC 1035). IETF.

> **📈 트렌드 — '어디에 있는가'보다 '누구인가'로 연결한다**
>
> 컨테이너 시대에는 IP가 계속 바뀌기 때문에, IP를 기준으로 "이 주소는 허용, 저 주소는 차단"하는 옛 방식이 잘 맞지 않습니다. 그래서 요즘은 **서비스의 이름과 신원(identity)**을 기준으로 통신을 허용하는 방식이 퍼지고 있습니다. 4주차에 배울 **서비스 메시(Istio)**는 서비스마다 인증서로 된 신원을 주고 "catalog-api만 db에 접속 가능" 같은 규칙을 신원으로 표현합니다. 출발점은 오늘처럼 **이름으로 찾는 것**입니다.

## 정리

- 컨테이너 IP는 다시 띄울 때마다 바뀔 수 있다 → **IP를 설정에 적지 않는다.**
- 기본 `bridge` 네트워크는 **이름 찾기가 안 된다.**
- `docker network create`로 만든 **사용자 정의 네트워크**에서는 **컨테이너 이름 = 주소** (내장 DNS).
- `-p`는 바깥 ↔ 컨테이너, 네트워크는 컨테이너 ↔ 컨테이너. **DB에는 `-p`를 주지 않는다.**

> **✅ 확인 문제**
>
> 1. API 컨테이너의 `DB_HOST`에 `localhost`를 쓰면 안 되는 이유는?
> 2. 기본 `bridge` 네트워크의 두 컨테이너가 서로 이름으로 찾지 못하는 이유는?
> 3. DB 컨테이너의 IP를 설정에 적으면 어떤 문제가 생기나요?
> 4. 같은 `devmart-net`의 API가 DB에 접속할 주소는? (포트 포함)
> 5. DB 컨테이너에 `-p 5432:5432`를 주지 않은 이유는?
>
> <details><summary>정답</summary>
>
> 1. 컨테이너 안의 `localhost`는 API 컨테이너 자신이라 DB가 없다
> 2. 기본 bridge는 호환성 때문에 내장 DNS(이름 찾기)가 꺼져 있다
> 3. DB를 다시 띄우면 IP가 바뀌어 API가 엉뚱한 곳에 접속한다
> 4. `db:5432`
> 5. 바깥에서 DB에 접속할 필요가 없으므로 최소 노출 원칙에 따라 문을 열지 않는다
>
> </details>

## 참고 문헌

- Docker Docs. *Networking overview*, *Bridge network driver — Differences between user-defined bridges and the default bridge*. docs.docker.com/engine/network
- Mockapetris, P. (1987). RFC 1034 / RFC 1035. IETF.
- Kubernetes Docs. *DNS for Services and Pods*. kubernetes.io/docs/concepts/services-networking/dns-pod-service
