# Week 3 Day5 Hands-on Lab: Pod, Deployment, Service

## Lab Goal
kind cluster 위에서 첫 Kubernetes app을 실행한다. 오늘은 `week3` namespace 안에서 Pod, 장애 Pod, Deployment, Service, rollout을 확인한다.

## 공통 변수
```bash
export NS=week3
export LAB=week3/day5/labs/k8s-first-app
```

## Phase 0. Cluster target 확인
```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl get ns
k9s version 2>/dev/null || true
```

성공 기준:
```text
current-context가 kind-paperclip-week3 이거나 오늘 실습용 cluster를 가리킨다.
node STATUS가 Ready다.
```

주의:
```text
context가 다르면 엉뚱한 cluster에 배포할 수 있다.
명령이 실패하면 W3D4의 kind cluster 생성/확인 절차로 돌아간다.
```

k9s가 설치되어 있다면 현재 context를 확인한 뒤 UI를 잠깐 열어본다.

```bash
kubectl config current-context
k9s
```

최소 확인:
| 조작 | 확인 |
|---|---|
| `:nodes` | kind node가 보이는가 |
| `:ns` | `week3` namespace가 있는가 |
| `:pods` | Pod 목록 화면으로 이동 가능한가 |
| `q` | 종료 |

k9s는 선택 도구다. 설치가 안 되어 있으면 `kubectl` 명령만으로 실습을 진행한다.

## Phase 1. Namespace 생성
```bash
kubectl apply -f "$LAB/namespace.yaml"
kubectl get ns "$NS"
```

예상 패턴:
```text
namespace/week3 created 또는 unchanged
```

## Phase 2. 첫 Pod 실행
```bash
kubectl apply -f "$LAB/pod-hello.yaml"
kubectl -n "$NS" get pods -o wide
kubectl -n "$NS" describe pod hello-pod
kubectl -n "$NS" logs hello-pod
```

확인할 것:
| 명령 | 확인 기준 |
|---|---|
| `get pods -o wide` | `hello-pod`가 `Running`, `READY 1/1` |
| `describe pod` | image, containerPort, event |
| `logs` | nginx access/error log 출력 가능 |

Pod 내부에서 확인:
```bash
kubectl -n "$NS" exec hello-pod -- printenv HOSTNAME
kubectl -n "$NS" exec hello-pod -- nginx -v
```

## Phase 3. Pod 장애 1 - ImagePullBackOff
```bash
kubectl apply -f "$LAB/pod-bad-image.yaml"
kubectl -n "$NS" get pod bad-image-pod
kubectl -n "$NS" describe pod bad-image-pod
```

k9s를 쓰는 경우:
```text
:pods
/bad-image
d
```

이 화면에서 event를 확인하되, 기록은 `kubectl describe pod bad-image-pod -n week3` 출력으로 남긴다.

예상 패턴:
```text
STATUS: ImagePullBackOff 또는 ErrImagePull
Events: Failed to pull image
```

정리:
```bash
kubectl -n "$NS" delete pod bad-image-pod
```

## Phase 4. Pod 장애 2 - CrashLoopBackOff
```bash
kubectl apply -f "$LAB/pod-crashloop.yaml"
kubectl -n "$NS" get pod crashloop-pod
kubectl -n "$NS" logs crashloop-pod
kubectl -n "$NS" logs crashloop-pod --previous || true
kubectl -n "$NS" describe pod crashloop-pod
```

k9s를 쓰는 경우:
```text
:pods
/crashloop
l
d
```

log 화면에서 종료 메시지를 보고, describe 화면에서 restart/back-off event를 확인한다.

예상 패턴:
```text
STATUS: CrashLoopBackOff
RESTARTS가 증가한다.
logs에 intentional crash 메시지가 보인다.
```

`|| true`는 로그가 아직 previous container로 남지 않은 순간에도 실습 스크립트가 멈추지 않게 하기 위한 예외 처리다. 수업에서는 실패를 숨기는 용도가 아니라 "이 명령은 타이밍에 따라 실패할 수 있다"는 표시로 설명한다.

정리:
```bash
kubectl -n "$NS" delete pod crashloop-pod
```

## Phase 5. Deployment 배포
```bash
kubectl apply -f "$LAB/deployment.yaml"
kubectl -n "$NS" rollout status deployment/hello-web
kubectl -n "$NS" get deploy,rs,pod -l app=hello-web -o wide
```

