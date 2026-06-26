# Hands-on Lab: W4D4 RBAC과 Kyverno

## 0. 준비 확인
```bash
kubectl config current-context
kubectl get nodes
helm version --short
```

kind context인지 먼저 확인한다.

```bash
kind get clusters
kubectl config current-context
```

## 1. RBAC 실습 리소스 배포
```bash
kubectl apply -f week4/day4/labs/rbac/namespace.yaml
kubectl apply -f week4/day4/labs/rbac/serviceaccounts.yaml
kubectl apply -f week4/day4/labs/rbac/readonly-role.yaml
kubectl apply -f week4/day4/labs/rbac/sample-workload.yaml
```

확인:
```bash
kubectl -n week4-security get sa,role,rolebinding
kubectl -n week4-security get deploy,svc,pod
```

## 2. `kubectl auth can-i`
읽기 권한:
```bash
kubectl auth can-i list pods \
  --as=system:serviceaccount:week4-security:readonly-viewer \
  -n week4-security
```

예상:
```text
yes
```

삭제 권한:
```bash
kubectl auth can-i delete pods \
  --as=system:serviceaccount:week4-security:readonly-viewer \
  -n week4-security
```

예상:
```text
no
```

주의: `kubectl auth can-i`는 결과가 `no`일 때 exit code도 실패로 줄 수 있다. `set -e`를 켠 shell script에서는 여기서 멈출 수 있으므로 수업 중에는 한 줄씩 실행하거나 `|| true`로 evidence를 남긴다.

실제 forbidden 확인:
```bash
kubectl --as=system:serviceaccount:week4-security:readonly-viewer \
  -n week4-security delete pod -l app=security-api
```

예상:
```text
Error from server (Forbidden): pods ... is forbidden
```

## 3. ServiceAccount token mount 확인
```bash
kubectl apply -f week4/day4/labs/rbac/token-mounted-pod.yaml
kubectl -n week4-security get pod token-mounted-demo
```

token이 mount된 Pod:
```bash
kubectl -n week4-security exec token-mounted-demo -- \
  ls /var/run/secrets/kubernetes.io/serviceaccount
```

token을 mount하지 않는 workload:
```bash
pod="$(kubectl -n week4-security get pod -l app=security-api -o jsonpath='{.items[0].metadata.name}')"
kubectl -n week4-security exec "$pod" -- \
  ls /var/run/secrets/kubernetes.io/serviceaccount
```

예상:
```text
No such file or directory
```

## 4. Kyverno 설치
```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm upgrade --install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  -f week4/day4/labs/kyverno/values.yaml
```

확인:
```bash
helm list -n kyverno
kubectl -n kyverno get pods
kubectl get crd | grep kyverno
```

성공 기준:
```text
kyverno-admission-controller Running
kyverno-background-controller Running
kyverno-reports-controller Running
clusterpolicies.kyverno.io CRD 존재
```

실제 검증 예시:
```text
Chart version: 3.8.1
Kyverno version: v1.18.1
kyverno-admission-controller    1/1 Running
kyverno-background-controller   1/1 Running
kyverno-cleanup-controller      1/1 Running
kyverno-reports-controller      1/1 Running
```

## 5. Audit 정책
```bash
kubectl apply -f week4/day4/labs/kyverno/require-owner-label-audit.yaml
kubectl apply -f week4/day4/labs/kyverno/bad-pod-missing-owner.yaml
```

Audit 모드라서 Pod 생성은 허용될 수 있다.

```bash
kubectl -n week4-security get pod bad-missing-owner
kubectl get clusterpolicy require-owner-label-audit
```

정책 위반 report는 Kyverno 버전과 설정에 따라 `policyreport` 또는 admission report 계열로 보일 수 있다.

```bash
kubectl get policyreport -A 2>/dev/null || true
kubectl get admissionreport -A 2>/dev/null || true
```

## 6. Enforce 정책
```bash
kubectl apply -f week4/day4/labs/kyverno/disallow-latest-enforce.yaml
kubectl apply -f week4/day4/labs/kyverno/disallow-privileged-hostpath-enforce.yaml
```

latest tag 차단:
```bash
kubectl apply -f week4/day4/labs/kyverno/bad-pod-latest.yaml
```

예상:
```text
admission webhook ... denied the request
Do not use image tag latest
```

실제 검증에서는 policy와 rule 이름이 함께 보인다.
```text
disallow-latest-enforce:
  require-explicit-image-tag: validation failure: Do not use image tag latest.
```

privileged/hostPath 차단:
```bash
kubectl apply -f week4/day4/labs/kyverno/bad-pod-privileged-hostpath.yaml
```

예상:
```text
denied the request
Privileged containers are not allowed
hostPath volumes are not allowed
```

실제 검증 path:
```text
rule disallow-hostpath failed at path /spec/volumes/0/hostPath/
rule disallow-privileged failed at path /spec/containers/0/securityContext/privileged/
```

정상 Pod:
```bash
kubectl apply -f week4/day4/labs/kyverno/good-pod.yaml
kubectl -n week4-security get pod good-versioned-owner
```

정상 검증:
```text
good-versioned-owner   1/1   Running   0
```

## 7. 장애 구분표 작성
| 증상 | 먼저 볼 것 | 판단 |
|---|---|---|
| `Forbidden` | `kubectl auth can-i` | RBAC 문제 |
| `admission webhook denied` | policy 이름, message | Kyverno 정책 문제 |
| Pod Pending | `describe pod` event | scheduling/resource 문제 |
| Pod 생성은 됐지만 report 위반 | policy report | Audit 정책 위반 |

## 8. Cleanup
```bash
kubectl delete -f week4/day4/labs/kyverno/good-pod.yaml --ignore-not-found
kubectl delete -f week4/day4/labs/kyverno/bad-pod-missing-owner.yaml --ignore-not-found
kubectl delete clusterpolicy require-owner-label-audit --ignore-not-found
kubectl delete clusterpolicy disallow-latest-enforce --ignore-not-found
kubectl delete clusterpolicy disallow-privileged-hostpath-enforce --ignore-not-found
kubectl delete namespace week4-security
helm uninstall kyverno -n kyverno
kubectl delete namespace kyverno
```

W4D5에서 GitOps policy drift까지 이어가려면 Kyverno는 삭제하지 않아도 된다.
