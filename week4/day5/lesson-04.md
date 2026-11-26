<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [5일차](README.md) › 4/7교시</sub>

# 4교시 · 서비스 신원으로 허가

> [!NOTE]
> **이번 시간에 할 일**
>
> - catalog-api 허가를 **"devmart 안 누구나"**에서 **"order-api만"**으로 좁힙니다.
> - 같은 네임스페이스의 다른 Pod가 **거절되는** 것을 봅니다.
> - 어제 남긴 **Pod IP 우회로**를 ztunnel의 L4 규칙으로 막습니다.
> - L7 규칙과 L4 규칙이 **각각 어디서** 검사되는지 정리합니다.

## 지금의 규칙과 그 빈틈

```yaml
# 어제 (4일차 6교시)
  rules:
    - from:
        - source:
            namespaces: ["devmart"]
```

devmart 안의 **어느 Pod든** catalog-api를 부를 수 있습니다. web(nginx)이 뚫리면 catalog-api를 직접 부를 수 있다는 뜻입니다. 3교시에 서비스마다 신원을 나눴으니, 이제 **"누가"를 서비스로** 말할 수 있습니다.

## 실습 7 · order-api만 (커밋)

```bash
cd ~/devops-lab/k8s/w4d5
diff ~/devmart-deploy/devmart/catalog-authz.yaml deploy/catalog-authz.yaml
```

> **🟢 확인: diff**
>
> ```diff
> <             namespaces: ["devmart"]
> ---
> >             principals: ["cluster.local/ns/devmart/sa/order-api"]
> ```
> `principals`는 SPIFFE ID에서 `spiffe://`를 뺀 모양입니다.

```bash
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d5/deploy/catalog-authz.yaml devmart/
git commit -am "catalog-api는 order-api만 (서비스 신원)" && git push
kubectl run client -n devmart --image=curlimages/curl:8.17.0 --restart=Never -- sleep 3600
kubectl wait -n devmart --for=condition=Ready pod/client
sleep 45
kubectl exec -n devmart client -- curl -s -m 3 -w ' %{http_code}\n' catalog-api:8000/api/info
kubectl exec -n outsider client -- curl -s -m 3 -w ' %{http_code}\n' catalog-api.devmart:8000/api/info
curl -s -o /dev/null -w 'orders %{http_code}\n' -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'
curl -s -o /dev/null -w 'products %{http_code}\n' localhost:30080/api/products
```

> **🟢 확인: 확인**
>
> ```text
> RBAC: access denied 403
> RBAC: access denied 403
> orders 202
> products 200
> ```
> - devmart 안의 `client`(sa/default)도 이제 **403**입니다. 같은 네임스페이스라는 것만으로는 부족합니다.
> - 주문(order-api → catalog-api)은 그대로 됩니다.
> - 상품 목록(입구 → catalog-api)도 됩니다 — 입구는 **waypoint를 거치지 않으므로**(4일차 4교시) 이 L7 규칙의 검사 대상이 아닙니다.

## 실습 8 · 우회로 확인

```bash
IP=$(kubectl get pod -n devmart -l app=catalog-api -o jsonpath='{.items[0].status.podIP}')
kubectl exec -n devmart client -- curl -s -m 3 -o /dev/null -w 'client  → Pod IP %{http_code}\n' $IP:8000/api/info
kubectl exec -n outsider client -- curl -s -m 3 -o /dev/null -w 'outsider → Pod IP %{http_code}\n' $IP:8000/api/info
```

> **🟢 확인: 확인**
>
> ```text
> client  → Pod IP 200
> outsider → Pod IP 200
> ```
> Service 이름 대신 **Pod IP**로 부르면 waypoint를 지나지 않아 L7 규칙을 그대로 피합니다. 공격자는 `kubectl`이 없어도 같은 대역의 IP를 훑어 이 길을 찾을 수 있습니다.

## 실습 9 · L4 규칙으로 막기 (커밋)

```bash
cat ~/devops-lab/k8s/w4d5/deploy/catalog-l4.yaml
```

```yaml
spec:
  selector:                         # targetRefs(Service)가 아니라 selector(Pod) — ztunnel이 검사한다
    matchLabels: { app: catalog-api }
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/devmart/sa/waypoint"]   # L7 검사를 마친 것
    - from:
        - source:
            namespaces: ["envoy-gateway-system"]                   # 입구
```

| | L7 규칙 (`targetRefs: Service`) | L4 규칙 (`selector: Pod`) |
|---|---|---|
| 검사하는 곳 | waypoint | catalog-api 노드의 **ztunnel** |
| 볼 수 있는 것 | 신원 + 경로 · 메서드 · 헤더 | **신원 · 포트만** (HTTP는 모른다) |
| 원래 부른 쪽 | order-api (waypoint가 안다) | waypoint · 입구 (마지막으로 연결한 쪽) |
| 막는 길 | Service 이름으로 오는 호출 | **Pod로 들어오는 모든 연결** |

