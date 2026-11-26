# 8교시 · 네트워크 진단 도구 (강사 시연)

!!! goal "이번 시간에 할 일"
    - "연결이 안 돼요"를 **아래 층부터 위로** 하나씩 확인하는 순서를 압니다.
    - `ping` · `traceroute` · `dig` · `nc` · `curl -v`가 각각 **어느 층의 질문**에 답하는지 압니다.
    - 도구의 출력에서 **어디서 끊겼는지**를 읽습니다.
    - `ping`이 안 된다고 서버가 죽은 것은 아니라는 점을 압니다.

!!! warn "오늘도 따라 치지 않습니다"
    강사가 시연합니다. 2주차부터 컨테이너가 서로 못 찾거나, 3주차에 Pod끼리 통신이 안 될 때 **오늘 순서 그대로** 직접 쓰게 됩니다.

## 진단의 순서 — 아래 층부터

6교시의 "요청의 여정"을 거꾸로 따라갑니다. 위층(HTTP)이 실패하면 원인은 그 층일 수도, 그 아래 어느 층일 수도 있습니다. 그래서 **아래에서 위로** 하나씩 지워 나갑니다.

| 순서 | 질문 | 층 | 도구 | 대표 실패 |
|---|---|---|---|---|
| 1 | 내 컴퓨터에 주소와 길이 있나? | 네트워크 설정 | `ip addr`, `ip route` | 주소 없음, 기본 경로 없음 |
| 2 | 이름이 IP로 바뀌나? | DNS (4교시) | `dig`, `nslookup` | `NXDOMAIN`, 응답 없음 |
| 3 | 그 IP까지 길이 있나? | IP (2교시) | `ping`, `traceroute` | 중간에서 끊김 |
| 4 | 그 포트의 문이 열려 있나? | TCP (3교시) | `nc -zv`, `ss -tlnp` | `refused`, `timed out` |
| 5 | 암호화 악수가 되나? | TLS (5교시) | `curl -v`, `openssl s_client` | 인증서 오류 |
| 6 | 앱이 제대로 답하나? | HTTP (5교시) | `curl -i` | 4xx, 5xx |

!!! key "한 층씩 '여기까지는 된다'를 확인한다"
    2번이 되면 DNS는 범인이 아닙니다. 4번이 되면 방화벽도 범인이 아닙니다. 이렇게 **된다는 증거**를 쌓아 범위를 좁히는 것이 진단입니다. 처음부터 앱 로그를 뒤지면 아래층 문제를 놓칩니다.

## 시연 1 — 이름: `dig`

```text
$ dig +short shop.example.com
203.0.113.25

$ dig shop.example.com

;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4127
;; ANSWER SECTION:
shop.example.com.   300   IN   A   203.0.113.25
;; Query time: 23 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
```

| 어디를 보나 | 읽는 법 |
|---|---|
| `status: NOERROR` | 이름이 있다. `NXDOMAIN`이면 **그런 이름이 없음**(오타 · 레코드 미등록) |
| `300` | TTL(초). 4교시 "바꿨는데 왜 안 바뀌죠?"의 그 숫자 |
| `SERVER` | **누구에게 물었나**. 회사 · 클라우드 · 클러스터마다 다른 DNS 서버를 쓴다 |

`dig @8.8.8.8 shop.example.com`처럼 **물어볼 서버를 바꿔** 결과가 다르면, 내 쪽 DNS 서버(캐시)가 문제입니다.

## 시연 2 — 길: `ping` · `traceroute`

```text
$ ping -c 3 203.0.113.25
64 bytes from 203.0.113.25: icmp_seq=1 ttl=52 time=31.8 ms
64 bytes from 203.0.113.25: icmp_seq=2 ttl=52 time=32.1 ms
64 bytes from 203.0.113.25: icmp_seq=3 ttl=52 time=31.5 ms
--- 203.0.113.25 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
```

- `time` : 왕복 시간(RTT). 1교시의 "빛도 시간이 걸린다" — 서울↔미국 서부는 보통 130ms 이상
- `packet loss` : 잃어버린 비율. 0%가 아니면 길 어딘가가 불안정

```text
$ traceroute -n 203.0.113.25
 1  192.168.0.1     1.2 ms
 2  10.20.0.1       3.8 ms
 3  * * *
 4  198.51.100.9   28.4 ms
 5  203.0.113.25   31.9 ms
```

`traceroute`는 IP 패킷의 **TTL**(거칠 수 있는 라우터 수, DNS의 TTL과는 다른 것)을 1, 2, 3…으로 늘려 보내며, 각 라우터가 "여기서 수명이 다했다"고 돌려주는 답으로 **길 위의 정거장**을 하나씩 찾습니다. 1번은 집 공유기(사설 IP, 2교시), 마지막은 목적지입니다.

