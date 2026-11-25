# 2교시 · 타임아웃 · 재시도 · 헬스 체크

!!! goal "이번 시간에 할 일"
    - 타임아웃 값을 정하는 기준을 압니다.
    - **재시도**가 잠깐의 장애는 살리고, 긴 장애는 더 나쁘게 만드는 것을 실험으로 봅니다.
    - **지수 백오프**와 재시도하면 안 되는 경우를 구분합니다.
    - `compose.yaml`에 **헬스 체크**와 **재시작 정책**을 넣고, 크래시 루프를 관찰합니다.

## 타임아웃 — 얼마나 기다릴까

1교시의 결론은 "타임아웃이 길면 장애가 번진다"였습니다. 그렇다고 0.1초로 하면 정상일 때도 실패합니다. 기준은 **정상일 때 얼마나 걸리는가**입니다.

어제 5교시 여행 기록에서 catalog-api 호출은 **약 14ms**였습니다. 바쁠 때 열 배 느려져도 140ms입니다. 그러니 2초는 이미 넉넉합니다.

| 원칙 | 설명 |
|---|---|
| 정상 응답 시간을 먼저 잰다 | 보통은 상위 1% 느린 요청(p99) 시간의 몇 배 |
| 부르는 쪽이 부르는 쪽보다 짧게 | 사용자 ← nginx(60초) ← order-api ← catalog-api(2초). **안쪽일수록 짧게** |
| 모든 호출에 타임아웃 | 라이브러리 기본값이 "무한 대기"인 경우가 많다 |

!!! warn "기본값을 믿지 마라"
    파이썬 `urllib.request.urlopen`은 `timeout`을 주지 않으면 **끝없이** 기다립니다. 많은 HTTP · DB 라이브러리가 그렇습니다. 오늘 코드의 `timeout=CATALOG_TIMEOUT`, `connect_timeout=3`, `socket_timeout=10`은 모두 그 기본값을 막으려고 넣은 것입니다. 코드 리뷰에서 "이 호출에 타임아웃이 있나요?"는 가장 가치 있는 질문 중 하나입니다.

## 재시도 — 한 번 더 해 볼까

네트워크는 잠깐씩 실패합니다. 상대가 재시작하는 몇 초, 패킷 하나가 사라지는 순간 같은 것입니다. 이럴 땐 **조금 기다렸다 다시** 하면 성공합니다. 오늘 받은 order-api에는 `CATALOG_RETRIES` 설정이 생겼습니다.

```python
for attempt in range(CATALOG_RETRIES + 1):
    try:
        with urllib.request.urlopen(req, timeout=CATALOG_TIMEOUT) as res:
            return res.status, json.load(res)
    except urllib.error.HTTPError as e:
        return e.code, {}          # 404 같은 답은 다시 물어도 같다 → 재시도하지 않는다
    except Exception as e:         # 이름을 못 찾음, 연결 거부, 타임아웃 …
        log("catalog_error", request_id=request_id, attempt=attempt + 1, error=str(e))
        if attempt < CATALOG_RETRIES:
            time.sleep(0.2 * (2 ** attempt))   # 0.2 → 0.4 → 0.8 → 1.6초
```

- 다시 하기 전에 기다리는 시간을 **두 배씩** 늘립니다. 이것을 **지수 백오프(exponential backoff)**라고 합니다. 상대가 막 회복하는 중에 한꺼번에 몰려가 다시 쓰러뜨리지 않기 위해서입니다.
- **404 같은 "답"은 재시도하지 않습니다.** 없는 상품은 백 번 물어도 없습니다. 재시도는 **네트워크 문제**일 때만 합니다.

## 실습 3 · 재시도가 살리는 경우

!!! lab "실습 목표"
    catalog-api가 **잠깐 재시작하는** 동안 주문을 넣어, 재시도가 주문을 살리는 것을 봅니다.

`compose.yaml`의 `order-api` → `environment`에 한 줄을 추가합니다.

```yaml
      CATALOG_RETRIES: "4"
```

```bash
docker compose up -d order-api
sleep 3
docker compose stop catalog-api
curl -s -w '  (HTTP %{http_code}, %{time_total}초)\n' -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 2}' > /tmp/order.txt &
sleep 0.5
docker compose start catalog-api
sleep 5
cat /tmp/order.txt
docker compose logs order-api --no-log-prefix --tail 6
```

