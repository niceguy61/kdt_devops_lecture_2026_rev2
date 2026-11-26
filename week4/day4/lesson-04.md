<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [4일차](README.md) › 4/7교시</sub>

# 4교시 · waypoint와 트래픽 나누기

> [!NOTE]
> **이번 시간에 할 일**
>
> - L7 기능을 맡을 **waypoint**를 Git으로 만듭니다.
> - 메시 안에서 부르는 손님(client Pod)을 두고, catalog-api 호출을 **버전별로 셉니다.**
> - **카나리 Deployment**와 **HTTPRoute(Service가 부모)**로 메시 안 호출의 10%를 카나리로 보냅니다.
> - 입구에서 오는 요청은 왜 나눠지지 **않는지** 이해합니다.

## waypoint — 필요한 곳에만 L7

ztunnel은 연결만 봅니다(L4). "경로가 /api/products면", "10%는 저쪽으로", "3초 늦춰라" 같은 **HTTP 수준의 일**은 waypoint가 합니다. waypoint는 Envoy이고, **Gateway API의 Gateway 리소스**로 만듭니다 — 1일차에 만든 입구 Gateway와 같은 종류, 클래스만 `istio-waypoint`입니다.

```bash
cat ~/devops-lab/k8s/w4d4/deploy/waypoint.yaml
```

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: waypoint
  namespace: devmart
  labels:
    istio.io/waypoint-for: service       # Service로 가는 트래픽을 맡는다
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
```

| | 1일차 입구 Gateway | 오늘 waypoint |
|---|---|---|
| gatewayClassName | `eg` (Envoy Gateway) | `istio-waypoint` (Istio) |
| 받는 트래픽 | 밖에서 들어오는 HTTP (NodePort 30080) | 메시 안에서 **Service로 가는** HBONE |
| 붙는 라우트의 parentRef | 이 Gateway | **Service** (아래 실습 9) |

그리고 네임스페이스에 "이 네임스페이스의 Service 트래픽은 waypoint를 거쳐라"라는 라벨을 붙입니다 — 2교시에 주석으로 남겨 둔 줄입니다.

## 실습 8 · waypoint 만들기 (커밋)

```bash
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d4/deploy/waypoint.yaml devmart/
sed -i 's/^    # istio.io\/use-waypoint/    istio.io\/use-waypoint/' devmart/namespace.yaml     # Mac: sed -i ''
sed -i 's/^  - devmart-rules.yaml.*/&\n  - waypoint.yaml/' devmart/kustomization.yaml          # Mac: 편집기로 resources 끝에
git diff
git add . && git commit -m "devmart에 waypoint (L7)" && git push
sleep 60
kubectl get gateway -n devmart
istioctl ztunnel-config workloads | grep -E "NAMESPACE|catalog-api"
```

> **🟢 확인: 확인**
>
> ```text
> NAME       CLASS            ADDRESS        PROGRAMMED   AGE
> devmart    eg                              True         3d
> waypoint   istio-waypoint   10.96.88.140   True         40s
> NAMESPACE  POD NAME                      ADDRESS      NODE             WAYPOINT  PROTOCOL
> devmart    catalog-api-5d8c7b9f6-2xkq4   10.244.1.15  devmart-worker   waypoint  HBONE
> ```
> 같은 네임스페이스에 Gateway가 둘입니다 — 1일차의 입구(`eg`)와 오늘의 waypoint. **WAYPOINT** 칸에 이름이 찍혔습니다. `kubectl get pods -n devmart | grep waypoint`로 waypoint Pod(Envoy)도 보입니다. Argo CD 화면의 나무에도 waypoint Gateway가 새로 보입니다.

## 실습 9 · 메시 안의 손님

입구(30080)로 오는 요청은 Envoy Gateway가 **Pod IP로 바로** 보냅니다 — Service를 거치지 않으니 waypoint도 거치지 않습니다. 메시 안 호출을 흉내 낼 손님 Pod를 devmart 안에 둡니다.

```bash
kubectl run client -n devmart --image=curlimages/curl:8.17.0 --restart=Never -- sleep infinity
kubectl wait -n devmart --for=condition=Ready pod/client
cd ~/devops-lab/k8s/w4d4
cat test/load.sh
./test/load.sh 50
```

> **🟢 확인: 확인**
>
> ```text
>      50 "version":"2.0.0"
> ```

> [!TIP]
> **client는 왜 kubectl run으로?**
>
> 시험용 손님이라 Git에 넣지 않습니다. Argo CD의 **추적 표시가 없으므로** prune이 지우지도 않고, selfHeal이 건드리지도 않습니다(3일차 6교시). 다 쓰면 7교시에 직접 지웁니다.

## 실습 10 · 90/10 나누기 (커밋)

카나리 Deployment(같은 이미지, `APP_VERSION=2.1.0-canary`)와 두 Service, 그리고 나누는 규칙을 넣습니다.

```bash
cat deploy/catalog-split.yaml
```

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: catalog-split
  namespace: devmart
spec:
  parentRefs:
    - group: ""
      kind: Service            # Gateway가 아니라 Service가 부모 — "catalog-api로 가는 호출에 대한 규칙"
      name: catalog-api
      port: 8000
  rules:
    - backendRefs:
        - name: catalog-api-stable     # 기존 Pod만 고르는 Service
          port: 8000
          weight: 90
        - name: catalog-api-canary     # 카나리 Pod만 고르는 Service
          port: 8000
          weight: 10
```

