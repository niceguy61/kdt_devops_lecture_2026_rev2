# 2교시 · 코드 읽기와 apply

!!! goal "이번 시간에 할 일"
    - `devmart-infra`에 EKS 코드를 넣고, 파일마다 무엇을 만드는지 읽습니다.
    - 3일차 VPC와 **달라진 세 줄**을 찾습니다.
    - plan에서 **무엇을 봐야 하는지** 정하고, apply를 시작합니다(15~20분).

## 실습 1 · 코드 넣기

```bash
mkdir -p ~/devops-lab/aws/w5d4 && cp -r ~/course/labs/week5/day4/* ~/devops-lab/aws/w5d4/
cd ~/devmart-infra && git switch main && git pull
cp -r ~/devops-lab/aws/w5d4/terraform/eks terraform/
cd terraform/eks
ID=$(gh api user -q .login | tr 'A-Z' 'a-z')
sed -i "s/YOUR_ID/$ID/" versions.tf
cp terraform.tfvars.example terraform.tfvars && sed -i "s/your-github-id/$ID/" terraform.tfvars
ls
```

!!! check "확인"
    ```text
    eks.tf  outputs.tf  pod-identity.tf  terraform.tfvars  terraform.tfvars.example  variables.tf  versions.tf  vpc.tf
    ```

| 파일 | 만드는 것 |
|---|---|
| `versions.tf` | 프로바이더 · backend (`w5d4/eks/`) · 기본 태그 |
| `variables.tf` | 클러스터 이름 · 버전 1.36 · 노드 유형 · 수 |
| `vpc.tf` | VPC + 서브넷 4 + **NAT 하나** |
| `eks.tf` | EKS 클러스터 + 애드온 + 관리형 노드 그룹 |
| `pod-identity.tf` | Pod가 맡을 IAM 역할 둘 (EBS CSI · Load Balancer Controller) |
| `outputs.tf` | kubeconfig 명령 등 |

## vpc.tf — 3일차와 달라진 세 곳

```bash
diff ~/devops-lab/aws/w5d3/terraform/04-vpc/main.tf vpc.tf | grep '^[<>]' | head -20
```

```hcl
  enable_nat_gateway   = true # 노드(private)가 이미지를 받으려면 밖으로 나가야 한다
  single_nat_gateway   = true # 실습: 하나만 (운영: AZ마다 하나)

  public_subnet_tags  = { "kubernetes.io/role/elb" = 1 }
  private_subnet_tags = { "kubernetes.io/role/internal-elb" = 1 }
```

| 바뀐 곳 | 왜 |
|---|---|
| **NAT 켜기** | 노드가 private 서브넷에 있다(1일차 5교시). GHCR · Docker Hub에서 이미지를 받으려면 밖으로 나가야 한다 |
| **NAT 하나만** | AZ마다 두면 한 AZ가 죽어도 안전하지만 두 배 비용. 실습은 하나 |
| **서브넷 태그** | 4교시의 Load Balancer Controller가 "인터넷용 로드 밸런서는 어느 서브넷에?"를 이 태그로 찾는다 |

