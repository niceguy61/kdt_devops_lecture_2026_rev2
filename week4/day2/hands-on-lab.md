# Hands-on Lab: W4D2 Service, DNS, Gateway API

## Lab Goal
오늘 실습은 Kubernetes 내부 통신과 외부 traffic 진입을 한 흐름으로 확인한다.

```text
browser/curl
  -> Envoy Gateway data plane
  -> Gateway
  -> HTTPRoute
  -> frontend Service 또는 api Service
  -> ready Pod endpoint
```

Docker Compose의 `ports`와 reverse proxy 설정이 Kubernetes에서는 Gateway API object와 controller/data plane 구조로 나뉜다는 점을 계속 확인한다.

## 0. 준비 확인
```bash
bash week4/scripts/create-kind-cluster.sh paperclip-w4d2
bash week4/scripts/ensure-kind-context.sh paperclip-w4d2
kubectl config current-context
kubectl get nodes -o wide
helm version --short
```

기대값:
```text
current-context가 kind-paperclip-w4d2
node STATUS가 Ready
helm v3.x 출력
```

주의:
```text
이 확인을 건너뛰면 다른 cluster에 설치할 수 있다.
수업 중 새 manifest를 적용하기 전에는 ensure-kind-context를 반복한다.
```

## 1. Envoy Gateway Helm 설치
```bash
bash week4/scripts/ensure-kind-context.sh paperclip-w4d2

helm upgrade --install envoy-gateway oci://docker.io/envoyproxy/gateway-helm \
  --version v1.7.3 \
  --namespace envoy-gateway-system \
  --create-namespace \
  -f week4/day2/labs/envoy-gateway/values.yaml

kubectl apply -f week4/day2/labs/envoy-gateway/gatewayclass.yaml
```

Kubernetes 1.27 계열 kind cluster에서는 Envoy Gateway `v1.8.x` chart의 Gateway API CRD 설치가 `ValidatingAdmissionPolicy` 관련 오류로 실패할 수 있다. 수업에서는 호환성을 위해 `v1.7.3`을 사용한다.

확인:
```bash
helm list -n envoy-gateway-system
kubectl -n envoy-gateway-system get deploy,pod,svc
kubectl get crd | grep gateway.networking.k8s.io
kubectl get gatewayclass
```

성공 기준:
```text
envoy-gateway release STATUS deployed
envoy-gateway Pod READY 1/1
Gateway API CRD 존재
GatewayClass envoy-gateway 존재
```

## 2. MSA 앱 배포
```bash
bash week4/scripts/ensure-kind-context.sh paperclip-w4d2
export NS=week4
export LAB=week4/day2/labs/traffic-routing

kubectl apply -f "$LAB/namespace.yaml"
kubectl apply -f "$LAB/frontend-configmap.yaml"
kubectl apply -f "$LAB/db-secret.yaml"
kubectl apply -f "$LAB/frontend-deployment.yaml"
kubectl apply -f "$LAB/api-deployment.yaml"
kubectl apply -f "$LAB/db-deployment.yaml"
kubectl apply -f "$LAB/services.yaml"

kubectl -n "$NS" get deploy,pod,svc,endpoints -o wide
kubectl -n "$NS" get endpointslice
```

기대 출력:
```text
deployment.apps/frontend   2/2
deployment.apps/api        2/2
deployment.apps/postgres   1/1

service/frontend   ClusterIP   80/TCP
service/api        ClusterIP   80/TCP
service/postgres   ClusterIP   5432/TCP
```

## 3. 내부 DNS 확인
curlbox에서 Service 이름으로 호출한다.

```bash
kubectl -n "$NS" run curlbox --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 \
  -- curl -s http://api/api
```

기대 출력:
```json
{"service":"api","version":"v1","status":"ok"}
```

frontend도 확인한다.

```bash
kubectl -n "$NS" run curlbox --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 \
  -- curl -s http://frontend/ | head
```

## 4. Gateway와 HTTPRoute 적용
```bash
bash week4/scripts/ensure-kind-context.sh paperclip-w4d2
kubectl apply -f "$LAB/gateway.yaml"
kubectl apply -f "$LAB/httproute.yaml"

kubectl -n "$NS" get gateway,httproute
kubectl -n "$NS" describe gateway paperclip-gateway
kubectl -n "$NS" describe httproute paperclip-routes
```