> [!IMPORTANT]
> **Gateway API의 두 쓰임새**
>
> 1일차 HTTPRoute의 parentRef는 **입구 Gateway**였습니다(남북). 오늘은 **Service**입니다(동서) — "누가 catalog-api를 부르든, 그 호출을 이렇게 나눠라". 같은 HTTPRoute 문법을 메시에도 쓰자는 Gateway API의 작업 이름이 **GAMMA**입니다. 1일차에 익힌 것이 그대로 쓰입니다.

```bash
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d4/deploy/catalog-api-canary.yaml ~/devops-lab/k8s/w4d4/deploy/catalog-split.yaml devmart/
ID=$(gh api user -q .login | tr 'A-Z' 'a-z')
sed -i "s/YOUR_ID/$ID/g" devmart/catalog-api-canary.yaml                                       # Mac: sed -i ''
sed -i 's/^  - waypoint.yaml.*/&\n  - catalog-api-canary.yaml\n  - catalog-split.yaml/' devmart/kustomization.yaml
git add . && git commit -m "catalog-api 카나리 10% (메시 안 호출)" && git push
sleep 60
kubectl get pods -n devmart -l app=catalog-api-canary
cd ~/devops-lab/k8s/w4d4 && ./test/load.sh 100
```

> **🟢 확인: 확인**
>
> ```text
> NAME                                  READY   STATUS    RESTARTS   AGE
> catalog-api-canary-7b9c8d6f5-x2q4w    1/1     Running   0          45s
>      91 "version":"2.0.0"
>       9 "version":"2.1.0-canary"
> ```
> 정확히 90/10이 아니라 **확률**입니다(1일차 카나리와 같다). 여러 번 돌려 봅니다.

> [!TIP]
> **카나리 이미지의 태그**
>
> `catalog-api-canary.yaml`의 이미지 태그는 `YOUR_SHA` 그대로여도 됩니다. 이미지 **이름**이 kustomization의 `images:`와 같으므로 태그는 거기서 정해집니다(3일차 2교시). CI가 태그를 바꾸면 카나리도 함께 바뀝니다.

### 입구에서는?

```bash
for i in $(seq 20); do curl -s localhost:30080/api/info | grep -o '"version":"[^"]*"'; done | sort | uniq -c
```

> **🟢 확인: 확인**
>
> ```text
>      20 "version":"2.0.0"
> ```
> 입구에서 온 요청은 **나눠지지 않습니다.** Envoy Gateway가 `catalog-api` Service의 **Pod 목록**(EndpointSlice)을 직접 보고 보내기 때문에, Service에 붙은 규칙(waypoint)을 거치지 않습니다. 손님에게 카나리를 보이려면 1일차처럼 **입구의 HTTPRoute**에서 나눕니다. **남북은 입구에서, 동서는 메시에서** — 같은 Gateway API로.

