<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [2일차](README.md) › 7/7교시</sub>

# 7교시 · 지우는 순서 + 비용 점검

> [!NOTE]
> **이번 시간에 할 일**
>
> - 오늘 만든 것을 **의존 순서대로** 지웁니다.
> - 지우는 순서가 왜 있는지 그림으로 이해합니다.
> - 남은 것과 오늘의 비용을 확인합니다.
> - 내일(Terraform)이 왜 필요한지 몸으로 느낍니다.

## 무엇이 무엇에 기대고 있나

| 자원 | 기대고 있는 것 | 먼저 지워야 할 것 |
|---|---|---|
| Auto Scaling 그룹 | 시작 템플릿, 대상 그룹, 서브넷 | — (먼저 지운다, 인스턴스도 함께) |
| ALB | 서브넷, web-sg | 리스너(함께 지워짐) |
| 대상 그룹 | VPC | ALB 리스너 · ASG 연결 |
| 시작 템플릿 | 역할 · 보안 그룹 | ASG |
| S3 버킷 | — | **안의 객체** (비어 있어야 지워진다) |
| (남김) VPC · 보안 그룹 · 역할 | | 무료 · 내일 쓴다 |

## 실습 15 · 지우기

```bash
cat ~/devops-lab/aws/w5d2/cleanup-checklist.md
```

콘솔로 해도 되고, CLI로 같은 순서를 밟아도 됩니다. 오늘은 **CLI**로 해 봅니다 — 명령이 곧 기록입니다.

```bash
# 1. Auto Scaling 그룹 — 인스턴스까지 강제 종료
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name devmart-asg --force-delete
# 2. ALB와 대상 그룹
ALB=$(aws elbv2 describe-load-balancers --names devmart-alb --query 'LoadBalancers[0].LoadBalancerArn' --output text)
aws elbv2 delete-load-balancer --load-balancer-arn $ALB
aws elbv2 wait load-balancers-deleted --load-balancer-arns $ALB
TG=$(aws elbv2 describe-target-groups --names devmart-tg --query 'TargetGroups[0].TargetGroupArn' --output text)
aws elbv2 delete-target-group --target-group-arn $TG
# 3. 시작 템플릿
aws ec2 delete-launch-template --launch-template-name devmart-lt --query 'LaunchTemplate.LaunchTemplateName'
# 4. S3 — 비우고 지운다
B=devmart-assets-$(gh api user -q .login | tr 'A-Z' 'a-z')
aws s3 rb s3://$B --force
```

> **🟢 확인: 확인**
>
> ```text
> "devmart-lt"
> delete: s3://devmart-assets-niceguy61/notice.txt
> remove_bucket: devmart-assets-niceguy61
> ```
> 대상 그룹 삭제에서 `ResourceInUse`가 나면 ALB가 아직 지워지는 중입니다 — `wait`가 끝난 뒤 다시 합니다.

몇 분 뒤 인스턴스가 모두 종료되었는지 확인합니다.

```bash
sleep 120
aws ec2 describe-instances --filters Name=instance-state-name,Values=pending,running,stopping,stopped \
  --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`]|[0].Value]' --output text