확인할 것:
```text
GatewayClassName: envoy-gateway
Gateway listener: paperclip.local:80
HTTPRoute parentRefs: paperclip-gateway
HTTPRoute backendRefs: frontend:80, api:80
```

조건 확인:
| 리소스 | 볼 것 |
|---|---|
| Gateway | Accepted/Programmed 계열 condition |
| HTTPRoute | Accepted/ResolvedRefs |
| Service | backend service 이름과 port |
| EndpointSlice | Ready Pod IP 목록 |

## 5. 외부 확인: port-forward
kind 환경에서 가장 안정적인 방법은 Envoy data plane Service를 port-forward하는 것이다.

Envoy Service 이름 확인:
```bash
kubectl -n envoy-gateway-system get svc \
  -l gateway.envoyproxy.io/owning-gateway-name=paperclip-gateway
```

터미널 1:
```bash
ENVOY_SVC=$(kubectl -n envoy-gateway-system get svc \
  -l gateway.envoyproxy.io/owning-gateway-name=paperclip-gateway \
  -o jsonpath='{.items[0].metadata.name}')

kubectl -n envoy-gateway-system port-forward "svc/${ENVOY_SVC}" 8080:80
```

`8080`이 이미 사용 중이면 왼쪽 local port만 바꾼다. 예: `18080:80`

터미널 2:
```bash
curl -H "Host: paperclip.local" http://localhost:8080/
curl -H "Host: paperclip.local" http://localhost:8080/api
```

기대 출력:
```text
첫 번째 요청: Paperclip W4D2 Frontend HTML
두 번째 요청: {"service":"api","version":"v1","status":"ok"}
```

브라우저에서는 hosts 파일을 수정하지 않았다면 Header를 넣기 어렵다. 이 경우 curl로 먼저 검증하고, hosts 파일을 수정한 뒤 브라우저를 확인한다.

hosts 파일에 추가:
```text
127.0.0.1 paperclip.local
```

브라우저:
```text
http://paperclip.local:8080/
http://paperclip.local:8080/api
```

## 6. 장애 1: HTTPRoute parentRefs 오류
```bash
kubectl apply -f "$LAB/broken-httproute-wrong-parent.yaml"
kubectl -n "$NS" describe httproute paperclip-routes-wrong-parent
```

예상:
```text
parentRefs가 존재하지 않는 Gateway를 가리키므로 Route가 attach되지 않는다.
```

확인 기준:
| 확인 | 명령 |
|---|---|
| Gateway 목록 | `kubectl -n week4 get gateway` |
| Route condition | `kubectl -n week4 describe httproute paperclip-routes-wrong-parent` |
| 정상 Route와 비교 | `kubectl -n week4 describe httproute paperclip-routes` |

## 7. 장애 2: Service selector 오류
```bash
kubectl apply -f "$LAB/broken-service-wrong-selector.yaml"
kubectl -n "$NS" get svc,endpoints api-broken-selector
```

예상 출력:
```text
NAME                  ENDPOINTS
api-broken-selector   <none>
```

selector가 잘못되면 Service가 있어도 backend Pod를 찾지 못한다.

## 8. 장애 3: backendRef port 오류
```bash
kubectl apply -f "$LAB/broken-httproute-wrong-port.yaml"
kubectl -n "$NS" describe httproute paperclip-routes-wrong-port
curl -H "Host: paperclip.local" http://localhost:8080/api
```

예상:
```text
HTTPRoute가 api Service의 존재하지 않는 service port를 참조한다.
404 또는 503 계열로 보일 수 있으므로 describe httproute와 service port를 비교한다.
```

확인:
```bash
kubectl -n "$NS" get svc api -o yaml
kubectl -n "$NS" describe httproute paperclip-routes-wrong-port
```

## 9. rollout과 외부 traffic
API를 v2로 바꾼다.

```bash
kubectl apply -f "$LAB/api-deployment-v2.yaml"
kubectl -n "$NS" rollout status deploy/api
kubectl -n "$NS" rollout history deploy/api
curl -H "Host: paperclip.local" http://localhost:8080/api
```

