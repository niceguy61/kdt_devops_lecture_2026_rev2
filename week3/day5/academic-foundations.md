# Week 3 Day5 Academic Foundations

## Day5의 위치
W3D4가 Kubernetes가 왜 필요한지와 control plane/node 구조를 잡는 날이었다면, W3D5는 그 구조 위에서 처음으로 workload를 실행하는 날이다. 아직 Ingress, ConfigMap, Secret, Helm add-on, observability, RBAC, Kyverno, Argo CD, Istio로 가지 않는다. 그 전에 Pod, Deployment, Service가 정확히 무엇을 해결하는지 확인해야 한다.

## 핵심 Object 기준
| Object | 해결하는 문제 | 오늘 확인할 증거 |
|---|---|---|
| Namespace | 실습 리소스를 논리적으로 격리 | `kubectl get ns`, `kubectl -n week3 ...` |
| Pod | container 실행의 최소 Kubernetes 단위 | `STATUS`, `READY`, `RESTARTS`, `logs`, `describe` |
| Deployment | 원하는 replica 수와 Pod template 유지 | `deploy`, `rs`, `pod`, `rollout status` |
| ReplicaSet | Deployment가 만든 Pod 집합 관리 | `kubectl get rs`, owner reference |
| Service | 바뀌는 Pod IP 뒤에 안정적인 접근점 제공 | `svc`, `endpoints`, curlbox 응답 |

## Pod는 Container와 다르다
Pod는 container 하나와 같은 말이 아니다. 대부분의 첫 실습에서는 Pod 하나에 container 하나를 넣지만, Pod는 shared network namespace, volume, labels, restart policy, status를 포함하는 Kubernetes workload 단위다.

```text
Pod
  -> container spec
  -> shared network namespace
  -> labels
  -> volume reference
  -> status
```

## Deployment가 필요한 이유
Pod를 직접 만들면 한 번 실행은 가능하다. 하지만 운영에서는 Pod가 죽거나 node가 바뀌거나 image를 교체해야 한다. Deployment는 원하는 상태를 선언하고 ReplicaSet을 통해 Pod 집합을 유지한다.

| 직접 Pod | Deployment |
|---|---|
| 단일 실행 확인에 적합 | 운영 배포 단위에 적합 |
| Pod가 삭제되면 끝 | replica 수를 다시 맞춤 |
| rollout history 없음 | rollout status/history/undo 가능 |
| template 변경 추적이 약함 | Pod template 변경을 rollout으로 관리 |

## Service가 필요한 이유
Pod IP는 안정적인 계약이 아니다. Pod가 재생성되면 IP가 바뀔 수 있다. Service는 selector로 Pod 집합을 찾고, ClusterIP와 DNS 이름을 통해 안정적인 접근점을 제공한다.

```text
client Pod
  -> http://hello-web.week3.svc.cluster.local
  -> Service
  -> Endpoints
  -> Ready Pod IPs
```

## 장애 상태를 읽는 기준
| 상태 | 먼저 볼 것 | 흔한 원인 |
|---|---|---|
| `ImagePullBackOff` | `describe pod` event | image 이름/tag 오류, registry auth 문제 |
| `CrashLoopBackOff` | `logs --previous`, restart count | process가 시작 후 종료, command/env 오류 |
| `Pending` | `describe pod` scheduling event | resource 부족, taint/toleration, volume 문제 |
| `Running but NotReady` | readiness probe, endpoint | app 준비 실패, probe path/port 오류 |
| Service 응답 없음 | selector, endpoint, port/targetPort | label 불일치, Pod NotReady, 잘못된 port |

## Day5에서 Week4로 이어지는 질문
| Day5 질문 | Week4에서 다룰 주제 |
|---|---|
| 설정값을 image에 넣지 않으려면? | ConfigMap, Secret |
| 앱이 진짜 traffic 받을 준비가 됐는지 어떻게 아나? | readiness/liveness probe |
| CPU/memory 사용량을 어떻게 보나? | metrics-server, Prometheus/Grafana |
| cluster 밖에서 어떻게 접속하나? | ingress-nginx |
| 누가 배포할 수 있는지 어떻게 제한하나? | RBAC, ServiceAccount |
| 위험한 manifest를 어떻게 차단하나? | Kyverno |
| Git에 있는 manifest와 cluster 상태를 어떻게 맞추나? | Argo CD |
| 서비스 간 traffic을 더 세밀하게 제어하려면? | Istio, Kiali |

## 공식/현업 참고 자료
| 자료 | URL | 수업 연결 |
|---|---|---|
| Pods | https://kubernetes.io/docs/concepts/workloads/pods/ | Pod와 container 구분 |
| Deployments | https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ | ReplicaSet, rollout, desired state |
| Services | https://kubernetes.io/docs/concepts/services-networking/service/ | selector, endpoint, ClusterIP |
| kubectl Quick Reference | https://kubernetes.io/docs/reference/kubectl/quick-reference/ | 상태 확인 명령 |

## 수업 적용 원칙
- manifest는 "YAML 작성 과제"가 아니라 "원하는 상태를 API Server에 제출하는 계약"으로 읽는다.
- 장애 분석은 `get`으로 증상을 보고, `describe`로 event를 확인하고, `logs`로 app 출력을 확인하는 순서로 진행한다.
- 정상/비정상 판단은 브라우저 인상보다 command output, event, log, endpoint, rollout 상태로 남긴다.
- Day5에는 add-on을 설치하지 않는다. Week4부터 모든 Kubernetes add-on은 Helm으로 설치한다.
