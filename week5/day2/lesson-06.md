<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [2일차](README.md) › 6/7교시</sub>

# 6교시 · 장애와 교체 · 늘리기

> [!NOTE]
> **이번 시간에 할 일**
>
> - 서버 하나를 **종료**하고, 손님이 무엇을 보는지와 교체되기까지의 시간을 잽니다.
> - 서버는 살아 있지만 **앱만 죽은** 경우를 만들어, ELB 상태 검사가 서버를 바꾸는 것을 봅니다.
> - 원하는 용량을 바꿔 **늘리고 줄입니다.**
> - Kubernetes와 **속도**를 비교합니다.

## 손님 흉내 — 계속 켜 둔다

```bash
DNS=$(aws elbv2 describe-load-balancers --names devmart-alb --query 'LoadBalancers[0].DNSName' --output text)
while true; do
  printf '%s %s %s\n' "$(date +%T)" "$(curl -s -m 2 -o /tmp/r -w '%{http_code}' http://$DNS/)" "$(grep -o '"hostname": "[^"]*"' /tmp/r)"
  sleep 1
done
```

## 실습 12 · 서버 하나를 종료

다른 터미널에서:

```bash
VICTIM=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names devmart-asg --query 'AutoScalingGroups[0].Instances[0].InstanceId' --output text)
date +%T; aws ec2 terminate-instances --instance-ids $VICTIM --query 'TerminatingInstances[0].CurrentState.Name'
watch -n 10 "aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names devmart-asg --query 'AutoScalingGroups[0].Instances[].[InstanceId,AvailabilityZone,LifecycleState,HealthStatus]' --output text"
```

> **🟢 확인: 확인 — 손님 터미널**
>
> ```text
> 11:52:10 200 "hostname": "a1b2c3d4e5f6"
> 11:52:11 200 "hostname": "f6e5d4c3b2a1"
> 11:52:12 502
> 11:52:13 200 "hostname": "f6e5d4c3b2a1"
> 11:52:14 200 "hostname": "f6e5d4c3b2a1"
> …(한동안 한 서버만)…
> 11:54:40 200 "hostname": "0c9d8e7f6a5b"     ← 새 서버
> ```
> - 종료 순간 **한두 번 502**가 날 수 있습니다 — 종료되는 서버로 가던 요청입니다. ALB가 그 서버를 빼기까지 상태 검사 2회(약 20초)가 걸리지만, 종료가 시작되면 그룹이 대상 그룹에서 먼저 빼므로 대개 짧습니다.
> - 남은 서버 하나가 모든 요청을 받습니다.
> - **2~3분 뒤** 새 서버(새 hostname)가 합류합니다.

> **🟢 확인: 확인 — watch 터미널**
>
> ```text
> i-0b2c…  ap-northeast-2a  Terminating  Healthy
> i-0c3d…  ap-northeast-2c  InService    Healthy
> …
> i-0c3d…  ap-northeast-2c  InService    Healthy
> i-0d4e…  ap-northeast-2a  Pending      Healthy
> …
> i-0d4e…  ap-northeast-2a  InService    Healthy
> ```
> 새 서버는 **죽은 서버와 같은 AZ(2a)**에 생겼습니다 — 그룹이 AZ 균형을 다시 맞췄습니다. `Ctrl+C`로 watch를 멈춥니다.

| | 3주차 Kubernetes (Pod 지우기) | 오늘 (서버 종료) |
|---|---|---|
| 알아채기 | 즉시 (watch) | 수십 초 (EC2 상태 · ELB 상태 검사) |
| 새것이 준비될 때까지 | **몇 초** | **2~3분** — 부팅 + user data(Docker 설치 + 이미지 받기) + 상태 검사 2회 |
| 그동안 | 남은 Pod가 받는다 | 남은 서버가 받는다 |

교체가 느린 만큼, **여유 대수**(원하는 수 2 이상)가 중요합니다. 그리고 부팅 시간을 줄이려면 Docker · 이미지를 미리 넣은 **나만의 AMI**를 굽습니다(Packer, EC2 Image Builder) — 2주차에 이미지를 미리 빌드한 것과 같은 이유입니다.

## 실습 13 · 앱만 죽었을 때

서버는 살아 있는데 앱(podinfo)만 멈춘 상황입니다. EC2 상태 검사는 이것을 모릅니다.

EC2 → Auto Scaling 그룹의 인스턴스 하나 → **연결** → Session Manager:

```bash
sudo docker update --restart=no podinfo && sudo docker stop podinfo
```

노트북 터미널:

```bash
TG=$(aws elbv2 describe-target-groups --names devmart-tg --query 'TargetGroups[0].TargetGroupArn' --output text)
for i in $(seq 12); do date +%T; aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State]' --output text; sleep 15; done
```

> **🟢 확인: 확인**
>
> ```text
> 11:58:00
> i-0c3d…  healthy
> i-0d4e…  healthy
> 11:58:30
> i-0c3d…  healthy
> i-0d4e…  unhealthy          ← /healthz 실패 2회
> 11:59:15
> i-0c3d…  healthy
> i-0d4e…  draining           ← 그룹이 '건강하지 않음'으로 보고 교체 시작
> …
> 12:01:30
> i-0c3d…  healthy
> i-0e5f…  healthy            ← 새 서버
> ```
> - ALB는 실패 2회(약 20초) 만에 그 서버로 **보내기를 멈췄고**, 손님은 거의 오류를 보지 않습니다.
> - 그룹은 **ELB 상태 확인**(5교시에 켠 것) 덕분에 "EC2는 살아 있지만 앱이 죽은" 서버를 **교체**했습니다. 이것을 켜지 않았다면 죽은 앱이 든 서버가 계속 남아 원하는 수 2 중 하나는 쓸모없었을 것입니다.

