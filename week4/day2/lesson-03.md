<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [2일차](README.md) › 3/7교시</sub>

# 3교시 · 타깃과 PromQL

> [!NOTE]
> **이번 시간에 할 일**
>
> - Prometheus 화면에서 **무엇을 긁어 가고 있는지**(target) 확인합니다.
> - **PodMonitor**로 Envoy 프록시의 지표를 수집 대상에 더합니다.
> - 지표 원본(텍스트)을 직접 보고, **카운터 · 게이지 · 히스토그램**을 구분합니다.
> - **PromQL**로 DevMart의 R · E · D를 한 단계씩 계산합니다.

## 실습 3 · Prometheus 화면

```bash
kubectl port-forward -n monitoring service/kps-prometheus 9090:9090
```

브라우저에서 **http://localhost:9090** → 위쪽 메뉴 **Status → Target health**.

> **🟢 확인: 보이는 것 (줄여서)**
>
> | 대상 (job) | 상태 | 개수 |
> |---|---|---|
> | serviceMonitor/monitoring/kps-kubelet/… | **UP** | 노드 3 × 몇 개 |
> | serviceMonitor/monitoring/kps-prometheus-node-exporter/0 | **UP** | 3 |
> | serviceMonitor/monitoring/kps-kube-state-metrics/0 | **UP** | 1 |
> | serviceMonitor/monitoring/kps-apiserver/0 | **UP** | 1 |
> | serviceMonitor/monitoring/kps-coredns/0 | **UP** | 2 |
> | … (Prometheus · Alertmanager · Grafana · 운영자 자신) | **UP** | |
>
> 2교시에 끈 컨트롤러 매니저 · 스케줄러 · etcd는 **목록에 없습니다.** 모두 UP이어야 합니다. Envoy는 아직 없습니다.

> **📖 용어 — 타깃과 긁기(scrape)**
>
> **타깃**은 Prometheus가 지표를 가져가는 주소 하나입니다(대부분 `http://Pod-IP:포트/metrics`). 정해진 주기(오늘은 15초)마다 그 주소에 HTTP GET을 보내 **지금의 숫자들**을 받아 저장합니다. 앱이 Prometheus에 보내는 것이 아니라 Prometheus가 **가져가는**(pull) 방식이라, 앱이 죽으면 "가져가기 실패 = DOWN"으로 바로 드러납니다. `up` 지표(1이면 성공, 0이면 실패)가 모든 타깃에 자동으로 생깁니다.

## 실습 4 · Envoy 지표 더하기

### 단계 1 — 원본 보기

Prometheus가 무엇을 받아 가는지, 먼저 직접 봅니다.

```bash
# 다른 터미널 — 요청 몇 개 만들기
for i in $(seq 1 30); do curl -s -o /dev/null localhost:30080/api/products; done

ENVOY=$(kubectl get pod -n envoy-gateway-system -l app.kubernetes.io/component=proxy -o name | head -1)
kubectl port-forward -n envoy-gateway-system $ENVOY 19001:19001 &
sleep 2
curl -s localhost:19001/stats/prometheus | grep -E '^envoy_cluster_upstream_rq_(total|xx)\{' | grep 'httproute/devmart' | head -6
kill %1
```

- `19001` : Envoy Gateway가 Envoy의 **지표 포트**로 쓰는 번호. 경로는 `/stats/prometheus`

> **🟢 확인: 보이는 것**
>
> ```text
> envoy_cluster_upstream_rq_total{envoy_cluster_name="httproute/devmart/catalog/rule/0"} 1847
> envoy_cluster_upstream_rq_total{envoy_cluster_name="httproute/devmart/orders/rule/0"} 312
> envoy_cluster_upstream_rq_total{envoy_cluster_name="httproute/devmart/web/rule/0"} 96
> envoy_cluster_upstream_rq_xx{envoy_cluster_name="httproute/devmart/catalog/rule/0",envoy_response_code_class="2"} 1839
> envoy_cluster_upstream_rq_xx{envoy_cluster_name="httproute/devmart/catalog/rule/0",envoy_response_code_class="5"} 8
> envoy_cluster_upstream_rq_xx{envoy_cluster_name="httproute/devmart/orders/rule/0",envoy_response_code_class="2"} 310
> ```
> 한 줄 = **이름{라벨들} 숫자**. Envoy는 어제 만든 **HTTPRoute마다** 따로 셉니다 — `httproute/네임스페이스/라우트이름/rule/번호`. 어제 4교시에 서비스마다 라우트를 따로 만든 덕분에, 오늘 서비스마다 숫자가 따로 나옵니다. (`rule/0`의 5xx 8건은 어제 7교시 장애 2의 흔적일 수 있습니다.)

