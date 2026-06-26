# Academic Foundations: W4D2 Kubernetes Traffic

## 1. Traffic은 여러 번 라우팅된다
Kubernetes에서 사용자의 요청은 한 번에 Pod로 가지 않는다.

```text
외부 사용자
  -> Ingress Controller
  -> Ingress rule
  -> Service
  -> Endpoint
  -> Pod IP:containerPort
```

내부 통신은 Ingress를 거치지 않고 Service DNS로 간다.

```text
frontend Pod
  -> http://api.week4.svc.cluster.local
  -> api Service
  -> api Endpoint
  -> api Pod
```

## 2. Service와 Endpoint
Service는 stable virtual endpoint다. Pod IP는 바뀌지만 Service 이름과 ClusterIP는 안정적으로 유지된다.

| 요소 | 역할 |
|---|---|
| Pod label | Service가 Pod를 찾는 기준 |
| Service selector | 어떤 label의 Pod를 backend로 볼지 결정 |
| Endpoint/EndpointSlice | 실제로 traffic을 받을 Pod IP 목록 |
| targetPort | Service port가 Pod의 어느 containerPort로 갈지 결정 |

Service가 있어도 Endpoint가 비면 traffic은 갈 곳이 없다.

## 3. DNS 이름
같은 namespace에서는 짧은 이름으로 접근할 수 있다.

```text
http://api
```

다른 namespace까지 명시하려면 다음 형태를 쓴다.

```text
http://api.week4.svc.cluster.local
```

DNS가 되려면 CoreDNS가 정상이어야 하고, NetworkPolicy를 적용할 때 DNS egress를 막지 않아야 한다.

## 4. Ingress와 Ingress Controller
Ingress는 rule이고, Ingress Controller는 그 rule을 실제 proxy 설정으로 반영하는 controller다.

| 구분 | 의미 |
|---|---|
| Ingress object | host/path/backend rule |
| Ingress Controller | rule을 읽고 외부 traffic을 Service로 전달 |
| ingressClassName | 어떤 controller가 이 rule을 처리할지 결정 |
| ingress-nginx | NGINX 기반 Ingress Controller 구현체 |

Ingress object만 만들고 controller가 없으면 외부 traffic은 처리되지 않는다.

## 5. host/path routing
W4D2 실습은 다음 routing을 사용한다.

| 요청 | 이동 |
|---|---|
| `http://paperclip.local/` | frontend Service |
| `http://paperclip.local/api` | api Service |

local DNS를 바꾸기 어렵다면 `curl -H "Host: paperclip.local" http://localhost:8080/api`처럼 Host header를 직접 넣어 확인한다.

## 6. NetworkPolicy preview
NetworkPolicy는 Pod 간 통신 허용선을 선언한다. 하지만 모든 CNI가 NetworkPolicy enforcement를 지원하는 것은 아니다. kind 기본 CNI에서는 정책이 강제되지 않을 수 있으므로 오늘은 운영 개념 preview로 다룬다.

기본 Kubernetes namespace는 이름과 권한 범위를 나누는 논리적 경계다. 별도 NetworkPolicy가 없다면 많은 CNI 환경에서 서로 다른 namespace의 Pod도 Service DNS로 통신할 수 있다. 그래서 "namespace가 다르니까 자동으로 막힌다"라고 설명하면 안 된다.

NetworkPolicy는 이 기본 상태를 바꿔서 "어떤 Pod가 어떤 Pod로 들어가거나 나갈 수 있는가"를 label 기준으로 제한한다. 같은 namespace의 Pod는 `podSelector`로 고르고, 다른 namespace까지 조건에 넣으려면 `namespaceSelector`를 함께 사용한다.

| 선택자 | 의미 |
|---|---|
| `podSelector` | 기본적으로 policy가 있는 namespace 안의 Pod 선택 |
| `namespaceSelector` | 다른 namespace 또는 특정 namespace 집합 선택 |
| `namespaceSelector` + `podSelector` | 특정 namespace 안의 특정 Pod 선택 |
| `ipBlock` | cluster 외부 IP 대역 또는 특정 CIDR 선택 |

실무 기준의 의도는 다음과 같다.

```text
frontend -> api 허용
api -> db 허용
frontend -> db 차단
DNS egress 허용
```

## 7. 장애를 나누어 본다
Ingress 장애는 한 단어로 “안 됨”이라고 쓰면 해결이 어렵다.

| 증상 | 원인 후보 |
|---|---|
| 404 | host/path rule 불일치, class 처리 안 됨 |
| 503 | Service endpoint 없음, readiness 실패 |
| connection refused | controller Service/port-forward 문제 |
| timeout | controller, NetworkPolicy, backend 응답 지연 |
| DNS failure | service name 오타, CoreDNS, NetworkPolicy DNS 차단 |
