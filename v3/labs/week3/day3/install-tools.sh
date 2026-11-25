#!/usr/bin/env bash
# 클러스터 둘러보기 — 상태를 바꾸지 않는 명령만 모았습니다.
set -u
CTX=${1:-kind-devmart}
run() { echo; echo "\$ $*"; "$@"; }

run kubectl config current-context
run kubectl --context "$CTX" cluster-info
run kubectl --context "$CTX" get nodes -o wide
run kubectl --context "$CTX" get namespaces
run kubectl --context "$CTX" get pods -n kube-system -o wide
run docker ps --filter "label=io.x-k8s.kind.cluster=devmart" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
run docker exec devmart-control-plane ls /etc/kubernetes/manifests