!!! check "이렇게 나오면 성공"
    ```text
    {"order_id":11,"request_id":"965fd02c…","status":"pending","total_price":45000}  (HTTP 202, 1.72초)
    {"service": "order-api", "event": "order_received", …}
    {"service": "order-api", "event": "catalog_error", …, "attempt": 1, "error": "…Name or service not known>"}
    {"service": "order-api", "event": "catalog_error", …, "attempt": 2, "error": "…Name or service not known>"}
    {"service": "order-api", "event": "catalog_error", …, "attempt": 3, "error": "…Name or service not known>"}
    {"service": "order-api", "event": "order_saved", …}
    ```
    세 번 실패했지만 네 번째에 catalog-api가 돌아와 **주문이 성공**했습니다. 사용자는 1.7초 기다렸을 뿐, 장애를 몰랐습니다.

## 실습 4 · 재시도가 해치는 경우

같은 설정(재시도 4번, 타임아웃 2초)으로 catalog-api를 **얼립니다.**

```bash
docker compose pause catalog-api
curl -s -w '  (HTTP %{http_code}, %{time_total}초)\n' -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 2}'
docker compose unpause catalog-api
```

!!! check "보이는 것"
    ```text
    {"error":"catalog unavailable","request_id":"dbee1d16…"}  (HTTP 503, 13.01초)
    ```
    재시도 없이는 2초에 끝날 실패가 **13초**로 늘었습니다. 2초 × 5번 + 기다림 3초. 그동안 order-api의 일꾼은 13초 동안 묶여 있고, 1교시의 장애 전파가 **6배** 심해집니다.

| 장애 종류 | 재시도 효과 | 예 |
|---|---|---|
| 잠깐 (수백 ms ~ 몇 초) | **살린다** | 재시작, 배포 중 교체, 순간적인 네트워크 끊김 |
| 길게 (분 단위) | **해친다** — 기다림 × 횟수, 상대에게 부하 × 횟수 | 과부하, DB 잠금, 멈춘 서비스 |

!!! warn "재시도 폭풍"
    서비스가 층층이 있고 **층마다 3번씩 재시도**하면 어떻게 될까요? 맨 아래 서비스가 느려질 때, 위에서 내려오는 요청은 3 × 3 × 3 = **27배**가 됩니다. 이미 과부하로 느린 서비스에 27배의 요청이 쏟아져 회복할 기회를 빼앗습니다. 그래서 실무에서는 ① 재시도는 **한 층에서만** ② 전체 시도 수에 **예산**(예: 전체 요청의 10%까지만 재시도) ③ 계속 실패하면 **아예 부르지 않는** 서킷 브레이커를 함께 씁니다. 4주차 Istio가 이것을 설정 몇 줄로 해 줍니다.

!!! warn "재시도하면 안 되는 요청"
    "가격 조회"는 열 번 해도 결과가 같습니다. 그런데 "결제하기"를 재시도하면? 첫 요청이 실제로는 성공했는데 **응답만** 늦게 와서 타임아웃이 났다면, 재시도는 **두 번 결제**를 만듭니다. 여러 번 해도 결과가 같은 요청을 **멱등(idempotent)**하다고 합니다. 멱등하지 않은 요청을 재시도하려면 요청마다 고유 키를 붙여 "이미 처리한 키면 무시"하게 만들어야 합니다(3교시).

실험이 끝나면 되돌립니다.

```bash
git restore compose.yaml
docker compose up -d order-api
```

## 헬스 체크와 재시작 정책

어제 order-api에 `/health`와 `/ready`를 봤습니다. 지금까지는 사람이 `curl`로 물어봤는데, 이것을 **Docker가 자동으로** 묻게 합니다. 그리고 컨테이너가 죽으면 **자동으로 다시 띄우게** 합니다.

`compose.yaml`의 `order-api`와 `order-worker`에 다음을 추가합니다.

```yaml
  order-api:
    build: ./order-api
    image: devmart/order-api:1.0.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/ready', timeout=5)"]
      interval: 5s
      timeout: 6s
      retries: 3
    environment:
      …

  order-worker:
    build: ./order-worker
    image: devmart/order-worker:1.0.0
    restart: unless-stopped
    environment:
      …
```

| 설정 | 뜻 |
|---|---|
| `restart: unless-stopped` | 컨테이너가 **스스로 죽으면** 다시 띄운다. 사람이 `stop`한 것은 그대로 둔다 |
| `healthcheck.test` | 컨테이너 **안에서** 실행할 검사 명령. 0으로 끝나면 건강 |
| `interval: 5s` | 5초마다 검사 |
| `retries: 3` | 3번 연속 실패해야 `unhealthy` |

파이썬 이미지에는 `curl`이 없어서 파이썬으로 HTTP를 부릅니다. `urlopen`은 200이 아니면 오류를 내고 종료 코드 1로 끝납니다.

```bash
docker compose up -d order-api order-worker
sleep 10
docker compose ps --format 'table {{.Service}}\t{{.Status}}'
```