!!! myth "ping이 안 되니 서버가 죽었다?"
    아닙니다. `ping`은 TCP도 UDP도 아닌 **ICMP**라는 별도 프로토콜을 씁니다. 클라우드는 보안 그룹에서 ICMP를 따로 열지 않으면 **기본으로 막습니다**(7교시). 그래서 웹 서버는 멀쩡히 응답하는데 `ping`만 실패하는 일이 흔합니다. 위 `traceroute`의 `* * *`도 그 라우터가 답을 안 하도록 설정됐을 뿐, 길이 끊긴 것은 아닙니다(다음 줄이 이어지므로). **ping 실패는 '모른다'이지 '죽었다'가 아닙니다.** 판단은 4번(포트)에서 합니다.

## 시연 3 — 문: `nc` · `ss`

```text
$ nc -zv 203.0.113.25 443
Connection to 203.0.113.25 443 port [tcp/https] succeeded!

$ nc -zv -w 3 203.0.113.25 5432
nc: connect to 203.0.113.25 port 5432 (tcp) timed out
```

- `-z` : 데이터는 보내지 않고 **문이 열리는지만** 확인. `-w 3` : 3초만 기다림
- 3교시의 표 그대로: `succeeded` → 문 열림, `refused` → 받는 프로그램 없음, `timed out` → **방화벽이 조용히 버림**

서버 **안에서** 보면 반대쪽을 확인할 수 있습니다.

```text
$ sudo ss -tlnp
State   Local Address:Port   Process
LISTEN  127.0.0.1:5432       users:(("postgres",pid=812))
LISTEN  0.0.0.0:443          users:(("nginx",pid=640))
```

PostgreSQL이 `127.0.0.1`에서만 듣고 있습니다. 3교시의 표처럼 **자기 자신만 접속 가능** — 밖에서는 `refused`가 납니다. 2주차 컨테이너에서 `0.0.0.0`으로 열어야 하는 이유가 이것입니다.

## 시연 4 — 암호화와 앱: `curl -v`

```text
$ curl -v https://shop.example.com/api/health
*   Trying 203.0.113.25:443...
* Connected to shop.example.com (203.0.113.25) port 443
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: CN=shop.example.com
*  expire date: Feb 14 23:59:59 2027 GMT
*  SSL certificate verify ok.
> GET /api/health HTTP/2
> Host: shop.example.com
< HTTP/2 503
< content-type: application/json
{"status":"db unavailable"}
```

`curl -v` 한 번이 2~6번 질문에 모두 답합니다.

| 줄 | 층 | 이 출력에서 |
|---|---|---|
| `Trying 203.0.113.25` | DNS | 이름이 IP로 바뀌었다 ✓ |
| `Connected … port 443` | TCP | 문이 열렸다 ✓ |
| `SSL certificate verify ok` | TLS | 인증서가 유효하다 ✓ (`expire date`도 확인) |
| `< HTTP/2 503` | HTTP | **앱이 실패** — 503은 서버 쪽, 본문에 "DB 연결 안 됨" |

결론: 네트워크는 끝까지 멀쩡하고, **앱 뒤의 DB**가 범인입니다. 6교시의 여정에서 ⑦번 칸입니다.

!!! tip "자주 쓰는 curl 옵션"
    | 옵션 | 뜻 |
    |---|---|
    | `-i` | 응답 헤더도 보여 줘 |
    | `-v` | 연결 과정 전부 보여 줘 |
    | `-sS -o /dev/null -w '%{http_code} %{time_total}\n'` | 상태 코드와 걸린 시간만 |
    | `--resolve shop.example.com:443:10.0.1.5` | DNS를 건너뛰고 **이 IP로** 붙어 봐 (새 서버 미리 시험) |
    | `-k` | 인증서 검사를 끄기 — **진단용으로만**, 코드에 넣지 않는다 |

## 증상에서 도구로

| 증상 (에러 메시지) | 의심하는 층 | 먼저 쓸 도구 |
|---|---|---|
| `Could not resolve host` | DNS | `dig` |
| `Connection timed out` | 방화벽 · 경로 | `nc -zv`, 보안 그룹 확인 |
| `Connection refused` | 포트에 듣는 프로그램 없음 | 서버 안에서 `ss -tlnp` |
| `SSL certificate problem` | TLS | `curl -v`의 인증서 줄 |
| `HTTP 502 / 503 / 504` | 앱 · 앱 뒤의 의존성 | 앱 로그, 헬스 체크 |

