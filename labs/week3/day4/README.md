# 3주차 4일차 실습 파일

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `pod.yaml` | 2교시 | catalog-api Pod 하나 |
| `broken-image.yaml` · `worker-crash.yaml` · `too-big.yaml` | 3교시 | 일부러 망가뜨린 Pod 세 개 |
| `deployment.yaml` | 4~7교시 | catalog-api Deployment (3개) |
| `service.yaml` · `service-nodeport.yaml` | 6교시 | 클러스터 안 이름 · 브라우저용 30080 |

```bash
mkdir -p ~/devops-lab/k8s/day4 && cp ~/course/labs/week3/day4/*.yaml ~/devops-lab/k8s/day4/
cd ~/devops-lab/k8s/day4
GH=내GitHub아이디   SHA=sha-7f3c2e1   # 1교시 단계 2에서 확인한 값
sed -i "s/YOUR_ID/$GH/g; s/YOUR_SHA/$SHA/g" *.yaml     # Mac: sed -i '' "…" *.yaml
```

오늘 만든 Deployment · Service는 내일 아침에 지우고 DevMart 전체로 다시 올립니다.
