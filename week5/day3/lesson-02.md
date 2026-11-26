<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [3일차](README.md) › 2/8교시</sub>

# 2교시 · 설치와 첫 리소스

> [!NOTE]
> **이번 시간에 할 일**
>
> - Terraform을 설치하고 `aws login` 자격 증명이 Terraform에 닿는지 확인합니다.
> - S3 버킷 **하나**로 init · plan · apply · state · destroy를 한 바퀴 돕니다.
> - plan 출력의 기호(`+` `~` `-` `-/+`)를 읽습니다.
> - 무엇을 Git에 넣고 무엇을 넣지 않는지 정합니다.

## 실습 1 · 설치

**Linux · WSL2 Ubuntu (bash)** — HashiCorp 공식 apt 저장소를 추가하고 설치합니다.

```bash
wget -qO- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install -y terraform
```

**Mac (터미널 · Homebrew)** — Terraform은 라이선스(BUSL) 변경 뒤 Homebrew 기본 저장소에서 빠졌으므로 HashiCorp의 tap을 씁니다.

```bash
brew tap hashicorp/tap && brew install hashicorp/tap/terraform
```

**확인 (공통)**

```bash
terraform version
terraform -install-autocomplete 2>/dev/null; true
```

> **🟢 확인: 확인**
>
> ```text
> Terraform v1.16.○
> on linux_amd64
> ```
> 1.15 이상이면 됩니다. VS Code를 쓰면 **HashiCorp Terraform** 확장을 깔아 문법 강조 · 자동 완성을 받습니다.

> [!TIP]
> **다른 설치 방법 — winget · 직접 다운로드**
>
> | 방법 | 어디서 | 명령 · 주소 |
> |---|---|---|
> | winget | Windows PowerShell | `winget install -e --id Hashicorp.Terraform` |
> | 직접 다운로드 | 브라우저 | [developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install) — zip을 풀어 `terraform` 하나를 PATH에 |
>
> winget은 **Windows 쪽**에 설치하므로 PowerShell에서만 보입니다. 수업 명령은 WSL Ubuntu(bash)에서 치므로, Windows 사용자도 위의 **WSL 방법**으로 설치합니다. 전체 목록은 **부록 A · 도구 설치 가이드**.

## 실습 2 · 첫 리소스

```bash
mkdir -p ~/devops-lab/aws/w5d3 && cp -r ~/course/labs/week5/day3/* ~/devops-lab/aws/w5d3/
cd ~/devops-lab/aws/w5d3/terraform/01-first
ID=$(gh api user -q .login | tr 'A-Z' 'a-z')
sed -i "s/YOUR_ID/$ID/" main.tf          # Mac: sed -i ''
cat main.tf
```

```hcl
terraform {
  required_version = ">= 1.15"
  required_providers {
    aws = {
      source  = "hashicorp/aws"   # 레지스트리 주소
      version = "~> 6.0"          # 6.x 중 최신 (7.0은 받지 않는다)
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_s3_bucket" "first" {    # resource "종류" "코드 안의 이름"
  bucket = "devmart-tf-first-niceguy61"
  tags = { Project = "devmart", ManagedBy = "terraform" }
}
```

| 블록 | 뜻 |
|---|---|
| `terraform` | Terraform 자체 설정 — 버전, 쓸 프로바이더 |
| `provider "aws"` | AWS와 말하는 플러그인의 설정 — 리전 (자격 증명은 `aws login`에서 자동) |
| `resource "aws_s3_bucket" "first"` | 만들 것 하나. `aws_s3_bucket.first`가 **코드 안의 주소** |

```bash
terraform init
```

> **🟢 확인: 확인**
>
> ```text
> Initializing provider plugins...
> - Finding hashicorp/aws versions matching "~> 6.0"...
> - Installing hashicorp/aws v6.○○.○...
> - Installed hashicorp/aws v6.○○.○ (signed by HashiCorp)
> Terraform has created a lock file .terraform.lock.hcl …
> Terraform has been successfully initialized!
> ```
> `.terraform/`(내려받은 플러그인)과 `.terraform.lock.hcl`(고른 버전의 지문)이 생겼습니다. 잠금 파일은 Git에 **넣습니다** — 2주차의 `requirements.txt`처럼 모두가 같은 버전을 쓰게.

