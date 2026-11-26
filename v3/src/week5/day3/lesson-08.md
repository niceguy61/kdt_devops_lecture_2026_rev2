# 8교시 · Terraform 품질 — fmt · validate · tflint · Trivy · 리뷰

!!! goal "이번 시간에 할 일"
    - 7교시의 `fmt` · `validate`가 **잡는 것과 못 잡는 것**을 구분합니다.
    - **tflint**로 "문법은 맞는데 AWS에서는 틀린 것"(없는 인스턴스 타입 등)과 쓰지 않는 선언을 잡습니다.
    - 2주차에 쓴 **Trivy**로 이번에는 이미지가 아니라 **인프라 코드**의 보안 실수를 찾고, 의도한 예외에는 **이유를 적어** 넘깁니다.
    - `devmart-infra`의 PR에 **lint 잡**을 더하고, plan을 리뷰하는 **다섯 가지 질문**을 정합니다.

!!! key "AWS에 닿기 전에 걸러야 하는 이유"
    Terraform의 실수는 `apply` 뒤에야 드러나면 비쌉니다. 이미 만들어진 자원을 고치거나, 최악에는 **지우고 다시 만들어야** 합니다(`-/+`). 그래서 3주차 CI처럼 **싸고 빠른 검사부터 앞에** 둡니다. 오늘 도구는 모두 AWS 계정 없이, 자원을 하나도 만들지 않고 돕니다.

| 검사 | 잡는 것 | 못 잡는 것 |
|---|---|---|
| `terraform fmt -check` | 들여쓰기 · 정렬 | 그 밖의 모든 것 |
| `terraform validate` | 문법, 없는 변수 · 참조, 타입 | AWS가 받아 줄 값인지 |
| **tflint** | 없는 인스턴스 타입 · 쓰지 않는 선언 · 규칙 위반 | 보안 의도 |
| **Trivy config** | 0.0.0.0/0 · 암호화 없음 · 로그 꺼짐 같은 **보안 실수** | 비용 · 설계 |
| `terraform plan` + 사람 리뷰 | 실제로 **무엇이 바뀌는지** | — |

## 실습 17 · validate가 못 잡는 것

```bash
cd ~/devops-lab/aws/w5d3/terraform/04-vpc
terraform init -input=false > /dev/null
cat > lint-demo.tf <<'EOF'
# 일부러 틀린 파일 — 실습이 끝나면 지운다
variable "unused_name" {
  type = string
}

resource "aws_instance" "demo" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.mirco"        # 오타: micro
  subnet_id     = module.vpc.public_subnets[0]
}
EOF
terraform validate
```

!!! check "통과해 버립니다"
    ```text
    Success! The configuration is valid.
    ```
    `t3.mirco`는 그냥 **문자열**이라 문법상 문제가 없습니다. 이대로 PR이 합쳐지면 `apply` 중에 AWS가 `InvalidParameterValue`로 거절합니다 — 다른 자원이 반쯤 만들어진 뒤에.

## 실습 18 · tflint — AWS를 아는 lint

### 단계 1 — 설정 파일

```bash
cat > .tflint.hcl <<'EOF'
plugin "terraform" {
  enabled = true
  preset  = "recommended"          # 쓰지 않는 선언, 버전 고정, 이름 규칙 …
}

plugin "aws" {
  enabled = true
  version = "0.50.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
EOF
```

### 단계 2 — 컨테이너로 실행

```bash
TFLINT="docker run --rm -v $PWD:/data -v tflint-plugins:/root/.tflint.d --entrypoint sh ghcr.io/terraform-linters/tflint:v0.66.0 -c"
$TFLINT "tflint --init && tflint --format compact"
```

- `-v tflint-plugins:/root/.tflint.d` : AWS 규칙 묶음(플러그인)을 받아 둘 **이름 있는 볼륨** — 다음부터 다시 안 받는다(2주차 3일차 Trivy 캐시와 같은 수법)
- `--entrypoint sh … -c "…"` : 컨테이너 하나에서 `--init`(플러그인 받기)과 검사를 **이어서** 실행

!!! check "이렇게 나오면 성공"
    ```text
    Installing "aws" plugin...
    Installed "aws" (source: github.com/terraform-linters/tflint-ruleset-aws, version: 0.50.0)
    2 issue(s) found:

    lint-demo.tf:8:19: Error - "t3.mirco" is an invalid value as instance_type (aws_instance_invalid_type)
    lint-demo.tf:2:1: Warning - variable "unused_name" is declared but not used (terraform_unused_declarations)
    ```
    - `Error` — AWS가 **받아 주지 않을 값**. tflint의 AWS 규칙 묶음은 AWS API의 정의에서 만들어져 인스턴스 타입 · 리전 이름 등을 압니다
    - `Warning` — 동작은 하지만 **읽는 사람을 헷갈리게** 하는 것. 쓰지 않는 변수는 "이걸 바꾸면 뭐가 바뀌지?"라는 질문만 남깁니다

