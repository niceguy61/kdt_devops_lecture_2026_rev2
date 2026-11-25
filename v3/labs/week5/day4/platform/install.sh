#!/usr/bin/env bash
# 4 · 5교시 · EKS 위의 '플랫폼' — 4주차에 손으로 했던 것을 순서대로
set -euo pipefail
cd "$(dirname "$0")"
CLUSTER=${CLUSTER:-devmart}
REGION=${REGION:-ap-northeast-2}
VPC_ID=$(aws eks describe-cluster --name "$CLUSTER" --region "$REGION" --query cluster.resourcesVpcConfig.vpcId --output text)

echo "== 1. 기본 StorageClass gp3"
kubectl apply -f storageclass-gp3.yaml
kubectl annotate storageclass gp2 storageclass.kubernetes.io/is-default-class=false --overwrite 2>/dev/null || true

echo "== 2. AWS Load Balancer Controller"
helm repo add eks https://aws.github.io/eks-charts >/dev/null 2>&1 || true
helm repo update eks >/dev/null
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system \
  --set clusterName="$CLUSTER" --set region="$REGION" --set vpcId="$VPC_ID" \
  --set serviceAccount.create=true --set serviceAccount.name=aws-load-balancer-controller \
  --wait

echo "== 3. Envoy Gateway (4주차 1일차와 같은 차트 · 버전)"
helm upgrade --install eg oci://docker.io/envoyproxy/gateway-helm --version v1.10.0 \
  -n envoy-gateway-system --create-namespace -f envoy-gateway-values.yaml --wait
kubectl apply -f gatewayclass.yaml
kubectl create namespace devmart --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f envoyproxy-eks.yaml -f gateway.yaml

echo "== 4. Argo CD (4주차 3일차와 같은 values)"
helm repo add argo https://argoproj.github.io/argo-helm >/dev/null 2>&1 || true
helm repo update argo >/dev/null
helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace \
  ${ARGOCD_CHART_VERSION:+--version "$ARGOCD_CHART_VERSION"} -f argocd-values.yaml --wait

echo "== 완료 — 다음: Secret devmart-db, Application"
