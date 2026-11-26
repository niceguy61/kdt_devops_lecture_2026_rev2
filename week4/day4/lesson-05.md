[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [4일차](README.md)

# 5교시 · 장애 주입 · 타임아웃 · 재시도

> [!NOTE]
> **이번 시간에 할 일**
>
> - **장애 주입**(fault injection)이 무엇이고 왜 일부러 하는지 이해합니다.
> - catalog-api 호출을 **3초 늦추고**, 주문이 어떻게 실패하는지 Grafana · Kiali · 로그로 봅니다.
> - 호출의 **50%를 실패**시켜 봅니다.
> - **타임아웃 · 재시도**를 코드가 아니라 메시에 두는 법과 그 함정을 익힙니다.

## 왜 일부러 망가뜨리나

3주차 5일차에는 `break.sh`로 장애를 만들었습니다 — Secret을 틀리게, redis를 0개로. 그 장애들은 "**완전히 죽음**"이었습니다. 실제 운영에서 더 자주, 더 고약하게 오는 것은 "**느려짐**"과 "**가끔 실패**"입니다. 그때 우리 서비스가 어떻게 행동하는지는 **미리 해 보지 않으면 모릅니다.**

| 질문 | 장애 주입으로 답한다 |
|---|---|
| catalog가 3초 늦어지면 주문은? | 기다리나, 포기하나, 몇 초 만에? |
| catalog가 절반만 성공하면? | 손님은 몇 %를 실패로 보나? |
| 대시보드 · 알림이 그것을 잡나? | 2일차에 만든 규칙이 울리나? |

메시로 장애를 주입하면 **앱 코드 · 이미지는 그대로**이고, 특정 호출(order-api → catalog-api)에만, 원하는 비율로, Git 커밋 하나로 넣고 뺄 수 있습니다.

## 실습 11 · 먼저 나누기를 걷어 내기

같은 Service(catalog-api)에 HTTPRoute와 VirtualService를 **동시에 붙이면** 어느 것이 이길지 헷갈립니다. 4교시의 나누기를 Git에서 지웁니다(prune이 클러스터에서도 지운다).

```bash
cd ~/devmart-deploy
git rm -q devmart/catalog-split.yaml devmart/catalog-api-canary.yaml
sed -i '/  - catalog-split.yaml/d; /  - catalog-api-canary.yaml/d' devmart/kustomization.yaml    # Mac: sed -i '' …
git commit -am "카나리 실험 끝 — 나누기 제거" && git push
sleep 60; kubectl get httproute,deploy -n devmart | grep -E "split|canary" || echo "깨끗함"
```

## 실습 12 · 3초 늦추기 (커밋)

```bash
cat ~/devops-lab/k8s/w4d4/deploy/catalog-fault.yaml
```

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: catalog-fault
  namespace: devmart
spec:
  hosts:
    - catalog-api
  http:
    - fault:
        delay:
          percentage: { value: 100 }
          fixedDelay: 3s                 # order-api의 CATALOG_TIMEOUT(2초)보다 길게
      route:
        - destination:
            host: catalog-api
```

> [!IMPORTANT]
> **왜 VirtualService인가**
>
> Gateway API에는 아직 **장애 주입이 없습니다.** 그래서 Istio 고유의 VirtualService를 씁니다. 4교시 트렌드에서 본 권장 — "Gateway API에 없는 기능에만 VirtualService" — 의 예입니다. ambient에서 VirtualService는 waypoint가 처리합니다.

화면을 셋 띄웁니다 — Grafana DevMart 대시보드(어제, 시간 범위 Last 15 minutes · 10초 새로 고침), Kiali Traffic Graph, 터미널.

```bash
# 터미널 A — 손님: 1초마다 상품 목록과 주문
while true; do
  p=$(curl -s -o /dev/null -w '%{http_code}' localhost:30080/api/products)
  o=$(curl -s -o /dev/null -w '%{http_code} %{time_total}s' -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}')
  echo "$(date +%T) products=$p orders=$o"; sleep 1
done
```

```bash
# 터미널 B — 장애 넣기
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d4/deploy/catalog-fault.yaml devmart/
sed -i 's/^  - waypoint.yaml.*/&\n  - catalog-fault.yaml/' devmart/kustomization.yaml
git add . && git commit -m "장애 주입: catalog 3초 지연" && git push
```

> **🟢 확인: 확인 — 터미널 A (1분 안에)**
>
> ```text
> 14:20:11 products=200 orders=202 0.041s
> 14:20:12 products=200 orders=202 0.038s
> 14:20:51 products=200 orders=503 2.012s
> 14:20:54 products=200 orders=503 2.009s
> …
> ```
> - **orders는 503, 정확히 약 2초** — order-api가 catalog를 2초(`CATALOG_TIMEOUT`) 기다리다 포기하고 "catalog unavailable"을 돌려줍니다. 앱의 타임아웃 설정이 **실제로 동작하는지**를 처음으로 확인했습니다.
> - **products는 200 그대로** — 입구 → catalog-api는 waypoint를 거치지 않으므로(4교시) 지연이 걸리지 않았습니다. 장애가 **동서 호출에만** 들어갔습니다.

> **🟢 확인: 확인 — Grafana · Kiali**
>
> - Grafana: `orders` 라우트의 **오류율이 치솟고**, p95 응답 시간이 **약 2초**에 붙습니다. `catalog` 라우트는 평평합니다. 2분쯤 지나면 어제의 알림 `DevMartHighErrorRate`가 Pending → **Firing**이 됩니다(Alertmanager 화면).
> - Kiali: order-api → catalog-api 선의 응답 시간이 3초대로, 선 색이 바뀝니다.

```bash
kubectl logs -n devmart deploy/order-api --tail=3
kubectl logs -n devmart -l gateway.networking.k8s.io/gateway-name=waypoint --tail=2
```

> **🟢 확인: 확인**
>
> ```text
> {"event": "catalog_error", "request_id": "…", "error": "timed out", …}
> [2026-11-26T05:20:54.102Z] "GET /api/products/1 HTTP/1.1" 0 DI downstream_remote_disconnect … 2001 - "-" "Python-urllib/3.14" … catalog-api.devmart.svc.cluster.local …
> ```
> waypoint의 접근 로그(2교시의 `accessLogFile`)에 **`DI`**(Delay Injected) 표시가 있습니다. 앱 로그의 request_id로 같은 요청을 이어 볼 수 있습니다(2일차 세 기둥).

## 실습 13 · 1초 지연 — 느리지만 성공

```bash
sed -i 's/fixedDelay: 3s/fixedDelay: 1s/' devmart/catalog-fault.yaml       # Mac: sed -i ''
git commit -am "장애 주입: 1초 지연" && git push
```

> **🟢 확인: 확인 — 터미널 A**
>
> ```text
> 14:24:02 products=200 orders=202 1.043s
> 14:24:03 products=200 orders=202 1.039s
> ```
> 이번에는 **성공하지만 느립니다.** 오류율 그래프는 내려가고, p95만 1초대에 머뭅니다. 알림은 Resolved가 되고, `DevMartSlowResponses`(2일차)가 기준에 걸리는지 봅니다. "**성공했지만 느린 것**"은 오류율만 보는 알림으로는 잡히지 않습니다 — RED의 D를 따로 보는 이유입니다.

## 실습 14 · 50% 실패

`fault` 블록을 지연 대신 **중단(abort)**으로 바꿉니다. 편집기로 `devmart/catalog-fault.yaml`을 엽니다.

```yaml
    - fault:
        abort:
          percentage: { value: 50 }
          httpStatus: 503
```

```bash
git commit -am "장애 주입: 50% 503" && git push
```

> **🟢 확인: 확인 — 터미널 A**
>
> ```text
> 14:27:10 products=200 orders=202 0.039s
> 14:27:11 products=200 orders=503 0.012s
> 14:27:12 products=200 orders=503 0.010s
> 14:27:13 products=200 orders=202 0.041s
> ```
> 실패가 **빨라졌습니다**(0.01초) — 기다리지 않고 바로 503이 오기 때문입니다. 손님 입장에서 "느린 실패"와 "빠른 실패" 중 무엇이 나을까요? 대개 **빠른 실패**입니다 — 다시 시도하거나 다른 길로 갈 수 있으니까요. 이것이 아래 타임아웃의 동기입니다.

## 실습 15 · 타임아웃과 재시도를 메시에

장애를 걷어 내고, 평소에 둘 **회복 설정**으로 바꿉니다.

```bash
git rm -q devmart/catalog-fault.yaml
cp ~/devops-lab/k8s/w4d4/deploy/catalog-timeout.yaml devmart/
sed -i 's/  - catalog-fault.yaml/  - catalog-timeout.yaml/' devmart/kustomization.yaml
git add . && git commit -m "장애 주입 끝 · catalog 호출에 타임아웃 1초 + 재시도 2번" && git push
cat devmart/catalog-timeout.yaml
```

```yaml
  http:
    - timeout: 1s                        # 1초 넘게 걸리면 끊는다
      retries:
        attempts: 2                      # 실패하면 두 번 더
        perTryTimeout: 400ms
        retryOn: 5xx,connect-failure,reset
```

> **🟢 확인: 확인**
>
> 터미널 A가 다시 `orders=202 0.04s`로 돌아오고, Grafana의 오류율이 0으로 내려갑니다. 알림은 Resolved. 터미널 A는 `Ctrl+C`로 멈춥니다.

| 설정 | 앱 코드 (`CATALOG_TIMEOUT` · `CATALOG_RETRIES`) | 메시 (VirtualService) |
|---|---|---|
| 바꾸려면 | 환경 변수 → 롤아웃 | 커밋 → waypoint가 즉시 |
| 적용 범위 | 그 앱 하나 | catalog-api를 **부르는 모두** |
| 언어 | 앱마다 다시 구현 | 상관없음 |
| 아는 것 | 업무 맥락 ("이 호출은 재시도해도 안전한가") | 모른다 |

> [!WARNING]
> **재시도는 곱해진다**
>
> 앱이 2번, 메시가 2번 재시도하면 catalog는 최악의 경우 (1+2)×(1+2) = **9번** 불립니다. catalog가 이미 과부하라 느린 것이라면, 재시도가 부하를 9배로 키워 **완전히 쓰러뜨립니다**(재시도 폭풍). 규칙은 두 가지입니다. ① 재시도는 **한 층에서만** — 메시에 두었다면 앱의 `CATALOG_RETRIES`는 0으로. ② **안전한 요청만** — 상품 조회(GET)는 몇 번 다시 해도 같지만, 주문 생성(POST)을 재시도하면 **주문이 두 번** 생길 수 있습니다(2주차의 멱등성).

> **🎓 학술 노트 — 카오스 공학과 재시도 폭풍**
>
> 일부러 장애를 넣어 시스템의 반응을 확인하는 방법은 넷플릭스의 Chaos Monkey(2011)에서 시작해 Basiri 외의 *Chaos Engineering*(IEEE Software, 2016)으로 원칙이 정리되었습니다 — "정상 상태를 가설로 세우고, 실제와 비슷한 사건을 주입하고, 차이를 본다." 오늘의 "products는 200 그대로, orders는 2초에 503"이 바로 그 가설 검증입니다. 재시도가 장애를 키우는 현상은 Huang 외의 *Metastable Failures in Distributed Systems*(HotOS 2021) · Bronson 외(OSDI 2022)가 **준안정 장애**(metastable failure)로 정리했습니다 — 원인이 사라져도 재시도 부하 때문에 시스템이 회복하지 못하는 상태입니다.

> **📈 트렌드 2026 — 카오스를 파이프라인에**
>
> 장애 주입은 "가끔 하는 행사"에서 **배포 파이프라인의 한 단계**로 옮겨 가고 있습니다. Chaos Mesh · LitmusChaos(CNCF) 실험을 GitOps로 관리하고, AWS Fault Injection Service는 EKS의 Pod 장애 · 네트워크 지연을 관리형으로 제공합니다. 5주차에 EKS를 만들면 같은 실험을 클라우드에서 할 수 있습니다.

> **✅ 확인 문제**
>
> 1. 3초 지연에서 주문이 정확히 약 2초에 503이 된 이유는?
> 2. 같은 지연이 products에는 영향을 주지 않은 이유는?
> 3. "느린 실패"보다 "빠른 실패"가 나은 이유는?
> 4. 앱과 메시가 모두 재시도하면 생기는 문제와, POST를 재시도하면 생기는 문제는?
>
> <details><summary>정답</summary>
>
> 1. order-api의 CATALOG_TIMEOUT이 2초라 그만큼 기다리다 포기했기 때문
> 2. 입구 → catalog-api는 waypoint를 거치지 않아 VirtualService가 적용되지 않기 때문
> 3. 손님 · 앱이 기다리며 자원을 잡지 않고, 곧바로 다시 시도하거나 다른 길로 갈 수 있다
> 4. 재시도가 곱해져 부하가 폭증한다(재시도 폭풍). POST는 주문이 중복으로 생길 수 있다
>
> </details>

## 참고 문헌

- Istio Docs. *Fault Injection*, *Request Timeouts*, *Retries*. istio.io/latest/docs/tasks/traffic-management
- Basiri, A. 외 (2016). *Chaos Engineering*. IEEE Software 33(3).
- Huang, L. 외 (2021). *Metastable Failures in Distributed Systems*. HotOS '21.
- Bronson, N. 외 (2022). *Metastable Failures in the Wild*. OSDI '22.

---

⬅️ 이전: [4교시 · waypoint와 트래픽 나누기](lesson-04.md) &nbsp;|&nbsp; [⬆️ 4일차 목차](README.md) &nbsp;|&nbsp; 다음: [6교시 · mTLS STRICT와 호출 허가](lesson-06.md) ➡️
