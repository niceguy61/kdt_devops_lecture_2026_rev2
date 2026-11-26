#!/usr/bin/env bash
# 5교시 · 전부 지운다 — 앱 → 입구 → 클러스터 → 확인 (4일차 7교시를 한 번에)
set -uo pipefail
kubectl config use-context eks-devmart >/dev/null 2>&1 || true
~/devops-lab/aws/w5d4/cleanup.sh
cd ~/devmart-infra/terraform/eks && terraform destroy -auto-approve -input=false | tail -1
"$(dirname "$0")/leftovers.sh"
