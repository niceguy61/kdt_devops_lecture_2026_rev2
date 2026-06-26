# Hands-on Lab: W4D3 kube-prometheus-stack

## 0. 준비 확인
```bash
kubectl config current-context
kind version
kind get clusters
kubectl get nodes
helm version --short
```

W4D1 metrics-server와 W4D2 ingress-nginx가 남아 있으면 더 많은 관찰 지점이 생긴다.

이번 실습은 kind cluster 기준으로만 진행한다. 다른 local Kubernetes가 남아 있으면 `kubectl` context가 엉뚱한 cluster를 가리키거나, Helm release와 Service 이름이 섞여서 관찰 결과가 흔들릴 수 있다.

kind cluster가 없다면:
```bash
kind create cluster --name paperclip-w4d3
kubectl config use-context kind-paperclip-w4d3
kubectl get nodes -o wide
```

검증 예시:
```text
NAME                             STATUS   ROLES           VERSION
paperclip-w4d3-control-plane     Ready    control-plane   v1.31.x
```

### kind 버전 주의
Docker Engine이 최신인데 오래된 kind를 쓰면 cluster 생성 단계에서 실패할 수 있다.

```text
failed to create cluster: could not find a log line that matches "Reached target .*Multi-User System.*|detected cgroup v1"
```

이 경우 kind를 최신 버전으로 올리고 다시 만든다.

```bash
go install sigs.k8s.io/kind@latest
~/go/bin/kind version
~/go/bin/kind create cluster --name paperclip-w4d3
```

수업 중 명령은 `kind`로 쓰되, 내 PC에 오래된 `/usr/local/bin/kind`가 먼저 잡히면 `~/go/bin/kind`처럼 실제 최신 binary 경로를 사용한다.

## 1. kube-prometheus-stack 설치
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f week4/day3/labs/kube-prometheus-stack/values.yaml
```

확인:
```bash
helm list -n monitoring
kubectl -n monitoring get pod,svc
kubectl get crd | grep monitoring.coreos.com
```

성공 기준:
```text
Prometheus, Grafana, Alertmanager, node-exporter, kube-state-metrics Pod가 Running/Ready
ServiceMonitor, PodMonitor, PrometheusRule CRD 존재
```

실제 검증 출력 예시:
```text
alertmanager-kube-prometheus-stack-alertmanager-0          2/2 Running
kube-prometheus-stack-grafana-...                          3/3 Running
kube-prometheus-stack-kube-state-metrics-...               1/1 Running
kube-prometheus-stack-operator-...                         1/1 Running
kube-prometheus-stack-prometheus-node-exporter-...          1/1 Running
prometheus-kube-prometheus-stack-prometheus-0              2/2 Running
```

## 2. Prometheus 접속
```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-prometheus 9090:9090
```

브라우저:
```text
http://localhost:9090
```

확인할 메뉴:
| 메뉴 | 확인 |
|---|---|
| Status -> Targets | scrape target UP/DOWN |
| Alerts | alert rule 상태 |
| Graph | PromQL query |

kind/local 환경에서는 일부 control plane target이 `DOWN`으로 보일 수 있다. 예를 들어 `kube-scheduler`가 `up=0`으로 보이면 stack 전체 설치 실패라고 단정하지 말고 target error와 ServiceMonitor endpoint를 먼저 확인한다.

## 3. Grafana 접속
```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3000:80
```

브라우저:
```text
http://localhost:3000
```

로그인:
```text
user: admin
password: paperclip-local
```

확인 dashboard:
| dashboard keyword | 볼 것 |
|---|---|
| Kubernetes / Compute Resources / Namespace | namespace별 CPU/memory |
| Kubernetes / Compute Resources / Pod | Pod CPU/memory |
| Kubernetes / Kubelet | kubelet, pod resource |
| Node Exporter | node CPU/memory/disk/network |

## 4. PromQL 기본 확인
Prometheus Graph에서 실행:
```promql
up
```

```promql
kube_pod_container_status_restarts_total
```

```promql
sum by (namespace) (container_memory_working_set_bytes)
```

```promql
sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{container!="", image!=""}[5m]))
```

## 5. 장애 시나리오 배포
```bash
kubectl apply -f week4/day3/labs/observability-scenarios/namespace.yaml
kubectl apply -f week4/day3/labs/observability-scenarios/crashloop-demo.yaml
kubectl apply -f week4/day3/labs/observability-scenarios/cpu-pressure-demo.yaml
kubectl apply -f week4/day3/labs/observability-scenarios/readiness-bad-demo.yaml
```

kubectl 증거:
```bash
kubectl -n week4-observe get pod
kubectl -n week4-observe describe pod -l app=crashloop-demo
kubectl -n week4-observe describe pod -l app=readiness-bad-demo
```

PromQL:
```promql
kube_pod_container_status_restarts_total{namespace="week4-observe"}
```

```promql
sum by (pod) (rate(container_cpu_usage_seconds_total{namespace="week4-observe", container!="", image!=""}[2m]))
```

## 6. Alert preview
```bash
kubectl apply -f week4/day3/labs/observability-scenarios/prometheus-rule-preview.yaml
kubectl -n week4-observe get prometheusrule
```

Prometheus UI:
```text
Alerts -> Week4ObservePodRestarting
```

alert는 즉시 firing되지 않을 수 있다. `for: 1m` 동안 조건이 유지되어야 한다.

API로 확인:
```bash
curl -s --get 'http://localhost:9090/api/v1/query' \
  --data-urlencode 'query=ALERTS{alertname="Week4ObservePodRestarting"}'
```

검증 예시:
```text
alertname="Week4ObservePodRestarting"
alertstate="firing"
namespace="week4-observe"
pod="crashloop-demo-..."
value="1"
```

## 6.5 실제로 헷갈리는 readiness rollout 상태
`readiness-bad-demo`는 nginx에 존재하지 않는 `/not-ready` path를 readiness probe로 걸어 실패하게 만든다.

```bash
kubectl -n week4-observe describe pod -l app=readiness-bad-demo
```

event 예시:
```text
Readiness probe failed: HTTP probe failed with statuscode: 404
```

이미 Ready였던 이전 Pod가 남아 있고 새 Pod만 `0/1 Running`일 수 있다.

```text
readiness-bad-demo-...   1/1 Running
readiness-bad-demo-...   0/1 Running
```

이건 이상한 현상이 아니라 rollout이 새 Pod를 Ready로 만들지 못해 멈춘 상태다. 운영에서는 이때 `rollout status`, `describe pod`, Endpoint 변화를 함께 본다.

## 7. Cleanup
```bash
kubectl delete namespace week4-observe
helm uninstall kube-prometheus-stack -n monitoring
kubectl delete namespace monitoring
```

W4D4에서도 observability를 계속 쓰려면 stack은 삭제하지 않아도 된다.