```bash
rm lint-demo.tf
$TFLINT "tflint --format compact"; echo "종료 코드: $?"
```

!!! check "깨끗하면"
    ```text
    종료 코드: 0
    ```

## 실습 19 · Trivy로 인프라 코드 검사

2주차 3일차에 이미지를 검사한 그 Trivy가 **Terraform 파일**도 읽습니다.

```bash
docker run --rm -v "$PWD":/work -w /work -v trivy-cache:/root/.cache/ aquasec/trivy:0.76.2 \
  config --severity HIGH,CRITICAL --tf-exclude-downloaded-modules .
```

- `config` : 이미지가 아니라 **설정 파일**(Terraform · Kubernetes YAML · Dockerfile …)을 검사
- `--tf-exclude-downloaded-modules` : `.terraform/`에 받아 둔 **공개 모듈 안쪽**은 빼고 **우리 코드만** 본다(모듈 안쪽은 모듈 관리자의 몫, 6교시 학술 노트)

!!! check "이렇게 보입니다 (예시 — ID 표기는 버전에 따라 조금 다름)"
    ```text
    main.tf (terraform)
    Tests: 18 (SUCCESSES: 15, FAILURES: 3)
    Failures: 3 (HIGH: 0, CRITICAL: 3)

    CRITICAL: Security group rule allows unrestricted ingress from any IP address.
     main.tf:33   cidr_ipv4 = "0.0.0.0/0"          (aws_vpc_security_group_ingress_rule.web_http)
    CRITICAL: Security group rule allows unrestricted egress to any IP address.
     main.tf:41   cidr_ipv4 = "0.0.0.0/0"          (aws_vpc_security_group_egress_rule.web_all)
    …
    ```
    1일차 7교시의 "보안 그룹 규칙 읽기"를 기계가 했습니다. 그런데 **web의 80번은 인터넷에 열려 있어야 합니다** — 그게 웹 서버의 일이니까요. 이런 것은 **이유를 적고** 예외로 둡니다.

`main.tf`의 해당 리소스 바로 위에 주석을 붙입니다.

```hcl
# 예외 이유: web은 인터넷 손님을 받는 ALB용. 4일차부터 443만. (2026-12, 리뷰: 짝)
#trivy:ignore:aws-ec2-no-public-ingress-sgr
resource "aws_vpc_security_group_ingress_rule" "web_http" {
```

```hcl
# 예외 이유: 업데이트 · 이미지 받기. 운영은 VPC 엔드포인트로 좁힌다.
#trivy:ignore:aws-ec2-no-public-egress-sgr
resource "aws_vpc_security_group_egress_rule" "web_all" {
```

`#trivy:ignore:` 줄은 **리소스 바로 윗줄**에, 빈칸 없이 씁니다. 이유는 그 위의 보통 주석에 적습니다.

```bash
docker run --rm -v "$PWD":/work -w /work -v trivy-cache:/root/.cache/ aquasec/trivy:0.76.2 \
  config --severity HIGH,CRITICAL --tf-exclude-downloaded-modules --exit-code 1 . | grep -E "^Failures|Tests"
echo "종료 코드: ${PIPESTATUS[0]}"
```

!!! check "이렇게 나오면 성공"
    ```text
    Tests: 16 (SUCCESSES: 15, FAILURES: 1)
    Failures: 1 (HIGH: 0, CRITICAL: 1)
    종료 코드: 1
    ```
    남은 하나는 같은 규칙이 다른 보안 그룹(app의 egress 등)에 걸린 것입니다. 같은 방법으로 **이유를 적어** 예외로 두거나, 규칙을 좁힙니다. 모두 처리하면 종료 코드 0이 됩니다. 2주차 3일차의 `.trivyignore`처럼 **넘기는 것에는 이유 · 사람 · 기한**을 남기는 것이 핵심입니다.

!!! tip "Checkov도 같은 일을 한다"
    1일차 7교시 트렌드의 **Checkov**도 Terraform 보안 검사 도구입니다. 규칙 수와 표현이 조금 다를 뿐 하는 일은 같습니다. 회사에서 이미 쓰는 것을 따르면 됩니다. 중요한 것은 도구 이름이 아니라 **PR에서 자동으로 돌고, 예외에는 이유가 적힌다**는 것입니다.

## 실습 20 · PR에 lint 잡 더하기

### 단계 1 — 워크플로에 잡 하나

