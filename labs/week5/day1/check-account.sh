#!/usr/bin/env bash
# 5주차 1일차 · 내 계정 상태 한눈에 (읽기만 한다)
set -uo pipefail
echo "== 나는 누구인가";       aws sts get-caller-identity --output table
echo "== 기본 리전";           aws configure get region
echo "== 루트 MFA (1이면 켜짐)"; aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled'
echo "== IAM 사용자";          aws iam list-users --query 'Users[].UserName' --output text
echo "== 예산";                aws budgets describe-budgets --account-id "$(aws sts get-caller-identity --query Account --output text)" \
                                 --query 'Budgets[].[BudgetName,BudgetLimit.Amount]' --output text 2>/dev/null || echo "(없음)"
echo "== VPC";                 aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,CidrBlock,Tags[?Key==`Name`]|[0].Value,IsDefault]' --output table
echo "== 돈이 나가는 것 (NAT · EIP · LB)"
aws ec2 describe-nat-gateways --filter Name=state,Values=available --query 'NatGateways[].NatGatewayId' --output text
aws ec2 describe-addresses --query 'Addresses[].PublicIp' --output text
aws elbv2 describe-load-balancers --query 'LoadBalancers[].LoadBalancerName' --output text 2>/dev/null
