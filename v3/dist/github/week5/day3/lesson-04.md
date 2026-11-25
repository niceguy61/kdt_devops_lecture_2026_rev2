# 4교시 · state · 어긋남 · import

> [!NOTE]
> **이번 시간에 할 일**
>
> - state 파일 안을 들여다보고, 무엇이 들어 있는지(그리고 왜 조심해야 하는지) 압니다.
> - 콘솔에서 자원을 **손으로 바꿔** 어긋남(drift)을 만들고, plan이 그것을 잡는 것을 봅니다.
> - 콘솔로 만든 자원을 **import**로 코드에 데려오고, **removed**로 놓아줍니다.

## state 안 보기

```bash
cd ~/devops-lab/aws/w5d3/terraform/02-hcl
ls -la terraform.tfstate
python3 -c "import json; s=json.load(open('terraform.tfstate')); print('serial', s['serial']); [print(r['mode'], r['type'], r['name'], [i.get('index_key') for i in r['instances']]) for r in s['resources']]"
grep -o '"arn": "[^"]*assets"' terraform.tfstate | head -1
```

> **🟢 확인: 확인**
>
> ```text
> -rw-r--r-- 1 me me 14728 …  terraform.tfstate
> serial 5
> data aws_availability_zones available [None]
> data aws_caller_identity me [None]
> managed aws_s3_bucket this ['assets', 'logs']
> managed aws_s3_bucket_public_access_block this ['assets', 'logs']
> managed aws_s3_bucket_versioning this ['assets', 'logs']
> managed aws_s3_object notice [None]
> "arn": "arn:aws:s3:::devmart-niceguy61-assets"
> ```
> state는 **JSON 장부**입니다. 코드의 주소(`aws_s3_bucket.this["assets"]`) ↔ AWS의 실제 ID · 속성이 적혀 있습니다. `serial`은 apply할 때마다 올라가는 번호입니다.

> [!WARNING]
> **state는 손으로 고치지 않는다**
>
> 장부가 실제와 맞지 않게 되면 Terraform이 이미 있는 것을 다시 만들려 하거나, 남의 것을 지우려 할 수 있습니다. state를 바꿀 때는 `terraform state mv · rm`, `import` · `moved` · `removed` 블록처럼 **Terraform의 명령으로만** 합니다. 그리고 DB 비밀번호 같은 값은 state에 **평문으로** 들어갈 수 있습니다 — 다음 교시에 state를 잠긴 버킷으로 옮기는 이유입니다.

## 실습 5 · 어긋남 만들기

콘솔 → S3 → `devmart-<ID>-logs` → **속성** 탭

1. **버킷 버전 관리** → 편집 → **활성화** → 변경 사항 저장
2. **태그** → 편집 → `Project` 값을 `hacked`로 → 저장

누군가 "급하게" 콘솔에서 바꿨다고 합시다. 코드는 그대로입니다.

```bash
terraform plan
```

> **🟢 확인: 확인**
>
> ```text
> aws_s3_bucket.this["logs"]: Refreshing state... [id=devmart-niceguy61-logs]
> …
> Terraform will perform the following actions:
>
>   # aws_s3_bucket.this["logs"] will be updated in-place
>   ~ resource "aws_s3_bucket" "this" {
>       ~ tags_all = {
>           ~ "Project"   = "hacked" -> "devmart"
>       …
>   # aws_s3_bucket_versioning.this["logs"] will be updated in-place
>   ~ resource "aws_s3_bucket_versioning" "this" {
>       ~ versioning_configuration {
>           ~ status = "Enabled" -> "Suspended"
> …
> Plan: 0 to add, 2 to change, 0 to destroy.
> ```
> plan은 먼저 **새로 고침**(Refreshing state)으로 실제 AWS를 읽고, 코드와 다른 것을 **되돌리는** 계획을 냅니다. `왼쪽 -> 오른쪽`이 "지금(실제) → 코드대로"입니다.

> [!IMPORTANT]
> **Argo CD와 나란히**
>
> | 4주차 3일차 Argo CD | 오늘 Terraform |
> |---|---|
> | 계속 비교 — OutOfSync 표시 | **plan을 돌릴 때만** 비교 |
> | selfHeal이면 몇 초 만에 되돌린다 | `apply`를 해야 되돌린다 |
> | 손 수정이 옳았다면 Git에 PR | 손 수정이 옳았다면 **코드를 고친다** |
>
> 그래서 실무에서는 Terraform plan을 **매일 아침 CI로** 돌려 "변경 0"이 아니면 알림을 보내는 **drift 감지**를 둡니다(7교시의 워크플로를 schedule로 돌리면 된다).

어느 쪽이 맞나 정합니다 — 이번에는 손 수정이 실수입니다.

```bash
terraform apply -auto-approve | tail -1
terraform plan -refresh-only | tail -2
```

> **🟢 확인: 확인**
>
> ```text
> Apply complete! Resources: 0 added, 2 changed, 0 destroyed.
> No changes. Your infrastructure still matches the configuration.
> ```
> `-refresh-only`는 "바꾸지 말고 실제를 읽기만" — 어긋남 **점검용**입니다.

## 실습 6 · import — 콘솔 자원을 코드로

1일차에 콘솔로 만든 `devmart-web-sg`를 코드가 관리하게 해 봅니다. 먼저 ID를 찾습니다.

```bash
SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values=devmart-web-sg --query 'SecurityGroups[0].GroupId' --output text); echo $SG
cp import.tf.example import.tf
sed -i "s/sg-REPLACE_ME/$SG/" import.tf
cat import.tf
terraform plan -generate-config-out=generated.tf | tail -4
cat generated.tf
```