확인할 것:
| Resource | 확인 기준 |
|---|---|
| Deployment | `READY 2/2` |
| ReplicaSet | Deployment가 만든 ReplicaSet 존재 |
| Pod | label `app=hello-web` Pod 2개 |

Deployment와 ReplicaSet count를 따로 읽는다.

```bash
kubectl -n "$NS" get deploy hello-web
kubectl -n "$NS" get rs -l app=hello-web
kubectl -n "$NS" get pod -l app=hello-web -o wide
```

해석:
```text
Deployment READY 2/2 = 앱 전체 replica 2개가 Ready
ReplicaSet DESIRED 2 = 현재 Pod template으로 Pod 2개 유지
Pod NODE = Scheduler가 배치한 node
```

주의:
```text
Deployment/ReplicaSet의 replica count는 node별 개수가 아니다.
node마다 1개씩 유지해야 하는 workload는 DaemonSet으로 설명한다.
```

Self-healing 확인:
```bash
POD_NAME=$(kubectl -n "$NS" get pod -l app=hello-web -o jsonpath='{.items[0].metadata.name}')
kubectl -n "$NS" delete pod "$POD_NAME"
kubectl -n "$NS" get pod -l app=hello-web -w
```

`-w`는 새 Pod가 만들어지는 것을 본 뒤 `Ctrl+C`로 종료한다.

## Phase 6. Service 생성과 endpoint 확인
```bash
kubectl apply -f "$LAB/service.yaml"
kubectl -n "$NS" get svc,endpoints hello-web
kubectl -n "$NS" describe svc hello-web
```

확인할 것:
```text
Service type은 ClusterIP다.
Endpoints에 Ready Pod IP가 2개 보인다.
```

내부 DNS 확인:
```bash
kubectl -n "$NS" run curlbox --rm -it --image=curlimages/curl:8.8.0 --restart=Never -- \
  curl -sI http://hello-web
```

성공 패턴:
```text
HTTP/1.1 200 OK
Server: nginx
```

## Phase 7. Service selector 장애
```bash
kubectl -n "$NS" patch service hello-web -p '{"spec":{"selector":{"app":"wrong-label"}}}'
kubectl -n "$NS" get endpoints hello-web
kubectl -n "$NS" run curlbox-fail --rm -it --image=curlimages/curl:8.8.0 --restart=Never -- \
  curl -sS --max-time 3 http://hello-web || true
```

예상 패턴:
```text
endpoints가 비어 있다.
curl은 timeout 또는 connection failure가 난다.
```

복구:
```bash
kubectl apply -f "$LAB/service.yaml"
kubectl -n "$NS" get endpoints hello-web
```

## Phase 8. Rollout과 undo
현재 image 확인:
```bash
kubectl -n "$NS" get deployment hello-web -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
kubectl -n "$NS" rollout history deployment/hello-web
```

정상 image 변경:
```bash
kubectl -n "$NS" set image deployment/hello-web nginx=nginx:1.27-alpine
kubectl -n "$NS" rollout status deployment/hello-web
kubectl -n "$NS" rollout history deployment/hello-web
```

실패 image 변경:
```bash
kubectl -n "$NS" set image deployment/hello-web nginx=nginx:not-a-real-tag
kubectl -n "$NS" rollout status deployment/hello-web --timeout=20s || true
kubectl -n "$NS" get pods -l app=hello-web
kubectl -n "$NS" describe deployment hello-web
```

복구:
```bash
kubectl -n "$NS" rollout undo deployment/hello-web
kubectl -n "$NS" rollout status deployment/hello-web
kubectl -n "$NS" get pods -l app=hello-web
```

## Phase 9. Evidence 정리
```markdown
# W3D5 Evidence
- context:
- node Ready:
- namespace:
- first Pod status:
- ImagePullBackOff event:
- CrashLoopBackOff log:
- Deployment READY:
- Service endpoint count:
- curlbox HTTP status:
- rollout failure symptom:
- rollout undo result:
- k9s로 확인한 화면 또는 resource:
- Week4 question:
```

## Cleanup
수업 후 cluster를 계속 쓸 예정이면 namespace를 남겨도 된다. 깨끗하게 지우려면 다음을 실행한다.

```bash
kubectl delete namespace "$NS"
```
