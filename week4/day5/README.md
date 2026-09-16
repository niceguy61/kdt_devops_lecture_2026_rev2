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
| 7교시 | mesh traffic 선택 preview | sidecar 2/2와 app/proxy log 필수 preview, MSA graph/Kiali/fault injection 중 하나 선택 |
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

## 학습 제어: 회상·핵심·복구

### 시작 5분 회상
W4D4의 RBAC과 Kyverno를 자료 없이 비교한다. 하나는 “누가 요청할 수 있는가”, 다른 하나는 “요청 내용이 정책에 맞는가”라는 차이를 적는다.

### 오늘 반드시 가져갈 것
1. GitOps의 기준은 Git desired state이며, Argo CD는 이를 cluster state와 비교한다.
2. `Synced`와 `Healthy`는 다르다. sync 성공만으로 사용자 서비스 정상이라고 결론 내리지 않는다.
3. Istio/Kiali는 오늘의 필수 운영 모델이 아니라 GitOps 이후의 선택 관찰 preview다.

### 필수 경로와 선택 심화
필수 경로는 `Git manifest → Argo CD Application → sync → drift → 원인 확인`이다. Istio, sidecar, mTLS, Kiali graph, fault injection은 시간이 남을 때 수행하는 선택 심화이며, GitOps 필수 경로의 증거를 남긴 뒤 시작한다.

### 최소 복구 경로
`kubectl config current-context` → Argo CD Pod/Service → Application의 sync/health → Git path/revision → 대상 namespace의 `get/describe/events` 순서로 복구한다. 다음 날로 넘어가기 전 drift와 sync failure의 원인을 각각 한 문장으로 설명할 수 있어야 한다.

## 인지 부하를 줄이는 범위 경계

W4D5의 필수 학습 경로는 GitOps 하나로 고정한다.

```text
Git manifest → Argo CD Application → Sync/Health 확인 → Drift 재현 → 원인별 복구
```

Istio/Kiali는 Kubernetes 운영을 확장하는 선택 심화 preview다. sidecar, mTLS, traffic graph, fault injection은 Argo CD의 sync/health evidence를 완성한 뒤 다룬다. 시간이 부족하면 mesh 설치보다 GitOps drift 진단을 완료하는 것을 우선한다.