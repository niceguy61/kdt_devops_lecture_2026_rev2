# 4주차 1일차 실습 파일 — Helm + Gateway API

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `helm/podinfo-values.yaml` | 2교시 | 연습용 앱 podinfo의 내 설정 |
| `helm/podinfo-canary-values.yaml` | 6교시 | 가중치 실습용 두 번째 릴리스 |
| `gateway/envoy-gateway-values.yaml` | 5교시 | Envoy Gateway 컨트롤러 설정 |
| `gateway/gatewayclass.yaml` · `envoyproxy.yaml` · `gateway.yaml` | 5교시 | 문 만들기 (NodePort 30080) |
| `gateway/devmart-routes.yaml` | 6교시 | DevMart 경로 셋 |
| `gateway/podinfo-route.yaml` · `podinfo-split.yaml` | 6교시 | Host로 나누기 · 가중치로 나누기 |
| `drills/cross-ns-route.yaml` · `referencegrant.yaml` | 7교시 | 다른 네임스페이스로 보내기와 허락 |

```bash
mkdir -p ~/devops-lab/k8s/w4d1 && cp -r ~/course/labs/week4/day1/* ~/devops-lab/k8s/w4d1/
```
