# 6교시 · HTTPRoute — 경로 · Host · 가중치

> [!NOTE]
> **이번 시간에 할 일**
>
> - DevMart의 경로 셋을 **HTTPRoute**로 만들어, nginx가 하던 API 게이트웨이 일을 Gateway에 넘깁니다.
> - 라우트의 `status`에서 **Accepted · ResolvedRefs**를 읽습니다.
> - 요청 ID를 이제 **Envoy**가 붙인다는 것을 로그로 확인합니다.
> - 다른 네임스페이스의 앱(podinfo)을 **Host**로 나누어 같은 문에 붙입니다.
> - 두 버전에 **80:20**으로 나누는 카나리를 만듭니다.

## 실습 10 · DevMart를 Gateway 뒤로

### 단계 1 — 라우트 셋 적용

```bash
cd ~/devops-lab/k8s/w4d1
kubectl apply -f gateway/devmart-routes.yaml
kubectl get httproute -n devmart
```

> **🟢 확인: 보이는 것**
>
> ```text
> httproute.gateway.networking.k8s.io/orders created
> httproute.gateway.networking.k8s.io/catalog created
> httproute.gateway.networking.k8s.io/web created
> NAME      HOSTNAMES   AGE
> catalog               3s
> orders                3s
> web                   3s
> ```
> 서비스마다 **자기 라우트**를 따로 만들었습니다. 주문 팀은 `orders`만, 상품 팀은 `catalog`만 고치면 됩니다 — 4교시의 역할 분리를 앱 팀 사이에도 적용한 것입니다. 3주차 nginx 설정 파일 하나를 여러 팀이 함께 고치던 것과 다릅니다.

### 단계 2 — 라우트의 상태

```bash
kubectl describe httproute orders -n devmart | sed -n '/^Status:/,$p'
```

> **🟢 확인: 보이는 것 (줄여서)**
>
> ```text
> Status:
>   Parents:
>     Conditions:
>       Message:  Route is accepted
>       Reason:   Accepted
>       Status:   True
>       Type:     Accepted
>       Message:  Resolved all the Object references for the Route
>       Reason:   ResolvedRefs
>       Status:   True
>       Type:     ResolvedRefs
>     Controller Name:  gateway.envoyproxy.io/gatewayclass-controller
>     Parent Ref:
>       Name:  devmart
> ```

| 조건 | True의 뜻 | False라면 (7교시) |
|---|---|---|
| **Accepted** | 이 라우트가 Gateway에 **붙었다** | 붙을 수 없다 — 허락 없음, 리스너 없음… |
| **ResolvedRefs** | `backendRefs`의 Service를 **모두 찾았다** | Service가 없다, 다른 네임스페이스인데 허락이 없다… |

`Controller Name`이 이 상태를 **누가** 썼는지 알려 줍니다. 3주차 4일차의 Events `From` 칸과 같은 역할입니다.

### 단계 3 — 확인

```bash
for p in / /api/products /api/orders; do
  printf '%-15s ' $p; curl -s -o /dev/null -w '%{http_code}\n' localhost:30080$p
done
```

> **🟢 확인: 보이는 것**
>
> ```text
> /               200
> /api/products   200
> /api/orders     200
> ```
> 브라우저에서 **http://localhost:30080** 을 열고 주문을 하나 넣어 봅니다. 3주차 5일차와 같은 화면이지만, 이제 손님을 처음 받는 것은 nginx가 아니라 **Envoy**입니다.

### 단계 4 — 요청 ID는 누가 붙이나

```bash
curl -s -X POST localhost:30080/api/orders -H 'Content-Type: application/json' -d '{"product_id": 1}'; echo
```

> **🟢 확인: 보이는 것**
>
> ```text
> {"order_id":61,"request_id":"5b2e8f3c-9d41-4a7b-b6e0-2c8f1d9a7e54","status":"pending","total_price":59000}
> ```
> `request_id`의 **모양이 바뀌었습니다.** 3주차에는 nginx의 `$request_id`(32자리 16진수)였는데, 이제는 하이픈이 든 **UUID**입니다. Envoy는 들어오는 요청에 `x-request-id`가 없으면 **스스로 만들어 붙이고** 뒤로 넘깁니다. 우리 앱은 헤더 이름만 보고 읽으니 코드를 고칠 필요가 없었습니다.

