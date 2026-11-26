# 4주차 4일차 실습 파일 — 서비스 메시 (Istio ambient)

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `istio/*-values.yaml` | 2교시 | istiod · istio-cni · ztunnel 설치 설정 (ambient) |
| `monitoring/istio-monitors.yaml` | 3교시 | istiod · ztunnel · waypoint 지표 수집 |
| `kiali/kiali-values.yaml` | 3교시 | 메시 지도 Kiali |
| `deploy/namespace.yaml` | 2 · 4교시 | 배포 저장소 `devmart/namespace.yaml`을 이것으로 — 메시 등록 라벨 |
| `deploy/waypoint.yaml` | 4교시 | devmart의 L7 프록시 |
| `deploy/catalog-api-canary.yaml` · `catalog-split.yaml` | 4교시 | 카나리와 90/10 나누기 |
| `deploy/catalog-fault.yaml` · `catalog-timeout.yaml` | 5교시 | 장애 주입 · 타임아웃 · 재시도 |
| `deploy/peer-auth.yaml` · `catalog-authz.yaml` | 6교시 | mTLS STRICT · 호출 허가 |
| `test/outsider.yaml` · `test/load.sh` | 4 · 6교시 | 시험용 손님 |

`deploy/`의 파일은 **배포 저장소(`devmart-deploy/devmart/`)에 복사하고 커밋**합니다 — 3일차부터 DevMart는 Git으로만 바꿉니다.

```bash
mkdir -p ~/devops-lab/k8s/w4d4 && cp -r ~/course/labs/week4/day4/* ~/devops-lab/k8s/w4d4/
```
