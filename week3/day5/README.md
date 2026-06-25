# Week 3 Day5: Kubernetes 첫 앱 실행 - Pod, Deployment, Service

## Overview
Day 5는 W3D4에서 만든 kind cluster 위에 실제 workload를 올리는 날이다. 목표는 많은 object를 한 번에 외우는 것이 아니라 `kubectl`로 현재 상태를 읽고, manifest로 원하는 상태를 선언하고, 장애가 났을 때 `describe`, `events`, `logs`, `rollout`으로 증거를 찾는 감각을 만드는 것이다.

오늘은 add-on을 설치하지 않는다. Helm, metrics-server, ingress-nginx, Prometheus/Grafana, Kyverno, Argo CD, Istio는 Week4에서 주제별로 하나씩 심는다. Day5는 그 전에 반드시 잡아야 하는 기본 object인 Pod, Deployment, Service에 집중한다.

## Learning Goals
- `kubectl` context와 namespace를 확인하고, 잘못된 cluster에 배포하는 위험을 설명한다.
- Pod가 Kubernetes의 최소 workload 단위라는 점과 container와의 차이를 설명한다.
- `ImagePullBackOff`, `CrashLoopBackOff`, `Pending` 계열 장애에서 먼저 볼 증거를 구분한다.
- Deployment의 `replicas`, `selector`, `template`, ReplicaSet, self-healing 흐름을 설명한다.
- Service가 Pod IP 변화를 가리고 안정적인 DNS/ClusterIP를 제공하는 이유를 endpoint로 확인한다.
- rollout status/history/undo로 image 변경과 복구 흐름을 확인한다.
- Week4의 ConfigMap/Secret, Ingress, Observability, RBAC/Kyverno, Argo CD, Istio로 이어질 질문을 정리한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day4 요약 + kubectl 운영 루프 | context, namespace, get/describe/logs/events/apply/delete |
| 2교시 | 첫 Pod 실행 | Pod manifest, image, port, logs, exec, delete |
| 3교시 | Pod 장애 읽기 | ImagePullBackOff, CrashLoopBackOff, Pending 증거 구분 |
| 4교시 | Deployment가 필요한 이유 | replica, ReplicaSet, self-healing, 직접 Pod의 한계 |
| 5교시 | Deployment manifest 해부 | apiVersion, kind, metadata, spec, selector, template |
| 6교시 | Service와 내부 DNS | ClusterIP, selector, endpoint, service name DNS |
| 7교시 | rollout과 내부 통신 검증 | image tag 변경, rollout status/history/undo, curlbox |
| 8교시 | 구름 EXP 배움일기 | 오늘의 evidence, Week4 plugin 질문 정리 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 당일 실습 명령, 예상 결과, 장애 확인 순서 |
| `academic-foundations.md` | Pod/Deployment/Service 공식 개념과 운영 기준 |
| `labs/k8s-first-app/` | Pod, 장애 Pod, Deployment, Service 실습 manifest |

## Evidence Policy
오늘 evidence는 화면 캡처보다 명령과 핵심 출력 패턴을 우선한다.

| Evidence | 남길 내용 |
|---|---|
| cluster target | `kubectl config current-context`, `kubectl get nodes` |
| Pod 정상 | `kubectl -n week3 get pods -o wide`, `kubectl logs` |
| Pod 장애 | `kubectl describe pod`, event의 `Reason`, `Message` |
| Deployment | `kubectl get deploy,rs,pod`, replica 변화 |
| Service | `kubectl get svc,endpoints`, curlbox 응답 |
| rollout | `rollout status/history/undo` 결과 |

## Helm/Add-on Boundary
Day5에는 Helm add-on을 설치하지 않는다. 대신 Week4에서 아래 흐름으로 확장한다.

| Week4 | 연결되는 Day5 개념 |
|---|---|
| Helm + metrics-server | Pod resource 사용량과 `kubectl top` |
| ingress-nginx | Service 뒤의 app을 외부 traffic으로 노출 |
| kube-prometheus-stack | Pod/Deployment/Service 상태를 metric/dashboard로 관찰 |
| RBAC + Kyverno | 누가 배포할 수 있는지, 어떤 manifest가 차단되는지 확인 |
| Argo CD | 오늘 작성한 manifest를 Git 기준으로 sync |
| Istio/Kiali | Service 간 traffic을 mesh graph와 policy로 확인 |

## Official References
| Topic | Reference |
|---|---|
| Pods | https://kubernetes.io/docs/concepts/workloads/pods/ |
| Deployments | https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ |
| Services | https://kubernetes.io/docs/concepts/services-networking/service/ |
| kubectl Quick Reference | https://kubernetes.io/docs/reference/kubectl/quick-reference/ |

## End-Of-Day Checklist
- [ ] 지금 바라보는 cluster/context를 확인했다.
- [ ] Pod와 container의 차이를 설명했다.
- [ ] `ImagePullBackOff`와 `CrashLoopBackOff`에서 보는 증거를 구분했다.
- [ ] Deployment가 Pod를 다시 만드는 흐름을 확인했다.
- [ ] Service selector와 endpoint가 연결되는 것을 확인했다.
- [ ] rollout 실패와 undo 흐름을 설명했다.
- [ ] Week4에서 Helm add-on으로 확장할 질문을 남겼다.
