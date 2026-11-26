<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [2일차](README.md) › 8/8교시</sub>

# 8교시 · 로그 모으기 — Loki로 DevMart 로그 검색

> [!NOTE]
> **이번 시간에 할 일**
>
> - 1교시의 세 기둥 중 아직 비어 있는 **로그**를 채웁니다.
> - 로그 저장소 **Loki**와 수집기 **Alloy**를 Helm으로 설치하고, Grafana에 연결합니다.
> - **LogQL**로 DevMart 로그를 고르고(라벨), 걸러 내고(글자), 풀어 보고(JSON), 세어 봅니다(메트릭).
> - 3주차 5일차의 `kubectl logs | grep $RID`를 **서비스 여러 개에 걸쳐 한 번에** 합니다.

> [!IMPORTANT]
> **`kubectl logs`의 세 가지 한계**
>
> ① Pod가 지워지면 그 로그도 사라집니다(3주차의 롤링 업데이트 · OOMKilled 뒤를 떠올려 보세요). ② Pod가 여러 개면 **하나씩** 열어 봐야 합니다. ③ "지난 한 시간 동안 에러가 몇 번?" 같은 **집계**를 못 합니다. 로그를 **클러스터 밖으로(오래 사는 저장소로) 모으는** 이유입니다.

## Loki는 무엇이 다른가

| | 전통적 로그 검색 (Elasticsearch 등) | Loki |
|---|---|---|
| 색인 | 로그 **본문의 모든 단어**를 색인 | **라벨만** 색인 (namespace, app, pod …) |
| 저장 | 색인이 크고 비싸다 | 본문은 압축해 덩어리로 — 싸다 |
| 찾는 법 | 단어로 바로 | 라벨로 **좁힌 뒤** 본문을 훑는다 |
| 닮은 것 | 검색 엔진 | **Prometheus** (같은 라벨, 비슷한 문법) |

> **🧩 비유 — 도서관 서가**
>
> 전통적 방식은 책의 **모든 단어로 찾아보기**를 만들어 두는 도서관입니다. 빠르지만 찾아보기 책이 서가보다 커집니다. Loki는 **서가 번호(라벨)만** 붙여 둡니다. "3층 컴퓨터 서가"까지 가서 책장을 훑어봅니다. 그래서 라벨로 **먼저 좁히는 것**이 Loki를 잘 쓰는 법입니다.

## 실습 15 · Loki와 Alloy 설치

### 단계 1 — values 파일

```bash
cd ~/devops-lab/k8s/w4d2
code monitoring/loki-values.yaml
```

```yaml
# Loki — kind 실습용: 한 Pod(단일 바이너리) + 로컬 디스크
deploymentMode: SingleBinary
loki:
  auth_enabled: false              # 여러 팀이 나눠 쓰지 않는다 (운영은 켠다)
  commonConfig:
    replication_factor: 1
  storage:
    type: filesystem               # 운영은 S3 같은 객체 저장소 (5주차)
  schemaConfig:
    configs:
      - from: "2024-04-01"
        store: tsdb
        object_store: filesystem
        schema: v13
        index: { prefix: loki_index_, period: 24h }
  limits_config:
    retention_period: 48h          # 실습용: 이틀만 보관
singleBinary:
  replicas: 1
  persistence: { size: 2Gi }
  resources:
    requests: { cpu: 50m, memory: 256Mi }
    limits: { memory: 512Mi }
# 단일 바이너리에서는 쓰지 않는 부품들을 끈다
backend: { replicas: 0 }
read: { replicas: 0 }
write: { replicas: 0 }
gateway: { enabled: false }
chunksCache: { enabled: false }
resultsCache: { enabled: false }
lokiCanary: { enabled: false }
test: { enabled: false }
```

```bash
code monitoring/alloy-values.yaml
```

```yaml
# Alloy — devmart 네임스페이스 Pod의 로그를 Loki로 보낸다
controller:
  type: deployment                 # API로 로그를 읽으므로 한 대면 충분 (노드마다 둘 필요 없음)
  replicas: 1
alloy:
  resources:
    requests: { cpu: 20m, memory: 64Mi }
    limits: { memory: 256Mi }
  configMap:
    content: |
      discovery.kubernetes "pods" {
        role = "pod"
        namespaces { names = ["devmart"] }
      }

      discovery.relabel "pods" {
        targets = discovery.kubernetes.pods.targets
        rule { source_labels = ["__meta_kubernetes_namespace"]          target_label = "namespace" }
        rule { source_labels = ["__meta_kubernetes_pod_label_app"]      target_label = "app" }
        rule { source_labels = ["__meta_kubernetes_pod_name"]           target_label = "pod" }
        rule { source_labels = ["__meta_kubernetes_pod_container_name"] target_label = "container" }
      }

      loki.source.kubernetes "pods" {
        targets    = discovery.relabel.pods.output
        forward_to = [loki.write.default.receiver]
      }

      loki.write "default" {
        endpoint { url = "http://loki.monitoring.svc:3100/loki/api/v1/push" }
      }
```