## eks.tf — 클러스터

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = var.cluster_name        # devmart
  kubernetes_version = var.kubernetes_version  # 1.36

  endpoint_public_access                   = true   # 실습: 내 노트북에서 kubectl
  enable_cluster_creator_admin_permissions = true   # apply한 사람 = 클러스터 관리자 (3교시)

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets           # 노드는 private에

  addons = {
    vpc-cni                = { before_compute = true }
    eks-pod-identity-agent = { before_compute = true }
    kube-proxy             = {}
    coredns                = {}
    metrics-server         = {}
    aws-ebs-csi-driver     = { pod_identity_association = [{ role_arn = …, service_account = "ebs-csi-controller-sa" }] }
  }

  eks_managed_node_groups = {
    default = {
      ami_type       = "AL2023_x86_64_STANDARD"
      instance_types = ["t3.medium"]
      min_size = 1, max_size = 3, desired_size = 2
    }
  }
}
```

| 애드온 | 하는 일 | kind에서는 |
|---|---|---|
| `vpc-cni` | Pod에 **VPC IP**를 준다 — 노드보다 먼저(`before_compute`) | kindnet |
| `eks-pod-identity-agent` | Pod가 IAM 역할을 맡게 (3교시) | — |
| `kube-proxy` · `coredns` | Service 규칙 · 클러스터 DNS (3주차 4일차) | 같은 것 |
| `metrics-server` | `kubectl top` (6교시) | — |
| `aws-ebs-csi-driver` | PVC → **EBS 볼륨** (4 · 6교시) | local-path |

!!! tip "v21의 이름들"
    EKS 모듈 v21(2025)은 입력 이름을 정리했습니다 — `cluster_name` → `name`, `cluster_version` → `kubernetes_version`, `cluster_addons` → `addons`. 인터넷의 v20 예제를 쓸 때 가장 많이 걸리는 곳입니다(3일차 6교시의 "모듈 기본값 · 이름을 읽는다").

## 실습 2 · init · plan

```bash
terraform init
terraform plan -out=eks.tfplan | tail -3
terraform show -json eks.tfplan | python3 -c "
import sys,json,collections
p=json.load(sys.stdin); c=collections.Counter()
for r in p['resource_changes']:
    if 'create' in r['change']['actions']: c[r['type']]+=1