!!! check "이렇게 나오면 성공"
    ```text
    order-api      Up 10 seconds (healthy)
    order-worker   Up 10 seconds
    ```

## 실습 5 · 살아 있지만 준비되지 않은 상태

```bash
docker compose stop redis
sleep 25
docker compose ps order-api --format '{{.Status}}'
docker compose exec order-api python -c \
  "import urllib.request as u; print(u.urlopen('http://localhost:8000/health').read())"
curl -s -w '  (HTTP %{http_code})\n' -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 2}'
docker compose start redis
```

!!! check "보이는 것"
    ```text
    Up 37 seconds (unhealthy)
    b'{"status":"ok"}\n'
    {"error":"queue unavailable","order_id":12,"request_id":"62383be6…"}  (HTTP 503)
    ```
    order-api는 **살아 있고**(`/health` 정상) **준비되지 않았습니다**(`/ready` 실패 → `unhealthy`). 큐가 없으니 주문을 끝까지 처리할 수 없기 때문입니다. redis를 다시 켜면 10초쯤 뒤 `healthy`로 돌아옵니다.

    그런데 이 실패한 주문 `order_id: 12`를 기억해 두세요. 3교시에 다시 만납니다.

!!! key "살아 있음(liveness)과 준비됨(readiness)"
    | | `/health` — 살아 있나 | `/ready` — 일할 준비가 됐나 |
    |---|---|---|
    | 보는 것 | 이 프로세스만 | DB · 큐 같은 의존 대상까지 |
    | 실패하면 할 일 | **다시 시작** (고장 난 프로세스) | **손님을 보내지 않기** (다시 시작해도 소용없다) |
    | redis가 죽었을 때 | 성공 — 재시작하면 안 된다 | 실패 — 잠시 빼 둔다 |

    Docker Compose는 `unhealthy`를 표시만 하고 다른 일은 하지 않습니다. **Kubernetes는 둘을 구분해서 행동합니다.** liveness가 실패하면 컨테이너를 재시작하고, readiness가 실패하면 그 Pod에 요청을 보내지 않습니다(3주차 5일차). 만약 `/ready`를 liveness로 쓰면, redis 장애 때 모든 order-api가 **계속 재시작**되는 2차 사고가 납니다.

## 실습 6 · 크래시 루프

재시작 정책이 실제로 다시 띄우는지 봅니다. 처리기가 **시작하자마자 죽도록** 설정을 망가뜨립니다. `order-worker` → `WORK_SECONDS: "abc"`(숫자가 아님)로 바꾸고:

```bash
docker compose up -d order-worker
sleep 12
docker compose ps -a order-worker --format '{{.Service}} {{.Status}}'
docker inspect devmart-msa-order-worker-1 --format '재시작 횟수: {{.RestartCount}}'
docker compose logs order-worker --no-log-prefix --tail 2
```

!!! check "보이는 것"
    ```text
    order-worker Restarting (1) 3 seconds ago
    재시작 횟수: 7
    ValueError: could not convert string to float: 'abc'
    ```
    죽고 → 다시 띄우고 → 또 죽고를 반복합니다. 이것을 **크래시 루프(crash loop)**라고 합니다. Docker는 다시 띄우는 간격을 점점 늘립니다. 재시작 정책은 **우연한 죽음**에서는 서비스를 살리지만, **설정이나 코드가 틀린 경우**에는 아무리 다시 띄워도 소용없습니다. 로그의 마지막 줄이 진짜 원인을 알려 줍니다. 3주차 4일차 Kubernetes에서 같은 상태를 `CrashLoopBackOff`라는 이름으로 다시 만납니다.

```bash
git restore compose.yaml
docker compose up -d order-worker
```

헬스 체크와 재시작 정책은 앞으로도 쓸 것이므로 **다시 넣고 커밋**합니다(강의 저장소의 `labs/week3/day2/compose.yaml`이 완성본입니다).

```bash
# compose.yaml에 restart · healthcheck를 다시 넣은 뒤
docker compose config --quiet && docker compose up -d
cd ~/devops-lab && git add devmart-msa/compose.yaml && git commit -m "헬스 체크와 재시작 정책" && git push
```

