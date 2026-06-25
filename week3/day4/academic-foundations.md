# Week 3 Day4 Academic Foundations

## Kubernetes 정의
Kubernetes 공식 문서는 Kubernetes를 containerized workload와 service를 관리하기 위한 portable, extensible, open source platform으로 설명한다. 핵심은 "container 실행 명령 모음"이 아니라 "원하는 상태를 선언하고, cluster가 그 상태에 가까워지도록 조정하는 운영 API"라는 점이다.

## 탄생 배경
Kubernetes는 container가 많아졌기 때문에만 등장한 것이 아니다. 더 근본적인 배경은 cluster 단위로 workload를 배치하고, 실패를 복구하고, 원하는 상태를 계속 유지해야 하는 운영 문제다.

| 운영 문제 | Kubernetes가 다루는 방식 |
|---|---|
| workload 배치 | Scheduler가 node 선택 |
| 상태 저장 | API Server와 etcd에 object state 저장 |
| 상태 조정 | Controller가 desired/current state 차이를 줄임 |
| node 실행 | kubelet이 node에서 Pod 상태를 맞춤 |
| container 실행 | container runtime이 image pull/create/start |
| traffic 안정화 | Service가 Pod 집합의 안정적 접근점 제공 |

## 핵심 Architecture
| 구성요소 | 역할 |
|---|---|
| Cluster | Kubernetes가 관리하는 전체 실행 환경 |
| Control Plane | cluster 상태를 저장하고 조정하는 관리 계층 |
| API Server | `kubectl`과 controller가 통신하는 Kubernetes API 입구 |
| etcd | cluster desired/current state 저장소 |
| Scheduler | Pod를 어느 node에 배치할지 결정 |
| Controller Manager | desired state와 current state 차이를 줄이는 loop |
| Node | workload가 실제로 실행되는 machine |
| kubelet | node에서 Pod 상태를 맞추는 agent |
| Container Runtime | container를 실제로 실행하는 runtime |
| Pod | Kubernetes에서 배포/스케줄링되는 가장 작은 workload 단위 |
| Service | Pod 집합에 안정적인 접근 지점을 제공 |

## 기본 구성요소 구분
Kubernetes 기본 구성요소는 "요청을 보내는 도구", "요청을 받는 API", "상태 저장소", "배치 결정자", "상태 조정자", "node 실행 agent", "실제 workload 단위"로 나눠서 이해하면 쉽다.

| 구분 | 구성요소 | 설명 |
|---|---|---|
| Client | `kubectl` | kubeconfig의 context를 기준으로 API Server에 요청을 보냄 |
| API 입구 | API Server | 인증/인가, validation, admission, object 읽기/쓰기 담당 |
| 관리 계층 | Control Plane | API Server, etcd, Scheduler, Controller Manager 등 cluster 운영 구성요소의 묶음 |
| 상태 저장소 | etcd | Kubernetes object와 cluster state를 저장 |
| 배치 판단 | Scheduler | pending Pod를 어떤 node에 둘지 결정 |
| 상태 조정 | Controller Manager | desired state와 current state 차이를 줄임 |
| Node agent | kubelet | 자기 node에 배정된 Pod를 container runtime으로 실행 상태에 맞춤 |
| Workload 단위 | Pod | 하나 이상의 container를 포함하는 Kubernetes 최소 배포/스케줄링 단위 |

## Control Plane Node 선정 기준
예전에는 control plane node를 master node라고 부르는 자료가 많았다. 현재 수업에서는 `control plane node`라는 표현을 기준으로 사용한다.

control plane node는 app traffic을 많이 처리하는 서버가 아니라 cluster 운영 상태를 안정적으로 관리하는 서버다. 특히 API Server와 etcd가 흔들리면 전체 cluster의 배포, 조회, 복구, scheduling이 영향을 받는다.

| 기준 | 확인할 것 |
|---|---|
| CPU/memory 안정성 | API 요청과 controller loop가 밀리지 않는지 |
| disk 안정성 | etcd 저장소의 latency, 내구성, 백업 가능 여부 |
| network 안정성 | kubelet/API Server/component 간 통신이 안정적인지 |
| 장애 도메인 분산 | 여러 control plane을 같은 host/rack/AZ에 몰지 않았는지 |
| 운영 접근 통제 | SSH, certificate, kubeconfig, firewall 권한이 제한되어 있는지 |
| workload 격리 | 일반 app Pod가 control plane 자원을 소모하지 않도록 분리/taint를 적용하는지 |

학습용 kind에서는 단일 Docker container가 control plane node 역할을 한다. 운영 self-managed cluster에서는 보통 3대 이상의 홀수 개 control plane과 etcd quorum을 고려하고, managed Kubernetes에서는 cloud provider가 control plane 운영을 맡는다.

