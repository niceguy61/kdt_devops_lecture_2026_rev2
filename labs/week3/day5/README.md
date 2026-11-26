# 3주차 5일차 실습 파일

| 경로 | 쓰는 곳 | 내용 |
|---|---|---|
| `steps/catalog-v1.yaml` | 2교시 | ConfigMap · Secret으로 설정받는 catalog-api |
| `steps/catalog-v2.yaml` | 3교시 | + probe · preStop |
| `steps/oom.yaml` | 4교시 | 메모리 한도 초과 실험 |
| `devmart/` | 2 · 5교시 | DevMart MSA 전체 (`kubectl apply -k devmart/`) |
| `break.sh` · `fix.sh` | 6교시 | 장애 넣기 · 되돌리기 (짝끼리) |
| `incident-report-template.md` | 6교시 | 2일차와 같은 장애 보고서 양식 |
| `retro-week3.md` | 7교시 | 3주차 회고 |

```bash
mkdir -p ~/devops-lab/k8s/day5 && cp -r ~/course/labs/week3/day5/* ~/devops-lab/k8s/day5/
cd ~/devops-lab/k8s/day5
GH=$(gh api user --jq .login | tr 'A-Z' 'a-z')   SHA=sha-7f3c2e1    # 4일차 1교시와 같은 값
grep -rl YOUR_ID . | xargs sed -i "s/YOUR_ID/$GH/g; s/YOUR_SHA/$SHA/g"
```

Secret `devmart-db`는 파일로 두지 않습니다. 2교시에 `kubectl create secret`으로 만듭니다.
