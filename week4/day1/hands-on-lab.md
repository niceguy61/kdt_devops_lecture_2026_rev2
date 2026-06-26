# Hands-on Lab: W4D1 Helm, Config, Probe, Resource, Metrics

## Lab Goal
오늘 실습은 운영형 workload의 최소 기준을 확인한다.

1. namespace를 만들고 runtime config를 ConfigMap/Secret으로 분리한다.
2. readiness/liveness probe와 resources가 포함된 Deployment를 배포한다.
3. readiness 실패가 Service endpoint에 어떤 영향을 주는지 본다.
4. Helm으로 metrics-server를 설치하고 `kubectl top`으로 관찰한다.
5. 실습 후 release와 namespace를 안전하게 정리한다.

## 0. 준비 확인
```bash
kubectl config current-context
kubectl get nodes -o wide
helm version
```

기대값:
```text
current-context가 W3D4/W3D5에서 만든 kind cluster를 가리킨다.
node가 Ready 상태다.
helm version이 출력된다.
```

Helm이 없다면 먼저 설치한다.

macOS:
```bash
brew install helm
```

WSL Ubuntu:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

## 1. 실습 변수 설정
```bash
export NS=week4
export LAB=week4/day1/labs/workload-basics

kubectl apply -f "$LAB/namespace.yaml"
kubectl get ns "$NS"
```

## 2. ConfigMap과 Secret 적용
```bash
kubectl apply -f "$LAB/configmap.yaml"
kubectl apply -f "$LAB/secret.yaml"

kubectl -n "$NS" get configmap api-config
kubectl -n "$NS" get secret api-secret
```

Secret의 실제 값은 출력하지 않는다. 수업에서는 구조만 확인한다.

```bash
kubectl -n "$NS" describe secret api-secret
```

확인 포인트:
| 출력 | 의미 |
|---|---|
| `Data` | secret key 개수 |
| 값 미노출 | `describe`는 secret value를 그대로 보여주지 않음 |
| base64 저장 | `kubectl get secret -o yaml`에서는 인코딩된 값이 보일 수 있음 |

## 3. 운영형 Deployment 배포
```bash
kubectl apply -f "$LAB/deployment.yaml"
kubectl apply -f "$LAB/service.yaml"

kubectl -n "$NS" rollout status deploy/runtime-api
kubectl -n "$NS" get deploy,pod,svc,endpoints -o wide
```

기대값 예시:
```text
deployment "runtime-api" successfully rolled out
NAME                              READY   UP-TO-DATE   AVAILABLE
deployment.apps/runtime-api       2/2     2            2

NAME                 ENDPOINTS
endpoints/runtime-api 10.244.x.x:8080,10.244.x.y:8080
```

Pod 상세에서 env, probe, resources를 확인한다.

```bash
POD=$(kubectl -n "$NS" get pod -l app=runtime-api -o jsonpath='{.items[0].metadata.name}')
kubectl -n "$NS" describe pod "$POD"
```

확인할 위치:
| 항목 | 확인 내용 |
|---|---|
| Environment Variables from | ConfigMap/Secret 주입 |
| Readiness | path, delay, period, 실패 기준 |
| Liveness | restart 판단 기준 |
| Requests/Limits | CPU/memory 요청과 상한 |

## 4. Service 통신 확인
cluster 내부에서 curl용 임시 Pod를 띄워 Service DNS로 호출한다.

```bash
kubectl -n "$NS" run curlbox --rm -it --restart=Never \
  --image=curlimages/curl:8.10.1 \
  -- curl -s http://runtime-api
```

기대값:
```text
hello from kubernetes runtime config
```

여기서 중요한 점은 response text가 image에 baked-in된 값이 아니라 ConfigMap의 `RESPONSE_MESSAGE`에서 왔다는 것이다.

## 5. 잘못된 readiness 실험
```bash
kubectl apply -f "$LAB/deployment-bad-readiness.yaml"
kubectl -n "$NS" get pods -l app=runtime-api-bad-readiness
kubectl -n "$NS" describe pod -l app=runtime-api-bad-readiness
```

기대 출력 패턴:
```text
READY   STATUS
0/1     Running

Readiness probe failed: HTTP probe failed with statuscode: 404
```

