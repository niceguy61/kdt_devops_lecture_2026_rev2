#!/usr/bin/env bash
# 7교시 · EKS 지우기 — Kubernetes가 만든 AWS 자원(NLB · EBS)을 먼저, 그다음 terraform destroy
set -uo pipefail
echo "== 1. 앱을 지운다 — PVC가 지워지면 EBS 볼륨도 지워진다 (reclaimPolicy: Delete)"
kubectl -n argocd delete application devmart --wait=true 2>/dev/null
kubectl delete namespace devmart --wait=true --timeout=5m

echo "== 2. Envoy Gateway를 지운다 — LoadBalancer Service가 사라지면 NLB도 지워진다"
helm uninstall eg -n envoy-gateway-system 2>/dev/null
kubectl delete namespace envoy-gateway-system --wait=true --timeout=5m 2>/dev/null

echo "== 3. NLB가 정말 사라졌나 (빈 줄이 나올 때까지 기다린다)"
for i in $(seq 30); do
  LB=$(aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(LoadBalancerName,'devmart') || contains(LoadBalancerName,'k8s')].LoadBalancerName" --output text)
  [ -z "$LB" ] && echo "없음" && break
  echo "남음: $LB"; sleep 10
done

echo "== 4. 남은 EBS 볼륨 (kubernetes.io 태그)"
aws ec2 describe-volumes --filters Name=tag-key,Values=kubernetes.io/created-for/pvc/name \
  --query 'Volumes[].[VolumeId,State,Size]' --output text

echo "== 이제: cd terraform/eks && terraform destroy"