`devmart-infra`로 가서 `.github/workflows/terraform-plan.yml`의 `jobs:` 아래, `plan` **앞에** 추가합니다.

```yaml
  lint:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: terraform/04-vpc
    steps:
      - uses: actions/checkout@v6
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.16.1"
      - name: 모양 · 문법
        run: |
          terraform fmt -check -recursive ..
          terraform init -backend=false -input=false
          terraform validate
      - uses: terraform-linters/setup-tflint@v6
        with:
          tflint_version: v0.66.0
      - name: tflint
        run: tflint --init && tflint --format compact
        env:
          GITHUB_TOKEN: ${{ github.token }}     # 플러그인을 받을 때 GitHub API 한도를 넉넉히
      - name: 보안 검사 (Trivy)
        run: |
          docker run --rm -v "$PWD":/work -w /work aquasec/trivy:0.76.2 \
            config --severity HIGH,CRITICAL --tf-exclude-downloaded-modules --exit-code 1 .
```

그리고 `plan` 잡이 lint를 기다리게 합니다.

```yaml
  plan:
    needs: lint
```

| 부분 | 뜻 |
|---|---|
| `init -backend=false` | state 버킷에 **닿지 않고** 모듈만 받는다 — lint 잡에는 AWS 권한이 필요 없다 |
| `needs: lint` | 싼 검사가 실패하면 AWS에 닿는 plan은 **돌리지도 않는다** |

### 단계 2 — PR로 확인

```bash
cd ~/devmart-infra && git switch main && git pull
cp ~/devops-lab/aws/w5d3/terraform/04-vpc/.tflint.hcl terraform/04-vpc/
cp ~/devops-lab/aws/w5d3/terraform/04-vpc/main.tf terraform/04-vpc/      # trivy:ignore 주석이 든 것
git switch -c ci/lint
git add .github terraform/04-vpc
git commit -m "terraform: lint 잡 (fmt · validate · tflint · trivy)"
git push -u origin ci/lint
gh pr create --fill && gh pr checks --watch
```

!!! check "이렇게 나오면 성공"
    ```text
    ✓  lint    48s
    ✓  plan    1m10s
    ```
    `lint`가 실패하면 그 로그의 마지막 줄을 봅니다. 7교시처럼 PR은 합치되, 오늘 VPC는 이미 지웠으므로 **plan이 "만들기"로 나오는 것**은 정상입니다.

```bash
gh pr merge --squash --delete-branch
```

## plan을 리뷰하는 다섯 가지 질문

lint가 초록이어도 마지막은 **사람이 plan을** 읽습니다. 리뷰어는 이 다섯 줄만 확인해도 대부분의 사고를 막습니다. `devmart-infra`의 PR 설명 틀(`.github/pull_request_template.md`)에 넣어 두면 매번 떠올립니다.

| 질문 | plan에서 볼 곳 | 왜 |
|---|---|---|
| ① **지워지는 것**이 있나? | `Plan: … N to destroy` | 의도하지 않은 destroy는 데이터 손실 |
| ② **지우고 다시 만드는 것**(`-/+`)이 있나? | `must be replaced` | 이름 하나 바꿨는데 DB가 새로 만들어질 수 있다 |
| ③ 바뀌는 수가 **코드 변경에 비해** 너무 많지 않나? | `N to change` | 7교시의 태그 하나 → 9개처럼, 모듈이 퍼뜨린다 |
| ④ **0.0.0.0/0** · 공개 · 암호화 끔이 새로 생기나? | `+ cidr_ipv4` 등 | lint가 놓친 의도 |
| ⑤ **돈이 드는 것**이 새로 생기나? | NAT · LB · EIP · 큰 인스턴스 | 1일차의 무서운 줄 |

!!! cleanup "정리"
    `lint-demo.tf`는 이미 지웠습니다. `tflint-plugins` · `trivy-cache` 볼륨은 남겨 둡니다(다음에 빠름). 오늘 자원은 7교시에 모두 지웠습니다.

!!! academic "학술 노트 — 인프라 코드의 '일곱 가지 죄' (Rahman 외, ICSE 2019)"
    노스캐롤라이나 주립대의 아콘드 라만(Akond Rahman) 등은 오픈소스 인프라 코드(Puppet) 1,700여 개 스크립트를 분석해, 보안 사고로 이어지는 **보안 냄새(security smell)** 일곱 가지를 정리했습니다(ICSE 2019). 코드에 박힌 비밀번호, **0.0.0.0에 묶기**, 빈 비밀번호, 의심스러운 주석(`TODO: 나중에 막기`), HTTP 사용, 약한 암호화, 관리자 기본 사용자가 그것입니다. 연구진은 이런 냄새가 **수천 개** 있었고 고쳐지기까지 **오래 남아 있었다**는 것을 보여 주었습니다. 결론은 사람의 주의만으로는 부족하고 **자동 검사가 PR마다** 돌아야 한다는 것이었습니다. 오늘 lint 잡이 그 결론의 실천입니다.

    - Rahman, A., Parnin, C., & Williams, L. (2019). The seven sins: Security smells in infrastructure as code scripts. *ICSE 2019*, 164–175.

