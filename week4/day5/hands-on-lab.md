# Hands-on Lab: W4D5 GitOps와 Mesh Preview

## 0. 준비 확인
```bash
kubectl config current-context
kubectl get nodes
helm version --short
```

W4D4 Kyverno가 남아 있으면 GitOps manifest가 policy에 막히는 장면을 같이 볼 수 있다. 리소스가 부족하면 Kyverno를 먼저 정리한다.

## 1. Argo CD 설치
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

helm upgrade --install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  -f week4/day5/labs/argocd/values.yaml
```

확인:
```bash
helm list -n argocd
kubectl -n argocd get pods,svc
kubectl -n argocd wait --for=condition=Ready pod --all --timeout=240s
```

Argo CD가 cluster API를 호출할 identity와 권한을 확인한다.

```bash
kubectl -n argocd get sa
kubectl get clusterrolebinding | grep argocd
kubectl auth can-i create deployments \
  --as=system:serviceaccount:argocd:argocd-application-controller \
  -n week4-gitops
```

이 결과가 `yes`이면 Argo CD controller가 `week4-gitops` namespace에 Deployment를 만들 수 있다. Argo CD가 `argocd` namespace 밖에 리소스를 만드는 이유는 네트워크가 열려 있어서가 아니라 Kubernetes API와 RBAC이 허용하기 때문이다.

admin password:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d; echo
```

UI 접속:
```bash
kubectl -n argocd port-forward svc/argocd-server 18080:80
```

브라우저:
```text
http://localhost:18080
user: admin
password: 위 명령 결과
```

## 2. GitOps sample app 직접 배포 확인
Application 이전에 manifest 자체가 유효한지 확인한다.

```bash
kubectl apply -f week4/day5/labs/gitops-app/namespace.yaml
kubectl apply -f week4/day5/labs/gitops-app/configmap.yaml
kubectl apply -f week4/day5/labs/gitops-app/deployment.yaml
kubectl apply -f week4/day5/labs/gitops-app/service.yaml
kubectl -n week4-gitops get deploy,svc,pod,cm
kubectl -n week4-gitops port-forward svc/gitops-web 18085:80
```

브라우저:
```text
http://localhost:18085
```

정리:
```bash
kubectl delete -f week4/day5/labs/gitops-app/service.yaml --ignore-not-found
kubectl delete -f week4/day5/labs/gitops-app/deployment.yaml --ignore-not-found
kubectl delete -f week4/day5/labs/gitops-app/configmap.yaml --ignore-not-found
kubectl delete -f week4/day5/labs/gitops-app/namespace.yaml --ignore-not-found
```

## 3. Argo CD Application 생성
`application-template.yaml`의 `repoURL`과 `path`를 본인 GitHub repository 기준으로 바꾼다.

```bash
cp week4/day5/labs/argocd/application-template.yaml /tmp/w4d5-application.yaml
sed -n '1,120p' /tmp/w4d5-application.yaml
```

여기서 destination을 확인한다.

```bash
grep -n -A4 "destination:" /tmp/w4d5-application.yaml
```

`server: https://kubernetes.default.svc`는 cluster 내부 API server이고, `namespace: week4-gitops`는 manifest가 생성될 대상 namespace다.

수정 후:
```bash
kubectl apply -f /tmp/w4d5-application.yaml
kubectl -n argocd get application
```

UI에서 `w4d5-gitops-app`을 열고 Sync를 실행한다.

CLI 확인:
```bash
kubectl -n week4-gitops get deploy,svc,pod
```

## 4. drift와 sync
cluster에서 직접 replica를 바꿔 drift를 만든다.

```bash
kubectl -n week4-gitops scale deploy/gitops-web --replicas=2
kubectl -n week4-gitops get deploy gitops-web
```

Argo CD UI에서 OutOfSync 또는 drift를 확인한다. GitOps 기준에서는 cluster 직접 수정이 임시 조치인지, Git에 반영할 변경인지 판단해야 한다.

복구:
```bash
kubectl -n argocd get application w4d5-gitops-app -o yaml | sed -n '1,160p'
```

UI에서 Sync를 눌러 Git 기준으로 되돌린다.

## 5. Istio 설치
```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

helm upgrade --install istio-base istio/base \
  --namespace istio-system \
  --create-namespace \
  -f week4/day5/labs/istio/base-values.yaml

helm upgrade --install istiod istio/istiod \
  --namespace istio-system \
  -f week4/day5/labs/istio/istiod-values.yaml

helm upgrade --install istio-ingress istio/gateway \
  --namespace istio-ingress \
  --create-namespace \
  -f week4/day5/labs/istio/gateway-values.yaml
```

확인:
```bash
helm list -A | grep -E 'istio|istiod'
kubectl -n istio-system get pods
kubectl -n istio-ingress get pods,svc
```

## 6. Kiali 설치
```bash
helm repo add kiali https://kiali.org/helm-charts
helm repo update

helm upgrade --install kiali-operator kiali/kiali-operator \
  --namespace kiali-operator \
  --create-namespace \
  -f week4/day5/labs/istio/kiali-values.yaml
```

