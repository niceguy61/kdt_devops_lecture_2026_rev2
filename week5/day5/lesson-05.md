[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [5일차](README.md)

# 5교시 · 전부 지우기 · 남은 것 찾기 · 비용 보고

> [!NOTE]
> **이번 시간에 할 일**
>
> - EKS를 포함해 이번 과정에서 만든 **AWS 자원을 모두** 지웁니다.
> - **모든 리전**에서 남은 것을 찾습니다.
> - 일부러 남겨 둔 state 버킷 · OIDC 역할까지 정리합니다.
> - 이번 주 비용을 **서비스별**로 보고합니다.

## 실습 4 · EKS 지우기

```bash
cat ~/devops-lab/aws/w5d5/down.sh
time ~/devops-lab/aws/w5d5/down.sh
```

> **🟢 확인: 확인**
>
> ```text
> == 1. 앱을 지운다 — …
> == 2. Envoy Gateway를 지운다 — …
> == 3. NLB가 정말 사라졌나 …
> 없음
> == 4. 남은 EBS 볼륨 (kubernetes.io 태그)
> == 이제: cd terraform/eks && terraform destroy
> Destroy complete! Resources: 5○ destroyed.
> == 태그 Project=devmart 가 붙은 자원 (모든 리전)
> [ap-northeast-2] arn:aws:s3:::devmart-tfstate-niceguy61
> [ap-northeast-2] arn:aws:iam::…:role/devmart-tf-plan
> …
> == 서울 리전 — 시간당 요금이 나가는 것
> EKS:
> EC2:
> NAT:
> EIP:
> LB:
> EBS:
> (EKS · EC2 · NAT · EIP · LB · EBS 가 모두 비어 있으면 끝)
> ```

## 실습 5 · 남겨 둔 것까지

과정이 끝났으니 state 버킷과 OIDC 역할도 지웁니다. **순서**가 있습니다 — 장부(state)를 쓰는 프로젝트를 먼저 지우고, 장부를 담은 버킷을 마지막에.

```bash
ID=$(gh api user -q .login | tr 'A-Z' 'a-z'); GH=$(gh api user -q .login)
# 1. OIDC 역할 (장부는 state 버킷에 있다)
cd ~/devops-lab/aws/w5d3/terraform/05-github-oidc
terraform destroy -auto-approve -var github_owner=$GH -var state_bucket=devmart-tfstate-$ID | tail -1
# 2. state 버킷 — prevent_destroy를 풀고
cd ../03-backend
sed -i 's/prevent_destroy = true/prevent_destroy = false/' main.tf
aws s3api list-object-versions --bucket devmart-tfstate-$ID --query 'length(Versions)'
```

버킷에 **버전이 켜져 있어** 지운 장부의 옛 버전들이 남아 있습니다. 버킷을 지우려면 모든 버전을 지워야 합니다.

```bash
python3 - <<PY
import boto3
b = boto3.resource("s3").Bucket("devmart-tfstate-$ID")
b.object_versions.delete()
print("모든 버전 삭제")
PY
terraform destroy -auto-approve -var owner=$ID | tail -1
```

> [!TIP]
> **boto3가 없다면**
>
> `pip install --user boto3`, 또는 콘솔 → S3 → 버킷 → **비우기**(모든 버전까지 지운다) → 그다음 `terraform destroy`.

```bash
~/devops-lab/aws/w5d5/leftovers.sh
aws iam list-users --query 'Users[].UserName' --output text
aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text) --query 'Budgets[].BudgetName' --output text
```

> **🟢 확인: 확인**
>
> ```text
> == 태그 Project=devmart 가 붙은 자원 (모든 리전)
> (빈 줄)
> == 서울 리전 — 시간당 요금이 나가는 것
> EKS:  EC2:  NAT:  EIP:  LB:  EBS:   (모두 빈 줄)
> devops-admin
> zero-spend  monthly-20
> ```
> 남은 것은 **사람**(devops-admin)과 **알림**(예산 둘) — 둘 다 무료이고, 계정을 계속 쓸 거라면 남겨 둡니다.

> [!WARNING]
> **태그가 없는 것은 이 스크립트에 안 잡힌다**
>
> `leftovers.sh`의 첫 부분은 `Project=devmart` **태그**로 찾습니다. 1 · 2일차에 콘솔로 만들며 태그를 빠뜨린 것은 안 보입니다. 그래서 둘째 부분이 서울 리전의 **돈이 나가는 종류**를 태그 없이 훑습니다. 혹시 다른 리전에서 실습한 적이 있다면 콘솔 위 검색창의 **Resource Explorer**(모든 리전 검색)로 한 번 더 봅니다.

## 실습 6 · 비용 보고

**결제 및 비용 관리 → Cost Explorer**

1. 날짜: 이번 주 월요일 ~ 오늘, 세분화 **일별**
2. 그룹화 기준: **서비스**
3. (크레딧이 비용을 덮어 0으로 보이면) 필터 → **요금 유형**에서 `Credit`을 **제외**

> **🟢 확인: 확인 (예)**
>
> | 서비스 | 금액 | 언제 |
> |---|---|---|
> | Amazon Elastic Kubernetes Service | $0.70 | 목 · 금 |
> | Amazon Elastic Compute Cloud — Compute | $0.85 | 화 · 목 · 금 |
> | EC2 — Other (NAT · EBS · 공인 IP) | $0.80 | 화 · 목 · 금 |
> | Elastic Load Balancing | $0.30 | 화 · 목 · 금 |
> | Amazon S3 · 그 밖 | $0.01 | |
> | **합계 (크레딧 차감 전)** | **약 $2.7** | 청구액 $0 |
>
> 1일차 1교시 계산표의 "$5 안팎"과 비교해 봅니다. **가장 큰 줄**은 무엇이었나요? 대개 EC2 — Other(NAT 게이트웨이)가 생각보다 큽니다.

> [!IMPORTANT]
> **비용을 보는 습관**
>
> 오늘 본 표가 FinOps(1일차 1교시)의 첫 단계 — **보이게 하기** — 입니다. 회사에서는 이것을 팀 · 서비스별로(태그를 **비용 할당 태그**로 켜서) 매주 보고, 2단계(최적화: 스팟 · Graviton · NAT 줄이기 · 끄기)와 3단계(운영: 예산 · 이상 탐지 · PR 비용 예측)로 갑니다.

## 계정을 어떻게 할까

| 선택 | 할 일 |
|---|---|
| 계속 공부에 쓴다 (권장) | 예산 알림 그대로. Free 플랜이면 6개월 · 크레딧 소진 뒤 **멈춘다**는 것만 기억 |
| 당분간 안 쓴다 | 그대로 두어도 무료 자원뿐 — 단 루트 · devops-admin 비밀번호 · MFA는 잘 보관 |
| 닫는다 | 루트로 로그인 → 계정 → **계정 해지**. 90일 뒤 완전히 삭제 (그 사이 되살릴 수 있다) |

> **❓ 오해 — 계정을 닫으면 모든 과금이 바로 끝난다**
>
> 해지 전에 돌던 자원의 그 달 사용량은 청구되고, 해지 후 90일 안에는 되살릴 수 있어 일부 자원이 남아 있습니다. 그래서 순서는 언제나 **자원을 지운다 → 확인한다 → (필요하면) 계정을 닫는다**입니다.

> **🎓 학술 노트 — 클라우드 비용의 행동경제학**
>
> 클라우드 비용이 새는 데에는 기술보다 **행동**의 몫이 큽니다. '나중에 지우자'(현재 편향), '혹시 필요할지도'(손실 회피)가 자원을 남깁니다. FinOps Foundation의 *State of FinOps* 연례 조사는 해마다 '낭비 줄이기'와 '쓰지 않는 자원 정리'를 최우선 과제로 꼽습니다. 이번 주의 장치들 — 매일 같은 시각에 지우기, 스크립트로 확인하기, 예산 알림 — 은 의지가 아니라 **습관과 기본값**으로 이 편향을 이기는 방법입니다.

> **📈 트렌드 2026 — AI 워크로드와 비용**
>
> GPU 인스턴스는 EKS 노드 하나의 수십 배 단가라, 2026년 FinOps의 중심 주제는 **AI 학습 · 추론 비용**입니다. 그러나 원칙은 오늘과 같습니다 — 태그로 주인을 적고, 쓰지 않으면 끄고(0으로 줄이는 Karpenter · KEDA), 매일 보고, PR 단계에서 예측합니다.

> **✅ 확인 문제**
>
> 1. state 버킷을 가장 마지막에 지운 이유는?
> 2. 버전 관리가 켜진 버킷을 지우기 전에 해야 할 일은?
> 3. leftovers.sh가 두 방식(태그 · 종류)으로 찾는 이유는?
> 4. 이번 주 가장 큰 비용 줄과, 그것을 줄이는 방법 하나는?
>
> <details><summary>정답</summary>
>
> 1. 다른 프로젝트(OIDC 역할 등)의 장부가 그 버킷에 있어, 먼저 지우면 그 프로젝트를 destroy할 수 없기 때문
> 2. 모든 객체의 모든 버전을 지운다 (콘솔의 비우기, 또는 object_versions.delete)
> 3. 태그를 빠뜨린 자원(콘솔로 만든 것)도 찾기 위해 — 돈이 나가는 종류는 태그 없이 훑는다
> 4. (대개) EC2 — Other(NAT · EBS · 공인 IP) 또는 노드 — NAT를 끄거나 하나로, 쓰지 않으면 지운다, 스팟 · Graviton
>
> </details>

## 참고 문헌

- AWS Docs. *Analyzing your costs with AWS Cost Explorer*, *Activating user-defined cost allocation tags*. docs.aws.amazon.com/cost-management
- AWS Docs. *Deleting a bucket with versioning enabled*, *Close your AWS account*. docs.aws.amazon.com
- FinOps Foundation. *State of FinOps 2026*. data.finops.org

---

⬅️ 이전: [4교시 · 클라우드 장애 훈련 — 노드와 AZ](lesson-04.md) &nbsp;|&nbsp; [⬆️ 5일차 목차](README.md) &nbsp;|&nbsp; 다음: [6교시 · 5주 회고 + 포트폴리오](lesson-06.md) ➡️