Kiali 지도(Traffic Graph, Display → **Traffic Distribution** 켜기)에서 client → waypoint → catalog-api-stable / catalog-api-canary로 갈라지는 선과 **퍼센트**가 보입니다. 이제 선에 HTTP 요청 수와 응답 코드가 붙습니다 — waypoint가 L7이기 때문입니다.

> **❓ 오해 — 메시가 있으면 입구 Gateway는 필요 없다**
>
> Istio도 입구 Gateway를 만들 수 있으므로 하나로 합칠 수는 있습니다. 하지만 입구와 메시는 **책임이 다릅니다** — 입구는 TLS 인증서 · 도메인 · 외부 공격 방어, 메시는 서비스 사이 신원 · 정책. 오늘처럼 서로 다른 제품을 써도 Gateway API라는 **공통 언어** 덕분에 함께 쓸 수 있습니다.

> **🎓 학술 노트 — 점진적 배포의 통계**
>
> 카나리에 10%만 보내는 이유는 "문제가 있어도 피해를 10%로 제한"하는 것이지만, 동시에 **판단에 필요한 표본**을 모으는 일이기도 합니다. 요청 100건 중 9건으로는 오류율 1%와 5%를 구별하기 어렵습니다. 구글의 *Site Reliability Workbook*(2018) 16장 *Canarying Releases*는 카나리 기간 · 비율을 **통계적으로 의미 있는 차이를 볼 수 있을 만큼** 정하라고 권합니다 — 2일차의 SLO와 어제의 Argo Rollouts 분석 단계가 그 판단을 자동화합니다.

> **📈 트렌드 2026 — Gateway API로 하나 된 문법**
>
> Gateway API v1.x에서 **메시(GAMMA)용 HTTPRoute**가 표준 기능으로 자리 잡으면서, Istio · Linkerd · Cilium이 같은 HTTPRoute를 읽습니다. 메시 제품을 바꿔도 라우팅 규칙은 그대로 둘 수 있게 된 것입니다. Istio 고유 API(VirtualService)는 Gateway API에 아직 없는 기능(5교시 장애 주입 등)에만 쓰는 쪽으로 권장이 바뀌었습니다.

> **✅ 확인 문제**
>
> 1. waypoint는 어떤 리소스로 만들고, 1일차 Gateway와 무엇이 다른가요?
> 2. HTTPRoute의 parentRef가 Service라는 것은 무슨 뜻인가요?
> 3. 입구로 들어온 요청이 90/10으로 나눠지지 않은 이유는?
> 4. 시험용 client Pod를 Git에 넣지 않아도 Argo CD가 지우지 않는 이유는?
>
> <details><summary>정답</summary>
>
> 1. Gateway API의 Gateway. gatewayClassName이 istio-waypoint이고, 밖이 아니라 메시 안에서 Service로 가는 트래픽을 받는다
> 2. 누가 부르든 그 Service로 가는 호출에 이 규칙을 적용한다 (동서, GAMMA)
> 3. Envoy Gateway가 Service를 거치지 않고 Pod IP로 바로 보내 waypoint를 지나지 않기 때문
> 4. Argo CD의 추적 표시가 없어 관리 대상이 아니기 때문
>
> </details>

## 참고 문헌

- Istio Docs. *Ambient — Configure waypoint proxies*, *Traffic shifting (Gateway API)*. istio.io
- Gateway API. *GAMMA initiative — Service mesh support*. gateway-api.sigs.k8s.io/mesh
- Beyer, B. 외 (2018). *The Site Reliability Workbook*, Ch. 16 "Canarying Releases". O'Reilly.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [3교시 · mTLS 확인과 Kiali](lesson-03.md) | [⬆️ 4일차 목차](README.md) | [5교시 · 장애 주입 · 타임아웃 · 재시도](lesson-05.md) ➡️ |
