<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [3일차](README.md) › 6/8교시</sub>

# 6교시 · kubectl과 kind 설치

> [!NOTE]
> **이번 시간에 할 일**
>
> - Docker가 kind를 돌릴 준비(cgroup v2, 메모리)가 됐는지 확인합니다.
> - **kubectl**(클러스터에 말하는 도구)과 **kind**(로컬 클러스터를 만드는 도구)를 설치합니다.
> - 클러스터가 아직 없을 때 kubectl이 내는 오류를 미리 봐 둡니다.
> - 자동 완성과 `k` 별칭으로 앞으로의 타이핑을 줄입니다.

## 두 도구의 역할

| 도구 | 하는 일 | 비유 |
|---|---|---|
| **kubectl** | 클러스터의 apiserver에 요청을 보낸다. 어떤 Kubernetes든(kind · EKS) 똑같이 쓴다 | 리모컨 |
| **kind** | 내 노트북의 Docker 위에 클러스터를 만들고 지운다 | TV를 설치 · 철거하는 기사 |

kind는 클러스터를 **만들 때와 지울 때만** 씁니다. 그 사이의 모든 일은 kubectl로 합니다. 5주차 EKS에서는 kind 자리에 Terraform이 들어가고, kubectl은 그대로입니다.

> **📖 용어 — 버전 차이 허용 범위 (version skew)**
>
> kubectl과 클러스터의 버전은 **앞뒤로 한 단계**(마이너 버전 ±1)까지 맞춰 쓰도록 되어 있습니다. 클러스터가 v1.37이면 kubectl은 v1.36 ~ v1.38. 오늘은 둘 다 v1.37이라 걱정할 일이 없지만, 회사에서 오래된 클러스터에 최신 kubectl을 쓰다 이상한 오류를 만나면 가장 먼저 의심할 곳입니다.

## 실습 6 · Docker 점검

> **🧪 실습: 실습 목표**
>
> kind가 쓸 Docker의 상태를 확인합니다. **Windows는 WSL Ubuntu 터미널, Mac은 터미널**에서 합니다(2주차 1일차와 같다).

### 단계 1 — Docker 엔진이 응답하는지

```bash
docker version --format '클라이언트 {{.Client.Version}} / 서버 {{.Server.Version}}'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 클라이언트 29.x.x / 서버 29.x.x
> ```
> 숫자는 달라도 됩니다. **서버** 쪽 숫자가 나오면 Docker 엔진이 켜져 있습니다.

> **🛠️ 막혔다면: Cannot connect to the Docker daemon**
>
> Docker Desktop이 꺼져 있습니다. 켜고 고래 아이콘이 멈출 때까지 기다립니다. Windows에서 켜져 있는데도 이 오류라면 Docker Desktop → Settings → Resources → **WSL integration**에서 Ubuntu가 켜져 있는지 확인합니다(2주차 1일차).

### 단계 2 — cgroup 버전과 메모리

```bash
docker info 2>/dev/null | grep -E 'Cgroup Version|CPUs|Total Memory'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
>  Cgroup Version: 2
>  CPUs: 8
>  Total Memory: 7.653GiB
> ```
> - **Cgroup Version: 2** — 꼭 2여야 합니다. Kubernetes v1.35부터 kubelet은 cgroup v1에서 기본으로 시작하지 않습니다(3교시 트렌드).
> - **Total Memory** — Docker가 쓸 수 있는 메모리입니다. **4GiB 이상**이면 오늘과 내일 실습에 충분합니다.

> **🛠️ 막혔다면: Total Memory가 4GiB보다 작다**
>
> - **Mac**: Docker Desktop → Settings → Resources → Memory를 늘리고 **Apply & restart**.
> - **Windows (WSL2)**: WSL이 쓰는 메모리 한도가 적용됩니다. Windows 사용자 폴더(`C:\Users\내이름`)의 `.wslconfig` 파일에 한도를 적습니다. **PowerShell**에서:
>     ```powershell
>     notepad "$env:USERPROFILE\.wslconfig"     # 없으면 새로 만들지 묻는다 → 예
>     ```
>     메모장에 다음을 적고 저장합니다.
>     ```text
>     [wsl2]
>     memory=6GB
>     ```
>     다시 **PowerShell**에서 WSL을 껐다 켭니다. 그다음 Docker Desktop을 다시 실행합니다.
>     ```powershell
>     wsl --shutdown
>     ```
> - PC 메모리가 8GB뿐이면 4GB 정도로 두고, 7교시 클러스터를 워커 1대로 줄여 만듭니다(강사 안내).

## 실습 7 · kubectl 설치

> **🧪 실습: 실습 목표**
>
> kubectl 최신 안정판을 받아, 체크섬을 확인하고 설치합니다.

### Linux · WSL2 Ubuntu (bash)

#### 단계 1 — 최신 안정판 번호 확인

```bash
curl -fsSL https://dl.k8s.io/release/stable.txt; echo
```

