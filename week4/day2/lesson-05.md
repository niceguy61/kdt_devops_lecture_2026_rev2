# 5교시: Gateway/HTTPRoute 장애 분석

![Week 4 Day 2 Lesson 5](./assets/lesson-05-ingress-troubleshooting.png)

## 수업 목표
- 404, 503, connection refused, timeout을 한 덩어리로 보지 않는다.
- GatewayClass, Gateway, HTTPRoute, Service, EndpointSlice 장애를 출력으로 구분한다.
- Gateway API 장애에서 먼저 볼 증거 순서를 익힌다.

## 장애 분석 기본 순서
```text
curl/browser 증상
  -> Envoy data plane 접근 가능 여부
  -> Gateway listener condition
  -> HTTPRoute parentRefs/Accepted/ResolvedRefs
  -> Service name/port
  -> EndpointSlice 존재
  -> Pod readiness
  -> Envoy Gateway controller log
```

처음부터 app log만 보면 traffic이 app까지 도달하지 않은 경우를 놓친다.

## Docker 시절과 다른 점
Docker reverse proxy에서는 proxy 설정 파일과 container log를 주로 봤다.

```text
nginx.conf
docker logs reverse-proxy
docker logs api
```

Kubernetes Gateway API에서는 API object의 condition이 중요한 증거가 된다.

```text
kubectl describe gateway
kubectl describe httproute
kubectl get svc,endpointslice
kubectl logs deploy/envoy-gateway
```

즉 "프록시 설정 파일을 열어본다"가 아니라 "선언된 object가 controller에 의해 받아들여졌는지 condition으로 본다"로 바뀐다.

## 증상별 첫 판단
| 증상 | 원인 후보 | 먼저 볼 명령 |
|---|---|---|
| 404 | host/path 불일치, HTTPRoute가 Gateway에 attach되지 않음 | `describe httproute` |
| 503 | endpoint 없음, readiness 실패 | `get endpointslice`, `get endpoints` |
| connection refused | port-forward/data plane Service 문제 | `get svc -A | grep envoy` |
| timeout | NetworkPolicy, backend 지연, data plane 문제 | endpoint, networkpolicy, logs |
| DNS failure | hosts/CoreDNS/Service 이름 | hosts, svc, CoreDNS |

## 장애 1: HTTPRoute parentRefs 오류
```bash
kubectl apply -f week4/day2/labs/traffic-routing/broken-httproute-wrong-parent.yaml
kubectl -n week4 describe httproute paperclip-routes-wrong-parent
```

manifest에는 존재하지 않는 Gateway가 들어 있다.

```yaml
parentRefs:
  - name: missing-gateway
```

이 경우 HTTPRoute는 생성되지만 올바른 Gateway에 attach되지 않는다.

확인:
```bash
kubectl -n week4 get gateway
kubectl -n week4 get httproute
kubectl -n week4 describe httproute paperclip-routes-wrong-parent
```

볼 것:
| 조건 | 의미 |
|---|---|
| `Accepted=False` | Route가 Gateway에 받아들여지지 않음 |
| `ParentError` 계열 message | parentRefs 문제 가능 |
| Gateway 이름 불일치 | Route가 붙을 대상 없음 |

## 장애 2: Service selector 오류
```bash
kubectl apply -f week4/day2/labs/traffic-routing/broken-service-wrong-selector.yaml
kubectl -n week4 get svc,endpoints api-broken-selector
```

예상 출력:
```text
service/api-broken-selector   ClusterIP   10.96.x.x
endpoints/api-broken-selector <none>
```

Service는 있지만 endpoint가 없다. selector가 실제 Pod label과 맞지 않기 때문이다.

확인:
```bash
kubectl -n week4 get svc api-broken-selector -o yaml
kubectl -n week4 get pod --show-labels | grep api
```

판단:
| 출력 | 의미 |
|---|---|
| Service 존재 | DNS와 ClusterIP는 생김 |
| Endpoint `<none>` | traffic을 받을 Ready Pod가 없음 |
| Pod label `app=api` | Service selector가 `app=api-missing`이면 불일치 |

## 장애 3: backendRefs port 오류
```bash
kubectl apply -f week4/day2/labs/traffic-routing/broken-httproute-wrong-port.yaml
kubectl -n week4 describe httproute paperclip-routes-wrong-port
curl -H "Host: paperclip.local" http://localhost:8080/api
```