for k,v in c.most_common(12): print(f'{v:3} {k}')
print('합계', sum(c.values()))"
```

!!! check "확인"
    ```text
    Plan: 5○ to add, 0 to change, 0 to destroy.
     ○ aws_iam_role_policy_attachment
     ○ aws_route_table_association
     ○ aws_security_group_rule
     ○ aws_subnet
     ○ aws_eks_addon
     2 aws_iam_role …
     1 aws_eks_cluster
     1 aws_eks_node_group
     1 aws_nat_gateway
     …
    합계 5○
    ```
    어제 질문의 답 — **50~60개**(모듈 버전마다 조금 다르다). `-out`으로 저장한 plan은 apply할 때 **그대로** 쓰입니다 — 리뷰한 것과 실행되는 것이 같다는 보장입니다.

!!! key "50개 plan에서 무엇을 보나"
    전부 읽을 수는 없습니다. 3일차 2교시의 원칙대로 ① `destroy`와 `-/+`가 **0인지**, ② **돈이 나가는 것**(`aws_eks_cluster` · `aws_nat_gateway` · `aws_eks_node_group` · `aws_eip`)의 개수와 설정(인스턴스 유형 · 수), ③ **권한**(`aws_iam_*` — 어떤 정책이 붙나), ④ **공개**(`endpoint_public_access`, `0.0.0.0/0`)를 봅니다. 돈 · 권한 · 공개 · 삭제 — 이 넷이 사람이 보는 곳입니다.

## 실습 3 · apply 시작

```bash
date +%T; time terraform apply eks.tfplan
```

apply가 도는 동안 3교시로 넘어갑니다. 진행이 이렇게 보입니다.

```text
module.vpc.aws_vpc.this[0]: Creating...
module.vpc.aws_eip.nat[0]: Creating...
…
module.eks.aws_eks_cluster.this[0]: Creating...
module.eks.aws_eks_cluster.this[0]: Still creating... [1m0s elapsed]
…
module.eks.aws_eks_cluster.this[0]: Creation complete after 9m12s
module.eks.aws_eks_addon.before_compute["vpc-cni"]: Creating...
module.eks.module.eks_managed_node_group["default"].aws_eks_node_group.this[0]: Creating...
…
Apply complete! Resources: 5○ added, 0 changed, 0 destroyed.
real    16m○s
```

컨트롤 플레인 **약 10분** + 노드 그룹 **약 3분** + 애드온. 3주차 kind의 1분과 비교됩니다 — 실제 데이터센터의 서버와 네트워크를 고르고 잇는 시간입니다.

!!! trouble "apply가 실패하면"
    | 오류 | 원인 | 해결 |
    |---|---|---|
    | `UnsupportedAvailabilityZoneException` | 그 AZ에 EKS 용량이 없다 | `vpc.tf`의 AZ를 `a`, `b`로 바꿔 다시 |
    | `ExpiredToken` | 16분 사이 `aws login` 만료 | `aws login` 후 `terraform apply` 다시 (이미 만든 것은 건너뛴다) |
    | `InvalidParameterException … version` | 1.36을 아직 고를 수 없다 | `aws eks describe-cluster-versions --query 'clusterVersions[].clusterVersion'`로 최신을 보고 `variables.tf` 수정 |
    | 잠금 오류 | 다른 터미널의 plan | 3일차 5교시 |

    Terraform은 **멱등**이라, 중간에 실패해도 다시 apply하면 만든 것은 두고 남은 것만 합니다.

!!! academic "학술 노트 — 변경 집합의 리뷰"
    큰 변경을 리뷰할 때 사람이 놓치는 것은 '양'보다 '**어느 줄이 위험한가**'입니다. Bacchelli와 Bird의 *Expectations, Outcomes, and Challenges of Modern Code Review*(ICSE 2013)는 마이크로소프트의 코드 리뷰를 분석해, 리뷰어가 실제로 찾는 결함보다 **이해**에 더 많은 시간을 쓴다는 것을 보였습니다. IaC 리뷰에서 plan 요약(자원 종류별 개수, 돈 · 권한 · 공개 · 삭제 체크)을 자동으로 만드는 이유가 그 이해 비용을 줄이려는 것입니다.

!!! trend "트렌드 2026 — EKS를 만드는 여러 길"
    `eksctl`(명령 한 줄), 콘솔의 '빠른 구성'(Auto Mode), CloudFormation · CDK, Terraform 모듈, 그리고 **EKS Blueprints**(애드온까지 묶은 참조 구성)가 공존합니다. 조직은 대개 오늘처럼 Terraform 모듈로 클러스터를 만들고, 그 위의 플랫폼(입구 · Argo CD …)은 **GitOps**로 올리는 두 층 구조를 택합니다 — 4교시의 `install.sh`를 내일 Argo CD Application으로 바꾸는 것이 다음 걸음입니다.

!!! quiz "확인 문제"
    1. 3일차 VPC와 달라진 세 곳과 각각의 이유는?
    2. `before_compute = true`인 애드온 둘과 이유는?
    3. 50개 plan에서 사람이 꼭 보는 넷은?
    4. apply가 중간에 실패하면 어떻게 하나요?

    ??? answer "정답"
        1. NAT 켜기(private 노드가 이미지를 받으려고), NAT 하나(비용), 서브넷 태그(LBC가 로드 밸런서 서브넷을 찾으려고)
        2. vpc-cni(노드가 뜨자마자 Pod 네트워크가 필요), eks-pod-identity-agent(Pod가 역할을 맡게) — 노드보다 먼저
        3. 삭제 · 교체(-/+)가 0인지, 돈이 나가는 자원, 권한(IAM), 공개(public endpoint · 0.0.0.0/0)
        4. 원인을 고치고 다시 apply — 멱등이라 남은 것만 만든다

## 참고 문헌

- terraform-aws-modules. *eks — AWS EKS Terraform module (v21)*, *UPGRADE-21.0*. registry.terraform.io/modules/terraform-aws-modules/eks/aws
- AWS Docs. *Amazon EKS add-ons*, *Managed node groups*. docs.aws.amazon.com/eks
- Bacchelli, A. & Bird, C. (2013). *Expectations, Outcomes, and Challenges of Modern Code Review*. ICSE 2013.
