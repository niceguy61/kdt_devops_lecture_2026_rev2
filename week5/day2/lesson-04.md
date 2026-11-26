<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [2일차](README.md) › 4/8교시</sub>

# 4교시 · 시작 템플릿과 Auto Scaling 그룹

> [!NOTE]
> **이번 시간에 할 일**
>
> - 손으로 띄운 서버를 **시작 템플릿**으로 굳힙니다.
> - **Auto Scaling 그룹**으로 "AZ 둘에 서버 2대"를 원하는 상태로 적습니다.
> - 손으로 만든 첫 서버는 지우고, 그룹이 만든 서버만 남깁니다.

## 시작 템플릿 = Pod 템플릿

| 시작 템플릿에 담는 것 | 오늘 값 | 3주차 Deployment에서 |
|---|---|---|
| AMI | Amazon Linux 2023 | 이미지 |
| 인스턴스 유형 | t3.micro | resources |
| 보안 그룹 | devmart-app-sg | (4주차 메시 정책) |
| IAM 인스턴스 프로파일 | devmart-ec2-role | serviceAccountName |
| user data | podinfo 띄우기 | command · env |
| **담지 않는 것: 서브넷** | (그룹이 정한다) | (스케줄러가 노드를 정한다) |

템플릿에는 **버전**이 붙습니다. 고치면 새 버전이 생기고, 그룹은 "최신" 또는 특정 버전을 씁니다 — 3주차 4일차의 ReplicaSet 리비전과 같은 생각입니다.

## 실습 6 · 실행 중인 서버에서 템플릿 만들기

EC2 → 인스턴스 → `devmart-web-1` 체크 → **작업** → **이미지 및 템플릿** → **인스턴스에서 템플릿 생성**

| 칸 | 값 |
|---|---|
| 시작 템플릿 이름 | `devmart-lt` |
| 템플릿 버전 설명 | `podinfo 6.14.0 on AL2023` |
| Auto Scaling 지침 | **체크** (그룹용으로 쓰기 좋은지 검사해 준다) |
| 네트워크 설정 → 서브넷 | **시작 템플릿에 포함하지 않음** |
| 고급 네트워크 구성 → 네트워크 인터페이스 1 | 퍼블릭 IP 자동 할당 **활성화**, 보안 그룹 `devmart-app-sg` |
| 고급 세부 정보 | IAM 인스턴스 프로파일 `devmart-ec2-role`, 사용자 데이터에 user-data.sh가 **그대로 들어 있는지** 확인 |

**시작 템플릿 생성**.

> [!TIP]
> **네트워크 설정이 겹친다는 경고**
>
> '방화벽(보안 그룹)'과 '네트워크 인터페이스'에 보안 그룹을 **둘 다** 넣으면 시작이 실패합니다. 네트워크 인터페이스를 쓰면 위쪽 방화벽 칸은 비워 둡니다 — Auto Scaling 지침이 이것을 짚어 줍니다.

```bash
aws ec2 describe-launch-templates --launch-template-names devmart-lt \
  --query 'LaunchTemplates[0].[LaunchTemplateId,LatestVersionNumber]' --output text
aws ec2 describe-launch-template-versions --launch-template-name devmart-lt --versions '$Latest' \
  --query 'LaunchTemplateVersions[0].LaunchTemplateData.{type:InstanceType,profile:IamInstanceProfile.Arn,publicIp:NetworkInterfaces[0].AssociatePublicIpAddress,userData:UserData}' --output yaml | sed 's/\(userData: .\{40\}\).*/\1…/'
```

> **🟢 확인: 확인**
>
> ```yaml
> lt-0a1b2c3d4e5f60718    1
> profile: arn:aws:iam::123456789012:instance-profile/devmart-ec2-role
> publicIp: true
> type: t3.micro
> userData: IyEvYmluL2Jhc2gKIyBFQzLqsIAg7LKY7J2MIOy…
> ```
> user data는 **base64**로 저장됩니다(3주차 Secret과 같은 인코딩 — 암호화가 아니다). 그래서 user data에 비밀번호를 넣으면 안 됩니다.

## 실습 7 · Auto Scaling 그룹

EC2 → 왼쪽 맨 아래 **Auto Scaling 그룹** → **Auto Scaling 그룹 생성**

| 단계 | 칸 | 값 |
|---|---|---|
| 1 | 이름 · 시작 템플릿 | `devmart-asg` · `devmart-lt`, 버전 **Latest** |
| 2 | VPC · 가용 영역 및 서브넷 | `devmart-vpc` · `…public1-ap-northeast-2a`, `…public2-ap-northeast-2c` |
| 3 | 로드 밸런싱 | **로드 밸런서 없음** (5교시에 붙인다) |
| 3 | 상태 확인 | EC2 (기본값, 5교시에 ELB를 더한다) |
| 4 | 그룹 크기 | 원하는 용량 **2**, 최소 **1**, 최대 **3** |
| 4 | 크기 조정 정책 | **없음** (6교시에 손으로 바꾼다) |
| 6 | 태그 | `Name` = `devmart-asg-node` (**새 인스턴스에 태그 지정** 체크) |

**Auto Scaling 그룹 생성**.