> [!IMPORTANT]
> **probe와 상태 검사**
>
> | Kubernetes (3주차 5일차) | AWS |
> |---|---|
> | readiness 실패 → Service에서 빠진다 | 대상 그룹 상태 검사 실패 → ALB가 안 보낸다 |
> | liveness 실패 → 컨테이너 재시작 | ASG의 ELB 상태 확인 → **서버 교체** |

## 실습 14 · 늘리고 줄이기

```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name devmart-asg --desired-capacity 3
sleep 150
aws elbv2 describe-target-health --target-group-arn $TG --query 'length(TargetHealthDescriptions[?TargetHealth.State==`healthy`])'
aws autoscaling set-desired-capacity --auto-scaling-group-name devmart-asg --desired-capacity 1
sleep 60
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names devmart-asg --query 'AutoScalingGroups[0].Instances[].LifecycleState' --output text
```

> **🟢 확인: 확인**
>
> ```text
> 3
> InService Terminating Terminating
> ```
> `kubectl scale --replicas=3`과 같은 일입니다. 줄일 때 그룹은 기본 규칙(AZ 균형 → 가장 오래된 템플릿 버전 → …)에 따라 종료할 서버를 고르고, 대상 그룹에서 먼저 빼(**draining**) 처리 중인 요청을 마치게 한 뒤 종료합니다.

> [!TIP]
> **자동으로 늘리려면**
>
> 그룹의 **자동 크기 조정** 탭에서 '대상 추적 정책'을 만들면 "평균 CPU 50%", "대상당 요청 수 100"처럼 **지표를 유지하도록** 그룹이 스스로 원하는 용량을 바꿉니다. 오늘은 손으로만 해 봅니다 — 지표를 만들려면 부하 테스트(4주차 2일차 k6)가 필요하고, 그만큼 서버 시간이 늘어나기 때문입니다.

> **❓ 오해 — 서버가 자동으로 바뀌니 데이터도 안전하다**
>
> 교체된 서버의 디스크는 **사라집니다**(종료와 함께 EBS 루트 볼륨이 지워지는 것이 기본). 서버에 저장하던 파일 · 세션은 함께 없어집니다. 그래서 상태는 서버 밖 — S3 · RDS · ElastiCache — 에 둡니다. 3주차 1일차 12-Factor의 "**프로세스는 상태가 없다**"가 클라우드에서 실제 요구가 되는 순간입니다. 5일차 EKS의 db Pod에서 이 문제를 다시 만납니다.

> **🎓 학술 노트 — 가축과 애완동물**
>
> 서버를 이름 붙여 정성껏 돌보는 '**애완동물**'(pets)이 아니라 번호로 관리하고 아프면 바꾸는 '**가축**'(cattle)으로 다루라는 비유는 Bill Baker(Microsoft)의 발표에서 시작되어 Randy Bias(2012)가 클라우드 맥락으로 널리 퍼뜨렸습니다. 오늘 서버의 이름은 `i-0d4e…` 같은 번호이고, 죽으면 바뀝니다. 이 비유는 Kubernetes의 Pod로 한 번 더 작아졌습니다.

> **📈 트렌드 2026 — 인스턴스 새로 고침과 웜 풀**
>
> 서버가 늦게 뜨는 문제를 줄이려고, 미리 띄워 멈춰 둔 서버를 붙이는 **웜 풀**(warm pool)과, 템플릿이 바뀌면 서버를 조금씩 바꿔 끼우는 **인스턴스 새로 고침**(instance refresh, 3주차 롤링 업데이트의 VM판)이 널리 쓰입니다. 한편 '서버 교체 속도' 자체가 문제가 되는 서비스는 컨테이너 · Kubernetes로 옮겨 가는 이유가 되기도 합니다.

> **✅ 확인 문제**
>
> 1. 서버를 종료했을 때 새 서버가 준비되기까지 Pod보다 오래 걸린 이유는?
> 2. ELB 상태 확인을 켜지 않았다면 실습 13은 어떻게 되었을까요?
> 3. probe와 AWS 상태 검사를 짝지으면?
> 4. 교체되는 서버에 데이터를 두면 안 되는 이유는?
>
> <details><summary>정답</summary>
>
> 1. 부팅 + user data(Docker 설치 · 이미지 받기) + 상태 검사 통과까지 시간이 걸리기 때문
> 2. ALB는 그 서버로 보내지 않지만 그룹은 EC2가 살아 있으니 교체하지 않아, 쓸모없는 서버가 남는다
> 3. readiness = 대상 그룹 상태 검사, liveness(재시작) = ASG ELB 상태 확인(교체)
> 4. 교체될 때 루트 디스크와 함께 사라지기 때문 — 상태는 S3 · RDS 등 서버 밖에
>
> </details>

## 참고 문헌

- AWS Docs. *Health checks for instances in an Auto Scaling group*, *Set deregistration delay*. docs.aws.amazon.com
- AWS Docs. *Warm pools*, *Instance refresh*. docs.aws.amazon.com/autoscaling
- Bias, R. (2012). *Architectures for open and scalable clouds* (pets vs cattle). CloudScaling.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [5교시 · 대상 그룹과 ALB](lesson-05.md) | [⬆️ 2일차 목차](README.md) | [7교시 · 지우는 순서 + 비용 점검](lesson-07.md) ➡️ |
