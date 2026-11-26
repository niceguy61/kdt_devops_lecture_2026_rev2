# 4주차 5일차 실습 파일 — Kubernetes 보안 (RBAC · ServiceAccount · Kyverno)

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `rbac/devmart-developer.yaml` · `rbac/oncall.yaml` | 2교시 | 사람의 권한 — 개발자 읽기 전용, 당직자 재시작 |
| `test/pod-reader.yaml` | 3교시 | API를 부르는 프로그램의 신원 체험 |
| `deploy/serviceaccounts.yaml` · `deploy/kustomization-patches.yaml` | 3교시 | 서비스마다 ServiceAccount (배포 저장소에 커밋) |
| `deploy/catalog-authz.yaml` · `deploy/catalog-l4.yaml` | 4교시 | 서비스 신원으로 허가 · Pod IP 우회로 막기 (배포 저장소에 커밋) |
| `kyverno/*.yaml` | 5교시 | Kyverno 설치 설정과 정책 셋 |
| `drills/break-w4.sh` · `who-refused.md` · `incident-report-w4.md` | 6교시 | 4주차 종합 장애 훈련 |
| `retro-week4.md` · `security-checklist.md` | 7교시 | 주간 회고 · 보안 점검표 |

```bash
mkdir -p ~/devops-lab/k8s/w4d5 && cp -r ~/course/labs/week4/day5/* ~/devops-lab/k8s/w4d5/
```
