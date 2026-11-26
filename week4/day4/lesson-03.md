[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [4일차](README.md)

# 3교시 · mTLS 확인과 Kiali

> [!NOTE]
> **이번 시간에 할 일**
>
> - ztunnel 로그에서 **누가 누구를** 불렀는지 — 신원(SPIFFE ID)을 읽습니다.
> - 메시 밖 Pod에서 보면 통신이 **어떻게 보이는지** 확인합니다.
> - Istio의 지표를 어제의 Prometheus가 **긁게** 합니다.
> - **Kiali**를 설치해 DevMart의 **메시 지도**를 봅니다.

## 신원 — SPIFFE ID

메시 안의 모든 Pod는 istiod에게서 **인증서**를 받습니다. 그 인증서에 적힌 이름이 신원입니다.

```text
spiffe://cluster.local/ns/devmart/sa/default
         └ 신뢰 도메인 └ 네임스페이스 └ ServiceAccount
```

IP가 아니라 **네임스페이스 + ServiceAccount**가 신원이 됩니다. Pod가 죽고 다시 떠서 IP가 바뀌어도(3주차 4일차) 신원은 같습니다. 이 형식은 CNCF 표준 **SPIFFE**입니다.

> [!IMPORTANT]
> **지금 DevMart는 모두 sa/default**
>
> 3주차 5일차의 Deployment에는 `serviceAccountName`이 없습니다. 그래서 db · catalog-api · order-api 모두 **같은 신원**(`sa/default`)입니다. 오늘은 네임스페이스 단위로 허가하고(6교시), 서비스마다 ServiceAccount를 나눠 **서비스 단위 신원**을 만드는 것은 내일(5일차 RBAC) 합니다.

## 실습 4 · ztunnel 로그에서 신원 읽기

```bash
curl -s -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":2,"quantity":1}' >/dev/null
kubectl logs -n istio-system -l app=ztunnel --tail=200 | grep catalog-api | tail -2
```

> **🟢 확인: 확인**
>
> ```text
> 2026-11-26T02:14:07.511Z info access connection complete src.addr=10.244.2.18:51234 src.workload="order-api-6c9d7b8f5-k2m4x" src.namespace="devmart" src.identity="spiffe://cluster.local/ns/devmart/sa/default" dst.addr=10.244.1.15:15008 dst.hbone_addr=10.244.1.15:8000 dst.service="catalog-api.devmart.svc.cluster.local" dst.workload="catalog-api-5d8c7b9f6-2xkq4" dst.namespace="devmart" dst.identity="spiffe://cluster.local/ns/devmart/sa/default" direction="outbound" bytes_sent=213 bytes_recv=402 duration="12ms"
> ```
> - `src.identity` · `dst.identity` — 양쪽의 **증명된 신원**. mTLS의 '상호'가 여기에 있습니다.
> - `dst.addr=…:15008` — 실제로는 catalog-api의 8000이 아니라 **HBONE 포트 15008**로 갔습니다. 앱은 8000으로 보냈고, ztunnel이 가로채 감쌌습니다.

## 실습 5 · 메시 밖에서 보면

메시 밖(`default` 네임스페이스)에 Pod를 하나 띄워 catalog-api를 부릅니다.

```bash
kubectl run plain -n default --image=curlimages/curl:8.17.0 --restart=Never -- sleep 3600
kubectl wait -n default --for=condition=Ready pod/plain
kubectl exec -n default plain -- curl -s -m 3 catalog-api.devmart:8000/api/info; echo
```

> **🟢 확인: 확인**
>
> ```text
> {"env":"kind","hostname":"catalog-api-5d8c7b9f6-2xkq4","service":"catalog-api","version":"2.0.0"}
> ```
> **아직은 열립니다.** 메시의 기본값은 **PERMISSIVE** — mTLS로 오면 mTLS로, 평문으로 오면 평문으로 받습니다. 메시를 처음 켤 때 메시 밖의 손님(Envoy Gateway · Prometheus 등)이 끊기지 않게 하려는 기본값입니다. 6교시에 **STRICT**로 바꿔 이것을 막습니다. `plain` Pod는 6교시에 다시 씁니다.

## 실습 6 · Istio 지표를 Prometheus로

```bash
cd ~/devops-lab/k8s/w4d4
kubectl apply -f monitoring/istio-monitors.yaml
```

> [!TIP]
> **이건 kubectl apply여도 되나?**
>
> istio-system · monitoring은 DevMart가 아니라 **플랫폼**의 것이라 devmart Application이 관리하지 않습니다. 실무라면 플랫폼용 배포 저장소(또는 Application)를 따로 두고 거기에 커밋합니다. 오늘은 3일차의 경계 — "devmart 네임스페이스만 Git으로" — 를 지킵니다.

1분 뒤 Prometheus(`kubectl port-forward -n monitoring svc/kps-prometheus 9090:9090 &` → <http://localhost:9090>)의 **Status → Target health**에서 `serviceMonitor/istio-system/istiod/0`, `podMonitor/istio-system/ztunnel/0`이 UP인지 봅니다. 그리고 쿼리:

```promql
sum by (source_workload, destination_workload) (rate(istio_tcp_connections_opened_total{reporter="destination"}[5m]))
```

> **🟢 확인: 확인**
>
> ```text
> {destination_workload="catalog-api", source_workload="order-api"}   0.02
> {destination_workload="db",          source_workload="catalog-api"} 0.05
> {destination_workload="db",          source_workload="order-api"}   0.02
> {destination_workload="redis",       source_workload="order-api"}   0.02
> …
> ```
> 2일차에는 Envoy Gateway(입구)에서만 숫자를 셀 수 있었습니다. 이제 **서비스 사이의 연결**도 셉니다 — 앱에 /metrics가 없는데도요. 다만 ztunnel은 L4라 **연결 수와 바이트**만 압니다. HTTP 요청 수 · 상태 코드는 4교시 waypoint부터입니다.

## 실습 7 · Kiali 설치

```bash
helm repo add kiali https://kiali.org/helm-charts
helm repo update
helm search repo kiali/kiali-server
KVER=$(helm search repo kiali/kiali-server -o json | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['version'])")
echo "kiali-server $KVER" | tee -a VERSIONS.txt
helm install kiali-server kiali/kiali-server -n istio-system --version $KVER -f kiali/kiali-values.yaml --wait
kubectl port-forward -n istio-system svc/kiali 20001:20001 >/dev/null 2>&1 &
```

values의 요점은 둘입니다 — `external_services.prometheus.url`로 **어제의 Prometheus를 그대로** 쓰고, `view_only_mode: true`로 **화면에서 설정을 바꾸지 못하게** 합니다(설정은 Git으로, 3일차).

손님을 흉내 낸 뒤 지도를 봅니다.

```bash
for i in $(seq 60); do
  curl -s -o /dev/null localhost:30080/api/products
  curl -s -o /dev/null -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'
  sleep 1
done &
```

<http://localhost:20001> → 왼쪽 **Traffic Graph** → Namespace: `devmart` → Display에서 **Traffic Animation** 켜기.

> **🟢 확인: 확인**
>
> order-api → catalog-api, order-api → db, order-api → redis, order-worker → redis · db, catalog-api → db로 **선이 그려집니다.** 3주차 1일차에 손으로 그렸던 DevMart 구조도와 같은 그림이 **실제 트래픽으로** 그려졌습니다. 선을 누르면 오른쪽에 초당 연결 · 바이트가 나옵니다. 선 위의 자물쇠 표시가 **mTLS**입니다.

> **❓ 오해 — 지도는 설계도다**
>
> Kiali의 지도는 **최근 몇 분 동안 실제로 오간 것**입니다. 호출이 없던 경로는 그려지지 않고, 설계에 없던 호출(누군가 몰래 부른 것)은 그려집니다. 그래서 오히려 **설계와 실제가 다른 곳**을 찾는 도구입니다.

> **🎓 학술 노트 — 의존 관계를 관찰로 알아내기**
>
> 서비스 사이의 의존 관계를 **실제 트래픽으로** 알아내는 연구는 분산 추적과 함께 발전했습니다. Aguilera 외의 *Performance debugging for distributed systems of black boxes*(SOSP 2003)는 앱을 고치지 않고 **메시지만 관찰해** 호출 경로와 지연을 추정할 수 있음을 보였습니다. 메시의 지도는 이 '블랙박스 관찰'을 프록시 단에서 정확하게 하는 것입니다.

> **📈 트렌드 2026 — SPIFFE 신원의 확장**
>
> SPIFFE 신원은 메시 밖으로도 넓어지고 있습니다. 서비스가 클라우드 API에 접근할 때 비밀 키 대신 **워크로드 신원**으로 인증하는 방식(AWS IAM Roles Anywhere, EKS Pod Identity, GCP Workload Identity Federation)이 표준이 되었고, AI 에이전트에도 SPIFFE 신원을 주자는 논의가 활발합니다. 5주차 EKS에서 Pod가 AWS 권한을 얻는 방식으로 다시 만납니다.

> **✅ 확인 문제**
>
> 1. SPIFFE ID `spiffe://cluster.local/ns/devmart/sa/default`의 세 부분은?
> 2. 메시 밖 Pod가 아직 catalog-api를 부를 수 있는 이유는?
> 3. ztunnel 지표만으로 알 수 없는 것은?
> 4. Kiali를 view_only로 둔 이유는?
>
> <details><summary>정답</summary>
>
> 1. 신뢰 도메인(cluster.local), 네임스페이스(devmart), ServiceAccount(default)
> 2. 기본 mTLS 모드가 PERMISSIVE라 평문도 받기 때문
> 3. HTTP 요청 수 · 상태 코드 · 경로 같은 L7 정보 (waypoint가 있어야)
> 4. 설정 변경은 Git(배포 저장소)으로만 하기 위해 — 화면에서 바꾸면 어긋남이 생긴다
>
> </details>

## 참고 문헌

- SPIFFE. *SPIFFE Concepts — SPIFFE ID*. spiffe.io/docs
- Istio Docs. *Ambient — Verify mutual TLS is enabled*, *Prometheus integration*. istio.io
- Kiali Docs. *Installation — Helm*, *Configuration — external services*. kiali.io/docs
- Aguilera, M. K. 외 (2003). *Performance debugging for distributed systems of black boxes*. SOSP '03.

---

⬅️ 이전: [2교시 · Istio 설치와 메시 등록](lesson-02.md) &nbsp;|&nbsp; [⬆️ 4일차 목차](README.md) &nbsp;|&nbsp; 다음: [4교시 · waypoint와 트래픽 나누기](lesson-04.md) ➡️