> **🟢 확인: 확인**
>
> ```text
> sg-0a1b2c3d4e5f60718
> import {
>   to = aws_security_group.console_web
>   id = "sg-0a1b2c3d4e5f60718"
> }
> …
> Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.
> # __generated__ by Terraform
> resource "aws_security_group" "console_web" {
>   description = "HTTP from internet"
>   egress      = [ { cidr_blocks = ["0.0.0.0/0"], from_port = 0, protocol = "-1", … } ]
>   ingress     = [ { cidr_blocks = ["0.0.0.0/0"], from_port = 80, protocol = "tcp", … } ]
>   name        = "devmart-web-sg"
>   tags        = { Project = "devmart" }
>   vpc_id      = "vpc-0f1e2d3c4b5a69788"
>   …
> }
> ```
> Terraform이 실제 자원을 읽어 **코드를 대신 써 주었습니다.** 1일차 6교시 트렌드의 "콘솔에서 코드로"입니다.

```bash
terraform apply -auto-approve | tail -1
terraform state list | grep console
```

> **🟢 확인: 확인**
>
> `Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.` — 아무것도 만들거나 바꾸지 않고 **장부에 올리기만** 했습니다. 이제 `generated.tf`를 고쳐 apply하면 이 보안 그룹이 바뀝니다.

### removed — 놓아주기

하지만 이 보안 그룹은 1일차 VPC의 것이고, 6교시에 그 VPC를 **콘솔로** 지울 것입니다. 지금 `terraform destroy`를 하면 Terraform이 이 그룹까지 지우려 하고, app-sg가 그것을 참조하고 있어 실패합니다. 그래서 **장부에서만 빼고 AWS에는 남깁니다.**

```bash
rm import.tf generated.tf
cat > removed.tf <<'HCL'
removed {
  from = aws_security_group.console_web
  lifecycle {
    destroy = false   # 장부에서만 빼고, AWS의 자원은 지우지 않는다
  }
}
HCL
terraform apply -auto-approve | grep -E "removed|forget|Apply"
rm removed.tf
aws ec2 describe-security-groups --group-ids $SG --query 'SecurityGroups[0].GroupName' --output text
```

> **🟢 확인: 확인**
>
> ```text
>   # aws_security_group.console_web will no longer be managed by Terraform
> Apply complete! Resources: 0 added, 0 changed, 0 destroyed. 1 forgotten.
> devmart-web-sg
> ```
> 장부에서는 빠졌고(`forgotten`), AWS에는 그대로 있습니다. `import`(데려오기) · `removed`(놓아주기) · `moved`(코드 안에서 이름 바꾸기)가 state를 **안전하게** 다루는 세 블록입니다 — 모두 코드로 남아 PR로 리뷰할 수 있습니다.

> **❓ 오해 — Terraform이 계정의 모든 것을 안다**
>
> Terraform은 **장부에 있는 것만** 압니다. 콘솔로 만든 자원, 다른 프로젝트가 만든 자원은 plan에 나오지 않고, destroy도 건드리지 않습니다. 4주차 4일차의 "추적 표시가 없으면 Argo CD가 지우지 않는다"와 같습니다. 그래서 '남은 것 찾기'(2일차 7교시)는 Terraform만으로는 끝나지 않습니다.

> **🎓 학술 노트 — 구성 표류의 측정**
>
> IaC 도입 뒤에도 어긋남이 생기는 이유를 조사한 연구들은 ① 장애 대응 중의 수동 수정, ② 콘솔 · 다른 도구가 만든 자원, ③ 클라우드 서비스가 **스스로** 바꾸는 속성(기본값 변경 등)을 꼽습니다. Guerriero 외의 *Adoption, Support, and Challenges of Infrastructure-as-Code: Insights from Industry*(ICSME 2019)는 실무자 인터뷰에서 **drift**와 **state 관리**를 IaC의 가장 큰 어려움으로 보고했습니다. 오늘의 refresh-only · import · removed가 그 어려움을 다루는 도구들입니다.

> **📈 트렌드 2026 — drift를 자동으로**
>
> HCP Terraform · Spacelift · env0 같은 플랫폼은 **정기 drift 감지 + 알림**을 기본 기능으로 제공하고, Terraform 1.14+의 `terraform query`는 계정의 기존 자원을 목록으로 찾아 import 블록을 한꺼번에 만들게 합니다. "콘솔로 만든 계정을 코드로 옮기기"(brownfield 이전)가 IaC 도입의 큰 시장이 되었습니다.

> **✅ 확인 문제**
>
> 1. plan이 콘솔의 손 수정을 알아챈 방법은?
> 2. Terraform과 Argo CD의 어긋남 처리 차이는?
> 3. import 블록과 `-generate-config-out`이 해 준 일은?
> 4. removed 블록에서 `destroy = false`의 뜻은?
>
> <details><summary>정답</summary>
>
> 1. plan 전에 새로 고침(refresh)으로 실제 AWS를 읽어 코드와 비교했다
> 2. Argo CD는 계속 비교하고 selfHeal로 바로 되돌리고, Terraform은 plan · apply를 실행할 때만 비교 · 되돌린다
> 3. 기존 자원을 장부에 올리고, 그 자원의 현재 설정으로 코드를 써 주었다
> 4. 장부에서만 빼고 AWS의 실제 자원은 지우지 않는다
>
> </details>

## 참고 문헌

- HashiCorp. *State*, *Refresh-only mode*, *Import — import block, generating configuration*, *removed block*. developer.hashicorp.com/terraform
- Guerriero, M. 외 (2019). *Adoption, Support, and Challenges of Infrastructure-as-Code: Insights from Industry*. ICSME 2019.