```bash
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d5/deploy/catalog-l4.yaml devmart/
sed -i 's/^  - catalog-authz.yaml.*/&\n  - catalog-l4.yaml/' devmart/kustomization.yaml
git add . && git commit -m "catalog-api Pod는 waypoint와 입구만 (L4)" && git push
sleep 45
kubectl exec -n devmart client -- curl -s -m 3 -o /dev/null -w 'client  → Pod IP %{http_code}\n' $IP:8000/api/info
kubectl exec -n outsider client -- curl -s -m 3 -o /dev/null -w 'outsider → Pod IP %{http_code}\n' $IP:8000/api/info
curl -s -o /dev/null -w 'orders %{http_code}\n' -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'
curl -s -o /dev/null -w 'products %{http_code}\n' localhost:30080/api/products
kubectl logs -n istio-system -l app=ztunnel --tail=200 | grep -m1 "policy rejection"
```

> **🟢 확인: 확인**
>
> ```text
> client  → Pod IP 000
> outsider → Pod IP 000
> orders 202
> products 200
> … error access connection complete … src.identity="spiffe://cluster.local/ns/outsider/sa/default" … error="connection closed due to policy rejection: allow policies exist, but none allowed"
> ```
> 우회로가 닫혔습니다. L4 거절은 HTTP 응답이 아니라 **연결 끊김**(`000`)으로 보입니다 — 6교시 거절 지도의 한 칸입니다. 손님(products · orders)은 그대로입니다.

> [!WARNING]
> **규칙이 늘면 지도가 필요하다**
>
> 지금 catalog-api에 닿는 길은 세 개입니다 — ① order-api → waypoint(L7: order-api만) → ztunnel(L4: waypoint만) → catalog-api, ② 입구 → ztunnel(L4: 입구만) → catalog-api, ③ 그 밖은 모두 거절. 새 서비스가 catalog-api를 불러야 하면 **두 규칙을 모두** 고쳐야 합니다. 이런 규칙은 반드시 Git에 두고, 바꿀 때 PR에 "**누가 새로 부르게 되나**"를 적습니다.

> **❓ 오해 — mTLS를 켰으니 안전하다**
>
> mTLS(STRICT)는 "**누구인지 증명된** 연결만 받는다"까지입니다. 증명된 누구든 받습니다 — outsider도 메시 안이라 증명은 됐습니다. **허가**(누가 무엇을)가 있어야 비로소 제로 트러스트입니다. 인증과 인가는 언제나 짝입니다(1교시).

> **🎓 학술 노트 — 정책 검사 지점의 배치**
>
> 접근 제어 구조에서 정책을 **판단하는 곳**(PDP, Policy Decision Point)과 **집행하는 곳**(PEP, Policy Enforcement Point)을 나누는 모델은 XACML(OASIS, 2003)과 RFC 2904(*AAA Authorization Framework*, 2000)에서 정리되었습니다. 오늘 istiod가 정책을 나눠 주고(판단 규칙의 배포), waypoint와 ztunnel이 **두 개의 집행 지점**이 되었습니다. 집행 지점을 **모든 길목**에 두지 않으면 우회로가 생긴다는 것 — 실습 8 — 이 이 모델의 교훈입니다.

> **📈 트렌드 2026 — 신원 기반 세분화**
>
> IP 대역으로 나누던 네트워크 분리(세그먼테이션)가 **워크로드 신원 기반**으로 옮겨 가고 있습니다. 클라우드의 보안 그룹 · Kubernetes NetworkPolicy가 IP · 라벨을 보는 반면, 메시의 정책은 SPIFFE 신원을 봅니다. Cilium · Istio 모두 "L4는 커널 · 노드 단에서 싸게, L7은 필요한 곳에서"라는 오늘과 같은 두 층 구조로 수렴하고 있습니다.

> **✅ 확인 문제**
>
> 1. namespaces 규칙을 principals 규칙으로 바꾸자 무엇이 막혔나요?
> 2. 입구에서 오는 상품 목록이 L7 규칙에 걸리지 않은 이유는?
> 3. L4 규칙이 order-api가 아니라 waypoint의 신원을 허가하는 이유는?
> 4. L7 거절과 L4 거절은 손님에게 어떻게 다르게 보이나요?
>
> <details><summary>정답</summary>
>
> 1. 같은 devmart 안이지만 order-api가 아닌 Pod(client, sa/default)의 호출
> 2. 입구는 Service가 아니라 Pod IP로 바로 보내 waypoint를 거치지 않기 때문
> 3. order-api의 호출은 waypoint를 거쳐 오므로 catalog-api 앞의 ztunnel이 보는 상대는 waypoint이기 때문
> 4. L7은 HTTP 403 "RBAC: access denied", L4는 연결 끊김(curl 000)
>
> </details>

## 참고 문헌

- Istio Docs. *Ambient — Layer 4 and Layer 7 authorization policy*, *AuthorizationPolicy reference — targetRefs vs selector*. istio.io
- Vollbrecht, J. 외 (2000). *RFC 2904 AAA Authorization Framework*. IETF.
- OASIS (2003). *eXtensible Access Control Markup Language (XACML) 1.0*.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [3교시 · ServiceAccount — 프로그램의 신원](lesson-03.md) | [⬆️ 5일차 목차](README.md) | [5교시 · Kyverno 정책](lesson-05.md) ➡️ |
