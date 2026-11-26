#!/usr/bin/env bash
# 2교시 · EKS 위의 DevMart를 처음부터 — 어제 한 일을 한 번에 (시간을 잰다)
set -euo pipefail
START=$(date +%s)
t() { echo "[$(( ($(date +%s)-START)/60 ))분 $(( ($(date +%s)-START)%60 ))초] $*"; }
GH=$(gh api user -q .login)

t "1. 클러스터 (Terraform)"
cd ~/devmart-infra/terraform/eks
terraform apply -auto-approve -input=false >/tmp/up-tf.log
aws eks update-kubeconfig --name devmart --region ap-northeast-2 --alias eks-devmart >/dev/null
kubectl config use-context eks-devmart >/dev/null

t "2. 플랫폼 (StorageClass · LBC · Envoy Gateway · Argo CD)"
~/devops-lab/aws/w5d4/platform/install.sh >/tmp/up-platform.log

t "3. Secret과 Application"
kubectl get secret devmart-db -n devmart >/dev/null 2>&1 || \
  kubectl create secret generic devmart-db -n devmart --from-literal=DB_PASSWORD="$(openssl rand -hex 12)"
sed "s/YOUR_ID/$GH/" ~/devops-lab/aws/w5d4/argocd/devmart-eks-app.yaml | kubectl apply -f -

t "4. 손님이 들어올 수 있을 때까지"
NLB=""
until [ -n "$NLB" ]; do NLB=$(kubectl get gateway devmart -n devmart -o jsonpath='{.status.addresses[0].value}' 2>/dev/null); sleep 5; done
until [ "$(curl -s -o /dev/null -w '%{http_code}' -m 3 "http://$NLB/api/products")" = "200" ]; do sleep 10; done
t "완료 — http://$NLB/"
