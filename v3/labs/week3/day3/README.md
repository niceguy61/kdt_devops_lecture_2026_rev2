# 3주차 3일차 실습 파일

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `kind-devmart.yaml` | 7교시 실습 | 컨트롤 플레인 1대 + 워커 2대, 30080 포트 통로 |
| `install-tools.sh` | 6교시 실습 (선택) | Linux · WSL2에서 kubectl과 kind를 한 번에 설치 |
| `cluster-tour.sh` | 7교시 복습 | 클러스터 둘러보기 명령 모음 (읽기만 하는 명령) |

```bash
mkdir -p ~/devops-lab/k8s && cp ~/course/labs/week3/day3/* ~/devops-lab/k8s/
cd ~/devops-lab/k8s
kind create cluster --config kind-devmart.yaml
```

만든 클러스터는 **지우지 않고** 3주차 4~5일차에 계속 씁니다. 다 쓰면 `kind delete cluster --name devmart`.