| 블록 | 하는 일 |
|---|---|
| `discovery.kubernetes` | apiserver에 물어 **어떤 Pod가 있나** 찾는다(3주차 3일차 8교시의 list-watch) |
| `discovery.relabel` | Kubernetes가 붙인 메타데이터에서 **라벨 네 개만** 골라 Loki 라벨로 — 라벨이 많을수록 Loki가 느려진다 |
| `loki.source.kubernetes` | 그 Pod들의 로그를 **apiserver를 통해** 읽는다(`kubectl logs -f`와 같은 길) |
| `loki.write` | Loki에 보낸다 |

### 단계 2 — 설치

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update grafana
helm install loki grafana/loki --version 7.7.0 -n monitoring -f monitoring/loki-values.yaml --wait --timeout 5m
helm install alloy grafana/alloy --version 1.16.0 -n monitoring -f monitoring/alloy-values.yaml --wait
kubectl get pods -n monitoring | grep -E "loki|alloy"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> alloy-6b9f…-k2x8p   2/2     Running   0          30s
> loki-0              2/2     Running   0          2m
> ```
> Loki는 데이터를 디스크에 쓰므로 **StatefulSet**(`loki-0`)으로 뜹니다. 3주차 5일차의 DB와 같은 이유입니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인 | 해결 |
> |---|---|---|
> | `loki-0`이 `Pending` | 노드 메모리 부족 | `kubectl describe pod loki-0 -n monitoring`의 Events. k6 Pod 등 남은 것을 지운다 |
> | alloy 로그에 `connection refused … 3100` | Loki가 아직 안 떴다 | 1분 뒤 저절로 다시 보낸다 |
> | alloy 로그에 `forbidden … pods/log` | 로그 읽기 권한 없음 | 차트의 `rbac.create`가 켜져 있는지(기본 켜짐) |

### 단계 3 — Grafana에 데이터 소스 더하기

2교시에 대시보드를 ConfigMap으로 넣었듯이, **데이터 소스도 ConfigMap으로** 넣습니다.

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-datasource
  namespace: monitoring
  labels:
    grafana_datasource: "1"         # Grafana 사이드카가 이 라벨을 찾는다
data:
  loki.yaml: |
    apiVersion: 1
    datasources:
      - name: Loki
        type: loki
        uid: loki
        access: proxy
        url: http://loki.monitoring.svc:3100
EOF
kubectl port-forward -n monitoring service/kps-grafana 3000:80 > /tmp/grafana-pf.log 2>&1 &
```

**http://localhost:3000** → **Connections → Data sources**에 **Loki**가 보이면 성공입니다. 안 보이면 `kubectl rollout restart deployment kps-grafana -n monitoring` 후 30초 뒤 다시 port-forward 합니다.

## 실습 16 · LogQL 한 단계씩

먼저 손님을 만듭니다(6교시와 같은 방법).

```bash
for i in $(seq 1 20); do
  curl -s -X POST localhost:30080/api/orders -H 'Content-Type: application/json' \
    -d '{"product_id": 1}' > /dev/null
done
```

Grafana **Explore** → 데이터 소스 **Loki** → 오른쪽 위 **Code** 모드에서 차례로 실행합니다.

### 1 — 라벨로 고르기

```logql
{namespace="devmart", app="order-api"}
```

`{ }` 안은 Prometheus와 같은 **라벨 선택**입니다. 오늘 Alloy가 붙인 네 라벨만 쓸 수 있습니다.

### 2 — 글자로 거르기

```logql
{namespace="devmart", app="order-api"} |= "order_saved"
```

| 연산자 | 뜻 |
|---|---|
| `\|= "글자"` | 이 글자가 **있는** 줄 (`grep`) |
| `!= "글자"` | 없는 줄 (`grep -v`) |
| `\|~ "정규식"` | 정규식에 맞는 줄 (`grep -E`) |

### 3 — JSON 풀어서 칸으로

