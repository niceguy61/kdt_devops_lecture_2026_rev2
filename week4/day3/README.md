# Week 4 Day3: Kubernetes Observability - Prometheus와 Grafana

## Overview
W4D3는 W4D2에서 만든 traffic 경로를 관찰 가능한 운영 시스템으로 확장한다. `kubectl logs`, `kubectl describe`, `kubectl top`만으로는 장애의 흐름과 추세를 보기 어렵다. 오늘은 `kube-prometheus-stack`을 Helm으로 설치하고 Prometheus target, Grafana dashboard, Pod/node metric, alert preview를 확인한다.

실습 cluster는 kind 기준으로 통일한다. 다른 local Kubernetes가 남아 있으면 context와 mount, Service 이름, port-forward 대상이 섞여 troubleshooting 난도가 올라간다. 수업 전에는 `kubectl config current-context`, `kind get clusters`, `kubectl get nodes`로 내가 어느 cluster를 보고 있는지 먼저 확인한다.

## Learning Goals
- logs, events, metrics, traces의 차이를 설명한다.
- kube-prometheus-stack을 Helm으로 설치하고 Prometheus, Grafana, Alertmanager, node-exporter, kube-state-metrics 구성요소를 확인한다.
- Prometheus target의 `UP/DOWN` 상태와 ServiceMonitor/PodMonitor 개념을 설명한다.
- Grafana dashboard에서 node/pod CPU, memory, restart, namespace별 resource 사용량을 확인한다.
- bad rollout, readiness 실패, restart 증가, CPU/memory 압박을 metric과 연결한다.
- alert rule, firing, pending, silence, threshold noise를 preview 수준으로 이해한다.
- 관찰 runbook을 증상, 관련 metric, 확인 명령, dashboard 위치, 개발팀 전달 정보로 정리한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day2 요약 + observability 기준 | logs/events/metrics/traces 차이 |
| 2교시 | kube-prometheus-stack 설치 | Helm release, Prometheus, Grafana, Alertmanager |
| 3교시 | Prometheus target 확인 | scrape target, ServiceMonitor, target down |
| 4교시 | Grafana dashboard 확인 | node/pod CPU/memory/restart |
| 5교시 | 장애와 metric 연결 | readiness, rollout, restart, resource 압박 |
| 6교시 | alert preview | rule, firing, pending, silence, noise |
| 7교시 | 관찰 runbook 작성 | 증상, metric, 명령, dashboard, 전달 정보 |
| 8교시 | 구름 EXP 배움일기 | target down, dashboard, 운영 질문 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 설치와 관찰 실습 순서 |
| `academic-foundations.md` | observability와 Prometheus Operator 개념 |
| `labs/kube-prometheus-stack/values.yaml` | Helm 설치 values |
| `labs/observability-scenarios/` | readiness, restart, resource 압박, alert preview manifest |

## Verified Local Baseline
아래 흐름은 kind `v0.32.0`, Kubernetes node image `kindest/node:v1.31.9`, Docker Desktop/WSL2 환경에서 실제 검증했다.

```text
monitoring namespace:
- Prometheus      2/2 Running
- Grafana         3/3 Running
- Alertmanager    2/2 Running
- kube-state-metrics, node-exporter, operator Running

week4-observe namespace:
- crashloop-demo       CrashLoopBackOff
- cpu-pressure-demo    Running
- readiness-bad-demo   새 Pod READY 0/1, readiness 404 event
```

Prometheus에서는 `Week4ObservePodRestarting` alert가 firing되는 것까지 확인했다.

## Official References
| Topic | Reference |
|---|---|
| Kubernetes Observability | https://kubernetes.io/docs/concepts/cluster-administration/observability/ |
| Prometheus Operator | https://github.com/prometheus-operator/prometheus-operator |
| Prometheus Operator API | https://prometheus-operator.dev/docs/api-reference/api/ |
| kube-prometheus-stack chart | https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack |
| Prometheus community Helm charts | https://github.com/prometheus-community/helm-charts |
