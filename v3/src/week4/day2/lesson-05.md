# 5교시 · k6 부하 테스트

!!! goal "이번 시간에 할 일"
    - **k6** 스크립트를 읽고, 가상 사용자 · 단계 · 합격 기준(threshold)을 이해합니다.
    - 설치 없이 **컨테이너로** k6를 돌려 DevMart에 부하를 겁니다.
    - 부하 중에 Grafana 대시보드가 어떻게 움직이는지 봅니다.
    - 부하 **도중에** 장애를 넣고, 그래프와 k6 결과에서 같은 사건을 찾아 맞춥니다.

## 왜 부하를 거나

지금 DevMart의 그래프는 거의 0입니다. 손님이 없으니까요. 그래프와 알림이 **진짜 손님이 몰릴 때** 제대로 움직이는지는 손님을 만들어 봐야 압니다. 그리고 "초당 몇 건까지 버티나", "그때 응답 시간은?"은 운영 전에 알아야 할 숫자입니다.

| 종류 | 묻는 것 | 모양 |
|---|---|---|
| **부하 테스트** (load) | 평소 예상 손님에서 괜찮나 | 서서히 올려 유지 — 오늘 |
| 스트레스 테스트 (stress) | 어디서 무너지나 | 계속 올린다 |
| 스파이크 테스트 (spike) | 갑자기 몰리면 | 순간적으로 확 |
| 내구 테스트 (soak) | 오래 돌리면 새는 것이 있나 | 몇 시간 유지 (메모리 누수 — 3주차 5일차) |

## 스크립트 읽기

```bash
cd ~/devops-lab/k8s/w4d2
cat k6/load.js
```

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://host.docker.internal:30080';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // 30초 동안 사용자 0 → 10명
    { duration: '2m', target: 10 },    // 10명 유지
    { duration: '30s', target: 0 },    // 정리
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],     // 실패 1% 미만
    http_req_duration: ['p(95)<500'],   // 느린 쪽 5%도 0.5초 안에
  },
};

export default function () {                 // 가상 사용자 한 명이 반복하는 일
  if (Math.random() < 0.8) {
    const res = http.get(`${BASE}/api/products`, { tags: { name: 'products' } });
    check(res, { '상품 200': (x) => x.status === 200 });
  } else {
    const res = http.post(`${BASE}/api/orders`, JSON.stringify({ product_id: … }), …);
    check(res, { '주문 202': (x) => x.status === 202 });
  }
  sleep(0.5);                                // 사람처럼 잠깐 쉰다
}
```

| 낱말 | 뜻 |
|---|---|
| **VU** (가상 사용자) | `default` 함수를 계속 반복하는 가짜 손님 한 명 |
| `stages` | 시간에 따라 VU 수를 바꾸는 계획 — 3분짜리 |
| `check` | 응답 하나가 기대에 맞나 — 실패해도 테스트는 계속 |
| `thresholds` | 테스트 **전체의 합격 기준** — 어기면 k6가 **실패 코드(99)**로 끝난다. CI에 넣을 수 있다 |
| `__ENV.BASE_URL` | 바깥에서 주는 환경 변수 — 같은 스크립트로 kind와 EKS를 다 친다 |

!!! key "합격 기준을 먼저 쓴다"
    `thresholds`는 "이 정도면 괜찮다"를 **테스트 전에** 숫자로 적은 것입니다. 테스트를 돌린 뒤 결과를 보고 "음, 이 정도면 괜찮네"라고 판단하면, 무엇이든 괜찮아 보입니다. 7교시의 **SLO**가 이 숫자의 출처가 됩니다.

## 실습 10 · 평소의 부하

### 단계 1 — 대시보드 띄우기

4교시의 port-forward(3000)가 살아 있는지 확인하고, Grafana에서 `DevMart — RED + 자원`을 엽니다. 오른쪽 위 시간 범위를 **Last 15 minutes**, 새로 고침을 **10s**로.

### 단계 2 — k6 실행

```bash
docker run --rm -i --add-host=host.docker.internal:host-gateway \
  -e BASE_URL=http://host.docker.internal:30080 \
  grafana/k6:2.3.0 run - < k6/load.js
