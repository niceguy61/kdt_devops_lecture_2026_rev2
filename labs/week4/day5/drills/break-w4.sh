#!/usr/bin/env bash
# 4주차 종합 훈련 — 짝이 몰래 장애를 넣는다.  사용: ./break-w4.sh [1-5|random]
# 1~3, 5는 배포 저장소(~/devmart-deploy)에 '평범해 보이는' 커밋을 올린다. 4는 플랫폼(RBAC)을 바꾼다.
set -euo pipefail
N=${1:-random}
[[ "$N" == random ]] && N=$(( RANDOM % 5 + 1 ))
REPO=~/devmart-deploy/devmart
DIR=$(cd "$(dirname "$0")/.." && pwd)
commit() { cd ~/devmart-deploy && git add -A && git commit -qm "$1" && git push -q; }
cd ~/devmart-deploy && git pull -q
case $N in
  1) sed -i '/devmart-catalog-api/{n;s/newTag: .*/newTag: latest/;}' $REPO/kustomization.yaml
     commit "catalog-api 최신 이미지로" ;;
  2) sed -i 's#sa/order-api#sa/order-worker#' $REPO/catalog-authz.yaml
     commit "정책 정리" ;;
  3) sed -i 's/timeout: 1s/timeout: 10ms/' $REPO/catalog-timeout.yaml
     commit "응답 시간 목표 조정" ;;
  4) sed 's#"pods/log", ##' "$DIR/rbac/devmart-developer.yaml" | kubectl apply -f - >/dev/null ;;
  5) sed -i 's/^          port: 80$/          port: 8080/' $REPO/devmart-routes.yaml
     commit "web 포트 정리" ;;
  *) echo "1~5 또는 random"; exit 1 ;;
esac
echo "$N" > /tmp/.w4-break    # 정답 확인용 — 짝에게 보여 주지 않는다
echo "장애를 넣었습니다. 짝에게 '무언가 이상하다'고만 알려 주세요."
