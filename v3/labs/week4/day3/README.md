# 4주차 3일차 실습 파일 — GitOps (Argo CD)

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `deploy/kustomization.yaml` | 2교시 | 배포 저장소 `devmart-deploy`의 `devmart/kustomization.yaml` — 라우트 · 대시보드 · 규칙까지, 이미지 태그는 `images:`로 |
| `argocd/argocd-values.yaml` | 3교시 | Argo CD 설치 설정 |
| `argocd/devmart-app.yaml` | 4교시 | 첫 Application (손으로 Sync) |
| `argocd/devmart-app-auto.yaml` | 6교시 | 자동 동기화 · selfHeal · prune |
| `workflows/devmart-ci.yml` | 7교시 | CI 마지막에 '배포 저장소에 새 태그 적기' job을 더한 워크플로 |

```bash
mkdir -p ~/devops-lab/k8s/w4d3 && cp -r ~/course/labs/week4/day3/* ~/devops-lab/k8s/w4d3/
```

저장소가 둘이 됩니다.

| 저장소 | 담는 것 | 바꾸는 사람 |
|---|---|---|
| `devops-lab` (코드 저장소, 3주차부터) | `devmart-msa/` 소스 · Dockerfile, `.github/workflows/` | 개발자 (PR) |
| `devmart-deploy` (배포 저장소, 오늘 새로) | `devmart/` 매니페스트 묶음 | CI 봇(이미지 태그) · 운영자(설정) |

Secret(`devmart-db`, `grafana-admin`)은 어느 저장소에도 넣지 않습니다.