> **🟢 확인: 보이는 것**
>
> ```text
> v1.37.x
> ```
> `x`는 받는 날의 최신 패치 번호입니다. 아래 명령은 이 번호를 자동으로 씁니다.

#### 단계 2 — 내려받기

```bash
cd /tmp
KVER=$(curl -fsSL https://dl.k8s.io/release/stable.txt)
ARCH=$( [ "$(uname -m)" = aarch64 ] && echo arm64 || echo amd64 )
curl -fsSLO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"
curl -fsSLO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl.sha256"
```

- `ARCH` : 내 CPU가 Intel/AMD(`amd64`)인지 ARM(`arm64`)인지 고른다
- `.sha256` : 받은 파일이 깨지거나 바뀌지 않았는지 확인할 지문

#### 단계 3 — 지문 확인

```bash
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> kubectl: OK
> ```
> `FAILED`가 나오면 내려받다 깨진 것입니다. 단계 2부터 다시 합니다. 지문이 안 맞는 파일은 **절대 설치하지 않습니다** — 2주차에 이미지를 다이제스트로 확인한 것과 같은 이유입니다.

#### 단계 4 — 설치

```bash
sudo install -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl kubectl.sha256
```

- `install -m 0755` : 복사하면서 실행 권한까지 한 번에 준다

### Mac (터미널 · Homebrew)

```bash
brew install kubectl
```

> **🛠️ 막혔다면: Error: The `brew link` step did not complete successfully**
>
> Docker Desktop이 미리 깔아 둔 `kubectl`이 `/usr/local/bin`에 있어서입니다. Homebrew 쪽으로 덮어씁니다.
> ```bash
> brew link --overwrite kubectl
> ```

> [!TIP]
> **다른 설치 방법 — winget · 직접 다운로드**
>
> | 방법 | 어디서 | 명령 · 주소 |
> |---|---|---|
> | winget | Windows PowerShell | `winget install -e --id Kubernetes.kubectl` |
> | 직접 다운로드 | 브라우저 | [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/) |
>
> winget은 **Windows 쪽**에 설치하므로 PowerShell에서만 보입니다. 수업 명령은 WSL Ubuntu(bash)에서 치므로, Windows 사용자도 위의 **WSL 방법**으로 설치합니다. Docker Desktop도 Windows 쪽에 kubectl을 함께 깔지만, 버전이 늦을 수 있어 WSL 안에 따로 설치합니다. 전체 목록은 **부록 A · 도구 설치 가이드**.

### 단계 5 — 확인 (공통)

```bash
which kubectl
kubectl version --client
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> /usr/local/bin/kubectl
> Client Version: v1.37.x
> Kustomize Version: v5.x.x
> ```
> Mac(Apple Silicon)은 경로가 `/opt/homebrew/bin/kubectl`입니다. Kustomize는 kubectl에 함께 들어 있는 매니페스트 조립 도구입니다(4주차에 Helm과 비교).

### 단계 6 — 클러스터 없이 물어보기

`--client`를 빼고 실행해 봅니다. 아직 클러스터가 없습니다.

```bash
kubectl version
```

> **🟢 확인: 이 오류가 정상입니다**
>
> ```text
> Client Version: v1.37.x
> Kustomize Version: v5.x.x
> The connection to the server localhost:8080 was refused - did you specify the right host or port?
> ```
> kubectl은 **어느 클러스터에 말할지** `~/.kube/config` 파일에서 읽습니다. 파일이 없으니 기본값 `localhost:8080`에 말을 걸었다가 거절당했습니다. 이 메시지를 기억해 두세요. 회사에서 이 오류를 보면 "kubeconfig가 없거나, 엉뚱한 곳을 가리킨다"는 뜻입니다. 7교시에 kind가 이 파일을 만들어 줍니다.

## 실습 8 · kind 설치

### Linux · WSL2 Ubuntu (bash)

```bash
cd /tmp
ARCH=$( [ "$(uname -m)" = aarch64 ] && echo arm64 || echo amd64 )
curl -fsSLo kind "https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-${ARCH}"
sudo install -m 0755 kind /usr/local/bin/kind
rm kind
```

- `v0.33.0` : 2026년 8월 26일 나온 kind. 기본 Kubernetes가 v1.37.0이다

### Mac (터미널 · Homebrew)

```bash
brew install kind
```

