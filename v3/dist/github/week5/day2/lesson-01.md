# 1교시 · 1일차 요약 + 컴퓨트 고르기

> [!NOTE]
> **이번 시간에 할 일**
>
> - 어제 만든 계정 · VPC가 그대로인지 CLI로 확인합니다.
> - AWS에서 코드를 돌리는 **네 가지 방법**을 비교합니다.
> - 오늘 만들 구조를 그림으로 보고, 3 · 4주차 Kubernetes와 **짝지어** 둡니다.

## 1일차 요약 — 손으로 다시 확인

```bash
aws sts get-caller-identity --query Arn --output text
VPC=$(aws ec2 describe-vpcs --filters Name=tag:Name,Values=devmart-vpc --query 'Vpcs[0].VpcId' --output text); echo $VPC
aws ec2 describe-security-groups --filters Name=vpc-id,Values=$VPC --query 'SecurityGroups[].GroupName' --output text
~/devops-lab/aws/w5d1/check-account.sh | tail -4
```

> **🟢 확인: 이렇게 나오면 준비 완료**
>
> ```text
> arn:aws:iam::123456789012:user/devops-admin
> vpc-0f1e2d3c4b5a69788
> default  devmart-web-sg  devmart-app-sg
> == 돈이 나가는 것 (NAT · EIP · LB)
> (빈 줄)
> ```
> `aws login`이 만료되었다면 `ExpiredToken` 오류가 납니다 — `aws login`을 다시 합니다.

| 1일차 | 오늘 이어지는 곳 |
|---|---|
| IAM 역할 — 키 없는 신원 | EC2에 역할을 붙여 S3를 읽는다 (3교시) |
| public · private 서브넷 | 오늘은 서버를 public에 둔다 — 이유는 2교시 |
| web-sg · app-sg | ALB에는 web-sg, 서버에는 app-sg (5교시) |
| 정책 JSON의 Deny | 서버에서 S3 삭제를 시도해 막히는 것을 본다 (3교시) |

## 코드를 돌리는 네 가지 방법

| | EC2 | ECS (+ Fargate) | Lambda | EKS |
|---|---|---|---|---|
| 내가 관리하는 것 | **가상 서버 전체** — OS · 패치 · Docker | 컨테이너 정의 (Fargate면 서버 없음) | **함수 코드만** | Kubernetes 매니페스트 + (노드) |
| 단위 | 서버 | 작업(task) | 요청 하나 | Pod |
| 요금 | 켜 둔 시간 | 켜 둔 시간 (vCPU · 메모리) | **호출 수 × 실행 시간** | 클러스터 $0.10/h + 노드 |
| 잘 맞는 것 | 무엇이든, 옛 앱, 특수 소프트웨어 | AWS 안에서 단순한 컨테이너 서비스 | 짧은 이벤트 처리, 트래픽이 들쑥날쑥 | **여러 서비스 · 여러 팀 · 이식성** |
| 이번 과정 | **오늘** | (소개만) | (소개만) | 4 · 5일차 |

오늘 EC2를 직접 다루는 이유는, **EKS의 노드도 결국 EC2**이고, ALB · Auto Scaling · 역할이 EKS 아래에서 그대로 쓰이기 때문입니다. 바닥을 먼저 손으로 만져 봅니다.

## 오늘의 그림

![손님 → ALB(web-sg) → 대상 그룹 → Auto Scaling 그룹의 EC2 두 대(AZ 둘, app-sg) → 역할로 S3 읽기](../../assets/week5/day2/w5d2-arch.png)

![Pod 템플릿은 시작 템플릿, Deployment는 Auto Scaling 그룹, probe는 상태 검사, Service · Gateway는 ALB, ServiceAccount는 IAM 역할, kubectl exec는 Session Manager](../../assets/week5/day2/w5d2-k8s-map.png)

> [!IMPORTANT]
> **같은 생각, 다른 크기**
>
> 3주차 4일차에 Deployment의 `replicas: 2`는 "Pod가 둘이 되게 **계속 맞춰라**"였습니다. 오늘의 Auto Scaling 그룹은 "서버가 둘이 되게 계속 맞춰라"입니다. 원하는 상태를 적어 두면 무언가가 실제를 맞추는 **reconcile**이 이번에는 **가상 서버** 단위로 일어납니다. 다만 서버 하나가 뜨는 데는 Pod보다 훨씬 오래 걸립니다 — 6교시에 직접 잽니다.

> **❓ 오해 — 컨테이너 시대에 EC2는 몰라도 된다**
>
> EKS 노드, ECS의 EC2 모드, ALB의 대상, 쿠버네티스가 만드는 로드 밸런서 — 모두 EC2 · VPC의 규칙(보안 그룹 · 서브넷 · 역할) 위에서 움직입니다. 4일차에 EKS가 "노드가 클러스터에 안 붙는다"고 할 때, 원인은 대개 오늘 배우는 **서브넷 라우팅 · 보안 그룹 · 역할** 중 하나입니다.

> **🎓 학술 노트 — 탄력성의 정의**
>
> Herbst 외의 *Elasticity in Cloud Computing: What It Is, and What It Is Not*(ICAC 2013)는 **탄력성**(elasticity)을 "부하 변화에 맞춰 자원을 **자동으로** 늘리고 줄여, 어느 시점에서든 공급이 수요에 **가깝게** 맞는 정도"로 정의하고, 단순한 확장성(scalability)과 구별했습니다. 늘릴 수 있다(확장성)와 **자동으로, 빨리, 정확히** 늘고 준다(탄력성)는 다르다는 것입니다. Auto Scaling 그룹은 그 탄력성의 가장 기본적인 구현이고, 6교시에 그 '빠르기'를 잽니다.

> **📈 트렌드 2026 — 서버리스와 쿠버네티스의 수렴**
>
> Fargate · Lambda처럼 서버를 감추는 방식과 Kubernetes가 서로 다가가고 있습니다. EKS **Auto Mode**(2024~)는 노드 관리를 AWS에 맡기고, Karpenter는 Pod가 필요한 만큼만 EC2를 사서 붙였다 뗍니다. 반대로 Lambda는 컨테이너 이미지를 받고 실행 시간이 길어졌습니다. "**서버를 의식하는 정도**"를 고르는 문제가 되어 가고 있습니다 — 4일차에 EKS의 노드 선택지로 다시 봅니다.

> **✅ 확인 문제**
>
> 1. EC2 · Lambda · EKS의 요금 방식 차이는?
> 2. Auto Scaling 그룹은 Kubernetes의 무엇과 같은 일을 하나요?
> 3. EKS를 쓰는데도 EC2 · VPC를 알아야 하는 이유는?
>
> <details><summary>정답</summary>
>
> 1. EC2는 켜 둔 시간, Lambda는 호출 수 × 실행 시간, EKS는 클러스터 시간당 + 노드(EC2) 시간
> 2. Deployment · ReplicaSet — 원하는 수를 계속 맞춘다
> 3. EKS 노드가 EC2이고, 노드 · 로드 밸런서가 서브넷 · 보안 그룹 · 역할 위에서 움직이기 때문
>
> </details>

## 참고 문헌

- AWS. *Choosing an AWS compute service* (decision guide). docs.aws.amazon.com/decision-guides
- Herbst, N. R., Kounev, S. & Reussner, R. (2013). *Elasticity in Cloud Computing: What It Is, and What It Is Not*. ICAC '13.
- AWS Docs. *Amazon EKS Auto Mode*. docs.aws.amazon.com/eks