```bash
RID=5b2e8f3c-9d41-4a7b-b6e0-2c8f1d9a7e54        # 내 값으로
kubectl logs -n devmart -l 'app in (order-api,catalog-api,order-worker)' --prefix --tail=-1 | grep $RID | cut -c1-110
```

> **🟢 확인: 보이는 것**
>
> ```text
> [pod/order-api-…/order-api] {"service": "order-api", "event": "order_received", "request_id": "5b2e8f3c-…", …
> [pod/catalog-api-…/catalog-api] {"service": "catalog-api", "event": "get_product", "request_id": "5b2e8f3c-…", …
> [pod/order-api-…/order-api] {"service": "order-api", "event": "order_queued", …
> [pod/order-worker-…/order-worker] {"service": "order-worker", …, "event": "order_completed", …
> ```
> 3주차 5일차 5교시와 같은 여행 기록이 이어집니다. 출발점만 nginx에서 Envoy로 바뀌었습니다.

> [!TIP]
> **nginx는 이제 무엇을 하나**
>
> web(nginx)은 이제 `/`의 **정적 파일만** 내줍니다. `/api/…` 요청은 Gateway가 web을 거치지 않고 바로 각 서비스로 보냅니다. nginx 설정의 `location /api/` 부분은 이제 쓰이지 않습니다 — 정리는 회고 때 Try로 남겨 둘 만합니다.

## 실습 11 · Host로 나누기

2교시의 podinfo는 **default** 네임스페이스에 있습니다. 같은 문(30080)에 붙이되, **Host**가 `podinfo.localhost`일 때만 보냅니다.

```bash
sed -n '/spec:/,$p' gateway/podinfo-route.yaml
kubectl apply -f gateway/podinfo-route.yaml
kubectl get httproute -A
```

```yaml
spec:
  parentRefs:
    - name: devmart
      namespace: devmart        # 다른 네임스페이스의 Gateway
  hostnames:
    - podinfo.localhost
  rules:
    - backendRefs:
        - name: podinfo
          port: 9898
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAMESPACE   NAME      HOSTNAMES               AGE
> default     podinfo   ["podinfo.localhost"]   3s
> devmart     catalog                           10m
> devmart     orders                            10m
> devmart     web                               10m
> ```
> default의 라우트가 devmart의 Gateway에 붙을 수 있는 것은 Gateway가 `allowedRoutes: from: All`로 **허락**했기 때문입니다(4교시).

```bash
curl -s -H 'Host: podinfo.localhost' localhost:30080 | grep -E '"(hostname|message)"'
curl -s -o /dev/null -w '%{http_code}\n' localhost:30080/api/products
curl -s -H 'Host: podinfo.localhost' localhost:30080/api/orders | head -c 60; echo
```

- `-H 'Host: …'` : 요청의 Host 헤더를 바꾼다 — DNS 없이 "이 도메인으로 왔다"고 흉내 낸다

> **🟢 확인: 보이는 것**
>
> ```text
>   "hostname": "podinfo-7b9c8d6f5-k2x8p",
>   "message": "upgrade로 바꿨습니다",
> 200
> 404 page not found
> ```
> - Host가 `podinfo.localhost`면 podinfo로, 아니면 DevMart로 — **같은 문, 같은 포트**에서 갈립니다.
> - 마지막 줄이 4교시의 '함정'입니다. `/api/orders`인데도 DevMart가 아니라 **podinfo**로 갔습니다(podinfo가 그 경로를 몰라 404). **Host가 먼저** 갈리기 때문입니다.

> [!WARNING]
> **브라우저로 열면 안 될 수도 있다**
>
> 브라우저는 `podinfo.localhost`를 `127.0.0.1`로 찾아 주지만(`.localhost`는 예약된 이름), 요청에 **`Host: podinfo.localhost:30080`** — 포트가 붙은 Host — 를 보냅니다. Envoy는 기본으로 Host를 **포트까지 글자 그대로** 비교하므로, 설정에 따라 라우트에 안 맞아 404가 날 수 있습니다. 실제 서비스는 80/443 표준 포트를 쓰니 이 문제가 드뭅니다. 오늘은 `curl -H`로 확인합니다. Envoy Gateway의 ClientTrafficPolicy로 '포트 떼고 비교'를 켤 수도 있습니다.