DevMart의 서비스들은 3주차 1일차부터 로그를 **한 줄에 JSON 하나**로 남겼습니다. 그 덕을 지금 봅니다.

```logql
{namespace="devmart", app="order-api"} | json | event="order_saved" | total_price > 50000
```

> **🟢 확인: 보이는 것**
>
> 각 줄을 펼치면 `event`, `order_id`, `request_id`, `total_price`가 **칸(필드)**으로 보입니다. `| json`이 본문을 풀어 칸으로 만들었고, 그 칸으로 다시 걸렀습니다. 로그를 사람 문장이 아니라 **구조화된 JSON**으로 남겨야 하는 이유입니다.

### 4 — 세어서 그래프로

```logql
sum by (app) (count_over_time({namespace="devmart"} | json | event=~".*error.*" [1m]))
```

로그가 **숫자(메트릭)**가 되었습니다. 위쪽 그래프에 서비스별 에러 수가 그려집니다. 손님만 있고 에러가 없으면 빈 그래프입니다 — 다음 실습에서 만듭니다.

## 실습 17 · 요청 하나를 여러 서비스에 걸쳐 따라가기

3주차 5일차에는 `kubectl logs`를 서비스마다 열어 `grep $RID`를 했습니다. 이번에는 **한 쿼리로** 합니다.

```bash
RID=$(curl -s -X POST localhost:30080/api/orders -H 'Content-Type: application/json' \
  -d '{"product_id": 2}' | jq -r .request_id)
echo $RID
```

Explore에서 (`<RID>` 자리에 위 값):

```logql
{namespace="devmart"} |= "<RID>"
```

> **🟢 확인: 이렇게 보입니다 (시간 순)**
>
> ```text
> order-api     {"event":"order_received","request_id":"…","product_id":2,…}
> catalog-api   {"event":"get_product","product_id":2,…}
> order-api     {"event":"order_saved","request_id":"…","order_id":31,…}
> order-api     {"event":"order_queued","request_id":"…","order_id":31}
> order-worker  {"event":"order_processing","request_id":"…","order_id":31}
> order-worker  {"event":"order_completed","request_id":"…","order_id":31}
> ```
> 한 주문이 **세 서비스를 지나간 순서**가 한 화면에 나옵니다. Pod가 지워진 뒤에도 Loki에는 남아 있습니다(오늘 설정으로 48시간).

이제 장애를 만들고 에러 그래프를 봅니다.

```bash
kubectl scale deployment catalog-api -n devmart --replicas=0
for i in $(seq 1 10); do curl -s -o /dev/null -X POST localhost:30080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 1}'; done
kubectl scale deployment catalog-api -n devmart --replicas=2
```

실습 16의 4번 쿼리를 다시 실행하면 `order-api`의 `catalog_error` 막대가 솟아 있습니다. 6교시의 Prometheus 알림이 **"무언가 잘못됐다"**를 알려 준다면, Loki는 **"무엇이, 어떤 요청에서"**를 알려 줍니다.

> **🧹 정리: 정리**
>
> ```bash
> kill %1 2>/dev/null || pkill -f "port-forward -n monitoring service/kps-grafana"
> cd ~/devops-lab && git add k8s/w4d2/monitoring/loki-values.yaml k8s/w4d2/monitoring/alloy-values.yaml
> git commit -m "4주차 2일차: Loki + Alloy 로그 수집" && git push
> ```
> Loki와 Alloy는 **남겨 둡니다.** 3일차 GitOps 실습에서 배포가 일으킨 로그를 여기서 다시 봅니다. 노트북이 무거우면 `helm uninstall alloy loki -n monitoring`으로 지워도 내일 실습에는 지장이 없습니다.

> **🎓 학술 노트 — 로그는 구조를 가져야 한다**
>
> 로그를 사람이 읽는 **문장**이 아니라 기계가 읽는 **사건 기록(event)**으로 다뤄야 한다는 주장은 오래됐습니다. 구글의 **Dapper** 논문(Sigelman 외, 2010)은 요청 하나에 **추적 ID**를 붙여 수천 개 서비스를 지나는 길을 이어 붙이는 방법을 보였고, 이것이 3주차 1일차의 `X-Request-ID`와 오늘 `|= "<RID>"`의 뿌리입니다. 이후 OpenTelemetry는 로그 · 메트릭 · 트레이스가 **같은 trace ID와 같은 라벨(리소스 속성)**을 공유해야 서로 오갈 수 있다는 것을 표준으로 정리했습니다. 오늘 Loki의 라벨을 Prometheus와 같게(`namespace`, `app`) 붙인 이유입니다.
>
> - Sigelman, B. H. et al. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*. Google Technical Report dapper-2010-1.

