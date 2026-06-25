# Week 4: Kubernetes 운영 확장

Week 4는 W3D4~W3D5에서 시작한 Kubernetes 기본 흐름을 운영 가능한 MSA 배포 기준으로 확장한다. 모든 add-on 설치는 Helm을 기본 표준으로 사용하고, 설치 명령마다 release name, namespace, values file, 검증 명령, 제거 명령을 함께 남긴다.

## Day Index
| 일차 | 주제 | 핵심 산출물 |
|---|---|---|
| Day1 | 운영 가능한 workload와 resource 관찰 | Helm 설치 루프, ConfigMap/Secret, probe, resource, metrics-server |
| Day2 | Service, DNS, Ingress, 외부 traffic | ingress-nginx Helm 설치, host/path routing |
| Day3 | 장애와 성능 관찰 | kube-prometheus-stack, Prometheus target, Grafana dashboard |
| Day4 | 권한과 정책 | RBAC, Kyverno admission policy |
| Day5 | GitOps와 mesh preview | Argo CD, Istio, Kiali preview |