### 단계 2 — PodMonitor

```bash
cat monitoring/envoy-podmonitor.yaml | sed -n '/spec:/,$p'
kubectl apply -f monitoring/envoy-podmonitor.yaml
```

```yaml
spec:
  selector:
    matchLabels:                                    # 이 라벨의 Pod를
      app.kubernetes.io/component: proxy
      app.kubernetes.io/managed-by: envoy-gateway
  podMetricsEndpoints:
    - port: metrics                                 # 이 이름의 포트에서
      path: /stats/prometheus                       # 이 경로로 긁어라
      interval: 15s
```

30초쯤 뒤 Prometheus 화면의 **Target health**를 새로 고칩니다.

> **🟢 확인: 새 줄**
>
> `podMonitor/envoy-gateway-system/envoy-proxy/0` — **UP** (1/1)

| | ServiceMonitor | PodMonitor |
|---|---|---|
| 무엇을 고르나 | **Service**를 라벨로 고르고, 그 뒤의 Pod들을 긁는다 | **Pod**를 라벨로 직접 고른다 |
| 쓰는 곳 | 지표 포트가 Service에 열려 있을 때 (대부분) | Service 없이 Pod에만 있을 때 — 오늘의 Envoy 지표 포트 |

## 지표의 세 가지 모양

| 종류 | 뜻 | 예 | 그대로 보면 |
|---|---|---|---|
| **카운터** (counter) | 계속 **늘기만** 하는 수 (재시작하면 0부터) | `envoy_cluster_upstream_rq_total` · `kube_pod_container_status_restarts_total` | 의미 없다 — **얼마나 빨리 느나**(rate)를 본다 |
| **게이지** (gauge) | 오르내리는 지금 값 | `container_memory_working_set_bytes` · `kube_deployment_status_replicas_available` | 그대로 의미 있다 |
| **히스토그램** (histogram) | 값의 **분포** — "100ms 이하 몇 개, 250ms 이하 몇 개…" 칸(bucket)마다 카운터 | `envoy_cluster_upstream_rq_time_bucket{le="…"}` | 칸들로 **분위수**(p95 등)를 계산한다 |

> **❓ 오해 — 평균 응답 시간이면 충분하다**
>
> 요청 100개 중 99개가 10ms, 1개가 5초면 평균은 약 60ms입니다. "빠르다"고 보이지만 **100명 중 1명은 5초를 기다렸습니다.** 그래서 응답 시간은 **분위수**로 봅니다 — p95(느린 쪽 5%의 경계), p99(1%). 구글 SRE 책과 Dean & Barroso의 *The Tail at Scale*(CACM 2013)이 강조한 '꼬리 지연'입니다. 서비스가 여럿이면 꼬리가 곱해져 더 길어집니다 — 3주차 2일차의 장애 전파와 같은 원리입니다.

## 실습 5 · PromQL 한 단계씩

Prometheus 화면 위쪽 **Query** 탭에서 한 줄씩 입력하고 **Execute** → **Graph** 탭으로 봅니다. 다른 터미널에서 요청을 계속 만들어 둡니다.

```bash
while true; do curl -s -o /dev/null localhost:30080/api/products; curl -s -o /dev/null localhost:30080/api/orders; sleep 0.2; done
```

### 1 — 카운터 그대로

```promql
envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/.*"}
```

- `{…}` : 라벨로 고른다. `=~`는 정규식 일치

> **🟢 확인: 보이는 것**
>
> 세 줄(catalog · orders · web)이 **계단처럼 계속 오르는** 그래프. 카운터 그대로는 "지금 바쁜가"를 알 수 없습니다.

