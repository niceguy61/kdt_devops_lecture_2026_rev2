[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [1일차](README.md)

# 4교시 · 여섯 서비스 실행하기

> [!NOTE]
> **이번 시간에 할 일**
>
> - 실습 파일을 받아 내 저장소에 넣습니다.
> - 실행하기 전에 **성공 기준**을 먼저 적습니다.
> - `docker compose up` 한 줄로 여섯 서비스를 띄웁니다.
> - 상태 · 헬스 · 화면 · 로그로 **정상 기준선(baseline)**을 기록합니다.

## 실습 파일 받기

오늘부터는 서비스가 많아 파일을 하나씩 손으로 만들지 않고, 강의 저장소에서 복사합니다. 2주차에 손으로 만든 `catalog-api`가 조금 자라서 2.0.0이 되었고, `order-api` · `order-worker`가 새로 생겼습니다.

```bash
cd ~
git clone https://github.com/niceguy61/kdt_devops_lecture_2026_rev2.git course
cp -r ~/course/labs/week3/devmart-msa ~/devops-lab/
cd ~/devops-lab/devmart-msa
ls
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> catalog-api  compose.yaml  db  nginx  order-api  order-worker  web
> ```
> `ls -a`로 보면 `.env.example`, `.gitignore`도 있습니다.

```bash
cp .env.example .env
code .env          # DB_PASSWORD=아무-실습용-값 으로 바꾸기
```

> [!TIP]
> **먼저 읽고 실행한다**
>
> 남이 만든 `compose.yaml`이나 스크립트를 받으면 **실행하기 전에 읽습니다.** 3교시에 표를 채운 것이 바로 그 과정입니다. 무엇을 띄우는지, 어떤 포트를 여는지, 어떤 볼륨을 만드는지 모른 채 실행하는 것은 1주차 1일차 AI 검증 4단계의 "안전 확인"을 건너뛰는 것과 같습니다.

## 실행 전에 성공 기준부터

장애를 찾으려면 **정상이 어떤 모습인지** 먼저 알아야 합니다. 실행하기 전에 "이렇게 되면 성공"을 적어 둡니다. `notes/week3-day1.md`에 추가합니다.

```markdown
## 성공 기준 (실행 전에 적기)
- [ ] docker compose ps 에 6개 서비스가 모두 Up, db는 (healthy)
- [ ] http://localhost:8080 에 상품 5개
- [ ] 주문하기 → 주문 표에 pending → 1~2초 뒤 completed
- [ ] order-api /ready 가 {"status":"ready"}
- [ ] 각 서비스 로그에 error 없음
```

## 실습 3 · 한 줄로 띄우기

### 단계 1 — 2주차 DevMart 내리기

8080 포트를 두고 다투지 않도록 2주차 것을 내립니다.

```bash
cd ~/devops-lab/devmart && docker compose down
cd ~/devops-lab/devmart-msa
```

### 단계 2 — 문법 검사와 실행

```bash
docker compose config --quiet && echo "문법 OK"
docker compose up -d --build
```

> **🟢 확인: 이렇게 나오면 성공 (순서를 읽어 보세요)**
>
> ```text
>  ✔ Network devmart-msa_default        Created
>  ✔ Volume devmart-msa_db-data         Created
>  ✔ Container devmart-msa-db-1         Healthy
>  ✔ Container devmart-msa-redis-1      Started
>  ✔ Container devmart-msa-catalog-api-1  Started
>  ✔ Container devmart-msa-order-worker-1 Started
>  ✔ Container devmart-msa-order-api-1  Started
>  ✔ Container devmart-msa-web-1        Started
> ```
> 처음에는 이미지 세 개(`catalog-api`, `order-api`, `order-worker`)를 빌드하느라 1~2분 걸립니다. `db`가 `Healthy`가 된 **뒤에** 세 파이썬 서비스가 시작되고, `web`이 마지막입니다. 2주차 5일차의 `depends_on`이 그대로 일합니다.

### 단계 3 — 상태 확인

```bash
docker compose ps --format 'table {{.Service}}\t{{.Status}}\t{{.Ports}}'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> SERVICE        STATUS                   PORTS
> catalog-api    Up 30 seconds            8000/tcp
> db             Up 36 seconds (healthy)  5432/tcp
> order-api      Up 30 seconds            8000/tcp
> order-worker   Up 30 seconds
> redis          Up 36 seconds            6379/tcp
> web            Up 29 seconds            0.0.0.0:8080->80/tcp
> ```
> 3교시 표와 비교하세요. 바깥 공개는 `web`의 8080 하나, `order-worker`는 포트 칸이 비어 있습니다.

### 단계 4 — 화면에서 주문하기

브라우저에서 **http://localhost:8080** 을 엽니다.

> **🟢 확인: 이렇게 보이면 성공**
>
> - 위쪽 **상품** 영역: 카드 5개, 각 카드에 가격 · 재고 · **주문하기** 버튼
> - 아래쪽 **최근 주문** 표: 처음엔 비어 있음
> - 에코백의 **주문하기**를 누르면 표에 한 줄이 생기고, 상태가 주황색 **pending** → 1~2초 뒤 초록색 **completed**로 바뀝니다
>
> 화면은 2초마다 주문 목록을 다시 읽습니다. pending이 completed로 바뀌는 그 1~2초가 6교시의 주인공 — **큐를 거친 비동기 처리**입니다.

### 단계 5 — 명령줄로도 확인

```bash
curl -s http://localhost:8080/api/products | head -c 120; echo
curl -s -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 4, "quantity": 2}'; echo
sleep 2
curl -s http://localhost:8080/api/orders | head -c 200; echo
```

- `-X POST` : 읽기(GET)가 아니라 **새로 만들기(POST)** 요청
- `-H 'Content-Type: application/json'` : 보내는 내용이 JSON이라고 알린다
- `-d '{…}'` : 보낼 내용 (텀블러 2개)

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> {"items":[{"id":1,"name":"러닝화","price":59000,"stock":12},{"id":2,"name":"후드 집업",…
> {"order_id":2,"request_id":"d8f441e3c393d60b7f53f5c0949c544b","status":"pending","total_price":36000}
> {"hostname":"ef152e5f5ba0","items":[{"id":2,"product_name":"텀블러","quantity":2,"request_id":"d8f4…","status":"completed",…
> ```
> 주문 응답은 **`pending`**인데, 2초 뒤 목록에서는 **`completed`**입니다. 그리고 응답마다 `request_id`라는 긴 번호가 붙어 있습니다.

### 단계 6 — 준비 상태(readiness) 확인

`order-api`에는 헬스 주소가 둘 있습니다. 바깥에 열려 있지 않으므로 컨테이너 **안에서** 확인합니다.

```bash
docker compose exec order-api python -c \
  "import urllib.request as u; print(u.urlopen('http://localhost:8000/health').read()); print(u.urlopen('http://localhost:8000/ready').read())"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> b'{"status":"ok"}\n'
> b'{"checks":{"db":"ok","queue":"ok"},"status":"ready"}\n'
> ```

| 주소 | 묻는 것 | 확인 범위 |
|---|---|---|
| `/health` | **살아 있나?** | 이 프로세스만 |
| `/ready` | **일할 준비가 됐나?** | DB와 큐까지 |

둘을 나누는 이유는 2일차와 3주차 Kubernetes의 **liveness / readiness probe**에서 자세히 봅니다. 지금은 "살아 있는 것"과 "일할 수 있는 것"이 다르다는 것만 기억합니다. 2주차 4일차 5교시 트렌드에서 미리 말한 그 차이입니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 확인 |
> |---|---|
> | `Bind for 0.0.0.0:8080 failed: port is already allocated` | 2주차 DevMart가 떠 있다 → 그 폴더에서 `docker compose down` |
> | `required variable DB_PASSWORD is missing a value` | `.env`가 없다 → `cp .env.example .env` |
> | 빌드 중 `pip install` 오류 | 강의실 네트워크 확인 후 `docker compose build --no-cache 서비스` |
> | 화면에 상품은 나오는데 주문 표가 빨간 글씨 | `docker compose logs order-api` — 7교시 진단 순서 |
> | 주문이 계속 pending | `docker compose logs order-worker` — 7교시 장애 3 |

## 정상 기준선 기록하기

정상일 때의 모습을 **증거로 남겨 두면**, 나중에 이상할 때 비교할 수 있습니다. 이것을 **기준선(baseline)**이라고 합니다.

```bash
mkdir -p ~/devops-lab/notes
docker compose ps > ~/devops-lab/notes/baseline-ps.txt
docker compose logs --tail 5 > ~/devops-lab/notes/baseline-logs.txt
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' > ~/devops-lab/notes/baseline-stats.txt
cat ~/devops-lab/notes/baseline-stats.txt
```

> **🟢 확인: 보이는 것 (숫자는 사람마다 다르다)**
>
> ```text
> NAME                         CPU %     MEM USAGE / LIMIT
> devmart-msa-web-1            0.00%     5.1MiB / 7.6GiB
> devmart-msa-order-api-1      0.02%     38MiB / 7.6GiB
> devmart-msa-order-worker-1   0.01%     21MiB / 7.6GiB
> devmart-msa-catalog-api-1    0.02%     37MiB / 7.6GiB
> devmart-msa-redis-1          0.31%     4.2MiB / 7.6GiB
> devmart-msa-db-1             0.00%     30MiB / 7.6GiB
> ```
> 여섯 서비스가 합쳐 150MB 남짓 씁니다. 2주차의 세 서비스보다 두 배쯤입니다. 서비스 수만큼 **기본으로 드는 자원**이 늘어나는 것이 MSA의 비용 중 하나입니다.

이 파일들은 `~/devops-lab/notes/`에 두고 커밋합니다. `.env`는 `.gitignore`가 막아 줍니다.

```bash
cd ~/devops-lab
git add devmart-msa notes
git status --short | grep -c env        # .env.example 1개만 나와야 한다
git commit -m "3주차 1일차: DevMart MSA 실행과 기준선"
git push
```

> **🎓 학술 노트 — 기준선이 있어야 '이상'을 말할 수 있다**
>
> 통계적 공정 관리의 아버지 월터 슈하트(Walter A. Shewhart)는 1931년 『제조 제품 품질의 경제적 관리』에서 **관리도(control chart)**를 제안했습니다. 공정을 한동안 지켜보며 **평소의 흔들림 범위**를 먼저 재고, 그 범위를 벗어날 때만 "특별한 원인이 있다"고 판단하자는 것입니다. 평소의 흔들림을 모르면 모든 변화가 장애처럼 보이거나, 반대로 진짜 장애를 "원래 그래"라고 넘기게 됩니다.
>
> 현대 운영 모니터링도 같은 생각 위에 서 있습니다. 4주차 Prometheus에서 "평소 응답 시간의 99번째 백분위수"를 재고, 그보다 나빠질 때 경보를 울리는 것이 관리도의 직계 후손입니다. 오늘 `baseline-*.txt`는 그 출발점입니다.
>
> - Shewhart, W. A. (1931). *Economic Control of Quality of Manufactured Product*. Van Nostrand.

> **📈 트렌드 — 노트북 위의 MSA를 더 가볍게**
>
> 서비스가 수십 개인 회사에서는 개발자 노트북에 모든 서비스를 띄울 수 없습니다. 그래서 **내가 고치는 서비스 하나만 노트북에서 돌리고, 나머지는 공용 개발 클러스터의 것을 빌려 쓰는** 도구들(Telepresence, mirrord 같은 것)이나, 필요한 의존 서비스만 테스트 중에 잠깐 띄우는 Testcontainers(2주차 4일차)가 널리 쓰입니다. 공통된 고민은 **"개발 환경과 운영 환경을 얼마나 비슷하게 유지할 것인가"** — 12-Factor의 X번 원칙(개발/운영 일치)입니다.

## 정리

- 실행 전에 **읽고**, **성공 기준**을 적는다.
- `docker compose up -d --build` — db(healthy) → 파이썬 서비스 셋 → web.
- 성공 = 6개 Up, 상품 5개, 주문이 pending → completed, `/ready` 정상.
- `/health`는 살아 있나, `/ready`는 일할 준비가 됐나.
- **기준선**(ps · logs · stats)을 남겨야 나중에 "이상하다"를 말할 수 있다.

> **✅ 확인 문제**
>
> 1. 실행하기 전에 성공 기준을 적는 이유는?
> 2. 주문 응답은 `pending`인데 2초 뒤 목록은 `completed`인 이유는?
> 3. `/health`와 `/ready`의 차이는?
> 4. `order-api`의 `/ready`를 노트북에서 `curl localhost:8000/ready`로 확인할 수 없는 이유는?
> 5. 기준선으로 남긴 세 가지는?
>
> <details><summary>정답</summary>
>
> 1. 정상이 어떤 모습인지 알아야 이상을 알아챌 수 있기 때문
> 2. order-api는 저장과 큐 넣기까지만 하고 바로 답하고, 실제 처리는 order-worker가 나중에 하기 때문 (비동기)
> 3. /health는 프로세스가 살아 있는지, /ready는 DB와 큐까지 확인해 일할 준비가 됐는지
> 4. order-api는 바깥에 포트를 열지 않았다 (ports 없음). 컨테이너 안에서 확인한다
> 5. `docker compose ps`, 최근 로그, `docker stats` (상태 · 로그 · 자원)
>
> </details>

## 참고 문헌

- Docker Docs. *docker compose up / ps / exec / stats*. docs.docker.com/reference/cli/docker/compose
- Shewhart, W. A. (1931). *Economic Control of Quality of Manufactured Product*.
- Wiggins, A. (2011). *The Twelve-Factor App — X. Dev/prod parity*. 12factor.net

---

⬅️ 이전: [3교시 · DevMart MSA 구조 읽기](lesson-03.md) &nbsp;|&nbsp; [⬆️ 1일차 목차](README.md) &nbsp;|&nbsp; 다음: [5교시 · 요청 ID로 통신 추적하기](lesson-05.md) ➡️
