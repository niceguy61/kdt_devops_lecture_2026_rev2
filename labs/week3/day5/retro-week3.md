# 3주차 회고 (KPT)

## 이번 주에 만든 것
- [ ] DevMart MSA — Compose로 여섯 서비스 실행 (1일차)
- [ ] GitHub Actions CI — PR마다 테스트, main이면 GHCR push (2일차)
- [ ] kind 클러스터 devmart — 노드 3대 (3일차)
- [ ] catalog-api Deployment · Service · 롤링 업데이트 (4일차)
- [ ] DevMart 전체를 Kubernetes에 — localhost:30080 (5일차)

## Compose → Kubernetes 한 줄씩
| Compose | Kubernetes | 내 말로 차이 |
|---|---|---|
| `services:` 하나 | Deployment + Service | |
| `environment:` | ConfigMap · Secret | |
| `.env` | Secret (Git 밖) | |
| `healthcheck:` | readiness · liveness probe | |
| `restart: unless-stopped` | kubelet 재시작 + ReplicaSet | |
| `volumes:` (named) | PersistentVolumeClaim | |
| `ports: "8080:80"` | NodePort · (4주차) Gateway | |
| `--scale` | `replicas:` | |

## Keep
-

## Problem
-

## Try (4주차에)
-

## 장애 연습에서 내가 맡은 장애와 걸린 시간
| 장애 번호 | 첫 증상 | 원인을 찾은 명령 | 걸린 시간 |
|---|---|---|---|
| | | | |
