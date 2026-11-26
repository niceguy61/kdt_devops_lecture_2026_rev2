[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [3일차](README.md)

# 6교시 · 모듈로 VPC

> [!NOTE]
> **이번 시간에 할 일**
>
> - **모듈**이 무엇이고, 공개 레지스트리의 모듈을 어떻게 고르는지 압니다.
> - `terraform-aws-modules/vpc`로 1일차 VPC를 **코드 몇십 줄**로 다시 만듭니다.
> - 콘솔 VPC와 코드 VPC를 CLI로 나란히 비교합니다.
> - 콘솔 VPC는 **지우고**, 이제부터 VPC는 코드로만 만듭니다.

## 모듈 = 인프라의 함수 · 차트

| | 4주차 1일차 Helm 차트 | Terraform 모듈 |
|---|---|---|
| 정체 | 템플릿 묶음 | `.tf` 묶음 (폴더 하나) |
| 입력 | values | variables |
| 출력 | (NOTES) | outputs |
| 저장소 | Artifact Hub · OCI | **Terraform Registry** · Git |
| 버전 고정 | `--version 6.14.0` | `version = "~> 6.0"` |

`terraform-aws-modules`는 커뮤니티가 관리하는 AWS 모듈 모음으로, VPC · EKS 모듈은 내려받기 수가 각각 수억 회입니다. 모듈을 고를 때는 ① 관리자와 최근 커밋, ② 내려받기 수, ③ **필요한 프로바이더 버전**, ④ 예제와 입력 문서를 봅니다 — 1일차의 Helm 차트를 고를 때와 같습니다.

## 실습 10 · 코드 읽기

```bash
cd ~/devops-lab/aws/w5d3/terraform/04-vpc
sed -i "s/YOUR_ID/$(gh api user -q .login | tr 'A-Z' 'a-z')/" versions.tf
cat main.tf | head -18
```

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = "devmart-tf"
  cidr = "10.0.0.0/16"

  azs             = ["ap-northeast-2a", "ap-northeast-2c"]
  public_subnets  = ["10.0.0.0/20", "10.0.16.0/20"]
  private_subnets = ["10.0.128.0/20", "10.0.144.0/20"]

  enable_nat_gateway   = false # 오늘은 없음 (4일차에 true)
  enable_dns_hostnames = true
  enable_dns_support   = true
}
```

1일차 5교시의 **설계표가 그대로 코드**가 되었습니다. 그 아래에는 S3 게이트웨이 엔드포인트와 보안 그룹 둘(web · app)이 직접 쓴 자원으로 있습니다. app-sg의 규칙을 봅니다.

```hcl
resource "aws_vpc_security_group_ingress_rule" "app_from_web" {
  security_group_id            = aws_security_group.app.id
  ip_protocol                  = "tcp"
  from_port                    = 9898
  to_port                      = 9898
  referenced_security_group_id = aws_security_group.web.id   # SG를 출발지로 (1일차 7교시)
}
```

## 실습 11 · 만들기

```bash
terraform init
ls .terraform/modules/
terraform plan | tail -1
terraform apply -auto-approve | tail -6
```

> **🟢 확인: 확인**
>
> ```text
> Initializing modules...
> Downloading registry.terraform.io/terraform-aws-modules/vpc/aws 6.○.○ for vpc...
> Initializing the backend...
> Successfully configured the backend "s3"!
> …
> modules.json  vpc
> Plan: 22 to add, 0 to change, 0 to destroy.
> …
> Apply complete! Resources: 22 added, 0 changed, 0 destroyed.
> Outputs:
> private_subnets = [ "subnet-0a…", "subnet-0b…" ]
> public_subnets = [ "subnet-0c…", "subnet-0d…" ]
> vpc_id = "vpc-0e1f2a3b4c5d6e7f8"
> ```
> 코드 약 70줄이 자원 **22개**가 되었습니다(VPC · 서브넷 4 · 라우팅 테이블 · 연결 · IGW · 경로 · 기본 SG/NACL 관리 · 엔드포인트 · 보안 그룹 · 규칙 …). 정확한 수는 모듈 버전마다 조금 다릅니다. 처음부터 backend가 S3라 장부는 버킷의 `w5d3/vpc/`에 있습니다.

## 실습 12 · 콘솔 VPC와 나란히

```bash
for name in devmart-vpc devmart-tf; do
  V=$(aws ec2 describe-vpcs --filters Name=tag:Name,Values=$name --query 'Vpcs[0].VpcId' --output text)
  echo "== $name ($V)"
  aws ec2 describe-subnets --filters Name=vpc-id,Values=$V --query 'sort_by(Subnets,&CidrBlock)[].[AvailabilityZone,CidrBlock]' --output text
  aws ec2 describe-route-tables --filters Name=vpc-id,Values=$V --query 'length(RouteTables)'