> [!TIP]
> **다른 설치 방법 — winget · 직접 다운로드**
>
> | 방법 | 어디서 | 명령 · 주소 |
> |---|---|---|
> | winget | Windows PowerShell | `winget install -e --id Kubernetes.kind` |
> | 직접 다운로드 | 브라우저 | [github.com/kubernetes-sigs/kind/releases](https://github.com/kubernetes-sigs/kind/releases) |
>
> winget은 **Windows 쪽**에 설치하므로 PowerShell에서만 보입니다. 수업 명령은 WSL Ubuntu(bash)에서 치므로, Windows 사용자도 위의 **WSL 방법**으로 설치합니다. 전체 목록은 **부록 A · 도구 설치 가이드**.

### 확인 (공통)

```bash
kind version
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> kind v0.33.0 go1.x.x linux/amd64
> ```
> Mac은 `darwin/arm64`(Apple Silicon) 또는 `darwin/amd64`(Intel)입니다. Homebrew는 더 새 kind를 받았을 수 있습니다. 그래도 7교시 설정 파일이 노드 이미지를 v1.37.0으로 **고정**하므로 같은 클러스터가 만들어집니다.

> [!TIP]
> **한 번에 설치하기**
>
> 강의 저장소의 `labs/week3/day3/install-tools.sh`가 위 kubectl · kind 설치를 한 번에 합니다(Linux · WSL). 단계마다 무슨 일이 일어나는지 이해한 뒤에 쓰세요.

## 실습 9 · 자동 완성과 `k` 별칭

kubectl 명령은 깁니다. 현업에서는 거의 모두 자동 완성과 `k` 별칭을 씁니다.

### Linux · WSL2 (bash)

```bash
cat >> ~/.bashrc <<'EOF'
# kubectl
source <(kubectl completion bash)
alias k=kubectl
complete -o default -F __start_kubectl k
EOF
source ~/.bashrc
```

### Mac (zsh)

```bash
cat >> ~/.zshrc <<'EOF'
# kubectl
autoload -Uz compinit && compinit
source <(kubectl completion zsh)
alias k=kubectl
EOF
source ~/.zshrc
```

### 확인 (공통)

```bash
k version --client
```

이어서 `kubectl get no`까지 치고 **Tab** 키를 눌러 봅니다.

> **🟢 확인: 이렇게 되면 성공**
>
> `k version --client`가 `kubectl version --client`와 같은 결과를 냅니다. `kubectl get no` 뒤에서 **Tab**을 누르면 `nodes`로 채워집니다(클러스터가 없으면 일부 완성은 동작하지 않습니다 — 7교시에 다시 해 봅니다).

> [!TIP]
> **교재 표기**
>
> 교재는 처음 보는 사람도 알아보도록 계속 `kubectl`로 씁니다. 여러분은 `k`로 쳐도 됩니다.

> **🎓 학술 노트 — 공급망과 체크섬**
>
> 단계 3에서 확인한 지문(SHA-256 해시)은 "**내가 받은 파일 = 만든 사람이 올린 파일**"을 확인하는 가장 기본적인 방법입니다. 다만 지문 파일도 같은 서버에서 받으므로, 서버 자체가 뚫리면 둘 다 바뀔 수 있습니다. 그래서 Kubernetes 프로젝트는 릴리스 파일에 **서명**(Sigstore cosign)과 **SBOM**(부품 목록)도 함께 냅니다. 어제 6교시의 SLSA · 출처 증명(provenance)과 같은 흐름입니다. 참고: Kubernetes Docs, *Verify Signed Kubernetes Artifacts*.

> **📈 트렌드 2026 — 터미널 옆의 AI**
>
> kubectl 오류 메시지를 AI 도우미에게 붙여 넣어 설명을 듣는 일이 흔해졌고, 자연어로 "worker2에 뭐가 떠 있어?"라고 물으면 kubectl 명령을 만들어 실행하는 도구들도 나왔습니다. 편리하지만, 오늘 배운 구조를 모르면 AI가 만든 명령이 **무엇을 바꾸는지** 판단할 수 없습니다. 이 과정에서는 먼저 손으로 치고, 결과를 읽는 법을 익힙니다.

> **✅ 확인 문제**
>
> 1. kubectl과 kind 중, EKS를 쓸 때도 그대로 쓰는 도구는?
> 2. `docker info`에서 반드시 확인할 값 두 가지는?
> 3. `The connection to the server localhost:8080 was refused`는 무슨 뜻인가요?
> 4. 클러스터가 v1.37일 때 쓸 수 있는 kubectl 버전 범위는?
>
> <details><summary>정답</summary>
>
> 1. kubectl
> 2. `Cgroup Version: 2`, `Total Memory` (4GiB 이상 권장)
> 3. kubeconfig가 없거나 엉뚱한 곳을 가리켜, kubectl이 기본 주소 localhost:8080에 말했다가 거절당했다
> 4. v1.36 ~ v1.38 (마이너 버전 ±1)
>
> </details>

## 참고 문헌

- Kubernetes Docs. *Install and Set Up kubectl on Linux* · *on macOS*. kubernetes.io/docs/tasks/tools
- Kubernetes Docs. *Version Skew Policy* · *Verify Signed Kubernetes Artifacts*. kubernetes.io
- kind. *Quick Start — Installation*. kind.sigs.k8s.io/docs/user/quick-start
- kind Releases. *v0.33.0*. github.com/kubernetes-sigs/kind/releases

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [5교시 · 장단점과 선택지](lesson-05.md) | [⬆️ 3일차 목차](README.md) | [7교시 · 첫 클러스터 — 둘러보고, 지우고, 끄기](lesson-07.md) ➡️ |
