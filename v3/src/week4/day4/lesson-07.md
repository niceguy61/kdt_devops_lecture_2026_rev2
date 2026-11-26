# 7교시 · 메시 운영 판단

!!! goal "이번 시간에 할 일"
    - 오늘 더한 메시가 **얼마나 비싼지** 직접 잽니다.
    - 메시가 **필요 없는 경우**와 대안을 정리합니다.
    - 메시의 **업그레이드**가 왜 어려운지, 어떻게 하는지 압니다.
    - 실험용 손님을 정리하고, 내일까지 남길 것을 정합니다.

## 실습 19 · 비용 재기

2일차의 Prometheus로 잽니다(<http://localhost:9090>).

```promql
sum by (namespace) (container_memory_working_set_bytes{namespace=~"istio-system|devmart|argocd|monitoring", container!=""}) / 1024 / 1024
```

```promql
sum by (pod) (container_memory_working_set_bytes{namespace=~"istio-system|devmart", pod=~"istiod.*|ztunnel.*|istio-cni.*|waypoint.*|kiali.*", container!=""}) / 1024 / 1024
```

!!! check "확인 (값은 환경마다 다르다)"
    ```text
    {namespace="monitoring"}    1180
    {namespace="argocd"}         410
    {namespace="istio-system"}   330
    {namespace="devmart"}        620
    …
    {pod="istiod-…"}            110
    {pod="ztunnel-…"}            14   (× 3)
    {pod="istio-cni-node-…"}     40   (× 3)
    {pod="waypoint-…"}           35
    {pod="kiali-…"}              60
    ```
    배움일기에 적을 숫자입니다. 같은 일을 sidecar 모드로 했다면 devmart의 Pod 9개마다 Envoy(Pod당 수십 MB)가 붙었을 것입니다.

| 비용 | 오늘 본 것 | 운영에서 |
|---|---|---|
| **자원** | 메모리 수백 MB | 노드 수 · Pod 수에 비례 — sidecar는 Pod 수, ambient는 노드 수 |
| **지연** | waypoint를 거치는 한 번 더 | 호출당 1ms 안팎 — 호출이 깊게 이어지면 쌓인다 |
| **복잡도** | 503의 원인이 하나 늘었다 (6교시) | 장애 조사 때 "앱인가 메시인가"를 먼저 가려야 한다 |
| **업그레이드** | 버전 경고 (2교시) | 클러스터 업그레이드 순서가 메시에 묶인다 |

## 메시가 필요한가 — 판단표

| 이런 상황이면 | 메시 대신 |
|---|---|
| 서비스가 몇 개뿐이고 한 팀이 다 안다 | 앱의 타임아웃 · 재시도 + 2일차의 관찰로 충분 |
| 암호화만 필요하다 | 앱 TLS, 또는 ambient의 **L4만**(ztunnel, waypoint 없이) |
| 남북 트래픽(입구)만 다룬다 | 1일차의 Gateway면 된다 |
| 네트워크 차단이 목적이다 | NetworkPolicy (내일) — 더 단순하고 싸다 |
| 서비스가 많고, 팀이 여럿이고, 규제로 **서비스 사이 암호화 · 접근 기록**이 요구된다 | **메시가 맞다** |

!!! myth "오해 — 마이크로서비스면 메시가 필수다"
    많은 회사가 메시 없이 마이크로서비스를 운영합니다. 메시는 **서비스 수 × 팀 수 × 보안 요구**가 커져서 "앱마다 같은 것을 구현하는 비용"이 "메시를 운영하는 비용"보다 커질 때 이득입니다. 오늘처럼 ambient의 L4(mTLS)부터 켜고, L7은 필요한 네임스페이스에만 waypoint를 두는 **단계적 도입**이 위험을 줄입니다.

## 다른 메시들

| | Istio | Linkerd | Cilium |
|---|---|---|---|
| 데이터 평면 | Envoy(waypoint) + ztunnel(Rust) | 자체 Rust 프록시(사이드카) | **eBPF**(커널) + Envoy |
| 강점 | 기능이 가장 넓다, Gateway API · ambient | 가볍고 단순하다 | 네트워크(CNI)와 메시를 한 도구로 |
| 오늘과 같은 것 | — | mTLS · 재시도 · 지표 | mTLS · L7 정책 · Gateway API |

어느 것을 고르든 **오늘의 개념 — 신원 · mTLS · 허가 · 나누기 · 장애 주입 — 은 같습니다.** 그리고 라우팅 규칙은 Gateway API(HTTPRoute)로 쓰면 제품을 바꿔도 남습니다.

## 업그레이드 — revision과 카나리

메시는 **모든 서비스 사이 통신의 길목**이라, 업그레이드가 잘못되면 전체가 끊깁니다. 그래서 Istio는 istiod를 **두 버전 동시에** 띄우는 방법(revision)을 씁니다.

1. 새 버전 istiod를 `revision=1-32`로 **옆에** 설치한다 (옛 것은 그대로).
2. 네임스페이스 하나만 새 revision으로 옮긴다 → 대시보드로 지켜본다.
3. 괜찮으면 나머지를 옮기고, 옛 istiod를 지운다.

3주차의 롤링 업데이트, 1일차의 카나리와 같은 생각을 **메시 자신**에게 적용한 것입니다. ztunnel(DaemonSet)은 노드 단위로 바뀌므로, 노드를 하나씩 비우며(drain) 올리는 방법도 함께 씁니다.

## 실습 20 · 정리

```bash
kubectl delete pod plain -n default
kubectl delete namespace outsider
kubectl delete pod client -n devmart
```

| 남긴다 (내일 · 5주차 대비) | 이유 |
|---|---|
| Istio(istiod · cni · ztunnel) · Kiali | 내일 보안 실습에서 신원을 쓴다 |
| devmart의 ambient 등록 · waypoint | 배포 저장소에 커밋되어 있다 |
| mTLS STRICT · catalog-api 허가 규칙 | 내일 ServiceAccount로 좁힌다 |
| catalog 타임아웃 · 재시도 | 평소의 회복 설정 |
| envoy-gateway-system 메시 등록 | STRICT를 유지하려면 필요 — `platform-changes.md`에 적었다 |

!!! warn "'5분 복구'에 더할 것"
    클러스터를 다시 만들 때 순서가 하나 늘었습니다: Secret → kps · Argo CD · **Istio 네 차트** `helm install` → `envoy-gateway-system` 라벨 → `kubectl apply -f root.yaml`(3일차 8교시). Istio가 Argo CD보다 **먼저** 있어야 devmart의 waypoint · 정책 리소스가 바로 적용됩니다(CRD가 없으면 Sync가 실패한다).

!!! academic "학술 노트 — 미들웨어의 순환"
    서비스 사이 통신의 공통 기능(재시도 · 보안 · 관찰)을 어디에 둘지는 오래된 질문입니다. 2000년대의 **ESB**(Enterprise Service Bus)는 그것을 중앙 버스에 두었다가 병목과 단일 장애점이 되었고, 마이크로서비스는 그 반동으로 "똑똑한 끝점, 멍청한 파이프"(Fowler & Lewis, 2014)를 외쳤습니다. 그러자 끝점마다 같은 코드(Netflix Hystrix · Ribbon 같은 라이브러리)가 쌓였고, 서비스 메시는 그것을 다시 **인프라로 끌어내린** 것입니다. Morgan(Buoyant, 2017)의 *What's a service mesh?*가 이 이름을 처음 널리 쓴 글입니다. 오늘의 ambient는 그 인프라를 다시 **노드 단위로** 모은 것 — 같은 질문에 대한 시대별 답입니다.

!!! trend "트렌드 2026 — 메시 위의 AI 트래픽"
    LLM 호출과 AI 에이전트의 도구 호출(MCP)이 서비스 사이 트래픽의 새 종류가 되면서, 메시가 **토큰 수 기반 제한 · 모델별 라우팅 · 프롬프트 기록**까지 맡으려 합니다. Istio 1.31의 agentgateway waypoint, Gateway API Inference Extension이 그 예입니다. 오늘 배운 "코드 밖에서 통신 규칙을 정한다"는 생각이 AI 트래픽에도 그대로 적용되고 있습니다.

!!! quiz "확인 문제"
    1. 메시의 비용 네 가지는?
    2. 메시 대신 NetworkPolicy가 더 나은 경우는?
    3. Istio를 revision으로 업그레이드하는 순서는?
    4. 클러스터 복구 때 Istio를 Argo CD Application보다 먼저 설치해야 하는 이유는?

    ??? answer "정답"
        1. 자원(메모리), 지연, 복잡도(장애 원인이 늘어남), 업그레이드 부담
        2. 목적이 네트워크 차단뿐일 때 — 더 단순하고 싸다
        3. 새 revision의 istiod를 옆에 설치 → 네임스페이스 하나 옮겨 지켜봄 → 나머지 옮김 → 옛 istiod 제거
        4. waypoint · AuthorizationPolicy 같은 Istio CRD가 없으면 Argo CD의 Sync가 실패하기 때문

## 참고 문헌

- Istio Docs. *Canary Upgrades (revisions)*, *Ambient — Upgrade*. istio.io
- Linkerd Docs. *Architecture*. linkerd.io · Cilium Docs. *Service Mesh*. docs.cilium.io
- Fowler, M. & Lewis, J. (2014). *Microservices*. martinfowler.com
- Morgan, W. (2017). *What's a service mesh? And why do I need one?* Buoyant blog.
- Gateway API. *Inference Extension*. gateway-api-inference-extension.sigs.k8s.io
