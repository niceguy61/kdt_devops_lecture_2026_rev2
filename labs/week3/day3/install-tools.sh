#!/usr/bin/env bash
# kubectl(최신 안정판)과 kind v0.33.0을 /usr/local/bin에 설치합니다. Linux · WSL2 Ubuntu용.
# Mac은 이 스크립트 대신: brew install kubectl kind
set -euo pipefail

KIND_VERSION=v0.33.0

case "$(uname -m)" in
  x86_64)  ARCH=amd64 ;;
  aarch64) ARCH=arm64 ;;
  *) echo "지원하지 않는 CPU: $(uname -m)"; exit 1 ;;
esac

tmp=$(mktemp -d)
cd "$tmp"

echo "== kubectl =="
KVER=$(curl -fsSL https://dl.k8s.io/release/stable.txt)
curl -fsSLO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl"
curl -fsSLO "https://dl.k8s.io/release/${KVER}/bin/linux/${ARCH}/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -m 0755 kubectl /usr/local/bin/kubectl

echo "== kind =="
curl -fsSLo kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-${ARCH}"
sudo install -m 0755 kind /usr/local/bin/kind

cd - >/dev/null
rm -rf "$tmp"

kubectl version --client
kind version
