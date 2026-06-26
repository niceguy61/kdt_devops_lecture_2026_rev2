# Hands-on Lab: W4D2 Service, DNS, Ingress

## Lab Goal
오늘 실습은 Kubernetes 내부 통신과 외부 traffic 진입을 한 흐름으로 확인한다.

```text
browser/curl
  -> ingress-nginx
  -> Ingress rule
  -> frontend Service 또는 api Service
  -> ready Pod endpoint
```

## 0. 준비 확인
```bash
kubectl config current-context
kubectl get nodes -o wide
helm version --short
```

기대값:
```text
node STATUS가 Ready
helm v3.x 출력
```

## 1. ingress-nginx Helm 설치
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  -f week4/day2/labs/ingress-nginx/values.yaml
```

확인:
```bash
helm list -n ingress-nginx
helm status ingress-nginx -n ingress-nginx
kubectl -n ingress-nginx get deploy,pod,svc
kubectl get ingressclass
```

성공 기준:
```text
ingress-nginx-controller Pod READY 1/1
IngressClass nginx 존재
controller Service type NodePort
```

## 2. MSA 앱 배포
```bash
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

## 4. Ingress 적용
```bash
kubectl apply -f "$LAB/ingress.yaml"
kubectl -n "$NS" get ingress
kubectl -n "$NS" describe ingress paperclip
```

기대 출력:
```text
Name:             paperclip
Ingress Class:    nginx
Rules:
  Host             Path  Backends
  paperclip.local
                   /api  api:80
                   /     frontend:80
```

## 5. 외부 확인 방법 A: port-forward
kind 환경에서 가장 안정적인 방법은 ingress-nginx controller Service를 port-forward하는 것이다.

터미널 1:
```bash
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80
```

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

## 6. 외부 확인 방법 B: hosts + NodePort
kind cluster가 host port mapping 없이 만들어졌다면 NodePort `30080`이 host에서 바로 열리지 않을 수 있다. 이 경우 방법 A를 사용한다.

hosts 파일에 추가:
```text
127.0.0.1 paperclip.local
```

확인:
```bash
curl http://paperclip.local:30080/
curl http://paperclip.local:30080/api
```

## 7. 장애 1: className 누락
```bash
kubectl apply -f "$LAB/broken-ingress-no-class.yaml"
kubectl -n "$NS" describe ingress paperclip-no-class
curl -H "Host: broken.paperclip.local" http://localhost:8080/
```

예상:
```text
ingressClassName이 없으면 controller 설정에 따라 처리되지 않을 수 있다.
```

확인 기준:
| 확인 | 명령 |
|---|---|
| Ingress class | `kubectl -n week4 get ingress paperclip-no-class -o yaml` |
| controller log | `kubectl -n ingress-nginx logs deploy/ingress-nginx-controller --tail=80` |
| 정상 Ingress와 비교 | `kubectl -n week4 describe ingress paperclip` |

## 8. 장애 2: Service selector 오류
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

## 9. 장애 3: backend port 오류
```bash
kubectl apply -f "$LAB/broken-ingress-wrong-port.yaml"
kubectl -n "$NS" describe ingress paperclip-wrong-port
curl -H "Host: wrong-port.paperclip.local" http://localhost:8080/api
```

예상:
```text
Ingress가 api Service의 존재하지 않는 service port 8080을 참조한다.
404 또는 503 계열로 보일 수 있으므로 describe ingress와 service port를 비교한다.
```

확인:
```bash
kubectl -n "$NS" get svc api -o yaml
kubectl -n "$NS" describe ingress paperclip-wrong-port
```

## 10. rollout과 외부 traffic
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

## 11. NetworkPolicy preview
적용 전에 현재 Service와 Endpoint를 먼저 본다.

```bash
kubectl -n "$NS" get svc,endpoints
kubectl -n "$NS" get pod --show-labels
kubectl get ns --show-labels
```

NetworkPolicy가 없으면 namespace가 다르다는 이유만으로 Pod traffic이 자동 차단된다고 가정하면 안 된다. 실제 차단은 CNI와 NetworkPolicy enforcement가 담당한다.

```bash
kubectl apply -f "$LAB/networkpolicy-preview.yaml"
kubectl -n "$NS" get networkpolicy
kubectl -n "$NS" describe networkpolicy default-deny-all
kubectl -n "$NS" describe networkpolicy allow-frontend-to-api
kubectl -n "$NS" describe networkpolicy allow-api-to-db
kubectl -n kube-system get pod -l k8s-app=kube-dns --show-labels
```

주의:
```text
kind 기본 CNI에서는 NetworkPolicy가 강제되지 않을 수 있다.
오늘은 traffic 허용선과 DNS egress를 설명하는 preview로 사용한다.
```

확인 질문:
| 질문 | 봐야 할 것 |
|---|---|
| frontend -> api는 왜 허용되는가 | api ingress + frontend egress |
| api -> postgres는 왜 허용되는가 | postgres ingress + api egress |
| frontend -> postgres는 왜 막아야 하는가 | db 직접 접근 차단 |
| DNS는 왜 따로 여는가 | Service 이름 해석이 CoreDNS를 사용 |
| 다른 namespace까지 허용하려면 무엇이 필요한가 | `namespaceSelector` |

## Cleanup
```bash
kubectl delete namespace week4
helm uninstall ingress-nginx -n ingress-nginx
kubectl delete namespace ingress-nginx
```

W4D3에서도 ingress를 계속 쓰고 싶다면 삭제하지 않아도 된다. 남겨둘 경우 `helm list -A`와 `kubectl get ns`에 evidence를 남긴다.