~/devops-lab/aws/w5d1/check-account.sh | tail -5
```

> **🟢 확인: 확인**
>
> 첫 명령은 **아무것도 출력하지 않습니다**(종료된 것만 남았다). `check-account.sh`의 "돈이 나가는 것" 세 줄도 비어 있습니다.

> [!WARNING]
> **종료됨(terminated)은 잠시 보인다**
>
> 종료된 인스턴스는 콘솔 목록에 **한 시간쯤** 회색으로 남았다가 사라집니다. 요금은 나가지 않습니다. 반대로 **중지됨(stopped)**은 인스턴스 요금은 멈추지만 디스크(EBS) 요금은 계속 나갑니다 — 실습 서버는 '중지'가 아니라 '**종료**'합니다.

## 오늘의 비용

**결제 및 비용 관리 → Cost Explorer**(처음 켜면 데이터가 하루 뒤부터 보인다) 또는 **청구서**에서 오늘 날짜의 EC2 · ELB · VPC(공인 IPv4) 항목을 봅니다.

| 오늘 쓴 것 | 대략 |
|---|---|
| EC2 t3.micro × 평균 2대 × 4시간 | $0.10 |
| 공인 IPv4 × 평균 4개(EC2 2 + ALB 2) × 4시간 | $0.08 |
| ALB × 4시간 + 사용량 | $0.10 |
| S3 · 데이터 전송 | ≈ 0 |
| 합계 | **약 $0.3** — 크레딧에서 |

ALB도 AZ마다 **공인 IP**를 가지므로 공인 IPv4 요금이 붙습니다. 1일차 5교시 트렌드에서 말한 "공인 IP 줄이기"가 이렇게 숫자로 보입니다.

## 오늘 클릭을 세어 보면

| 만들기 | 지우기 |
|---|---|
| 역할 · 인스턴스 · 템플릿 · 그룹 · 대상 그룹 · ALB · 버킷 — 화면 열 개 남짓, 칸 백 개 가까이 | 순서를 알아야 하는 명령 여섯 줄 |
| 내일 다시 만들려면 — **다시 전부** | 하나라도 빠뜨리면 — **계속 과금** |

이 두 칸이 내일 Terraform의 동기입니다. 내일은 오늘의 VPC를 **코드 몇십 줄**로 만들고, `terraform destroy` **한 줄**로 순서까지 알아서 지웁니다.

> **❓ 오해 — 콘솔에서 지우면 깔끔하다**
>
> 콘솔은 화면마다 따로 지우므로, ALB가 만든 네트워크 인터페이스 · 남은 EBS 볼륨 · 해제 안 한 탄력적 IP · 다른 리전에 만든 것을 놓치기 쉽습니다. 그래서 7교시마다 **CLI로 다시 확인**합니다. 마지막 날에는 리소스 탐색기(Resource Explorer)로 **모든 리전**을 훑습니다.

> **🎓 학술 노트 — 의존 그래프와 위상 정렬**
>
> "무엇을 먼저 지워야 하나"는 자원들 사이의 **의존 그래프**를 **위상 정렬**(topological sort, Kahn 1962)하는 문제입니다. 만들 때는 정렬 순서대로, 지울 때는 그 **역순**으로 하면 됩니다. Terraform은 코드에서 이 그래프를 자동으로 만들고(`terraform graph`) 정렬해 실행합니다 — 내일 직접 그래프를 그려 봅니다.

> **📈 트렌드 2026 — 남은 자원 찾기의 자동화**
>
> 클라우드 비용 사고의 큰 부분이 '잊힌 자원'이라, AWS는 **Resource Explorer**(계정 · 리전 전체 검색), **Cost Optimization Hub**(쓰지 않는 자원 추천)를 넓혔고, 실습 · 데모 환경에는 **만료 태그**(예: `expires=2026-12-01`)를 붙여 스케줄러가 자동으로 지우는 방식이 흔해졌습니다. 내일 Terraform으로 만드는 모든 자원에는 `Project` · `Owner` 태그가 자동으로 붙습니다.

> **✅ 확인 문제**
>
> 1. Auto Scaling 그룹을 먼저 지우는 이유는?
> 2. S3 버킷이 바로 지워지지 않는 이유와 `--force`가 하는 일은?
> 3. 실습 서버를 '중지'가 아니라 '종료'하는 이유는?
> 4. ALB도 공인 IPv4 요금이 붙는 이유는?
>
> <details><summary>정답</summary>
>
> 1. 그룹이 인스턴스를 다시 만들고, 템플릿 · 대상 그룹을 붙잡고 있기 때문
> 2. 버킷이 비어 있어야 지워진다. --force는 안의 객체를 먼저 지운다
> 3. 중지는 디스크(EBS) 요금이 계속 나가고, 종료는 디스크까지 지운다
> 4. 인터넷 경계 ALB는 AZ마다 공인 IPv4 주소를 갖기 때문
>
> </details>

> [!NOTE]
> **오늘의 배움일기**
>
> - 오늘 만든 것들을 3 · 4주차 Kubernetes의 무엇과 짝지었나 (최소 넷)
> - Session Manager로 들어간 서버에서 본 신원(assumed-role/…)과, 그것이 키 없이 S3를 읽은 원리
> - 서버를 종료했을 때: 502가 몇 번, 새 서버까지 몇 분? Pod와 비교하면?
> - 앱만 죽은 서버를 바꾼 것은 무엇이었나 — 그것을 켜지 않았다면?
> - 오늘 지운 순서와, 하나를 빠뜨렸다면 무엇이 계속 과금되었을지
> - 내일 전에 궁금한 것: 오늘 클릭 백 번을 **코드로 적어 두고**, 한 줄로 만들고 한 줄로 지울 수는 없을까? 그 코드가 실제 계정과 **어긋나면** 어떻게 알까?

## 참고 문헌

- AWS Docs. *Delete your Auto Scaling infrastructure*, *Delete an Application Load Balancer*, *Deleting a bucket*. docs.aws.amazon.com
- AWS Docs. *AWS Resource Explorer*, *Cost Optimization Hub*. docs.aws.amazon.com
- Kahn, A. B. (1962). *Topological sorting of large networks*. Communications of the ACM 5(11).

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · 장애와 교체 · 늘리기](lesson-06.md) | [⬆️ 2일차 목차](README.md) | [5주차 3일차 목차](../day3/README.md) ➡️ |
