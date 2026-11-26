[🏠 과정 목차](../README.md)

📕 PDF: [보기](../downloads/pdf/appendix-install.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/appendix-install.pdf)

# 부록 A · 도구 설치 가이드

5주 동안 설치하는 모든 도구를 한곳에 모았습니다. 수업 중에는 각 교시의 설치 실습을 따라가면 되고, 이 부록은 **다른 방법이 필요할 때**(회사 PC라 스크립트가 막혔다, Mac인데 brew를 안 쓴다, Windows에서 PowerShell로만 쓰고 싶다)와 **새 노트북을 한 번에 준비할 때** 씁니다.

> [!IMPORTANT]
> **세 가지 원칙**
>
> 1. **명령은 bash 하나로.** Windows는 WSL2의 Ubuntu 터미널에서, Mac은 터미널 앱에서 **같은 명령**을 칩니다. PowerShell은 WSL · VS Code · Docker Desktop처럼 **Windows 쪽에 까는 앱**에만 씁니다.
> 2. **CLI 도구는 명령을 치는 곳에 깝니다.** Windows 사용자는 kubectl · helm · aws · terraform을 **WSL Ubuntu 안에** 설치합니다. winget으로 깐 도구는 Windows 쪽에 깔려 **PowerShell에서만** 보이고, WSL bash에서는 보이지 않습니다.
> 3. **받은 파일은 확인하고 실행합니다.** 체크섬(`sha256sum --check`)을 맞춰 보고, 설치 스크립트는 받아서 읽은 뒤 실행합니다(`curl … | bash`로 바로 실행하지 않기).

## 어느 창에 칠까 — PowerShell과 bash 구분

| 창 | 여는 법 | 프롬프트 모양 | 이 책의 코드 블록 표시 |
|---|---|---|---|
| **Windows PowerShell** | 시작 버튼 오른쪽 클릭 → **터미널** (관리자가 필요하면 **터미널(관리자)**) | `PS C:\Users\me>` | `PowerShell · Windows` |
| **WSL Ubuntu (bash)** | 시작 메뉴 → **Ubuntu 24.04 LTS**, 또는 터미널 탭의 ∨ → Ubuntu | `me@PC:~$` | `bash · WSL Ubuntu · macOS` |
| **macOS 터미널 (zsh)** | `Command` + `Space` → "터미널" | `me@MacBook ~ %` | `bash · WSL Ubuntu · macOS` |

> [!TIP]
> **Mac의 zsh에서도 bash 블록이 그대로 됩니다**
>
> macOS의 기본 셸은 zsh지만 이 과정의 명령(`export`, `$(…)`, `&&`, `|`, heredoc)은 zsh에서도 똑같이 동작합니다. 다른 점이 있는 곳은 본문에 따로 적었습니다.

> [!WARNING]
> **섞어 치면 생기는 일**
>
> - PowerShell에 `export A=1` → `export : 'export' 용어가 … 인식되지 않습니다`. PowerShell은 `$env:A = "1"`로 씁니다.
> - PowerShell의 `curl`은 진짜 curl이 아닌 경우가 있습니다(`Invoke-WebRequest` 별칭). PowerShell에서 curl을 쓰려면 `curl.exe`라고 적습니다.
> - WSL에서 `winget …` → `command not found`. winget은 Windows 프로그램입니다.
> - **프롬프트가 `PS`로 시작하면 PowerShell, `$`로 끝나면 bash** — 치기 전에 한 번 봅니다.

## 한눈에 보기

