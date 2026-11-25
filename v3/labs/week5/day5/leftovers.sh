#!/usr/bin/env bash
# 5교시 · 남은 것 찾기 — Project=devmart 태그가 붙은 것과, 태그 없이 돈이 나가는 것 (모든 리전)
set -uo pipefail
echo "== 태그 Project=devmart 가 붙은 자원 (모든 리전)"
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  aws resourcegroupstaggingapi get-resources --region "$r" --tag-filters Key=Project,Values=devmart \
    --query 'ResourceTagMappingList[].ResourceARN' --output text 2>/dev/null | tr '\t' '\n' | sed "s/^/[$r] /" | grep -v '^\[.*\] $'
done
echo "== 서울 리전 — 시간당 요금이 나가는 것"
R=ap-northeast-2
echo "EKS:  $(aws eks list-clusters --region $R --query clusters --output text)"
echo "EC2:  $(aws ec2 describe-instances --region $R --filters Name=instance-state-name,Values=pending,running,stopping,stopped --query 'Reservations[].Instances[].InstanceId' --output text)"
echo "NAT:  $(aws ec2 describe-nat-gateways --region $R --filter Name=state,Values=available,pending --query 'NatGateways[].NatGatewayId' --output text)"
echo "EIP:  $(aws ec2 describe-addresses --region $R --query 'Addresses[].PublicIp' --output text)"
echo "LB:   $(aws elbv2 describe-load-balancers --region $R --query 'LoadBalancers[].LoadBalancerName' --output text)"
echo "EBS:  $(aws ec2 describe-volumes --region $R --query 'Volumes[].VolumeId' --output text)"
echo "(EKS · EC2 · NAT · EIP · LB · EBS 가 모두 비어 있으면 끝)"
