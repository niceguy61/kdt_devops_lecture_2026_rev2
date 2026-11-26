# 4주차 2일차 실습 파일 — Observability

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `monitoring/kps-values.yaml` | 2교시 | kube-prometheus-stack 설정 (kind용) |
| `monitoring/envoy-podmonitor.yaml` | 3교시 | Envoy 프록시 지표 수집 |
| `monitoring/devmart-dashboard.yaml` | 4교시 | DevMart 대시보드 (ConfigMap) |
| `k6/load.js` | 5교시 | 부하 테스트 |
| `monitoring/devmart-rules.yaml` | 6교시 | 알림 규칙 |
| `runbook-template.md` | 7교시 | 런북 양식 |

```bash
mkdir -p ~/devops-lab/k8s/w4d2 && cp -r ~/course/labs/week4/day2/* ~/devops-lab/k8s/w4d2/
```