| 도구 | 처음 쓰는 때 | WSL Ubuntu (bash) | macOS (Homebrew) | Windows PowerShell (winget) |
|---|---|---|---|---|
| WSL2 + Ubuntu | 2주차 1일차 | — | — | `wsl --install -d Ubuntu-24.04` |
| 기본 도구 (curl · unzip · jq) | 2주차 1일차 | `apt` | `brew install jq` | (WSL에서) |
| VS Code | 2주차 1일차 | (Windows에 설치) | `brew install --cask visual-studio-code` | `Microsoft.VisualStudioCode` |
| Git | 2주차 1일차 | `apt` | `brew install git` | (WSL에서) · `Git.Git` |
| GitHub CLI `gh` | 2주차 1일차 | `apt` | `brew install gh` | (WSL에서) · `GitHub.cli` |
| Docker Desktop | 2주차 1일차 | (Windows에 설치) | `brew install --cask docker-desktop` | `Docker.DockerDesktop` |
| kubectl | 3주차 3일차 | 바이너리 + 체크섬 | `brew install kubectl` | (WSL에서) · `Kubernetes.kubectl` |
| kind | 3주차 3일차 | 바이너리 | `brew install kind` | (WSL에서) · `Kubernetes.kind` |
| Helm | 4주차 1일차 | 공식 스크립트 | `brew install helm` | (WSL에서) · `Helm.Helm` |
| Argo CD CLI | 4주차 3일차 | 바이너리 | `brew install argocd` | (WSL에서) · `argoproj.argocd` |
| istioctl | 4주차 4일차 | 공식 스크립트 | `brew install istioctl` | (WSL에서) · winget 없음¹ |
| AWS CLI v2 | 5주차 1일차 | 공식 zip | `brew install awscli` | (WSL에서) · `Amazon.AWSCLI` |
| Terraform | 5주차 3일차 | HashiCorp apt 저장소 | `brew install hashicorp/tap/terraform` | (WSL에서) · `Hashicorp.Terraform` |

**(WSL에서)** = Windows 사용자도 수업에서는 WSL Ubuntu 쪽 방법으로 설치한다는 뜻입니다. 그 옆의 winget ID는 PowerShell에서 따로 쓰고 싶을 때만 씁니다.
¹ winget의 `Istio.Istio`는 오래된 1.17에서 멈춰 있습니다. 직접 다운로드를 씁니다.

winget ID는 이렇게 씁니다(`-e`는 ID가 정확히 같은 것만).

```powershell
winget install -e --id Microsoft.VisualStudioCode
winget search kubectl          # ID를 모를 때 찾기
winget upgrade --all           # 깔린 것 모두 업데이트
```

## 1. 작업대 — WSL2 · 기본 도구 · VS Code

### WSL2 + Ubuntu (Windows만)

**Windows · PowerShell (관리자)**

```powershell
wsl --install -d Ubuntu-24.04
# 재시작 후
wsl -l -v                      # VERSION 열이 2인지 확인
```

