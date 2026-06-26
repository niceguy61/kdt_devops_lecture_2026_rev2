# Week 4 Day5: GitOps와 Service Mesh Preview

## Overview
W4D5는 W3D4부터 이어진 Kubernetes 7일 탐험의 마지막 날이다. GitHub Actions가 image를 만들고 push하는 CI라면, Argo CD는 Git repository의 Kubernetes manifest를 cluster 상태로 맞추는 CD/GitOps 도구다. 후반부에는 Istio와 Kiali를 Helm으로 설치하고 sidecar, traffic graph, fault injection preview를 확인한다.

오늘도 설치는 Helm으로 통일한다. Argo CD, Istio, Kiali 모두 Helm release와 values file, 검증 명령, cleanup 명령을 함께 둔다.

## Learning Goals
- GitHub Actions와 Argo CD의 역할 차이를 설명한다.
- Argo CD를 Helm으로 설치하고 UI/API 접속 기준을 확인한다.
- Application manifest로 Git repository path를 cluster namespace에 sync한다.
- drift, OutOfSync, manual sync, prune/self-heal의 의미를 설명한다.
- Istio sidecar, Envoy, mesh traffic, mTLS, VirtualService 개념을 preview 수준으로 이해한다.
- Istio/Kiali를 Helm으로 설치하고 namespace injection과 sidecar container를 확인한다.
- Kiali graph에서 서비스 간 traffic을 확인하고 fault injection preview를 적용한다.
- MSA 형태의 mesh sample app으로 `frontend -> bff -> catalog/order -> inventory/payment` 통신 구조를 graph로 확인한다.
- GitOps/mesh를 운영 runbook과 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day4 요약 + GitOps 개념 | CI/CD 책임 분리, Git desired state |
| 2교시 | Argo CD 설치 | Helm release, admin password, port-forward |
| 3교시 | Argo CD Application 생성 | repoURL/path/targetRevision, sync status |
| 4교시 | drift와 sync | OutOfSync, manual sync, prune/self-heal |
| 5교시 | Istio 개념 preview | sidecar, Envoy, mTLS, traffic policy |
| 6교시 | Istio/Kiali 설치 | istio-base, istiod, gateway, Kiali |
| 7교시 | mesh traffic 확인 | sidecar injection, MSA graph, Kiali graph, delay preview |
| 8교시 | 구름 EXP 배움일기 | GitOps/mesh evidence와 Kubernetes 7일 회고 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 전체 실습 순서 |
| `academic-foundations.md` | GitOps와 mesh 개념 |
| `labs/argocd/values.yaml` | Argo CD Helm values |
| `labs/argocd/application-template.yaml` | 개인 repo용 Application template |
| `labs/gitops-app/` | Argo CD가 sync할 sample manifest |
| `labs/istio/*.yaml` | Istio/Kiali Helm values |
| `labs/mesh-app/` | sidecar injection과 Kiali graph용 sample app |
| `labs/mesh-msa-app/` | MSA 통신 구조 확인용 mesh sample app |

## Official References
| Topic | Reference |
|---|---|
| Argo CD Docs | https://argo-cd.readthedocs.io/ |
| Argo Helm Charts | https://github.com/argoproj/argo-helm |
| Istio Helm Install | https://istio.io/latest/docs/setup/install/helm/ |
| Kiali Installation | https://kiali.io/docs/installation/ |
| Istio Traffic Management | https://istio.io/latest/docs/concepts/traffic-management/ |
