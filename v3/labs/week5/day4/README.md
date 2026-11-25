# 5주차 4일차 실습 파일 — Terraform으로 EKS

| 폴더 · 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `terraform/eks/` | 2 · 3교시 | VPC(NAT 하나) + EKS(1.36, 노드 t3.medium × 2) + 애드온 + Pod Identity — `devmart-infra/terraform/eks/`로 복사 |
| `platform/` | 4교시 | gp3 StorageClass · AWS Load Balancer Controller · Envoy Gateway(NLB) · Argo CD — `install.sh` |
| `deploy/` | 5교시 | 배포 저장소의 `eks/` 폴더 — 4주차 `devmart/`를 쓰고 Istio · 모니터링 리소스만 뺀다 |
| `argocd/devmart-eks-app.yaml` | 5교시 | EKS의 Argo CD가 볼 Application (path: eks) |
| `cleanup.sh` | 7교시 | 지우는 순서 — 앱(EBS) → 입구(NLB) → terraform destroy |

```bash
mkdir -p ~/devops-lab/aws/w5d4 && cp -r ~/course/labs/week5/day4/* ~/devops-lab/aws/w5d4/
```

!!! warn "오늘은 시간당 약 $0.3"
    EKS($0.10) + NAT($0.059) + 노드 2대($0.104) + NLB · 공인 IP. **7교시에 반드시 `cleanup.sh` → `terraform destroy`.**