- `wsl --install`이 "이미 설치됨"이라며 WSL 2가 아니라면: `wsl --update` → `wsl --set-default-version 2`
- winget으로 WSL 본체만 먼저 받을 수도 있습니다: `winget install -e --id Microsoft.WSL`
- 직접 다운로드: Microsoft Store의 **Ubuntu 24.04 LTS**, 또는 [learn.microsoft.com/windows/wsl/install](https://learn.microsoft.com/windows/wsl/install)

### 기본 도구

**WSL Ubuntu · bash**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget unzip jq ca-certificates gnupg lsb-release
python3 --version              # Ubuntu 24.04에는 python3가 이미 있다
```

**macOS · 터미널** — Homebrew가 없으면 [brew.sh](https://brew.sh)의 한 줄 설치 명령을 먼저 실행합니다.

```bash
brew install jq
xcode-select -p || xcode-select --install   # git · python3 · make가 들어 있는 명령줄 도구
```

### VS Code

**Windows · PowerShell** — WSL 안이 아니라 **Windows에** 설치합니다.

```powershell
winget install -e --id Microsoft.VisualStudioCode
```

**macOS · 터미널**

```bash
brew install --cask visual-studio-code
```

직접 다운로드: [code.visualstudio.com/download](https://code.visualstudio.com/download). Windows 설치 중 **PATH에 추가**를 켜 두어야 WSL에서 `code .`가 됩니다.

## 2. Git · GitHub CLI

**WSL Ubuntu · bash**

```bash
sudo apt install -y git gh
git --version && gh --version
```

Ubuntu 저장소의 `gh`는 조금 오래됐습니다(2.45). 최신이 필요하면 GitHub 공식 apt 저장소를 씁니다.

```bash
sudo mkdir -p -m 755 /etc/apt/keyrings
wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh
```

**macOS · 터미널**

```bash
brew install git gh
```

**Windows · PowerShell** (WSL 밖에서도 Git이 필요할 때만)

```powershell
winget install -e --id Git.Git
winget install -e --id GitHub.cli
```

직접 다운로드: [git-scm.com/downloads](https://git-scm.com/downloads) · [cli.github.com](https://cli.github.com)

## 3. Docker Desktop

**Windows · PowerShell**

```powershell
winget install -e --id Docker.DockerDesktop
```

설치 후 Docker Desktop → Settings → **Resources → WSL integration**에서 Ubuntu-24.04를 켭니다(2주차 1일차 6교시). WSL 안에 `apt install docker.io`로 엔진을 **또** 깔지 않습니다.

**macOS · 터미널**

```bash
brew install --cask docker-desktop
```

직접 다운로드: [docs.docker.com/desktop](https://docs.docker.com/desktop/) — Mac은 칩(`uname -m`이 `arm64`면 Apple silicon)에 맞는 파일을 받습니다. Linux 노트북은 Docker Engine을 씁니다(2주차 1일차 6교시 참고 상자).

## 4. Kubernetes 도구 — kubectl · kind · Helm

**WSL Ubuntu · bash**

```bash
cd /tmp
ARCH=$( [ "$(uname -m)" = aarch64 ] && echo arm64 || echo amd64 )

# kubectl — 최신 안정판 + 체크섬
KVER=$(curl -fsSL https://dl.k8s.io/release/stable.txt)
curl -fsSLO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"
curl -fsSLO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check && sudo install -m 0755 kubectl /usr/local/bin/kubectl
rm -f kubectl kubectl.sha256

# kind
curl -fsSLo kind "https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-${ARCH}"
sudo install -m 0755 kind /usr/local/bin/kind && rm kind

# Helm 4 — 스크립트를 받아 읽고 실행
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
less get_helm.sh && bash get_helm.sh && rm get_helm.sh
```

**macOS · 터미널**

```bash
brew install kubectl kind helm
```

**Windows · PowerShell** (수업에서는 쓰지 않음)

```powershell
winget install -e --id Kubernetes.kubectl
winget install -e --id Kubernetes.kind
winget install -e --id Helm.Helm
```

직접 다운로드: [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/) · [kind 릴리스](https://github.com/kubernetes-sigs/kind/releases) · [helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/)

## 5. Argo CD CLI · istioctl

**WSL Ubuntu · bash**

```bash
cd /tmp
# Argo CD CLI — 클러스터의 서버 버전과 맞춘다 (4주차 3일차)
ARGO_VER=v3.6.2               # 또는 kubectl로 서버 이미지 태그를 읽는다
curl -fsSLo argocd "https://github.com/argoproj/argo-cd/releases/download/${ARGO_VER}/argocd-linux-amd64"
sudo install -m 555 argocd /usr/local/bin/argocd && rm argocd

# istioctl — 4주차 4일차와 같은 버전
ISTIO=1.31.0
curl -sL https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIO TARGET_ARCH=x86_64 sh -
sudo install -m 555 istio-$ISTIO/bin/istioctl /usr/local/bin/istioctl
```

**macOS · 터미널**

```bash
brew install argocd istioctl
```

**Windows · PowerShell** (수업에서는 쓰지 않음)

```powershell
winget install -e --id argoproj.argocd
# istioctl은 winget이 오래됨 → github.com/istio/istio/releases 에서 istioctl-…-win.zip
```

직접 다운로드: [argo-cd 릴리스](https://github.com/argoproj/argo-cd/releases) · [istio 릴리스](https://github.com/istio/istio/releases)

## 6. AWS CLI v2 · Terraform

**WSL Ubuntu · bash**

```bash
# AWS CLI v2 (x86_64 — ARM이면 awscli-exe-linux-aarch64.zip)
cd /tmp
curl -sSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip -q -o awscliv2.zip && sudo ./aws/install --update && rm -rf aws awscliv2.zip

# Terraform — HashiCorp apt 저장소
wget -qO- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install -y terraform
```

**macOS · 터미널**

```bash
brew install awscli
brew tap hashicorp/tap && brew install hashicorp/tap/terraform
```

Terraform은 라이선스 변경(BUSL) 뒤 Homebrew 기본 저장소에서 빠졌습니다. `brew install terraform`이 오래된 버전을 깔거나 실패하면 위처럼 **hashicorp/tap**을 씁니다.

**Windows · PowerShell** (수업에서는 쓰지 않음)

```powershell
winget install -e --id Amazon.AWSCLI
winget install -e --id Hashicorp.Terraform
```

직접 다운로드: AWS CLI는 Windows `AWSCLIV2.msi` · macOS `AWSCLIV2.pkg`([설치 안내](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)), Terraform은 [developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)

## 설치 점검 — 한 번에 확인

**WSL Ubuntu · macOS · bash**

```bash
for c in git gh docker kubectl kind helm argocd istioctl aws terraform jq; do
  if command -v $c >/dev/null; then printf '%-10s ✓ %s\n' $c "$(command -v $c)"; else printf '%-10s ✗ 없음\n' $c; fi
done
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> git        ✓ /usr/bin/git
> gh         ✓ /usr/bin/gh
> docker     ✓ /usr/bin/docker
> kubectl    ✓ /usr/local/bin/kubectl
> …
> ```
> 그 주에 아직 배우지 않은 도구는 `✗`여도 괜찮습니다. Windows에서 `docker`가 `✗`이면 Docker Desktop의 WSL integration을 확인합니다.

> **🛠️ 막혔다면: winget으로 깔았는데 WSL에서 `command not found`**
>
> 정상입니다. winget은 Windows 쪽에 설치합니다. WSL Ubuntu 안에 위의 **bash 방법**으로 한 번 더 설치합니다. (Windows의 `.exe`를 WSL에서 `kubectl.exe`처럼 부를 수는 있지만, 설정 파일 위치 `~/.kube`가 달라 수업 흐름과 어긋납니다.)

## 업데이트와 삭제

| | WSL Ubuntu (bash) | macOS (bash/zsh) | Windows (PowerShell) |
|---|---|---|---|
| 전부 업데이트 | `sudo apt update && sudo apt upgrade -y` | `brew update && brew upgrade` | `winget upgrade --all` |
| 하나 지우기 | `sudo apt remove 이름` · `/usr/local/bin`의 파일은 `sudo rm` | `brew uninstall 이름` | `winget uninstall -e --id ID` |

`/usr/local/bin`에 직접 넣은 바이너리(kubectl · kind · argocd · istioctl)는 apt가 모릅니다. 새 버전은 같은 설치 명령을 다시 실행하면 덮어씁니다.

## 참고 문헌

- Microsoft (2026). *Install WSL*; *Use WinGet to install and manage applications*. learn.microsoft.com
- Homebrew (2026). *Homebrew Documentation* · `docker-desktop` · `visual-studio-code` 캐스크. docs.brew.sh
- Kubernetes (2026). *Install Tools*. kubernetes.io/docs/tasks/tools
- Helm (2026). *Installing Helm*. helm.sh/docs/intro/install
- Amazon Web Services (2026). *Installing or updating to the latest version of the AWS CLI*. docs.aws.amazon.com
- HashiCorp (2026). *Install Terraform*. developer.hashicorp.com/terraform/install
- GitHub (2026). *Installing gh on Linux and BSD*. github.com/cli/cli