## 실습 12 · 가중치로 나누기 — 카나리

새 버전을 모두에게 한꺼번에 내보내지 않고, **일부에게만** 먼저 보내는 것을 **카나리 배포**라고 합니다(3주차 4일차 7교시 학술 노트). 3주차의 롤링 업데이트는 Pod **개수**로 섞였지만, Gateway는 **요청 비율**을 직접 정합니다.

### 단계 1 — 두 번째 버전 설치

```bash
cat helm/podinfo-canary-values.yaml
helm install podinfo-canary oci://ghcr.io/stefanprodan/charts/podinfo --version 6.14.0 \
  -f helm/podinfo-canary-values.yaml --wait
kubectl get service -l 'app.kubernetes.io/name in (podinfo,podinfo-canary)'
```

> **🟢 확인: 보이는 것**
>
> ```text
> ...
> NAME             TYPE        CLUSTER-IP     PORT(S)             AGE
> podinfo          ClusterIP   10.96.51.9     9898/TCP,9999/TCP   2h
> podinfo-canary   ClusterIP   10.96.73.140   9898/TCP,9999/TCP   15s
> ```
> **같은 차트를 다른 릴리스 이름으로** 한 번 더 설치했습니다 — 1교시의 "릴리스 = 설치된 한 벌".

### 단계 2 — 80:20 라우트

```bash
diff gateway/podinfo-route.yaml gateway/podinfo-split.yaml
kubectl apply -f gateway/podinfo-split.yaml
```

> **🟢 확인: 보이는 것 (차이)**
>
> ```text
> >           weight: 80
> >         - name: podinfo-canary
> >           port: 9898
> >           weight: 20
> ```
> `podinfo-split.yaml`은 같은 이름(`podinfo`)의 라우트라서, 적용하면 **기존 라우트를 바꿉니다**(선언형).

### 단계 3 — 세어 보기

```bash
for i in $(seq 1 50); do
  curl -s -H 'Host: podinfo.localhost' localhost:30080 | grep -o '"message": "[^"]*"'
done | sort | uniq -c
```

> **🟢 확인: 보이는 것 (매번 조금 다름)**
>
> ```text
>      41 "message": "upgrade로 바꿨습니다"
>       9 "message": "카나리 — 새 버전"
> ```
> 50번 중 약 40 : 10. 정확히 80:20이 아닌 것은 **확률로** 나누기 때문입니다. 요청이 많을수록 비율에 가까워집니다.

> **📘 예시 — 카나리를 끝까지 올리기**
>
> 문제가 없으면 `weight`를 50:50 → 0:100으로 옮기고, 마지막에 옛 릴리스를 `helm uninstall`합니다. 문제가 보이면 **0:100이 아니라 100:0으로** — 즉시 되돌립니다. 3주차의 `rollout undo`는 Pod를 다시 만들어야 했지만, 가중치 되돌리기는 **Envoy 설정 한 줄**이라 1초 안에 끝납니다. 4주차 4일차 Istio와 이후 Argo Rollouts가 이 단계를 자동으로 진행합니다(3주차 4일차 트렌드).

### 표준 필드로 타임아웃

3주차 2일차에 "안쪽일수록 짧게, nginx 60초 > catalog 2초"를 배웠습니다. Ingress 시절에는 어노테이션이었던 타임아웃이 HTTPRoute에서는 **표준 필드**입니다. (읽기만 — 4주차 4일차에 다시 다룹니다.)

```yaml
  rules:
    - matches:
        - path: { type: PathPrefix, value: /api/orders }
      timeouts:
        request: 5s            # 손님 쪽에서 본 전체 시간 상한
      backendRefs:
        - name: order-api
          port: 8000
```

## 실습 13 · 비교표 마무리