```

- `--rm -i … run - < 파일` : k6를 설치하지 않고 컨테이너로 돌린다. 스크립트는 표준 입력으로 준다 (2주차 `docker run`)
- `host.docker.internal` : 컨테이너 안에서 **내 노트북**을 가리키는 이름. `--add-host=…:host-gateway`는 Linux에서도 이 이름이 통하게 한다 (Docker Desktop은 원래 된다)

3분 동안 Grafana를 봅니다.

!!! check "Grafana에서 보이는 것"
    - **요청 수**: 30초 동안 오르다가 catalog 초당 약 14, orders 초당 약 3.5에서 평평 → 마지막 30초에 내려간다. 80:20 비율 그대로.
    - **5xx 비율**: 없음(빈 패널).
    - **p95**: catalog 수십 ms, orders는 그보다 조금 길다.
    - **CPU**: catalog-api · order-api Pod가 살짝 오른다. db도.

!!! check "k6 결과 (줄여서, 숫자는 매번 다름)"
    ```text
      █ THRESHOLDS

        http_req_duration
        ✓ 'p(95)<500' p(95)=41.3ms

        http_req_failed
        ✓ 'rate<0.01' rate=0.00%

      █ TOTAL RESULTS

        checks_succeeded...: 100.00% 3127 out of 3127
        ...
        http_req_duration..: avg=17.2ms min=2.4ms med=11.8ms max=263.1ms p(90)=33.9ms p(95)=41.3ms
        http_req_failed....: 0.00%   0 out of 3127
        http_reqs..........: 3127    17.37/s
    ```
    합격 기준 둘 다 ✓. **k6가 잰 p95(41ms)와 Grafana의 p95**를 비교해 보세요. 비슷하지만 같지 않습니다 — k6는 **손님 쪽**에서 네트워크 왕복까지 포함해 재고, Envoy는 **입구에서 뒤쪽까지**만 잽니다. 어느 쪽에서 재느냐에 따라 숫자가 다르다는 것을 기억합니다.

## 실습 11 · 부하 중 장애

이번에는 테스트 **도중에** 상품 서비스를 멈춥니다. 터미널 두 개를 씁니다.

```bash
# 터미널 A — 다시 3분짜리 부하
docker run --rm -i --add-host=host.docker.internal:host-gateway \
  -e BASE_URL=http://host.docker.internal:30080 \
  grafana/k6:2.3.0 run - < k6/load.js