```bash
terraform plan
```

> **🟢 확인: 확인**
>
> ```text
> Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
>   + create
>
> Terraform will perform the following actions:
>
>   # aws_s3_bucket.first will be created
>   + resource "aws_s3_bucket" "first" {
>       + arn                         = (known after apply)
>       + bucket                      = "devmart-tf-first-niceguy61"
>       + id                          = (known after apply)
>       + region                      = "ap-northeast-2"
>       + tags                        = {
>           + "ManagedBy" = "terraform"
>           + "Project"   = "devmart"
>         }
>       …
>     }
>
> Plan: 1 to add, 0 to change, 0 to destroy.
> ```
> `(known after apply)` — ARN · ID처럼 **만들어 봐야 아는 값**입니다.

> **🛠️ 막혔다면: No valid credential sources found**
>
> 프로바이더가 `aws login` 자격 증명을 읽지 못하는 경우입니다. ① `aws sts get-caller-identity`로 로그인이 살아 있는지 보고, ② 그래도 안 되면 1일차 4교시의 방법으로 임시 자격 증명을 환경 변수에 넣습니다: `eval "$(aws configure export-credentials --format env)"`. 이 셸에서만, 한 시간쯤 유효합니다.

```bash
terraform apply          # plan을 다시 보여 주고 묻는다 → yes
terraform state list
terraform state show aws_s3_bucket.first | head -12
aws s3 ls | grep devmart-tf-first
terraform apply          # 한 번 더
```

> **🟢 확인: 확인**
>
> ```text
> aws_s3_bucket.first: Creating...
> aws_s3_bucket.first: Creation complete after 2s [id=devmart-tf-first-niceguy61]
> Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
> aws_s3_bucket.first
> # aws_s3_bucket.first:
> resource "aws_s3_bucket" "first" {
>     arn    = "arn:aws:s3:::devmart-tf-first-niceguy61"
>     bucket = "devmart-tf-first-niceguy61"
>     …
> 2026-12-01 10:12:41 devmart-tf-first-niceguy61
> …
> No changes. Your infrastructure matches the configuration.
> ```
> 두 번째 apply는 **아무것도 하지 않습니다** — 멱등입니다(1교시 표).

## 실습 3 · 바꾸고 지우기

`main.tf`의 tags에 `Day = "w5d3"`를 한 줄 더하고 plan합니다.

```bash
sed -i 's/ManagedBy = "terraform"/ManagedBy = "terraform", Day = "w5d3"/' main.tf
terraform plan | grep -E "^\s+[~+-]|Plan:"
```

> **🟢 확인: 확인**
>
> ```text
>   ~ update in-place
>   ~ resource "aws_s3_bucket" "first" {
>       ~ tags                        = {
>           + "Day"       = "w5d3"
>   Plan: 0 to add, 1 to change, 0 to destroy.
> ```

이번에는 **이름**을 바꿔 봅니다(apply하지 않는다).

```bash
sed -i 's/devmart-tf-first-/devmart-tf-1st-/' main.tf
terraform plan | grep -E "must be replaced|forces replacement|Plan:"
sed -i 's/devmart-tf-1st-/devmart-tf-first-/' main.tf
```

> **🟢 확인: 확인**
>
> ```text
> -/+ resource "aws_s3_bucket" "first" {
>       ~ bucket = "devmart-tf-first-niceguy61" -> "devmart-tf-1st-niceguy61" # forces replacement
> Plan: 1 to add, 0 to change, 1 to destroy.
> ```

| 기호 | 뜻 | 위험도 |
|---|---|---|
| `+` | 새로 만든다 | 낮음 |
| `~` | 그 자리에서 고친다 | 중간 |
| `-` | 지운다 | 높음 |
| `-/+` | **지우고 다시 만든다** (바꿀 수 없는 속성이 바뀜) | **높음** — 데이터가 사라질 수 있다 |