> **📈 트렌드 — 수집기는 하나로, 표준은 OpenTelemetry로**
>
> 한때는 로그용(Promtail · Fluent Bit), 메트릭용, 트레이스용 수집기를 따로 두었습니다. Grafana는 Promtail을 **2026년에 지원 종료**하고 하나의 수집기 **Alloy**로 합쳤고, Alloy는 OpenTelemetry Collector를 바탕으로 세 신호를 함께 다룹니다. 업계 전체도 **OpenTelemetry 프로토콜(OTLP)**로 보내고, 저장소(Loki · Prometheus · Tempo · 클라우드 서비스)는 골라 쓰는 쪽으로 가고 있습니다. 오늘 `loki.write`를 다른 곳으로 바꾸면 수집 쪽은 그대로 둘 수 있습니다.

## 정리

- `kubectl logs`는 Pod와 함께 사라지고, 하나씩 보고, 집계를 못 합니다 → **모은다**.
- Loki는 **라벨만 색인**합니다. 라벨로 좁히고 → 글자로 거르고 → `| json`으로 풀고 → `count_over_time`으로 셉니다.
- Alloy가 apiserver로 Pod 로그를 읽어 **라벨 네 개**만 붙여 보냅니다. 라벨은 적게.
- 요청 ID 하나로 **여러 서비스의 로그를 한 화면에** 모읍니다. 구조화된 JSON 로그가 그 전제입니다.

> **✅ 확인 문제**
>
> 1. Loki가 전통적 로그 검색보다 저장 비용이 싼 이유는?
> 2. `{namespace="devmart"} |= "error"`와 `{namespace="devmart"} | json | event="catalog_error"`의 차이는?
> 3. Alloy에서 `pod` 이름 말고 **요청 ID**를 라벨로 붙이면 안 되는 이유는?
> 4. 롤링 업데이트로 사라진 옛 Pod의 로그를 보고 싶습니다. 어디서 보나요?
> 5. 6교시의 알림과 오늘의 로그 검색은 장애 대응에서 각각 어떤 질문에 답하나요?
>
> <details><summary>정답</summary>
>
> 1. 본문 전체가 아니라 라벨만 색인하고, 본문은 압축 덩어리로 저장하기 때문
> 2. 앞은 본문에 "error" 글자가 있는 모든 줄, 뒤는 JSON을 풀어 `event` 칸이 정확히 `catalog_error`인 줄
> 3. 요청마다 값이 달라 라벨 조합(스트림)이 끝없이 늘어나 Loki가 느려지고 비싸진다(높은 카디널리티)
> 4. Loki — Pod가 지워져도 보관 기간 동안 남아 있다
> 5. 알림 — "무언가 잘못됐다(언제, 얼마나)". 로그 — "무엇이, 어떤 요청에서 잘못됐나"
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - 로그 · 메트릭 · 트레이스를 각각 한 문장으로, DevMart 예와 함께
> - 오늘 만든 PromQL 중 가장 쓸모 있다고 느낀 것 하나와 그 이유
> - 5교시 장애에서 k6 · Grafana · events가 각각 알려 준 것
> - 알림이 Firing이 되기까지 걸린 시간 — 줄여야 할까, 늘려야 할까?
> - DevMart 주문의 SLO를 내가 정한다면 몇 %로? 근거는?
> - 내일 전에 궁금한 것: 런북 · 대시보드 · 규칙을 모두 Git에 올렸다. 그렇다면 **클러스터 자체도** Git에 있는 대로 맞춰지게 할 수는 없을까?

## 참고 문헌

- Sigelman, B. H., Barroso, L. A., Burrows, M., Stephenson, P., Plakal, M., Beaver, D., Jaspan, S., & Shanbhag, C. (2010). *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*. Google.
- Grafana Labs. *Loki Documentation* — Install the monolithic Helm chart; LogQL; Label best practices (cardinality). grafana.com/docs/loki
- Grafana Labs. *Grafana Alloy* — loki.source.kubernetes, discovery.kubernetes; *Promtail deprecation and migration to Alloy*. grafana.com/docs/alloy
- OpenTelemetry. *Logs Data Model*; *Semantic Conventions — Kubernetes resource attributes*. opentelemetry.io

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 관찰 런북과 SLO](lesson-07.md) | [⬆️ 2일차 목차](README.md) | [4주차 3일차 목차](../day3/README.md) ➡️ |