## Compose와 Kubernetes의 차이
Compose는 이미 충분히 배운 로컬 다중 container 실행 도구다. Kubernetes 수업에서는 Compose와의 비교를 보조 설명으로만 사용한다.

| 구분 | Docker Compose | Kubernetes |
|---|---|---|
| 주 사용 맥락 | 로컬/단일 host 개발, 작은 통합 환경 | cluster 기반 운영, 다수 node, 다수 workload |
| 실행 단위 | service/container | Pod, Deployment, Service 등 API object |
| 상태 관리 | `docker compose up/down` 중심 | desired state reconciliation |
| 복구 | restart policy 수준 | scheduler, controller, probe, rollout |
| 네트워크 | compose network/service name | cluster DNS, Service, Ingress |
| 확장 | 로컬 scale 제한 | node capacity와 controller 기반 확장 |
| 운영 비용 | 낮음 | 학습/관찰/보안/비용 관리 필요 |

## Declarative Operation
Kubernetes에서는 보통 "nginx container를 지금 실행해"보다 "nginx Pod/Deployment가 이런 상태로 있어야 해"라고 선언한다.

```text
desired state: replicas=3
current state: replicas=2
controller action: 부족한 Pod 1개 생성
```

이 방식은 편리하지만, YAML을 썼다고 자동으로 좋은 운영이 되는 것은 아니다. resource request/limit, probe, rollout strategy, secret, network policy, observability가 함께 설계되어야 한다.

## Kubernetes가 자주 쓰이는 이유
| 이유 | 설명 |
|---|---|
| 표준 API | cloud/vendor가 달라도 비슷한 object model 사용 |
| self-healing | 죽은 Pod 재생성, ready 아닌 Pod 제외 |
| service discovery | Pod IP가 바뀌어도 Service/DNS로 접근 |
| rollout/rollback | 새 버전 배포와 되돌리기 흐름 제공 |
| scaling | replica 수 조정, HPA 같은 자동 확장 연결 |
| ecosystem | Helm, Argo CD, Prometheus, service mesh 등 풍부 |

## 단점과 운영 비용
| 비용 | 설명 |
|---|---|
| 러닝커브 | object, controller, network, storage 개념이 많음 |
| YAML 복잡도 | 들여쓰기와 필드 의미를 모르면 장애가 숨어 있음 |
| 관찰 부담 | Pod, Deployment, Service, Event, Log를 함께 봐야 함 |
| 보안 범위 | RBAC, Secret, image pull, admission, network policy 필요 |
| 비용 관리 | node capacity, request/limit, idle resource 관리 필요 |
| 디버깅 난도 | "내 앱 문제"와 "cluster 문제"를 구분해야 함 |

## kind와 k3s
| 도구 | 적합한 경우 | 주의 |
|---|---|---|
| kind | 로컬 학습, CI 테스트, 빠른 cluster 생성/삭제 | Docker가 필요하고 실제 운영 cluster와 차이가 있음 |
| k3s | 경량 운영/edge/lab server | 설치 후 host에 오래 남는 운영 성격이 강함 |
| minikube | 로컬 학습, 다양한 driver | 환경 옵션이 많아 수업 표준화가 어려울 수 있음 |
| Docker Desktop Kubernetes | Docker Desktop 사용자에게 편함 | 학생 환경별 UI/상태 차이가 큼 |

이번 과정은 WSL/macOS 학생이 섞여 있고, Day5에서 첫 Pod와 Service로 빠르게 넘어가야 하므로 kind를 기준으로 한다.

## Day5 연결
Day4의 목표는 cluster를 만든 것에서 끝나지 않는다. Day5에서는 이 cluster 위에 다음 object를 올린다.

| Day4에서 확인 | Day5에서 사용 |
|---|---|
| `kubectl config current-context` | 어떤 cluster에 배포하는지 확인 |
| `kubectl get nodes` | workload가 올라갈 node 확인 |
| namespace | 실습 리소스 격리 |
| Pod manifest | 첫 workload 생성 |
| bad image manifest | ImagePullBackOff 분석 |

## 공식 문서 확인 기준
설치 명령은 시간이 지나며 바뀔 수 있다. 수업 자료의 명령이 실패하면 공식 문서를 먼저 확인한다.

| 확인할 문서 | 확인 이유 |
|---|---|
| Kubernetes kubectl install docs | OS별 최신 설치 명령 |
| kind Quick Start | 최신 kind 설치 방식과 cluster 생성 |
| kind Configuration | config file로 cluster 옵션 지정 |
| Kubernetes Components | control plane/node 용어 확인 |