!!! academic "학술 노트 — 진단 도구도 '프로토콜의 빈틈'에서 나왔다"
    `traceroute`는 1988년 로런스 버클리 연구소의 **밴 제이컵슨(Van Jacobson)**이 만들었습니다. 그는 IP 헤더의 TTL이 0이 되면 라우터가 ICMP "시간 초과" 메시지를 돌려준다는 규칙(RFC 792, 1981)을 **원래 의도와 다르게** 써서, 길 위의 라우터를 하나씩 드러내는 방법을 고안했습니다. 같은 해 그는 3교시에서 본 1986년 인터넷 혼잡 붕괴를 해결한 **TCP 혼잡 제어** 논문도 발표했습니다. 네트워크 진단의 기본 도구들이 새로운 장비가 아니라 **이미 있는 프로토콜의 동작을 영리하게 관찰**하는 데서 나왔다는 점은, 4주차의 관찰 가능성(시스템이 이미 내놓는 신호를 읽는다)과 같은 생각입니다.

    - Postel, J. (1981). *RFC 792: Internet Control Message Protocol*.
    - Jacobson, V. (1988). Congestion avoidance and control. *ACM SIGCOMM '88*.

!!! trend "트렌드 — 진단 도구도 클러스터 안으로"
    컨테이너 이미지는 크기를 줄이려고 `ping`, `dig`, `curl`조차 빼는 경우가 많습니다(2주차 3일차의 작은 이미지). 그래서 요즘은 문제가 생긴 컨테이너 **옆에 진단 도구만 든 임시 컨테이너를 붙여** 같은 네트워크에서 오늘의 명령을 실행합니다. Kubernetes의 `kubectl debug`(3주차 4일차)와, 진단 도구를 모아 둔 `nicolaka/netshoot` 같은 이미지가 그 방법입니다. 도구는 같고, **어디서 실행하느냐**만 바뀌었습니다.

## 정리

- 연결 문제는 **설정 → DNS → 경로 → 포트 → TLS → HTTP** 순서로, 아래층부터 "여기까지는 된다"를 쌓습니다.
- `dig`는 이름, `ping`·`traceroute`는 길, `nc`·`ss`는 문, `curl -v`는 TLS와 앱까지 한 번에 봅니다.
- **ping 실패는 '모른다'**입니다. 클라우드는 ICMP를 기본으로 막습니다.
- `refused`는 듣는 프로그램이 없음, `timed out`은 방화벽 — 3교시의 표가 진단의 핵심입니다.

!!! quiz "확인 문제"
    1. `curl`이 `Could not resolve host`를 냈습니다. 어느 층부터 보나요, 어떤 도구로?
    2. 웹 페이지는 잘 열리는데 그 서버로 `ping`이 실패합니다. 서버가 아픈가요?
    3. `nc -zv db 5432`가 `refused`입니다. 서버 안에서 무엇을 확인하나요?
    4. `curl -v` 출력에 `SSL certificate verify ok`와 `HTTP/2 504`가 함께 보입니다. 네트워크와 앱 중 어디가 문제인가요?
    5. DNS를 건너뛰고 특정 IP의 새 서버에 미리 붙어 보는 `curl` 옵션은?

    ??? answer "정답"
        1. DNS — `dig 이름`으로 이름이 있는지(NXDOMAIN 여부), 어느 서버에 물었는지 확인합니다.
        2. 아닙니다. ICMP만 막혀 있을 수 있습니다. 판단은 포트(HTTP)가 열리는지로 합니다.
        3. `ss -tlnp`로 PostgreSQL이 그 포트에서 듣고 있는지, `127.0.0.1`에만 묶여 있지 않은지 봅니다.
        4. TLS까지는 정상이고 504(게이트웨이 시간 초과)는 앱 쪽 — 프록시 뒤의 앱이나 그 의존성이 늦게 답하고 있습니다.
        5. `--resolve 이름:포트:IP`

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - 오늘 배운 것 중 2주차 Docker 실습에서 바로 쓸 것 같은 한 가지 (예: 0.0.0.0과 127.0.0.1)
    - 3교시의 에러 메시지 표(refused, timed out…)를 내 말로 한 줄씩 다시 써 보기
    - 내일(현대 애플리케이션 구조) 수업 전에 궁금한 것 하나

## 참고 문헌

- Postel, J. (1981). *RFC 792: Internet Control Message Protocol*. IETF.
- Jacobson, V. (1988). Congestion avoidance and control. *Proceedings of ACM SIGCOMM '88*.
- curl project. *Everything curl* — Verbose, `--resolve`, `-w` variables. everything.curl.dev
- ISC. *dig — DNS lookup utility* (BIND 9 Administrator Reference Manual).
- man7.org. *ss(8), ip(8), traceroute(8), nc(1)*.
- Kubernetes Documentation. *Debug Running Pods — Ephemeral containers*.