기대 출력:
```json
{"service":"api","version":"v2","status":"ok"}
```

되돌리기:
```bash
kubectl -n "$NS" rollout undo deploy/api
kubectl -n "$NS" rollout status deploy/api
curl -H "Host: paperclip.local" http://localhost:8080/api
```

rollout 직후에는 EndpointSlice와 Envoy data plane 반영 사이의 짧은 타이밍 때문에 첫 요청이 실패할 수 있다. 이때는 endpoint를 확인하고 1-2초 간격으로 다시 요청한다.

```bash
kubectl -n "$NS" get endpointslice -l kubernetes.io/service-name=api
for i in $(seq 1 10); do
  curl -sS -H "Host: paperclip.local" http://localhost:8080/api && break
  echo
  sleep 2
done
```

## 10. NetworkPolicy와 Cilium/Hubble preview
적용 전에 현재 Service와 Endpoint를 먼저 본다.

```bash
kubectl -n "$NS" get svc,endpoints,endpointslice
kubectl -n "$NS" get pod --show-labels
kubectl get ns --show-labels
```

NetworkPolicy가 없으면 namespace가 다르다는 이유만으로 Pod traffic이 자동 차단된다고 가정하면 안 된다. 실제 차단은 CNI와 NetworkPolicy enforcement가 담당한다.

```bash
kubectl apply -f "$LAB/networkpolicy-preview.yaml"
kubectl -n "$NS" get networkpolicy
kubectl -n "$NS" describe networkpolicy default-deny-all
kubectl -n "$NS" describe networkpolicy allow-envoy-gateway-to-frontend
kubectl -n "$NS" describe networkpolicy allow-envoy-gateway-to-api
kubectl -n "$NS" describe networkpolicy allow-frontend-to-api
kubectl -n "$NS" describe networkpolicy allow-api-to-db
kubectl -n kube-system get pod -l k8s-app=kube-dns --show-labels
```

주의:
```text
kind 기본 CNI에서는 NetworkPolicy가 강제되지 않을 수 있다.
오늘은 traffic 허용선과 DNS egress를 설명하는 preview로 사용한다.
Cilium/Hubble은 실제 flow와 drop reason을 볼 수 있는 선택지로 소개한다.
```

확인 질문:
| 질문 | 봐야 할 것 |
|---|---|
| frontend -> api는 왜 허용되는가 | api ingress + frontend egress |
| api -> postgres는 왜 허용되는가 | postgres ingress + api egress |
| Gateway -> frontend/api는 왜 허용되는가 | Envoy namespace + Envoy Pod label 기준 ingress |
| frontend -> postgres는 왜 막아야 하는가 | db 직접 접근 차단 |
| DNS는 왜 따로 여는가 | Service 이름 해석이 CoreDNS를 사용 |
| 다른 namespace까지 허용하려면 무엇이 필요한가 | `namespaceSelector` |
| Hubble이 있다면 무엇을 볼 수 있는가 | frontend/api/db flow와 drop reason |

## Cleanup
수업 종료 시점에는 반드시 cluster를 유지할지 삭제할지 결정한다.

다음 수업에서 이어 쓸 경우:
```bash
bash week4/scripts/ensure-kind-context.sh paperclip-w4d2
kind get clusters
kubectl get ns
helm list -A
```

완전히 지우는 경우:
```bash
bash week4/scripts/delete-kind-cluster.sh paperclip-w4d2
kind get clusters
```

## S6-S8 검증 스크립트
NetworkPolicy, Gateway port-forward, rollout/rollback을 한 번에 확인하려면 다음 스크립트를 실행한다.

```bash
bash week4/day2/labs/traffic-routing/verify-s6-s8.sh
```

`8080`을 이미 사용 중인 환경에서는 스크립트가 기본으로 `18080`을 사용한다. 다른 port가 필요하면 `LOCAL_PORT=18081`처럼 지정한다.

W4D3에서도 traffic stack을 계속 쓰고 싶다면 삭제하지 않아도 된다. 남겨둘 경우 `helm list -A`, `kubectl get ns`, `kind get clusters`에 evidence를 남긴다.