```

```bash
# 터미널 B — 부하가 1분쯤 돌았을 때
date +%T; kubectl scale deployment catalog-api -n devmart --replicas=0
sleep 40
date +%T; kubectl scale deployment catalog-api -n devmart --replicas=2
```

!!! check "Grafana에서 보이는 것"
    - **5xx 비율**: catalog 라우트가 **거의 100%**로 치솟고, orders 라우트도 오른다 — 주문은 안에서 catalog를 부르므로(3주차 2일차 장애 전파).
    - **p95**: orders 라우트가 길어질 수 있다 — order-api가 catalog를 기다리다(타임아웃 2초) 포기하기 때문.
    - **요청 수**: 거의 그대로 — 손님은 계속 온다. 실패할 뿐.
    - 40초 뒤 catalog가 돌아오면 모든 선이 원래대로. 터미널 B에 찍은 **두 시각**과 그래프의 튀는 구간을 맞춰 봅니다.

!!! check "k6 결과"
    ```text
      █ THRESHOLDS

        http_req_duration
        ✓ 'p(95)<500' p(95)=…

        http_req_failed
        ✗ 'rate<0.01' rate=21.4…%

    ...
    ERRO[0180] thresholds on metrics 'http_req_failed' have been crossed
    ```
    실패율 기준을 넘어 ✗ — k6가 **실패 코드**로 끝납니다. 이 테스트를 CI에 넣었다면 배포가 멈췄을 것입니다.

| 같은 사건을 본 곳 | 보이는 모습 |
|---|---|
| k6 (손님) | `http_req_failed` 21% — **얼마나** 실패했나 |
| Grafana (입구) | catalog 5xx 100%, orders 5xx 상승 — **어느 서비스**가, **언제부터 언제까지** |
| `kubectl get events -n devmart` | `Scaled down replica set catalog-api-… to 0` — **왜** (누가 무엇을 바꿨나) |

!!! example "예시 — 증상에서 원인으로"
    그래프만 받았다고 생각해 보세요. "14:32부터 catalog 5xx 100%, orders도 동반 상승" → **catalog가 먼저, orders가 따라** — 의존 방향(3주차 1일차 지도)을 알면 orders는 원인이 아니라 **피해자**라고 판단할 수 있습니다. → catalog의 Pod 수 패널이나 `kubectl get events`로 "누군가 0으로 줄였다"를 찾습니다. 1교시의 **메트릭으로 알아채고 → 좁히고 → 로그 · 이벤트로 원인**의 흐름입니다.

!!! warn "부하 테스트는 아무 데나 하지 않는다"
    부하 테스트는 **허락받은 내 시스템**에만 합니다. 남의 서비스나 공유 환경(회사의 공용 스테이징 등)에 사전 협의 없이 부하를 거는 것은 장애를 만드는 일이고, 외부 서비스라면 공격으로 볼 수 있습니다. 5주차 EKS에서도 **내 계정의 내 클러스터**에만 겁니다.

!!! academic "학술 노트 — 리틀의 법칙"
    대기열 이론의 **리틀의 법칙**(Little, 1961, *Operations Research*): 시스템 안에 머무는 평균 요청 수 L = 도착률 λ × 평균 머무는 시간 W. 오늘 k6: VU 10명이 각자 (응답 ~20ms + 쉼 500ms)마다 요청하니, 초당 요청은 약 10 / 0.52 ≈ **19**. 실제 결과 초당 17.4와 가깝습니다. 반대로 응답 시간 W가 늘면, 같은 도착률에서 시스템 안에 **쌓이는 요청 L이 늘어** 일꾼(gunicorn)이 묶입니다 — 3주차 2일차 1교시 장애 전파를 수식으로 쓴 것입니다.

!!! trend "트렌드 2026 — k6 2.0과 테스트의 자동화"
    k6는 2025년 1.0(TypeScript 지원, 안정성 보장)에 이어 2026년 5월 **2.0**을 냈습니다. 오래된 명령 · 옵션을 정리하고, AI 도우미와 함께 테스트를 쓰고 해석하는 흐름에 맞춘 명령들을 더했습니다. 또한 CI에서 PR마다 짧은 부하 테스트를 돌려 "이 변경이 p95를 몇 ms 늘렸나"를 보는 **성능 회귀 테스트**가 흔해지고 있습니다. 2주차 CI의 테스트 단계에 오늘의 `thresholds`를 그대로 붙일 수 있습니다.

!!! quiz "확인 문제"
    1. k6의 `check`와 `thresholds`의 차이는?
    2. k6가 잰 p95와 Grafana(Envoy)의 p95가 다른 이유는?
    3. catalog-api를 0개로 줄였을 때 orders 라우트의 오류도 늘어난 이유는?
    4. 같은 장애를 k6 · Grafana · events가 각각 어떻게 보여 주었나요?
    5. 리틀의 법칙으로 보면, 응답 시간이 늘 때 시스템 안에서 무슨 일이 생기나요?

    ??? answer "정답"
        1. `check` — 응답 하나의 확인(실패해도 계속), `thresholds` — 테스트 전체의 합격 기준(어기면 실패 코드로 끝)
        2. k6는 손님 쪽에서 네트워크 왕복을 포함해 재고, Envoy는 입구에서 뒤쪽 서비스까지만 잰다
        3. order-api가 주문 처리 중에 catalog-api를 동기로 부르기 때문 (3주차 2일차 장애 전파)
        4. k6 — 실패 비율(얼마나), Grafana — 어느 라우트가 언제부터 언제까지, events — 누가 무엇을 바꿨나(왜)
        5. 같은 도착률이면 머무는 요청 수가 늘어 일꾼이 묶이고, 더 느려지는 악순환이 된다

## 참고 문헌

- Grafana k6 Docs. *Get started* · *Thresholds* · *Test types*. grafana.com/docs/k6
- Grafana Labs (2026-05-12). *k6 2.0 is here*. grafana.com/blog
- Little, J. D. C. (1961). A Proof for the Queuing Formula: L = λW. *Operations Research*, 9(3).
- Envoy Gateway Docs. *Proxy Metrics*. gateway.envoyproxy.io/docs/tasks/observability
