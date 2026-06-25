# Week 4 Day1: 운영 가능한 Workload와 Helm 기반 관찰

## Overview
W4D1은 W3D4~W3D5에서 배운 Kubernetes 기본 요소를 운영 가능한 workload 기준으로 끌어올리는 날이다. Pod, Deployment, Service를 만들 수 있다는 것은 시작점일 뿐이다. 실제 운영에서는 image 밖 설정, secret 주입, health check, resource 요청/제한, metric 관찰이 함께 있어야 한다.

오늘부터 add-on 설치 표준은 Helm이다. `kubectl apply -f <remote-url>`로 설치를 끝내지 않고, chart repository, release name, namespace, values file, upgrade, rollback, uninstall까지 하나의 설치 루프로 기록한다.

## Learning Goals
- W3D4~W3D5에서 배운 Pod, Deployment, Service를 운영 기준으로 다시 설명한다.
- Helm의 chart, repository, release, namespace, values, upgrade, rollback, uninstall을 구분한다.
- Helm 설치를 `repo add/update -> upgrade --install -> status/list -> values 확인 -> uninstall` 루프로 반복한다.
- ConfigMap과 Secret을 image 밖 runtime config로 사용하고 `.env`와 Kubernetes object의 관계를 설명한다.
- liveness/readiness/startup probe가 restart와 traffic 수용에 미치는 차이를 확인한다.
- resource requests/limits가 scheduling, OOMKilled, CPU throttling, 비용 감각과 연결되는 이유를 설명한다.
- metrics-server를 Helm으로 설치하고 `kubectl top node/pod`로 resource metric을 확인한다.
- 실습 결과를 구름 EXP 배움일기에 운영 evidence 중심으로 정리한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Week3 Kubernetes 2일 요약 + 운영 가능한 workload 기준 | config, secret, health, resource, metric 기준 |
| 2교시 | Helm 기본 개념 | chart, repository, release, values, upgrade, rollback, uninstall |
| 3교시 | Helm 공통 설치 루프 | repo add/update, upgrade --install, list/status, uninstall |
| 4교시 | ConfigMap과 Secret | `.env`, runtime config, Secret base64와 보안 주의 |
| 5교시 | probe와 readiness | liveness/readiness/startup, endpoint, restart |
| 6교시 | resource requests/limits | scheduler, OOMKilled, CPU throttling, 비용 |
| 7교시 | metrics-server 설치와 관찰 | Helm install, Metrics API, `kubectl top`, HPA preview |
| 8교시 | 구름 EXP 배움일기 | Helm 패턴과 운영 evidence 정리 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 당일 실습 명령, 예상 결과, 장애 확인 순서 |
| `academic-foundations.md` | Helm, ConfigMap/Secret, probe, resource, metrics-server 개념 정리 |
| `labs/workload-basics/` | 운영형 Deployment, ConfigMap, Secret, probe/resource 실습 manifest |
| `labs/helm-metrics-server/values.yaml` | kind/local 실습용 metrics-server Helm values |

## Evidence Policy
오늘 evidence는 “설치했다”보다 “설치 기준과 관찰 결과를 설명할 수 있다”에 둔다.

| Evidence | 남길 내용 |
|---|---|
| Helm release | `helm list -A`, `helm status ...` |
| values | `helm get values ...`, 수업 repo의 values file |
| runtime config | `kubectl describe pod`, env 주입 결과 |
| readiness | Service endpoint 변화, readiness 실패 메시지 |
| resource | `kubectl describe pod`, requests/limits, OOMKilled 또는 throttling 힌트 |
| metrics | `kubectl top node`, `kubectl top pod -n week4` |

## Official References
| Topic | Reference |
|---|---|
| Helm install/upgrade | https://helm.sh/docs/helm/helm_upgrade/ |
| Helm rollback | https://helm.sh/docs/helm/helm_rollback/ |
| ConfigMaps | https://kubernetes.io/docs/concepts/configuration/configmap/ |
| Secrets | https://kubernetes.io/docs/concepts/configuration/secret/ |
| Probes | https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ |
| Resource management | https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| Metrics Server | https://github.com/kubernetes-sigs/metrics-server |

## End-Of-Day Checklist
- [ ] Helm chart, repository, release, values의 차이를 설명했다.
- [ ] `helm upgrade --install`을 왜 기본 설치 명령으로 쓰는지 설명했다.
- [ ] ConfigMap과 Secret을 image 재빌드 없이 runtime config로 주입했다.
- [ ] Secret이 base64일 뿐 암호화 자체가 아니라는 점을 설명했다.
- [ ] readiness 실패가 Service endpoint에서 빠지는 흐름을 확인했다.
- [ ] requests/limits가 scheduling과 장애 양상에 미치는 영향을 설명했다.
- [ ] metrics-server를 Helm으로 설치하고 `kubectl top` 결과를 확인했다.

