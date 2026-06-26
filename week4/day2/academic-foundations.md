# Academic Foundations: W4D2 Kubernetes Traffic

## 1. Docker에서 Kubernetes로 바뀌는 지점
Docker Compose에서는 외부 traffic을 보통 `ports`와 reverse proxy 설정으로 이해했다.

```yaml
services:
  frontend:
    ports:
      - "8080:80"
  api:
    expose:
      - "8080"
```

이 구조에서 중요한 질문은 "host port가 어느 container port로 가는가"였다.

Kubernetes에서는 질문이 더 세분화된다.

```text
누가 외부 traffic을 받는가?
  -> Gateway implementation

어떤 listener를 열 것인가?
  -> Gateway

어떤 host/path를 어느 Service로 보낼 것인가?
  -> HTTPRoute

Service 뒤에 실제 Ready Pod가 있는가?
  -> EndpointSlice
```

즉 Kubernetes traffic model은 단순 port binding이 아니라 `선언된 routing 의도`와 `그 의도를 반영하는 controller`가 분리된 구조다.

## 2. Traffic은 여러 번 라우팅된다
외부 traffic은 한 번에 Pod로 가지 않는다.

```text
외부 사용자
  -> Envoy Gateway data plane
  -> Gateway listener
  -> HTTPRoute rule
  -> Service
  -> EndpointSlice
  -> Ready Pod IP:containerPort
```

내부 통신은 Gateway를 거치지 않고 Service DNS로 간다.

```text
frontend Pod
  -> http://api.week4.svc.cluster.local
  -> api Service
  -> api EndpointSlice
  -> api Pod
```

이 두 흐름을 섞으면 장애 분석이 꼬인다. 내부 DNS 문제가 아닌데 Gateway를 고치거나, HTTPRoute 문제가 아닌데 Pod log만 보는 식의 삽질이 생긴다.

## 3. Service와 EndpointSlice
Service는 stable virtual endpoint다. Pod IP는 바뀌지만 Service 이름과 ClusterIP는 안정적으로 유지된다.

| 요소 | 역할 |
|---|---|
| Pod label | Service가 Pod를 찾는 기준 |
| Service selector | 어떤 label의 Pod를 backend로 볼지 결정 |
| EndpointSlice | 실제 traffic을 받을 Ready Pod IP 목록 |
| Service port | client가 호출하는 port |
| targetPort | Service port가 Pod의 어느 containerPort로 갈지 결정 |

Service가 있어도 EndpointSlice가 비면 traffic은 갈 곳이 없다.

```text
Service exists
EndpointSlice empty
  -> 이름은 있지만 backend가 없음
```

## 4. DNS 이름
같은 namespace에서는 짧은 이름으로 접근할 수 있다.

```text
http://api
```

다른 namespace까지 명시하려면 다음 형태를 쓴다.

```text
http://api.week4.svc.cluster.local
```

DNS가 되려면 CoreDNS가 정상이어야 하고, NetworkPolicy를 적용할 때 DNS egress를 막지 않아야 한다.

## 5. Gateway API와 Envoy Gateway
Gateway API는 Kubernetes의 traffic routing API다. Ingress보다 역할이 더 명확하게 나뉜다.

| 리소스 | 의미 |
|---|---|
| GatewayClass | 어떤 controller 구현체가 Gateway를 처리할지 지정 |
| Gateway | listener, port, protocol, route attach 정책 |
| HTTPRoute | host/path/header 같은 HTTP routing rule |
| Service | 실제 backend 안정 진입점 |
| EndpointSlice | Ready Pod IP 목록 |

Envoy Gateway는 Gateway API를 구현하는 controller다. 사용자는 Gateway와 HTTPRoute를 선언하고, Envoy Gateway가 이를 Envoy proxy 설정과 data plane으로 반영한다.

```text
GatewayClass: envoy
  -> Envoy Gateway controller가 처리
Gateway: port 80 listener
  -> 어떤 traffic을 받을지 선언
HTTPRoute: /api -> api Service
  -> 어디로 보낼지 선언
```

## 6. Ingress와 Gateway API 비교
NGINX Ingress Controller는 현업에서 여전히 자주 보인다. 그러나 이번 수업의 표준 실습은 Gateway API다.

| 기준 | Ingress | Gateway API |
|---|---|---|
| 핵심 리소스 | Ingress | GatewayClass, Gateway, HTTPRoute |
| 역할 분리 | 비교적 단순 | infra owner와 app owner 역할 분리 가능 |
| routing 확장성 | annotation 의존이 많아질 수 있음 | Route 종류와 policy 확장 구조 |
| 수업 기준 | 비교 언급 | 직접 실습 |

수업에서는 이렇게 설명한다.

```text
Ingress는 오래 쓰인 단순한 외부 HTTP routing API다.
Gateway API는 그 경험을 바탕으로 역할과 확장성을 더 명확히 나눈 새 traffic API다.
```

## 7. host/path routing
W4D2 실습은 다음 routing을 사용한다.

| 요청 | 이동 |
|---|---|
| `http://paperclip.local/` | frontend Service |
| `http://paperclip.local/api` | api Service |

local DNS를 바꾸기 어렵다면 `curl -H "Host: paperclip.local" http://localhost:8080/api`처럼 Host header를 직접 넣어 확인한다.

## 8. NetworkPolicy와 Cilium preview
NetworkPolicy는 Pod 간 통신 허용선을 선언한다. 하지만 실제 packet 차단은 CNI plugin이 수행한다.

| 환경 | 주의 |
|---|---|
| kind 기본 CNI | NetworkPolicy enforcement가 기대처럼 동작하지 않을 수 있음 |
| Calico/Cilium | NetworkPolicy enforcement 가능 |
| cloud managed cluster | provider/CNI 설정 확인 필요 |

Cilium은 eBPF 기반 CNI로 NetworkPolicy, CiliumNetworkPolicy, service/network observability를 제공한다. Hubble은 Cilium 위에서 flow와 service dependency를 관찰하는 도구다.

오늘은 Cilium을 깊게 설치하지 않아도 다음 관점을 가져간다.

```text
Service/DNS/Endpoint가 정상이어도
NetworkPolicy/CNI가 packet을 막으면 timeout이 날 수 있다.

Prometheus/Grafana가 resource metric을 보여준다면
Hubble은 network flow와 dependency를 보여줄 수 있다.
```

## 9. 장애를 나누어 본다
Gateway 장애는 한 단어로 “안 됨”이라고 쓰면 해결이 어렵다.

| 증상 | 원인 후보 |
|---|---|
| 404 | host/path rule 불일치, HTTPRoute가 attach되지 않음 |
| 503 | Service endpoint 없음, readiness 실패 |
| connection refused | port-forward, LoadBalancer/NodePort, Envoy data plane 접근 문제 |
| timeout | NetworkPolicy, backend 지연, Gateway data plane 문제 |
| DNS failure | service name 오타, CoreDNS, NetworkPolicy DNS 차단 |

## 10. 수업에서 고정할 운영 문장
```text
Gateway API는 외부 traffic의 의도를 선언한다.
Envoy Gateway는 그 의도를 실제 proxy/data plane으로 반영한다.
Service는 Pod IP 변화를 숨긴다.
EndpointSlice는 Ready Pod 목록이다.
NetworkPolicy/CNI는 packet 허용선을 결정한다.
```
