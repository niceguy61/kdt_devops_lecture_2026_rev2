[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [3일차](README.md)

# 3교시 · HCL — 변수 · 참조 · for_each

> [!NOTE]
> **이번 시간에 할 일**
>
> - 변수(`variable`) · 값 파일(`tfvars`) · 지역 값(`locals`) · 출력(`output`)을 씁니다.
> - **데이터 소스**로 이미 있는 것(내 계정 번호, AZ 목록)을 읽습니다.
> - `for_each`로 같은 모양의 자원을 여러 개 만듭니다.
> - 자원 사이의 **참조**가 곧 **의존 관계**라는 것을 그래프로 봅니다.

## 파일 나누기

```bash
cd ~/devops-lab/aws/w5d3/terraform/02-hcl
ls
```

```text
main.tf  outputs.tf  terraform.tfvars.example  variables.tf  versions.tf
```

Terraform은 폴더 안의 `.tf`를 **모두 합쳐** 읽습니다. 파일 이름은 사람을 위한 관례입니다 — `versions.tf`(버전 · 프로바이더), `variables.tf`(입력), `main.tf`(자원), `outputs.tf`(출력).

## 변수와 값

```hcl
variable "owner" {
  description = "내 GitHub ID (소문자) — 버킷 이름과 태그에 쓴다"
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.owner))
    error_message = "owner는 소문자 · 숫자 · 하이픈만 쓸 수 있습니다 (S3 버킷 이름 규칙)."
  }
}

variable "buckets" {
  type = map(object({ versioning = bool }))
  default = {
    assets = { versioning = true }
    logs   = { versioning = false }
  }
}
```

| 값을 주는 방법 | 예 | 쓰는 때 |
|---|---|---|
| `default` | 위의 buckets | 대부분 같은 값 |
| `terraform.tfvars` 파일 | `owner = "niceguy61"` | 내 환경의 값 (Git에 넣지 않는다) |
| `-var` | `terraform plan -var owner=niceguy61` | 한 번만 |
| 환경 변수 `TF_VAR_owner` | CI에서 | 비밀 값 |

`validation`은 잘못된 값을 **plan 전에** 막습니다 — 4주차 5일차 Kyverno의 입장 제어를 변수에 건 것과 같습니다.

```bash
terraform init
terraform plan -var owner=NiceGuy61 2>&1 | grep -A2 "Invalid value"
cp terraform.tfvars.example terraform.tfvars
sed -i "s/your-github-id/$(gh api user -q .login | tr 'A-Z' 'a-z')/" terraform.tfvars
cat terraform.tfvars
```

> **🟢 확인: 확인**
>
> ```text
> │ Error: Invalid value for variable
> │ owner는 소문자 · 숫자 · 하이픈만 쓸 수 있습니다 (S3 버킷 이름 규칙).
> owner = "niceguy61"
> ```

## 자원 읽기 — main.tf

```hcl
data "aws_caller_identity" "me" {}                 # 이미 있는 것을 읽는다 — 만들지 않는다
data "aws_availability_zones" "available" { state = "available" }

locals {
  prefix = "devmart-${var.owner}"                   # 여러 곳에 쓸 계산 값
}

resource "aws_s3_bucket" "this" {
  for_each      = var.buckets                       # assets, logs — 두 개
  bucket        = "${local.prefix}-${each.key}"     # devmart-niceguy61-assets
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "this" {
  for_each = var.buckets
  bucket   = aws_s3_bucket.this[each.key].id        # ← 위 버킷을 참조
  versioning_configuration {
    status = each.value.versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_object" "notice" {
  bucket  = aws_s3_bucket.this["assets"].id
  key     = "notice.txt"
  content = "DevMart 공지 — Terraform이 올렸다 (계정 ${data.aws_caller_identity.me.account_id})"
}
```

| 문법 | 뜻 | 3 · 4주차에서 |
|---|---|---|
| `var.owner` | 변수 | Helm values의 `.Values.x` |
| `local.prefix` | 지역 계산 값 | — |
| `data.…` | **이미 있는 것** 읽기 | `kubectl get` |
| `for_each = map` | 키마다 하나씩 — 주소가 `aws_s3_bucket.this["assets"]` | Helm의 `range` |
| `each.key` · `each.value` | 지금 만드는 것의 키 · 값 | |
| `"${…}"` | 문자열 끼워 넣기 | |
| `cond ? a : b` | 조건 | |

> [!IMPORTANT]
> **참조 = 의존**
>
> `aws_s3_bucket_versioning`이 `aws_s3_bucket.this[...].id`를 **참조**하므로, Terraform은 "버킷을 먼저 만들고 버전 설정을 나중에" 해야 한다는 것을 **스스로** 압니다. 지울 때는 거꾸로 합니다. 2일차 7교시에 사람이 표로 정리했던 의존 순서를 코드의 참조에서 자동으로 뽑는 것입니다.

## 실습 4 · 만들기와 그래프

```bash
terraform plan | tail -3
terraform apply -auto-approve
terraform output
aws s3 cp s3://$(terraform output -json bucket_names | python3 -c "import sys,json;print(json.load(sys.stdin)['assets'])")/notice.txt -
```

> **🟢 확인: 확인**
>
> ```text
> Plan: 7 to add, 0 to change, 0 to destroy.
> …
> Apply complete! Resources: 7 added, 0 changed, 0 destroyed.
>
> Outputs:
>
> account_id = "123456789012"
> azs = tolist([
>   "ap-northeast-2a",
>   "ap-northeast-2b",
>   "ap-northeast-2c",
>   "ap-northeast-2d",
> ])
> bucket_names = {
>   "assets" = "devmart-niceguy61-assets"
>   "logs" = "devmart-niceguy61-logs"
> }
> DevMart 공지 — Terraform이 올렸다 (계정 123456789012)
> ```
> 7개 = 버킷 2 + 버전 설정 2 + 공개 차단 2 + 파일 1. 버킷 둘은 **동시에** 만들어집니다 — 서로 의존하지 않으니까요.

```bash
terraform graph | grep -E '"aws_s3_(bucket|object)' | grep -- '->' | head -6
```

> **🟢 확인: 확인**
>
> ```text
> "aws_s3_bucket_public_access_block.this (expand)" -> "aws_s3_bucket.this (expand)"
> "aws_s3_bucket_versioning.this (expand)" -> "aws_s3_bucket.this (expand)"
> "aws_s3_object.notice (expand)" -> "aws_s3_bucket.this (expand)"
> "aws_s3_object.notice (expand)" -> "data.aws_caller_identity.me (expand)"
> …
> ```
> 화살표가 "**이것은 저것에 기댄다**"입니다. 2일차 7교시 학술 노트의 위상 정렬을 Terraform이 이 그래프로 합니다. (`terraform graph | dot -Tpng > graph.png`로 그림도 됩니다 — graphviz가 있으면.)

## for_each로 하나 더

`variables.tf`의 `buckets` 기본값에 한 줄을 더합니다.

```bash
sed -i 's/    logs   = { versioning = false }/    logs   = { versioning = false }\n    backup = { versioning = true }/' variables.tf
terraform plan | grep -E '^\s+# |Plan:'
```

> **🟢 확인: 확인**
>
> ```text
>   # aws_s3_bucket.this["backup"] will be created
>   # aws_s3_bucket_public_access_block.this["backup"] will be created
>   # aws_s3_bucket_versioning.this["backup"] will be created
> Plan: 3 to add, 0 to change, 0 to destroy.
> ```
> 키로 주소가 정해지므로, 목록 **중간**에 하나를 넣거나 빼도 다른 것은 영향을 받지 않습니다. (`count`로 0, 1, 2 번호를 쓰면 중간을 빼는 순간 뒤의 것들이 **모두 다시 만들어질** 수 있습니다 — 이름이 있는 것은 `for_each`.)

```bash
sed -i '/    backup = { versioning = true }/d' variables.tf
terraform plan | tail -1
```

`No changes.`로 돌아옵니다(apply하지 않았으니).

> **❓ 오해 — 코드가 길어지면 복사해서 붙이면 된다**
>
> 같은 모양을 복사해 붙이면 한 곳을 고칠 때 나머지를 잊습니다. 같은 모양은 `for_each`로, 같은 **묶음**은 모듈(6교시)로 만듭니다. 2주차의 함수, 4주차의 Helm 차트와 같은 이유입니다.

> **🎓 학술 노트 — 설정 언어의 표현력**
>
> HCL처럼 '데이터 + 약간의 계산'을 담는 설정 언어는 너무 약하면 복사가 늘고, 너무 강하면(반복 · 재귀 · 부수 효과) 이해하기 어려워집니다. 구글 Borg의 설정 언어 BCL을 돌아본 Burns 외(*Borg, Omega, and Kubernetes*, 2016, 4주차 3일차)는 "설정이 **튜링 완전한 프로그램**이 되면서 관리가 어려워졌다"고 썼고, 그 반성이 CUE · Jsonnet · KCL 같은 **제약 있는 설정 언어** 연구로 이어졌습니다. HCL은 일부러 '프로그래밍 언어가 아닌' 쪽에 머뭅니다.

> **📈 트렌드 2026 — 테스트되는 IaC**
>
> Terraform은 `terraform test`(`.tftest.hcl`)로 **plan 결과를 단언**하는 테스트를 지원하고, 1.15의 변수 폐기 표시 · 출력 타입 제약처럼 모듈을 **라이브러리처럼** 관리하는 기능이 늘고 있습니다. "IaC도 단위 테스트 · 버전 · 폐기 정책을 갖춘 소프트웨어"라는 흐름입니다.

> **✅ 확인 문제**
>
> 1. `data` 블록과 `resource` 블록의 차이는?
> 2. Terraform이 "버킷 먼저, 버전 설정 나중"을 아는 방법은?
> 3. `for_each`가 `count`보다 안전한 이유는?
> 4. validation이 하는 일은?
>
> <details><summary>정답</summary>
>
> 1. data는 이미 있는 것을 읽기만, resource는 만들고 관리한다
> 2. 버전 설정이 버킷의 id를 참조하기 때문 — 참조가 의존 관계가 된다
> 3. 키로 주소가 정해져 중간에 넣고 빼도 다른 자원이 다시 만들어지지 않는다
> 4. 잘못된 변수 값을 plan 전에 막는다
>
> </details>

## 참고 문헌

- HashiCorp. *Input Variables*, *Local Values*, *Data Sources*, *The for_each Meta-Argument*. developer.hashicorp.com/terraform/language
- HashiCorp. *terraform graph*, *terraform test*. developer.hashicorp.com/terraform/cli
- Burns, B. 외 (2016). *Borg, Omega, and Kubernetes*. ACM Queue 14(1).

---

⬅️ 이전: [2교시 · 설치와 첫 리소스](lesson-02.md) &nbsp;|&nbsp; [⬆️ 3일차 목차](README.md) &nbsp;|&nbsp; 다음: [4교시 · state · 어긋남 · import](lesson-04.md) ➡️