### 2 — 초당 증가량: rate

```promql
rate(envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/.*"}[1m])
```

- `[1m]` : 최근 1분 동안의 값들로
- `rate()` : 초당 평균 증가량 — **초당 요청 수**가 된다. 카운터가 재시작으로 0이 되어도 알아서 이어 준다

> **🟢 확인: 보이는 것**
>
> 평평한 선 — catalog와 orders가 각각 초당 약 4~5. 루프를 멈추면 1분에 걸쳐 0으로 내려갑니다. **R(Rate)**입니다.

### 3 — 묶기: sum by

```promql
sum by (envoy_cluster_name) (rate(envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/.*"}[1m]))
```

- `sum by (라벨)` : 그 라벨이 같은 것끼리 더한다. Envoy Pod가 여러 개여도 라우트별 합계가 된다

### 4 — 오류 비율 (E)

```promql
sum by (envoy_cluster_name) (rate(envoy_cluster_upstream_rq_xx{envoy_response_code_class="5", envoy_cluster_name=~"httproute/devmart/.*"}[1m]))
/
sum by (envoy_cluster_name) (rate(envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/.*"}[1m]))
```

> **🟢 확인: 보이는 것**
>
> 지금은 **결과 없음**이거나 0입니다. 5xx가 없으면 분자 쪽 시계열이 아예 없기 때문입니다. 5교시에 장애를 넣으면 나타납니다.

### 5 — 응답 시간 p95 (D)

```promql
histogram_quantile(0.95,
  sum by (le, envoy_cluster_name) (rate(envoy_cluster_upstream_rq_time_bucket{envoy_cluster_name=~"httproute/devmart/.*"}[1m])))
```

- `le` : 히스토그램 칸의 경계("이하") 라벨 — `by`에 꼭 남겨야 분위수를 계산할 수 있다
- 결과 단위는 Envoy 기준 **밀리초**

> **🟢 확인: 보이는 것**
>
> catalog · orders 모두 수 ms~수십 ms. orders가 조금 더 깁니다 — 주문은 안에서 catalog를 한 번 더 부르고 DB에 쓰기 때문입니다(3주차 1일차).

### 6 — 자원 쪽 (USE)

```promql
sum by (pod) (rate(container_cpu_usage_seconds_total{namespace="devmart", container!=""}[1m]))
```

```promql
kube_deployment_status_replicas_available{namespace="devmart"}
```

- 첫 줄: Pod별 CPU 사용(코어). 3주차 5일차의 requests(catalog-api 50m = 0.05)와 비교해 본다
- 둘째 줄: kube-state-metrics가 만든 **게이지** — Deployment마다 준비된 Pod 수

> **📘 예시 — 질문을 PromQL로**
>
> | 1교시의 질문 | PromQL |
> |---|---|
> | 지금 주문이 초당 몇 건? | `sum(rate(envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/orders/.*"}[1m]))` |
> | 최근 15분에 재시작한 Pod는? | `increase(kube_pod_container_status_restarts_total{namespace="devmart"}[15m]) > 0` |
> | catalog-api가 CPU requests의 몇 배를 쓰나? | `sum(rate(container_cpu_usage_seconds_total{namespace="devmart",pod=~"catalog-api.*"}[5m])) / sum(kube_pod_container_resource_requests{namespace="devmart",pod=~"catalog-api.*",resource="cpu"})` |
>
> "pending 주문 수"는 PromQL로 답할 수 없습니다 — 그런 지표를 아무도 내놓지 않기 때문입니다. 지표는 **누군가 내놓아야** 있습니다. 앱이 직접 `/metrics`를 열거나(계측), DB용 exporter를 붙여야 합니다. 이번 주 Try 후보입니다.

> [!WARNING]
> **라벨에 무엇을 넣으면 안 되나**
>
> 라벨 값 하나하나가 **새 시계열**이 됩니다. 라벨에 요청 ID · 사용자 ID · 주문 번호처럼 **끝없이 늘어나는 값**을 넣으면 시계열이 폭발해 Prometheus가 메모리를 다 먹습니다(카디널리티 폭발). 요청 ID는 **로그와 트레이스**의 몫이고, 메트릭 라벨은 라우트 · 서비스 · 응답 코드처럼 **가짓수가 정해진 값**만 씁니다.

