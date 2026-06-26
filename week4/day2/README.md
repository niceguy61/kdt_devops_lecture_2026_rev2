# Week 4 Day2: Service, DNS, Gateway API, Envoy Gateway

## Overview
W4D2는 Docker Compose에서 익숙했던 `ports`, service name DNS, reverse proxy 감각을 Kubernetes의 traffic model로 확장하는 날이다.

Docker에서는 보통 다음처럼 생각했다.

```text
browser
  -> host port
  -> container port
  -> compose service name
```

Kubernetes에서는 같은 문제가 더 많은 계층으로 나뉜다.

```text
external client
  -> Gateway implementation
  -> Gateway
  -> HTTPRoute
  -> Service
  -> EndpointSlice
  -> Ready Pod
```

오늘의 표준 실습은 `ingress-nginx`가 아니라 Gateway API와 Envoy Gateway다. NGINX Ingress Controller는 현업에서 여전히 많이 쓰이는 기존 Ingress 생태계의 대표 사례로 비교만 한다. 새 실습은 Kubernetes 공식 Gateway API의 `GatewayClass`, `Gateway`, `HTTPRoute`를 기준으로 잡고, Envoy Gateway를 controller 구현체로 사용한다.

## Learning Goals
- Docker Compose의 port publish/reverse proxy 구조가 Kubernetes에서 Service, Gateway, Route, Controller로 분리되는 이유를 설명한다.
- Pod IP, Service, EndpointSlice, DNS, selector 관계를 출력으로 확인한다.
- frontend, api, database 성격의 MSA 앱을 Kubernetes Service DNS로 연결한다.
- Envoy Gateway를 Helm으로 설치하고 GatewayClass, Gateway, HTTPRoute를 확인한다.
- `/`는 frontend, `/api`는 api로 routing되는 것을 curl/browser 기준으로 확인한다.
- GatewayClass 누락, HTTPRoute parentRefs 오류, Service selector 오류, backend port 오류, readiness 실패를 404/503/connection refused/timeout과 연결해 분석한다.
- NetworkPolicy preview와 Cilium/Hubble preview를 통해 "namespace는 network 격리벽이 아니다"를 명확히 이해한다.
- rollout이 외부 traffic에 미치는 영향을 Gateway 경로로 확인한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day1 요약 + Kubernetes networking 다시 잡기 | Pod IP, Service, EndpointSlice, DNS, selector |
| 2교시 | MSA 앱 내부 통신 | frontend/api/db Service DNS와 targetPort |
| 3교시 | Gateway API와 Envoy Gateway 설치 | Helm release, GatewayClass, controller Pod |
| 4교시 | HTTPRoute 작성 | host/path routing, `/`, `/api`, curl/browser |
| 5교시 | Gateway/HTTPRoute 장애 분석 | GatewayClass, parentRefs, backendRefs, endpoint |
| 6교시 | NetworkPolicy와 Cilium preview | traffic 허용선, DNS egress, CNI/eBPF 관찰 |
| 7교시 | rollout과 external traffic | image/tag 변경, rollout status/history/undo |
| 8교시 | 구름 EXP 배움일기 | Service/Gateway/DNS 증거와 장애 메모 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 당일 실습 명령과 예상 출력 |
| `academic-foundations.md` | Service, Gateway API, Envoy Gateway, NetworkPolicy 개념 |
| `labs/traffic-routing/` | frontend/api/db, Service, HTTPRoute, 장애/NetworkPolicy manifest |
| `labs/envoy-gateway/values.yaml` | Envoy Gateway Helm values |

## Official References
| Topic | Reference |
|---|---|
| Kubernetes Service | https://kubernetes.io/docs/concepts/services-networking/service/ |
| Kubernetes Gateway API | https://gateway-api.sigs.k8s.io/ |
| Gateway API overview | https://gateway-api.sigs.k8s.io/concepts/api-overview/ |
| Envoy Gateway install | https://gateway.envoyproxy.io/docs/install/install-helm/ |
| Kubernetes NetworkPolicy | https://kubernetes.io/docs/concepts/services-networking/network-policies/ |
| Cilium NetworkPolicy | https://docs.cilium.io/en/stable/security/policy/ |
| Hubble observability | https://docs.cilium.io/en/stable/observability/hubble/ |

## End-Of-Day Checklist
- [ ] Service selector와 EndpointSlice가 연결되는 것을 확인했다.
- [ ] Service DNS 이름으로 frontend -> api 통신을 확인했다.
- [ ] Envoy Gateway를 Helm으로 설치하고 release와 controller 상태를 확인했다.
- [ ] GatewayClass, Gateway, HTTPRoute의 역할을 구분했다.
- [ ] `/`와 `/api`가 서로 다른 Service로 routing되는 것을 확인했다.
- [ ] Gateway 장애에서 class, parentRefs, backendRefs, selector, endpoint, readiness를 구분했다.
- [ ] NetworkPolicy와 Cilium/Hubble이 해결하는 문제가 무엇인지 설명했다.
- [ ] rollout이 외부 경로에 어떤 영향을 주는지 확인했다.