3교시 실습 5의 마지막 열(Gateway API)을 오늘 해 본 것으로 채웁니다.

> **🟢 확인: 예시 답**
>
> | | Gateway API (오늘) |
> |---|---|
> | 경로로 나누기 | **표준** HTTPRoute `matches.path` — 순서가 아니라 규칙으로 우선순위 |
> | 설정을 바꾸려면 | 라우트를 고쳐 `apply` — **프록시 재시작 없이** 바로 반영(xDS) |
> | 다른 구현으로 바꾸려면 | GatewayClass만 바꾸면 라우트는 **그대로** (표준 필드만 썼다면) |
> | 장애 상태를 어디서 보나 | 라우트 · Gateway의 **status.conditions** (7교시) |

> **🎓 학술 노트 — 카나리와 '작은 실험'**
>
> '탄광의 카나리아'에서 온 이름입니다 — 유독 가스에 민감한 새를 먼저 들여보내 위험을 알았듯, 새 버전을 소수에게 먼저 보내 문제를 일찍 봅니다. 구글 SRE 책의 *The Site Reliability Workbook*(Beyer 외, 2018) 16장 *Canarying Releases*는 카나리를 **통계적 실험**으로 다룹니다 — 카나리 집단과 대조 집단의 오류율을 비교해 차이가 의미 있는지 판단하고, 카나리 비율이 너무 작으면 문제를 못 보고 너무 크면 피해가 커진다는 균형을 설명합니다. 오늘 50번 중 9번처럼, 적은 요청 수로는 비율조차 흔들린다는 것을 직접 봤습니다.

> **📈 트렌드 2026 — 입구 하나로 여러 앱**
>
> 오늘 하나의 Gateway(문)에 DevMart와 podinfo, 서로 다른 네임스페이스의 두 앱을 붙였습니다. 클라우드에서는 **로드 밸런서 하나가 곧 비용**이라(3교시), 여러 팀이 Gateway 하나를 나눠 쓰고 팀마다 라우트만 관리하는 구성이 흔합니다. Gateway API v1.5에서 표준이 된 **ListenerSet**은 한발 더 나아가, 팀마다 자기 **도메인 · 인증서(리스너)**까지 Gateway를 건드리지 않고 따로 붙이게 해 줍니다.

> **✅ 확인 문제**
>
> 1. DevMart 경로를 라우트 하나가 아니라 셋으로 나눈 이유는?
> 2. 라우트 status의 Accepted와 ResolvedRefs는 각각 무엇을 확인하나요?
> 3. 요청 ID의 모양이 바뀐 이유는? 앱 코드를 고치지 않아도 된 이유는?
> 4. `Host: podinfo.localhost`로 `/api/orders`를 요청하면 어디로 가나요? 왜?
> 5. 가중치 되돌리기가 `rollout undo`보다 빠른 이유는?
>
> <details><summary>정답</summary>
>
> 1. 서비스(팀)마다 자기 라우트만 고치게 하려고 — 역할 분리
> 2. Accepted — Gateway에 붙었나, ResolvedRefs — 보낼 Service를 모두 찾았나
> 3. 이제 Envoy가 `x-request-id`를 UUID로 만들어 붙이기 때문. 앱은 헤더 이름만 보고 읽으니 값의 모양은 상관없다
> 4. podinfo — Host가 지정된 라우트가 먼저 갈린다 (podinfo는 그 경로를 몰라 404)
> 5. Pod를 새로 만들 필요 없이 Envoy 설정(비율)만 바꾸면 되기 때문
>
> </details>

## 참고 문헌

- Gateway API. *HTTP routing* · *HTTP traffic splitting* · *HTTP timeouts* · *Cross-namespace routing*. gateway-api.sigs.k8s.io/guides
- Envoy Proxy Docs. *x-request-id header*. envoyproxy.io/docs/envoy/latest/configuration/http/http_conn_man/headers
- Envoy Gateway Docs. *HTTP Routing* · *Traffic Splitting*. gateway.envoyproxy.io/docs/tasks/traffic
- Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., & Thorne, S. (Eds.) (2018). *The Site Reliability Workbook*, Ch. 16 "Canarying Releases". O'Reilly.