HTTPRoute는 Service의 `port`를 참조해야 한다. api Service는 80번 port를 제공하고, targetPort로 Pod의 8080에 보낸다. HTTPRoute backendRef에 9999나 8080을 쓰면 Service port와 맞지 않는다.

확인:
```bash
kubectl -n week4 get svc api -o yaml
kubectl -n week4 describe httproute paperclip-routes-wrong-port
```

정상 Service:
```yaml
ports:
  - port: 80
    targetPort: http
```

HTTPRoute backendRef는 `port: 80`이어야 한다.

## 장애 4: readiness 실패와 endpoint 없음
Pod가 Running이어도 Ready가 아니면 endpoint에서 빠진다.

```bash
kubectl -n week4 get pod
kubectl -n week4 get endpoints api
kubectl -n week4 get endpointslice
kubectl -n week4 describe pod -l app=api
```

출력 예시:
```text
READY   STATUS
0/1     Running

endpoints/api   <none>

Readiness probe failed
```

이 경우 Gateway/HTTPRoute는 정상이어도 503 계열 장애로 보일 수 있다.

## controller가 보는 backend 상태
Envoy Gateway controller는 Kubernetes API에서 Gateway, HTTPRoute, Service, EndpointSlice 정보를 읽어 Envoy data plane 설정을 만든다. backend Service가 없거나 endpoint가 비면 condition과 log가 단서가 된다.

```bash
kubectl -n envoy-gateway-system logs deploy/envoy-gateway --tail=100
kubectl -n week4 describe gateway paperclip-gateway
kubectl -n week4 describe httproute paperclip-routes
```

볼 수 있는 단서:
| 단서 | 의미 |
|---|---|
| `Accepted` | Gateway/Route가 controller에 받아들여짐 |
| `ResolvedRefs` | backendRef가 올바르게 해석됨 |
| `Programmed` | data plane 반영 상태 |
| backend service not found | Service 이름/namespace 오류 |
| invalid backend port | Service port 오류 |

## 장애별 curl 출력 예시
| curl 출력 | 해석 시작점 |
|---|---|
| `404 Not Found` | host/path/HTTPRoute attach mismatch |
| `503 Service Unavailable` | endpoint 없음, readiness 실패 |
| `Failed to connect to localhost port 8080` | port-forward/data plane 접근 문제 |
| `Could not resolve host` | hosts 파일 또는 DNS 문제 |
| 응답은 200인데 body가 예상과 다름 | path가 다른 backend로 갔을 가능성 |

## 빠른 비교 명령
정상 Gateway와 Route를 먼저 본다.

```bash
kubectl -n week4 describe gateway paperclip-gateway
kubectl -n week4 describe httproute paperclip-routes
```

정상 Service와 broken Service를 비교한다.

```bash
kubectl -n week4 get svc api api-broken-selector -o wide
kubectl -n week4 get endpoints api api-broken-selector
kubectl -n week4 get endpointslice
```

비교의 핵심:
| 비교 | 정상 | 문제 |
|---|---|---|
| GatewayClass | `envoy-gateway` | class 없음/불일치 |
| parentRefs | `paperclip-gateway` | 존재하지 않는 Gateway |
| backend service port | `80` | `9999` 또는 Service에 없는 port |
| endpoint | Pod IP 목록 | `<none>` |
| Pod READY | `1/1` | `0/1` |

## 장애 분석 템플릿
```markdown
## 증상
- curl/browser:

## Gateway
- GatewayClass:
- listener:
- Accepted/Programmed:

## HTTPRoute
- parentRefs:
- host/path:
- backendRefs:
- Accepted/ResolvedRefs:

## Service/Endpoint
- service port:
- endpoint:

## Pod
- READY:
- event:

## 판단
- 원인 후보:
- 다음 조치:
```

## Evidence Note
```markdown
# W4D2S5 Gateway troubleshooting
- 내가 본 증상:
- HTTP status 또는 curl error:
- Gateway listener/condition:
- HTTPRoute parentRefs/backendRefs:
- Service port와 targetPort:
- Endpoint 상태:
- Pod READY/event:
- 가장 가능성 높은 원인:
```

## 한 줄 요약
```text
Gateway API 장애는 Gateway, HTTPRoute, Service, EndpointSlice, readiness를 층별로 나누어 확인한다.
```