`port-forward`와 요청 루프는 이 교시가 끝나면 Ctrl+C로 멈춥니다.

> **🎓 학술 노트 — 꼬리 지연과 시계열 압축**
>
> - **Dean, J., & Barroso, L. A. (2013). "The Tail at Scale." CACM 56(2).** — 요청 하나가 서버 100대에 퍼져 처리되면, 각 서버가 1% 확률로 느려도 **전체 요청의 63%가 느려집니다**(1 − 0.99¹⁰⁰). 평균이 아니라 p99를 봐야 하는 수학적 이유입니다.
> - **Pelkonen 외 (2015). "Gorilla: A Fast, Scalable, In-Memory Time Series Database." VLDB.** — 페이스북의 시계열 압축 기법(시간 간격과 값의 차이를 비트 단위로 압축)으로, 한 점을 평균 약 1.37바이트에 저장했습니다. Prometheus의 저장 방식이 이 기법을 바탕으로 해서, 15초마다 수십만 시계열을 저장해도 노트북에서 돌아갑니다.

> **📈 트렌드 2026 — 네이티브 히스토그램**
>
> 오늘 본 히스토그램은 칸(bucket) 경계를 **미리 정해** 칸마다 시계열 하나를 씁니다. 칸이 많으면 정확하지만 시계열이 많아지고, 적으면 부정확합니다. Prometheus의 **네이티브 히스토그램**은 칸을 **자동으로, 지수 간격으로** 잡아 하나의 시계열에 담습니다. Prometheus 3 세대에서 안정화가 진행되며 OpenTelemetry의 지수 히스토그램과도 맞물려, 앞으로 "칸을 어떻게 나눌지"를 사람이 고민할 일이 줄어들 것입니다.

> **✅ 확인 문제**
>
> 1. Prometheus가 지표를 가져가는 방식은 push인가 pull인가요? 그 장점 하나는?
> 2. Envoy 지표를 ServiceMonitor가 아니라 PodMonitor로 모은 이유는?
> 3. 카운터를 그대로 그래프로 그리면 왜 쓸모가 적나요? 무엇을 씌우나요?
> 4. `histogram_quantile`을 쓸 때 `sum by`에 `le`를 꼭 남기는 이유는?
> 5. 메트릭 라벨에 요청 ID를 넣으면 안 되는 이유는?
>
> <details><summary>정답</summary>
>
> 1. pull — 앱이 죽으면 '가져가기 실패(up=0)'로 바로 드러난다 / 앱은 주소만 열어 두면 된다
> 2. Envoy의 지표 포트가 Service에 열려 있지 않고 Pod에만 있어서
> 3. 늘기만 하는 누적값이라 '지금 얼마나 바쁜가'를 보여 주지 않는다 → `rate()`로 초당 증가량을 본다
> 4. 분위수는 칸(le)별 분포로 계산하므로, 칸 경계 라벨이 사라지면 계산할 수 없다
> 5. 값이 끝없이 늘어나 시계열이 폭발한다(카디널리티) — 요청 ID는 로그 · 트레이스의 몫
>
> </details>

## 참고 문헌

- Prometheus Docs. *Metric types* · *Querying basics* · *Histograms and summaries*. prometheus.io/docs
- Prometheus Operator. *PodMonitor* · *ServiceMonitor*. prometheus-operator.dev/docs
- Envoy Gateway Docs. *Proxy Metrics*. gateway.envoyproxy.io/docs/tasks/observability
- Dean, J., & Barroso, L. A. (2013). The Tail at Scale. *Communications of the ACM*, 56(2).
- Pelkonen, T. 외 (2015). Gorilla: A Fast, Scalable, In-Memory Time Series Database. *PVLDB*, 8(12).

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [2교시 · kube-prometheus-stack 설치](lesson-02.md) | [⬆️ 2일차 목차](README.md) | [4교시 · Grafana 대시보드](lesson-04.md) ➡️ |