!!! academic "학술 노트 — 지수 백오프의 기원, 이더넷 (Metcalfe & Boggs, 1976)"
    지수 백오프는 인터넷보다 오래된 아이디어입니다. 1976년 제록스 PARC의 로버트 메트칼프(Robert Metcalfe)와 데이비드 보그스(David Boggs)는 *Communications of the ACM*에 이더넷 논문을 발표했습니다. 이더넷은 여러 컴퓨터가 한 전선을 나눠 쓰기 때문에, 두 컴퓨터가 동시에 보내면 신호가 **충돌**합니다. 해법은 충돌하면 **무작위 시간**만큼 기다렸다 다시 보내되, 또 충돌하면 기다림의 범위를 **두 배로** 넓히는 것이었습니다(이진 지수 백오프).

    "모두가 같은 순간에 다시 시도하면 또 충돌한다"는 통찰은 오늘의 재시도에도 그대로 적용됩니다. 그래서 실무 코드에서는 기다림에 **무작위 흔들림(jitter)**을 더합니다. AWS 아키텍처 블로그의 글 「Exponential Backoff And Jitter」(Brooker, 2015)는 흔들림을 넣었을 때 재시도 요청이 고르게 퍼져 전체 작업이 훨씬 빨리 끝난다는 것을 시뮬레이션으로 보여 주었습니다. 오늘 코드는 단순하게 흔들림을 넣지 않았습니다. 여러분이라면 어디에 `random.uniform()`을 넣을까요?

    - Metcalfe, R. M., & Boggs, D. R. (1976). Ethernet: Distributed packet switching for local computer networks. *CACM, 19*(7).
    - Brooker, M. (2015). *Exponential Backoff And Jitter*. AWS Architecture Blog.

!!! trend "트렌드 — 재시도는 코드 밖으로"
    오늘은 재시도를 파이썬 코드에 직접 썼습니다. 서비스가 수십 개이고 언어가 제각각이면, 서비스마다 타임아웃 · 재시도 · 서킷 브레이커를 똑같이 구현하기 어렵습니다. 그래서 이런 **통신 정책을 코드 밖의 인프라 계층으로 옮기는** 흐름이 자리 잡았습니다. 4주차에 배울 Istio 같은 서비스 메시는 서비스 옆에 붙은 프록시가 "이 서비스 호출은 타임아웃 2초, 재시도 2번, 연속 5번 실패하면 30초 동안 차단"을 설정 파일 몇 줄로 대신해 줍니다. 개발자는 업무 코드에 집중하고, 통신 정책은 플랫폼 팀이 한곳에서 관리합니다.

## 정리

- 타임아웃은 **정상 응답 시간**을 기준으로, **안쪽 호출일수록 짧게**. 기본값(무한 대기)을 믿지 않는다.
- 재시도는 **잠깐의 장애는 살리고, 긴 장애는 키운다.** 지수 백오프 + 흔들림, 한 층에서만, 예산 안에서.
- 404 같은 답과 **멱등하지 않은 요청**(결제)은 그냥 재시도하지 않는다.
- `restart: unless-stopped` — 우연한 죽음은 살리지만, 틀린 설정은 **크래시 루프**.
- `/health`(살아 있나 → 재시작) vs `/ready`(준비됐나 → 손님 안 보내기). 섞으면 2차 사고.

!!! quiz "확인 문제"
    1. catalog-api 호출의 타임아웃을 2초로 정한 근거는?
    2. 재시도 4번이 실습 3에서는 도움이 되고 실습 4에서는 해가 된 이유는?
    3. 층마다 3번씩 재시도하는 서비스가 3층이면, 맨 아래에는 최대 몇 배의 요청이 가나요?
    4. 결제 요청을 그냥 재시도하면 생길 수 있는 문제는?
    5. redis가 죽었을 때 order-api를 재시작하면 안 되는 이유는?

    ??? answer "정답"
        1. 정상 응답이 약 14ms라 바쁠 때 열 배 느려져도 넉넉하고, 안쪽 호출이라 바깥(nginx 60초)보다 훨씬 짧아야 하기 때문
        2. 실습 3은 잠깐의 재시작이라 다시 시도하면 성공했고, 실습 4는 계속 멈춘 상태라 기다림만 13초로 늘었다
        3. 27배 (3 × 3 × 3)
        4. 첫 요청이 실제로 성공했는데 응답만 늦었다면 두 번 결제된다 (멱등하지 않음)
        5. order-api 자체는 멀쩡하고 문제는 redis라서, 다시 시작해도 해결되지 않고 재시작만 반복된다. 손님을 보내지 않는 것(readiness)이 맞다

## 참고 문헌

- Brooker, M. (2015). *Exponential Backoff And Jitter*. AWS Architecture Blog.
- Metcalfe, R. M., & Boggs, D. R. (1976). Ethernet. *Communications of the ACM, 19*(7).
- Google SRE Book (2016), Ch. 22 "Addressing Cascading Failures". sre.google
- Docker Docs. *Compose file reference — restart, healthcheck*. docs.docker.com/reference/compose-file/services
- Kubernetes Docs. *Configure Liveness, Readiness and Startup Probes*. kubernetes.io