> [!WARNING]
> **plan에서 -/+ 를 보면 멈춘다**
>
> S3 버킷 이름 · DB 엔진 · EKS 클러스터 이름처럼 **바꿀 수 없는 속성**을 고치면 Terraform은 지우고 새로 만듭니다. 버킷 안의 파일 · DB의 데이터는 함께 사라집니다. plan 리뷰에서 가장 먼저 찾을 것이 `-/+`와 `destroy` 개수입니다 — 2일차 8교시의 의존 순서와 함께, 사람이 plan을 읽는 이유입니다.

```bash
terraform apply -auto-approve      # 태그만 바뀐다
terraform destroy                  # 묻는다 → yes
terraform state list               # 아무것도 없다
```

## Git에 넣는 것 · 넣지 않는 것

```bash
cat ~/devops-lab/aws/w5d3/terraform/.gitignore
```

| 넣는다 | 넣지 않는다 |
|---|---|
| `*.tf` — 코드 | `.terraform/` — 내려받은 플러그인 (수백 MB) |
| `.terraform.lock.hcl` — 버전 고정 | `*.tfstate` — **장부, 비밀 값이 평문으로 들어갈 수 있다** (5교시) |
| `*.tfvars.example` — 변수 예시 | `*.tfvars` — 실제 값 (개인 · 비밀) |

> **❓ 오해 — state 파일은 Git으로 공유하면 된다**
>
> state를 Git에 넣으면 ① 비밀 값(DB 비밀번호 등)이 이력에 영원히 남고, ② 두 사람이 동시에 apply하면 서로의 state를 **덮어써** 장부가 깨집니다. state는 **잠금이 되는 원격 저장소**에 둡니다 — 5교시.

> **🎓 학술 노트 — 의미 있는 버전**
>
> `~> 6.0`은 **유의적 버전**(SemVer 2.0.0, Preston-Werner 2013)의 약속 — 주 버전(6)이 같으면 호환된다 — 에 기대는 표현입니다. 하지만 Raemaekers 외의 *Semantic versioning and impact of breaking changes in the Maven repository*(JSS, 2017)는 부 버전 업데이트의 상당수가 실제로는 호환성을 깼다는 것을 보였습니다. 그래서 범위(`~>`)와 함께 **잠금 파일**로 실제 버전을 고정하고, 올리는 것은 PR로 합니다 — 2주차의 이미지 태그 고정과 같은 원리입니다.

> **📈 트렌드 2026 — 프로바이더 v6**
>
> AWS 프로바이더 v6(2025년 6월)는 프로바이더 하나로 **여러 리전**의 자원을 다루는 `region` 인자를 자원마다 쓸 수 있게 했고(plan 출력의 `region` 칸), 오래된 인자들을 정리했습니다. 인터넷의 예제 코드 상당수가 v4 · v5 문법이라, 복사해 쓸 때 `terraform validate`와 plan으로 먼저 확인하는 습관이 필요합니다.

> **✅ 확인 문제**
>
> 1. `init`이 만드는 두 가지와 각각 Git에 넣는지는?
> 2. 두 번째 apply가 아무것도 하지 않은 이유는?
> 3. plan의 `-/+`는 무슨 뜻이고 왜 위험한가요?
> 4. state를 Git에 넣으면 안 되는 이유 둘은?
>
> <details><summary>정답</summary>
>
> 1. `.terraform/`(플러그인, 넣지 않는다)와 `.terraform.lock.hcl`(버전 고정, 넣는다)
> 2. 코드 · state · 실제가 같아서 할 일이 없기 때문 (멱등)
> 3. 바꿀 수 없는 속성이 바뀌어 지우고 다시 만든다는 뜻 — 안의 데이터가 사라질 수 있다
> 4. 비밀 값이 평문으로 이력에 남는다, 동시에 apply하면 서로 덮어써 장부가 깨진다
>
> </details>

## 참고 문헌

- HashiCorp. *Install Terraform*, *terraform init · plan · apply · destroy*. developer.hashicorp.com/terraform
- HashiCorp. *AWS Provider v6 upgrade guide*. registry.terraform.io/providers/hashicorp/aws
- Preston-Werner, T. (2013). *Semantic Versioning 2.0.0*. semver.org

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [1교시 · 2일차 요약 + 코드로 인프라](lesson-01.md) | [⬆️ 3일차 목차](README.md) | [3교시 · HCL — 변수 · 참조 · for_each](lesson-03.md) ➡️ |
