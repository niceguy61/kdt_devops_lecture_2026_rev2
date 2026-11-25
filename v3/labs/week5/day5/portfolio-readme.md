# DevMart — 클라우드 네이티브 DevOps 실습 포트폴리오

> 5주 과정에서 만든 것을 한 장으로. 각 저장소의 README 맨 위에 이 표를 둔다.

| 저장소 | 담은 것 | 보여 주는 능력 |
|---|---|---|
| `devops-lab` | DevMart MSA 소스 · Dockerfile · CI (GitHub Actions) | 컨테이너화 · 테스트 자동화 · 이미지 빌드 |
| `devmart-deploy` | Kubernetes 매니페스트 (kustomize: devmart/ · eks/) | GitOps (Argo CD) · 환경별 오버레이 |
| `devmart-infra` | Terraform — VPC · EKS · Pod Identity, PR plan (OIDC) | IaC · 원격 state · 키 없는 CI |

## 구조
(아키텍처 그림 — 손님 → NLB → Envoy Gateway → 서비스 → db, Argo CD ← Git, CI → GHCR)

## 재현
```bash
./up.sh      # 약 30분 — Terraform → 플랫폼 → 앱
./down.sh    # 앱 → 입구 → 클러스터 → 남은 것 확인
```

## 운영에서 다룬 것
- 관찰: Prometheus · Grafana · 알림 · 런북 · SLO
- 서비스 메시: Istio ambient — mTLS · 트래픽 나누기 · 장애 주입 · 호출 허가
- 보안: RBAC · ServiceAccount · Kyverno · IAM 역할 · OIDC
- 장애 훈련: 장애 보고서 두 장 (3 · 4주차)

## 비용
이 구성을 하루 6시간 띄우면 약 $2 (서울 리전, 2026년 12월).