done
```

> **🟢 확인: 확인**
>
> ```text
> == devmart-vpc (vpc-0f1e2d3c4b5a69788)
> ap-northeast-2a  10.0.0.0/20
> ap-northeast-2c  10.0.16.0/20
> ap-northeast-2a  10.0.128.0/20
> ap-northeast-2c  10.0.144.0/20
> 4
> == devmart-tf (vpc-0e1f2a3b4c5d6e7f8)
> ap-northeast-2a  10.0.0.0/20
> ap-northeast-2c  10.0.16.0/20
> ap-northeast-2a  10.0.128.0/20
> ap-northeast-2c  10.0.144.0/20
> 4
> ```
> 서브넷 · 라우팅 테이블 수(기본 1 + public 1 + private 2)가 같습니다. 같은 설계를 클릭 대신 코드로 만들었다는 확인입니다. 차이는 **이름**과 **태그**(코드 쪽은 `ManagedBy = terraform`이 모두에 붙었다), 그리고 모듈이 기본 보안 그룹 · 기본 NACL의 규칙까지 **관리 대상으로 가져간다**는 점입니다 — plan의 자원 목록에서 `aws_default_security_group`을 찾아보세요. 모듈의 기본값을 읽어야 하는 이유입니다.

> [!TIP]
> **CIDR이 겹치는데 괜찮나?**
>
> 두 VPC가 같은 `10.0.0.0/16`입니다. 서로 **연결하지 않는 한** 문제없습니다(각자 격리). 연결(피어링)하려면 겹치면 안 됩니다 — 1일차 5교시의 경고. 어차피 콘솔 VPC는 지금 지웁니다.

## 실습 13 · 콘솔 VPC 지우기

1일차의 `devmart-vpc`와, 2일차에 쓴 IAM 역할을 정리합니다. 이제 VPC는 코드로만 만듭니다.

**VPC → 사용자의 VPC → `devmart-vpc` 체크 → 작업 → VPC 삭제**

삭제 확인 화면에 **함께 지워질 것**의 목록이 나옵니다 — 서브넷 넷, 라우팅 테이블, 인터넷 게이트웨이, 보안 그룹 둘, S3 엔드포인트. 2일차 7교시에 고민했던 의존 순서를 콘솔이 이번에는 대신 처리합니다. `delete`를 입력해 삭제.

```bash
aws iam delete-role-policy --role-name devmart-ec2-role --policy-name devmart-s3-read
aws iam detach-role-policy --role-name devmart-ec2-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
aws iam remove-role-from-instance-profile --instance-profile-name devmart-ec2-role --role-name devmart-ec2-role
aws iam delete-instance-profile --instance-profile-name devmart-ec2-role
aws iam delete-role --role-name devmart-ec2-role
aws ec2 describe-vpcs --query 'Vpcs[].[Tags[?Key==`Name`]|[0].Value,IsDefault]' --output text
```

> **🟢 확인: 확인**
>
> ```text
> devmart-tf   False
> None         True
> ```
> 남은 VPC는 기본 VPC와 **코드로 만든** `devmart-tf`뿐입니다. 역할 하나를 지우는 데 명령 다섯 줄 — 역할에 붙은 것을 먼저 떼야 합니다. Terraform이었다면 `destroy` 한 줄이었을 것입니다.

> **❓ 오해 — 공개 모듈은 블랙박스로 쓰면 된다**
>
> 모듈은 내 계정에 **수십 개 자원**을 만듭니다. 기본값(NAT 개수, 기본 보안 그룹 규칙 관리 등)이 내 의도와 다를 수 있고, 메이저 버전이 바뀌면 입력 이름이 바뀝니다(EKS 모듈 v21의 `cluster_name` → `name`처럼). 처음 쓸 때는 **plan의 자원 목록을 다 읽어 봅니다.**

> **🎓 학술 노트 — 재사용과 공급망**
>
> 공개 모듈은 소프트웨어 재사용의 이득과 함께 **공급망 위험**을 가져옵니다. 2주차의 이미지 · 3주차의 의존성과 마찬가지로, 남이 만든 IaC 모듈도 악성 코드나 과한 권한을 넣을 수 있습니다. 이 때문에 모듈 버전 고정 · 잠금 파일 · 내부 미러, 그리고 IaC 정적 분석(Checkov · Trivy의 misconfig 검사)이 권장됩니다. Rahman 외(2019, 1교시)의 보안 냄새 연구가 그 근거 중 하나입니다.

> **📈 트렌드 2026 — 모듈의 버전 관리**
>
> Terraform 1.15는 변수 · 출력에 **폐기 표시**(deprecated)를 붙여, 모듈 작성자가 "다음 메이저에서 이 입력이 사라진다"를 사용자에게 경고할 수 있게 했습니다. 동적 모듈 소스(변수로 `source` · `version` 지정)도 생겨, 환경마다 다른 모듈 버전을 쓰기가 쉬워졌습니다. 조직은 내부 **사설 레지스트리**에 검증한 모듈만 올려 쓰는 것이 일반적입니다.

> **✅ 확인 문제**
>
> 1. 모듈과 Helm 차트의 공통점 셋은?
> 2. 공개 모듈을 고를 때 볼 것 넷은?
> 3. 콘솔 VPC와 모듈 VPC를 비교했을 때 같은 것과 다른 것은?
> 4. IAM 역할을 지울 때 명령이 여러 줄 필요했던 이유는?
>
> <details><summary>정답</summary>
>
> 1. 입력(values/variables)으로 바꿀 수 있다, 저장소에서 받는다, 버전을 고정한다 (여러 자원을 한 묶음으로)
> 2. 관리자 · 최근 커밋, 내려받기 수, 필요한 프로바이더 버전, 예제 · 입력 문서
> 3. 같다(4개) — 차이는 이름 · 태그, 그리고 모듈이 기본 보안 그룹 · NACL까지 관리한다는 점
> 4. 역할에 붙은 정책 · 인스턴스 프로파일을 먼저 떼어야 지울 수 있기 때문 (의존 순서)
>
> </details>

## 참고 문헌

- terraform-aws-modules. *vpc — AWS VPC Terraform module*. registry.terraform.io/modules/terraform-aws-modules/vpc/aws
- HashiCorp. *Modules — Module Sources, Version Constraints*. developer.hashicorp.com/terraform/language/modules
- AWS Docs. *Delete your VPC*. docs.aws.amazon.com/vpc

---

⬅️ 이전: [5교시 · 원격 state와 잠금](lesson-05.md) &nbsp;|&nbsp; [⬆️ 3일차 목차](README.md) &nbsp;|&nbsp; 다음: [7교시 · GitHub Actions에서 plan (OIDC)](lesson-07.md) ➡️