```bash
sleep 90
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names devmart-asg \
  --query 'AutoScalingGroups[0].{desired:DesiredCapacity,instances:Instances[].[InstanceId,AvailabilityZone,LifecycleState,HealthStatus]}' --output yaml
```

> **🟢 확인: 확인**
>
> ```yaml
> desired: 2
> instances:
> - - i-0b2c3d4e5f6071829
>   - ap-northeast-2a
>   - InService
>   - Healthy
> - - i-0c3d4e5f607182930
>   - ap-northeast-2c
>   - InService
>   - Healthy
> ```
> **AZ 둘에 하나씩** 흩어졌습니다. 그룹은 서브넷이 여럿이면 AZ 사이에 고르게 나눕니다 — 한 AZ가 멈춰도 한 대는 남습니다(1일차 5교시).

## 실습 8 · 손으로 만든 서버 지우기

`devmart-web-1`은 그룹이 모르는 서버입니다. 템플릿을 만들었으니 더는 필요 없습니다.

```bash
ID1=$(aws ec2 describe-instances --filters Name=tag:Name,Values=devmart-web-1 Name=instance-state-name,Values=running --query 'Reservations[0].Instances[0].InstanceId' --output text)
aws ec2 terminate-instances --instance-ids $ID1 --query 'TerminatingInstances[0].CurrentState.Name'
```

> **🟢 확인: 확인**
>
> `"shutting-down"` — 몇 분 뒤 **종료됨**. 그룹의 서버 둘은 그대로입니다. 그룹은 **자기가 만든 것만** 셉니다 — 4주차 Argo CD가 추적 표시가 붙은 것만 관리한 것과 같습니다.

> [!IMPORTANT]
> **Auto Scaling 그룹의 두 가지 일**
>
> ① **수를 맞춘다** — 원하는 용량과 실제 서버 수가 다르면 만들거나 지운다(6교시). ② **건강하지 않은 것을 바꾼다** — 상태 검사에 실패한 서버를 종료하고 새로 만든다(6교시). '고친다'가 아니라 '**바꾼다**'입니다 — 2교시 학술 노트의 불변 인프라.

> **❓ 오해 — Auto Scaling은 트래픽이 늘 때만 쓴다**
>
> 이름 때문에 '자동 확장'만 떠올리지만, 실무에서 가장 많이 쓰는 이유는 **원하는 수 유지와 자동 교체**입니다. 최소 = 최대 = 원하는 수 = 2로 두어도 그룹은 가치가 있습니다. 서버가 죽으면 사람이 깨지 않아도 다시 2대가 됩니다.

> **🎓 학술 노트 — 오토스케일링의 제어 이론**
>
> 부하에 따라 서버 수를 조절하는 문제는 제어 이론의 **피드백 제어**로 연구되어 왔습니다. Lorido-Botran 외의 *A Review of Auto-scaling Techniques for Elastic Applications in Cloud Environments*(J. Grid Computing, 2014)는 방법을 ① 정해진 규칙(임계값), ② 강화 학습, ③ 큐잉 이론, ④ 제어 이론, ⑤ 시계열 예측으로 분류했습니다. AWS의 **대상 추적 정책**(예: "평균 CPU 50% 유지")은 ④의 단순한 형태이고, **예측 조정**(predictive scaling)은 ⑤입니다.

> **📈 트렌드 2026 — 시작 템플릿 대신 '의도'를**
>
> EC2 인스턴스 유형을 하나로 고르지 않고 "vCPU 2개 · 메모리 4GB 이상"처럼 **속성으로** 고르게 하는 속성 기반 선택(attribute-based instance type selection)과, 여러 유형 · 스팟을 섞는 혼합 인스턴스 정책이 표준이 되었습니다. Kubernetes 쪽에서는 Karpenter가 같은 일을 Pod 요구에 맞춰 합니다(4일차 트렌드).

> **✅ 확인 문제**
>
> 1. 시작 템플릿에 서브넷을 넣지 않은 이유는?
> 2. user data에 비밀번호를 넣으면 안 되는 이유는?
> 3. 그룹이 서버를 AZ 둘에 나눈 이유는?
> 4. 손으로 만든 devmart-web-1을 지웠는데 그룹이 새 서버를 만들지 않은 이유는?
>
> <details><summary>정답</summary>
>
> 1. 어느 서브넷(AZ)에 둘지는 Auto Scaling 그룹이 정하게 하려고
> 2. base64로 저장될 뿐 암호화가 아니라, 템플릿을 볼 수 있는 누구나 읽을 수 있다
> 3. 한 AZ가 멈춰도 다른 AZ의 서버가 남도록
> 4. 그룹은 자기가 만든 인스턴스만 세기 때문
>
> </details>

## 참고 문헌

- AWS Docs. *Create a launch template from an existing instance*, *Auto Scaling groups*. docs.aws.amazon.com/autoscaling
- Lorido-Botran, T., Miguel-Alonso, J. & Lozano, J. A. (2014). *A Review of Auto-scaling Techniques for Elastic Applications in Cloud Environments*. Journal of Grid Computing 12(4).

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [3교시 · Session Manager · 메타데이터 · S3](lesson-03.md) | [⬆️ 2일차 목차](README.md) | [5교시 · 대상 그룹과 ALB](lesson-05.md) ➡️ |