!!! trend "트렌드 — AI가 쓴 인프라 코드일수록 검문소가"
    2026년에는 Terraform 코드를 AI가 쓰는 일이 흔합니다. AI는 그럴듯하지만 **없는 인자 · 지난 버전의 문법 · 너무 넓은 권한**을 섞어 쓰기도 합니다(1주차 1일차 3교시의 환각). 그래서 사람이 쓴 코드보다 오히려 **자동 검문소**(validate · tflint · Trivy · plan 리뷰)가 더 중요해졌습니다. 회사들은 여기에 **정책 코드**(OPA · Conftest, HCP Terraform의 Sentinel)를 더해 "태그 넷이 없는 자원 금지"(1일차 8교시), "NAT는 dev 환경에서 금지" 같은 조직 규칙까지 PR에서 막습니다.

## 정리

- `fmt`(모양) → `validate`(문법) → **tflint**(AWS가 받을 값 · 쓰지 않는 선언) → **Trivy config**(보안 실수) → **plan + 사람**(실제 변화). 싼 것부터 앞에.
- 의도한 예외(웹의 0.0.0.0/0)는 **이유를 적은 주석**으로 넘깁니다.
- lint 잡은 `init -backend=false`로 **AWS 권한 없이**, plan은 `needs: lint`로 그 뒤에.
- plan 리뷰 다섯 질문: **destroy · 교체(-/+) · 변경 수 · 공개 · 돈**.

!!! quiz "확인 문제"
    1. `instance_type = "t3.mirco"`를 `terraform validate`가 통과시키는 이유는? 무엇이 잡나요?
    2. Trivy가 web 보안 그룹의 0.0.0.0/0 규칙을 CRITICAL로 잡았습니다. 어떻게 처리하나요?
    3. lint 잡에서 `terraform init -backend=false`를 쓰는 이유는?
    4. plan에 `must be replaced`가 보입니다. 왜 특히 조심해야 하나요?
    5. `--tf-exclude-downloaded-modules`를 쓰는 이유는?

    ??? answer "정답"
        1. 문법상 그냥 문자열이기 때문. tflint의 AWS 규칙(`aws_instance_invalid_type`)이 잡는다
        2. 의도한 것이면 이유 · 날짜 · 리뷰어를 적은 `trivy:ignore` 주석으로 넘기고, 아니면 규칙을 좁힌다
        3. state 버킷(AWS)에 닿지 않아 lint 잡에 AWS 권한이 필요 없게 하려고
        4. 자원을 지우고 다시 만들어서 데이터가 사라지거나 주소가 바뀔 수 있다
        5. 공개 모듈 안쪽의 결과는 우리가 고칠 수 없으므로, 우리 코드의 문제만 보려고

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - 콘솔 · CLI 스크립트 · Terraform을 한 줄씩, 어제의 경험을 예로
    - plan 기호 넷(+ ~ - -/+) 중 가장 무서운 것과 그 이유
    - 콘솔에서 바꾼 버전 관리 · 태그를 plan이 잡은 장면 — Argo CD의 OutOfSync와 무엇이 같고 다른가
    - state를 S3에 두고 잠금을 건 이유 셋
    - GitHub Actions가 키 없이 AWS에 들어간 순서를 그림으로
    - 내일 전에 궁금한 것: 오늘 VPC는 22개 자원이었다. **EKS 클러스터**를 코드로 만들면 몇 개일까? 그 위에 4주차의 DevMart를 **그대로** 올릴 수 있을까?

## 참고 문헌

- Rahman, A., Parnin, C., & Williams, L. (2019). The seven sins: Security smells in infrastructure as code scripts. *Proceedings of ICSE 2019*.
- HashiCorp. *Terraform CLI — fmt, validate, plan*. developer.hashicorp.com/terraform/cli
- TFLint. *TFLint* v0.66 · *tflint-ruleset-aws* v0.50 · *setup-tflint*. github.com/terraform-linters
- Aqua Security. *Trivy — Misconfiguration scanning (Terraform), Skipping checks (inline ignore), --tf-exclude-downloaded-modules*. trivy.dev
- Bridgecrew. *Checkov Documentation*. checkov.io
