# Week 3 Day4 Hands-on Lab: kind 설치와 cluster 확인

## Lab Rule
오늘은 Kubernetes 앱 배포를 많이 하지 않는다. 목표는 `kubectl`이 어느 cluster를 바라보는지, kind가 어떤 방식으로 local cluster를 만드는지, 실패했을 때 무엇을 먼저 확인해야 하는지 익히는 것이다.

## Phase 1. 공통 사전 확인
```bash
docker version
docker compose version
docker ps
kubectl version --client=true
kind version
k9s version 2>/dev/null || true
```

판정:

| 명령 | 정상 기준 | 실패 시 먼저 볼 것 |
|---|---|---|
| `docker version` | client/server 둘 다 출력 | Docker Desktop/daemon 실행 여부 |
| `docker ps` | container 목록 출력 | permission, Docker context |
| `kubectl version --client=true` | client version 출력 | kubectl 설치/PATH |
| `kind version` | kind version 출력 | kind 설치/PATH |
| `k9s version` | 선택 설치 시 version 출력 | 설치하지 않았으면 건너뜀 |

## Phase 2. WSL 설치 기준
WSL에서는 Docker Desktop의 WSL integration이 켜져 있어야 한다.

```bash
docker version
docker ps
```

`kubectl` 설치는 공식 문서 기준으로 진행한다. Linux amd64 예시는 다음과 같다.

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl
kubectl version --client=true
```

kind 설치:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

선택 도구 k9s 설치:

```bash
wget https://github.com/derailed/k9s/releases/latest/download/k9s_linux_amd64.deb
sudo apt install ./k9s_linux_amd64.deb
rm k9s_linux_amd64.deb
k9s version
```

WSL 확인 포인트:

| 증상 | 원인 후보 | 확인 |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop 미실행 또는 WSL integration off | Docker Desktop Settings |
| `permission denied` | Docker socket 권한 문제 | Docker Desktop 방식인지 Linux Engine 방식인지 확인 |
| `kind: command not found` | PATH 미등록 | `which kind` |
| `kubectl: command not found` | PATH 미등록 | `which kubectl` |
| `k9s: command not found` | 선택 도구 미설치 | 설치하지 않았으면 정상, 필요 시 설치 |

## Phase 3. macOS 설치 기준
Homebrew가 있다면 다음 흐름이 가장 단순하다.

```bash
brew install kubectl kind
brew install k9s
kubectl version --client=true
kind version
k9s version
docker version
```

macOS 확인 포인트:

| 증상 | 원인 후보 | 확인 |
|---|---|---|
| Docker server 정보 없음 | Docker Desktop 미실행 | Docker Desktop 실행 |
| `brew` 없음 | Homebrew 미설치 | 공식 설치 여부 확인 |
| cluster 생성 지연 | Docker resource 부족 | Docker Desktop CPU/Memory |

## Phase 4. kind cluster 생성
수업용 config file을 사용한다.

```bash
cd /mnt/d/paperclip
cat week3/day4/labs/kind-cluster/kind-config.yaml
kind create cluster --config week3/day4/labs/kind-cluster/kind-config.yaml
```

이미 같은 이름의 cluster가 있으면 다음 중 하나를 선택한다.

```bash
kind get clusters
kind delete cluster --name paperclip-week3
kind create cluster --config week3/day4/labs/kind-cluster/kind-config.yaml
```

## Phase 5. kubectl 대상 확인
```bash
kubectl config current-context
kubectl config get-contexts
kubectl cluster-info
kubectl get nodes -o wide
```

기대:

| 확인 | 정상 기준 |
|---|---|
| current-context | `kind-paperclip-week3` |
| cluster-info | Kubernetes control plane URL 출력 |
| nodes | `paperclip-week3-control-plane` Ready |

context가 다르면 엉뚱한 cluster에 명령을 보낼 수 있다. Kubernetes 실습에서 가장 먼저 확인하는 습관을 들인다.

## Phase 5-1. k9s로 상태 보기 preview
k9s는 terminal UI로 Kubernetes resource를 탐색하는 도구다. 새 API를 쓰는 별도 cluster manager가 아니라, 현재 kubeconfig context를 사용해 Kubernetes API를 조회한다.

```bash
kubectl config current-context
k9s
```

수업 중 보여줄 최소 조작:

| 조작 | 의미 |
|---|---|
| `:nodes` | node 목록 보기 |
| `:ns` | namespace 보기 |
| `:pods` | Pod 목록 보기 |
| `0` | 모든 namespace 보기 |
| `/검색어` | 현재 목록 필터링 |
| `d` | 선택 resource describe |
| `l` | 선택 Pod log |
| `Esc` | 이전 화면 |
| `q` | 종료 |

k9s가 편하더라도 원인 분석 언어는 여전히 `kubectl get`, `describe`, `logs`, `events`다. TUI는 상태를 빠르게 훑는 도구이고, evidence에는 재현 가능한 명령과 핵심 출력을 남긴다.

## Phase 6. Namespace와 첫 연결 확인
Day5에서 사용할 namespace만 미리 만들어본다.

```bash
kubectl apply -f week3/day4/labs/k8s-first-pod/namespace.yaml
kubectl get namespaces
kubectl get all -n week3
```

`get all`이 비어 있어도 실패가 아니다. namespace만 만든 상태이기 때문이다.

## Phase 7. Troubleshooting Drill
일부러 없는 cluster/context를 보는 대신, 안전한 확인 명령만 실행한다.

```bash
kind get clusters
kubectl config current-context
kubectl get nodes
docker ps --filter name=paperclip-week3
```

오류별 판단:

| 오류 | 의미 | 첫 확인 |
|---|---|---|
| `No kind clusters found` | kind cluster 없음 | `kind create cluster ...` |
| `connection refused` | API server 미기동/삭제됨 | `kind get clusters`, `docker ps` |
| `context was not found` | kubeconfig context 없음 | `kubectl config get-contexts` |
| node `NotReady` | node 내부 구성 준비 실패 | `kubectl describe node`, Docker resource |
| `could not find a log line that matches "Reached target ..."` | kind node container가 부팅 목표 상태에 도달하지 못함. WSL/Docker/cgroup/systemd 환경 문제 가능 | Docker Desktop/WSL 재시작, kind 최신 버전, Docker resource, `docker logs paperclip-week3-control-plane` |

## Phase 8. 종료 기준
Day5 실습을 바로 이어갈 경우 cluster를 삭제하지 않는다.

유지:

```bash
kind get clusters
kubectl get nodes
```

삭제:

```bash
kind delete cluster --name paperclip-week3
kind get clusters
```

## Evidence Note
```markdown
# W3D4 kind Evidence
- OS:
- Docker version:
- kubectl client version:
- kind version:
- k9s version 또는 미설치:
- cluster name:
- current context:
- node status:
- namespace:
- troubleshooting note:
- keep or delete:
```