확인:
```bash
kubectl -n kiali-operator get pods
kubectl -n istio-system get kiali
kubectl -n istio-system get svc kiali
```

UI:
```bash
kubectl -n istio-system port-forward svc/kiali 20001:20001
```

브라우저:
```text
http://localhost:20001
```

## 7. mesh app 배포와 sidecar 확인
먼저 단순한 2-service 예제로 sidecar injection과 Kiali graph가 보이는지 확인한다.

```bash
kubectl apply -f week4/day5/labs/mesh-app/namespace.yaml
kubectl apply -f week4/day5/labs/mesh-app/deployments.yaml
kubectl apply -f week4/day5/labs/mesh-app/services.yaml
kubectl -n mesh-demo rollout status deploy/mesh-api --timeout=180s
kubectl -n mesh-demo rollout status deploy/mesh-frontend --timeout=180s
```

sidecar 확인:
```bash
kubectl -n mesh-demo get pod
```

예상:
```text
mesh-api-...        2/2 Running
mesh-frontend-...   2/2 Running
```

Kiali Graph에서 `mesh-demo` namespace를 선택하고 traffic edge가 보이는지 확인한다.

## 8. MSA mesh app 배포와 통신 구조 확인
MSA 구조를 더 명확히 보기 위해 `frontend -> bff -> catalog/order -> inventory/payment` 샘플을 배포한다.

```bash
kubectl apply -f week4/day5/labs/mesh-msa-app/namespace.yaml
kubectl apply -f week4/day5/labs/mesh-msa-app/deployments.yaml
kubectl apply -f week4/day5/labs/mesh-msa-app/services.yaml

kubectl -n mesh-msa-demo rollout status deploy/frontend --timeout=180s
kubectl -n mesh-msa-demo rollout status deploy/bff --timeout=180s
kubectl -n mesh-msa-demo rollout status deploy/catalog --timeout=180s
kubectl -n mesh-msa-demo rollout status deploy/inventory --timeout=180s
kubectl -n mesh-msa-demo rollout status deploy/order --timeout=180s
kubectl -n mesh-msa-demo rollout status deploy/payment --timeout=180s
```

sidecar 확인:
```bash
kubectl -n mesh-msa-demo get pod
```

예상:
```text
frontend-...    2/2 Running
bff-...         2/2 Running
catalog-...     2/2 Running
inventory-...   2/2 Running
order-...       2/2 Running
payment-...     2/2 Running
```

traffic 확인:
```bash
kubectl -n mesh-msa-demo logs deploy/frontend -c traffic-generator --tail=20
```

Kiali Graph에서 `mesh-msa-demo` namespace를 선택하고 다음 edge가 보이는지 확인한다.

| Edge | 의미 |
|---|---|
| `frontend -> bff` | 사용자 진입점 |
| `bff -> catalog` | 상품 목록 |
| `bff -> inventory` | 재고 조회 |
| `bff -> order` | 주문 요청 |
| `order -> inventory` | 주문 중 재고 확인 |
| `order -> payment` | 결제 승인 |

## 9. fault injection preview
```bash
kubectl apply -f week4/day5/labs/mesh-app/virtualservice-preview.yaml
kubectl -n mesh-demo get virtualservice
```

frontend log:
```bash
kubectl -n mesh-demo logs deploy/mesh-frontend -c istio-proxy --tail=50
```

오늘은 delay가 traffic graph와 proxy log에 어떤 영향을 주는지만 preview로 본다.

MSA 샘플에서는 order 서비스에 지연을 넣고 `frontend -> bff -> order` 경로의 latency 변화를 본다.

```bash
kubectl apply -f week4/day5/labs/mesh-msa-app/virtualservice-order-delay.yaml
kubectl -n mesh-msa-demo get virtualservice
kubectl -n mesh-msa-demo logs deploy/frontend -c traffic-generator --tail=40
```

Kiali에서 `catalog` 경로와 `order` 경로의 차이를 비교한다.

## 10. Cleanup
```bash
kubectl delete -f week4/day5/labs/mesh-app/virtualservice-preview.yaml --ignore-not-found
kubectl delete -f week4/day5/labs/mesh-msa-app/virtualservice-order-delay.yaml --ignore-not-found
kubectl delete namespace mesh-msa-demo --ignore-not-found
kubectl delete namespace mesh-demo --ignore-not-found
kubectl delete namespace week4-gitops --ignore-not-found
kubectl delete application -n argocd w4d5-gitops-app --ignore-not-found

helm uninstall kiali-operator -n kiali-operator
kubectl delete namespace kiali-operator
helm uninstall istio-ingress -n istio-ingress
kubectl delete namespace istio-ingress
helm uninstall istiod -n istio-system
helm uninstall istio-base -n istio-system
kubectl delete namespace istio-system
helm uninstall argocd -n argocd
kubectl delete namespace argocd
```

W5로 넘어가기 전 local resource를 반드시 정리한다.
