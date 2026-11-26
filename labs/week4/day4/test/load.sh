#!/usr/bin/env bash
# 메시 안(devmart의 client Pod)에서 catalog-api를 N번 불러 버전별로 센다
N=${1:-50}
kubectl exec -n devmart client -- sh -c "
for i in \$(seq $N); do curl -s -m 3 catalog-api:8000/api/info | grep -o '\"version\":\"[^\"]*\"' || echo FAIL; done" | sort | uniq -c