이 Pod는 Running이어도 Ready가 아니다. Service가 붙어 있다면 endpoint에서 제외된다. 운영에서는 “컨테이너가 떠 있음”과 “사용자 traffic을 받아도 됨”을 분리해서 봐야 한다.

정리:
```bash
kubectl -n "$NS" delete deploy runtime-api-bad-readiness
```

## 6. OOMKilled 실험
memory limit이 너무 작으면 container가 종료될 수 있다.

```bash
kubectl apply -f "$LAB/pod-oom-demo.yaml"
kubectl -n "$NS" get pod oom-demo -w
```

다른 터미널에서:
```bash
kubectl -n "$NS" describe pod oom-demo
```

기대 출력 패턴:
```text
Reason: OOMKilled
Exit Code: 137
```

실습 시간이 부족하면 이 Pod는 오래 기다리지 말고 삭제한다.

```bash
kubectl -n "$NS" delete pod oom-demo --ignore-not-found
```

## 7. Helm으로 metrics-server 설치
```bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm repo update

helm upgrade --install metrics-server metrics-server/metrics-server \
  --namespace kube-system \
  -f week4/day1/labs/helm-metrics-server/values.yaml
```

설치 확인:
```bash
helm list -n kube-system
helm status metrics-server -n kube-system
kubectl -n kube-system get deploy,pod -l app.kubernetes.io/name=metrics-server
kubectl -n kube-system get sa | grep metrics-server
kubectl get apiservice v1beta1.metrics.k8s.io
```

metrics-server는 `kube-system`에 있지만 `kubectl top pod -n week4` 결과를 제공한다. 이건 `week4` Pod가 metrics-server와 직접 통신한다는 뜻이 아니라, API server가 `metrics.k8s.io` APIService를 통해 metrics-server로 요청을 전달한다는 뜻이다.

```bash
kubectl describe apiservice v1beta1.metrics.k8s.io
```

확인 포인트:
| 항목 | 의미 |
|---|---|
| `Service` | `kube-system/metrics-server`로 연결되는지 |
| `Available` | Metrics API가 사용 가능한지 |
| `Message` | 연결 실패 이유 |

kind/local에서 `--kubelet-insecure-tls`는 kubelet 인증서 검증 문제를 우회하기 위한 실습용 설정이다. 운영 환경에서는 cluster 인증서 체계에 맞게 해결해야 한다.

## 8. `kubectl top` 확인
metrics-server가 뜬 직후에는 metric이 바로 보이지 않을 수 있다. 30~90초 기다린다.

```bash
kubectl top node
kubectl top pod -n "$NS"
```

기대 출력:
```text
NAME                       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
paperclip-week3-control-plane ...

NAME                           CPU(cores)   MEMORY(bytes)
runtime-api-xxxxxxxxxx-xxxxx   1m           8Mi
```

자주 보는 오류:
| 증상 | 원인 후보 | 확인 |
|---|---|---|
| `Metrics API not available` | metrics-server 미설치 또는 아직 준비 전 | `kubectl get apiservice v1beta1.metrics.k8s.io` |
| metrics-server Pod CrashLoop | args, 권한, kubelet 연결 문제 | `kubectl -n kube-system logs deploy/metrics-server` |
| node metric 없음 | kubelet scrape 실패 | metrics-server log |
| `top pod`에 앱이 없음 | namespace 오타 또는 Pod 종료 | `kubectl -n week4 get pods` |

## 9. Helm rollback/uninstall 맛보기
이번 실습에서는 일부러 실패 upgrade를 오래 유지하지 않는다. 대신 명령의 의미를 확인한다.

```bash
helm history metrics-server -n kube-system
helm get values metrics-server -n kube-system
```

정리할 때:
```bash
helm uninstall metrics-server -n kube-system
kubectl delete namespace "$NS"
```

Day2 이후에도 metric을 계속 쓰려면 metrics-server는 삭제하지 않아도 된다. 단, 어떤 release를 남겼는지 `helm list -A`에 evidence를 남긴다.

## Evidence Template
```markdown
# W4D1 evidence

## Helm
- helm version:
- metrics-server release:
- values file:

## Workload
- namespace:
- Deployment ready:
- ConfigMap/Secret 주입 확인:
- readiness 실패 메시지:
- resource requests/limits:

## Metrics
- `kubectl top node` 핵심 출력:
- `kubectl top pod -n week4` 핵심 출력:
- 막힌 지점과 해결:
```
