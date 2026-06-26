# Week 3 Day4: Kubernetes 컨셉, 배경, kind 설치

## Overview
Day 4는 Kubernetes YAML을 많이 치는 날이 아니다. 먼저 Kubernetes가 어떤 운영 문제에서 탄생했는지, cluster라는 단위가 왜 필요한지, control plane이 무엇을 저장하고 조정하는지부터 밑바닥에서 끌어올린다. Compose와의 연결은 보조 설명으로만 사용하고, 핵심은 `API Server`, `etcd`, `Scheduler`, `Controller Manager`, `kubelet`, `container runtime`의 역할을 이해하는 것이다.

오늘의 흐름:

```text
Kubernetes 탄생 배경
  -> cluster 운영 문제
  -> control plane 내부 구조
  -> node와 workload 실행 구조
  -> 선언적 API와 reconciliation
  -> 많이 쓰이는 이유와 한계
  -> 사용 분야와 참고 사례
  -> kind 실습 표준 선택
  -> WSL/macOS 설치
  -> kind cluster 생성/확인/삭제 기준
```

## Learning Goals
- Kubernetes가 container orchestrator로 등장한 배경을 설명한다.
- control plane, node, kubelet, container runtime, Pod, Service의 역할을 구분한다.
- `kubectl`, API Server, etcd, Scheduler, Controller Manager, kubelet, Pod가 각각 client, API 입구, 상태 저장소, 배치 판단, 상태 조정, node agent, workload 단위 중 어디에 해당하는지 설명한다.
- Kubernetes의 장점과 단점을 운영 관점에서 함께 설명한다.
- MSA, SaaS, platform engineering, CI/CD, managed Kubernetes, edge 환경에서 Kubernetes가 쓰이는 이유를 설명한다.
- 이번 과정의 Kubernetes 실습 도구를 kind로 통일하는 이유와 한계를 설명한다.
- WSL/macOS에서 Docker, `kubectl`, `kind` 설치 상태를 확인한다.
- k9s 같은 Kubernetes TUI 도구를 선택 설치하고, `kubectl` current-context를 그대로 바라본다는 점을 이해한다.
- kind cluster를 만들고 context, node, cluster-info, namespace를 확인한다.
- cluster를 계속 유지할지 삭제할지 판단 기준을 세운다.

## Lesson Index
| 교시 | 주제 | 핵심 산출 |
|---|---|---|
| 1교시 | Kubernetes 탄생 배경과 cluster 운영 문제 | Borg/cluster scheduler/orchestrator 관점 |
| 2교시 | Control Plane 밑바닥 | API Server, etcd, Scheduler, Controller Manager |
| 3교시 | Node와 workload 실행 구조 | Node, kubelet, container runtime, Pod |
| 4교시 | 선언적 API와 reconciliation | desired state, controller loop, self-healing |
| 5교시 | 장점/단점과 사용 분야 | 표준화, 운영 비용, MSA/SaaS/platform team |
| 6교시 | kind를 선택하는 이유 | kind 단일 표준, Docker 기반 local cluster 한계 |
| 7교시 | WSL/macOS 설치 | Docker, kubectl, kind version evidence |
| 8교시 | kind cluster 생성과 확인 | context/node/cluster-info/namespace 확인, 다음날 연결 |

## Core Component Baseline
Day4에서 최소한 다음 문장은 말할 수 있어야 한다.

| 구성요소 | 한 줄 기준 |
|---|---|
| `kubectl` | 사용자가 Kubernetes API Server에 요청을 보내는 client |
| API Server | Kubernetes의 모든 요청이 들어오는 API 입구 |
| Control Plane | cluster 상태를 저장하고 배치/복구/조정을 담당하는 관리 계층 |
| etcd | desired/current state를 저장하는 cluster 상태 저장소 |
| Scheduler | 아직 node가 정해지지 않은 Pod의 배치 node를 결정 |
| Controller Manager | 원하는 상태와 현재 상태의 차이를 줄이는 controller 묶음 |
| kubelet | node 안에서 Pod spec을 실제 실행 상태로 맞추는 agent |
| Pod | Kubernetes가 배치하는 최소 workload 단위 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 설치 확인, kind cluster 생성/삭제 절차 |
| `academic-foundations.md` | Kubernetes 핵심 개념과 공식 문서 연결 |
| `labs/kind-cluster/kind-config.yaml` | 수업용 kind cluster 설정 |
| `labs/k8s-first-pod/` | Day5 첫 Pod 실습으로 이어질 manifest |

## Evidence Policy
오늘 evidence는 설치 성공보다 "어떤 대상과 연결되어 있는지"를 남기는 것이 중요하다.

| Evidence | 확인할 것 |
|---|---|
| Docker | `docker version`, Docker Desktop/Engine 실행 여부 |
| kubectl | client version, current-context |
| kind | kind version, cluster list |
| k9s | optional install, current context 확인 |
| cluster | `kubectl get nodes -o wide`에서 node Ready |
| context | `kind-paperclip-week3`를 보고 있는지 |
| troubleshooting | 실패 명령, 오류 메시지, 첫 확인 명령 |

## Official References
| Topic | Reference |
|---|---|
| Kubernetes Concepts | https://kubernetes.io/docs/concepts/ |
| Kubernetes Overview | https://kubernetes.io/docs/concepts/overview/ |
| Kubernetes Components | https://kubernetes.io/docs/concepts/overview/components/ |
| kubectl Linux Install | https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/ |
| kubectl macOS Install | https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/ |
| kind Quick Start | https://kind.sigs.k8s.io/docs/user/quick-start/ |
| kind Configuration | https://kind.sigs.k8s.io/docs/user/configuration/ |
| k9s Install | https://k9scli.io/topics/install/ |

## End-Of-Day Checklist
- [ ] Kubernetes가 Compose의 단순 대체물이 아니라 cluster 운영 API라는 점을 설명했다.
- [ ] control plane과 node의 역할을 구분했다.
- [ ] Pod가 container와 같은 말이 아니라 Kubernetes의 배포 최소 단위라는 점을 설명했다.
- [ ] Kubernetes의 장점과 단점을 둘 다 말했다.
- [ ] WSL/macOS 중 본인 환경 기준 설치 상태를 확인했다.
- [ ] 선택 사항으로 k9s를 설치하거나, k9s가 어떤 용도의 TUI인지 설명했다.
- [ ] kind cluster를 생성하고 `kubectl get nodes` 결과를 확인했다.
- [ ] context가 잘못되었을 때 생길 위험을 설명했다.
- [ ] Day5에서 Pod/Deployment/Service로 이어질 질문을 남겼다.
