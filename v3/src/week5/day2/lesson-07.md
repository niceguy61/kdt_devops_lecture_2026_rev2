# 7교시 · CloudWatch — 지표 · 알람 · 대시보드로 서버 무리 보기

!!! goal "이번 시간에 할 일"
    - AWS가 **설치 없이** 모아 두는 지표(ALB · 대상 그룹 · EC2 · ASG)를 CLI로 꺼내 봅니다.
    - "건강하지 않은 서버가 생기면 **메일**로 알려라" 알람을 만들고, 6교시의 '앱만 죽었을 때'를 다시 일으켜 **실제로 울려** 봅니다.
    - 지표 네 개를 담은 **대시보드**를 코드(JSON)로 만듭니다.
    - 4주차의 Prometheus · Grafana · Alertmanager가 AWS에서는 무엇인지 짝을 맞춥니다.

!!! key "4주차 2일차를 클라우드에서"
    kind에서는 Prometheus를 **직접 설치**해서 지표를 긁었습니다. AWS의 관리형 서비스(ALB · EC2 · ASG)는 **스스로 지표를 CloudWatch에 보냅니다.** 우리가 할 일은 무엇을 볼지, 언제 깨울지를 정하는 것뿐입니다.

    | 4주차 (kind) | AWS |
    |---|---|
    | Prometheus — 지표 저장 · PromQL | **CloudWatch 지표** — 네임스페이스 · 차원 · 통계 |
    | Alertmanager — 규칙 → 사람에게 | **CloudWatch 알람** → **SNS** → 메일 · 슬랙 |
    | Grafana — 대시보드 | **CloudWatch 대시보드** (Grafana도 연결 가능) |
    | Loki — 로그 | **CloudWatch Logs** (에이전트가 보냄 — 내일 · 4일차) |

## 실습 15 · 지표 꺼내 보기

6교시의 손님 흉내 반복문이 다른 터미널에서 아직 돌고 있으면 그대로 둡니다(요청 수가 쌓입니다). 멈췄다면 다시 켭니다. 서버는 둘로 맞춥니다.

```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name devmart-asg --desired-capacity 2
ALB_ARN=$(aws elbv2 describe-load-balancers --names devmart-alb --query 'LoadBalancers[0].LoadBalancerArn' --output text)
TG_ARN=$(aws elbv2 describe-target-groups --names devmart-tg --query 'TargetGroups[0].TargetGroupArn' --output text)
LB_DIM=${ALB_ARN#*:loadbalancer/}          # app/devmart-alb/1a2b3c…
TG_DIM=${TG_ARN##*:}                       # targetgroup/devmart-tg/4d5e6f…
echo $LB_DIM $TG_DIM
```

- 지표는 **네임스페이스**(`AWS/ApplicationELB`) · **이름**(`RequestCount`) · **차원**(어느 ALB, 어느 대상 그룹)으로 찾습니다. 4주차 PromQL의 `{label="…"}`이 차원입니다
- `${ALB_ARN#*:loadbalancer/}` : 3주차 2일차 8교시의 `${IMAGE%:*}`와 같은 셸 잘라 내기 — ARN에서 **차원 값**만 남긴다

```bash
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB --metric-name RequestCount \
  --dimensions Name=LoadBalancer,Value=$LB_DIM \
  --start-time "$(date -u -d '-30 minutes' +%FT%TZ)" --end-time "$(date -u +%FT%TZ)" \
  --period 300 --statistics Sum --query 'sort_by(Datapoints,&Timestamp)[].[Timestamp,Sum]' --output text
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB --metric-name HealthyHostCount \
  --dimensions Name=LoadBalancer,Value=$LB_DIM Name=TargetGroup,Value=$TG_DIM \
  --start-time "$(date -u -d '-10 minutes' +%FT%TZ)" --end-time "$(date -u +%FT%TZ)" \
  --period 60 --statistics Minimum --query 'sort_by(Datapoints,&Timestamp)[-1].Minimum'
```

Mac은 `date -u -v-30M +%FT%TZ`처럼 바꿉니다.

!!! check "보이는 것 (숫자는 다름)"
    ```text
    2026-12-01T05:35:00+00:00  288.0
    2026-12-01T05:40:00+00:00  300.0
    2026-12-01T05:45:00+00:00  297.0
    2.0
    ```
    5분마다 약 300건 — 손님 흉내가 1초에 한 번이니 맞습니다. 건강한 서버 2대. **아무것도 설치하지 않았는데** 이미 모이고 있었습니다.

| 지표 (AWS/ApplicationELB) | 4주차에 무엇과 같나 |
|---|---|
| `RequestCount` | `rate(envoy_…_rq_total)` — 요청 수 |
| `HTTPCode_Target_5XX_Count` | 5xx 비율의 분자 — 오류 |
| `TargetResponseTime` (p95) | 지연 분위수 — 4주차 2일차의 p95 · p99 |
| `HealthyHostCount` · `UnHealthyHostCount` | 준비된 Pod 수(readiness) |

요청 수 · 오류 · 지연 — 4주차의 **RED**가 그대로 있습니다.

## 실습 16 · 알람 — 메일로 깨우기

### 단계 1 — 받을 곳(SNS 주제)

```bash
TOPIC=$(aws sns create-topic --name devmart-alerts --tags Key=Project,Value=devmart Key=Env,Value=lab \
  --query TopicArn --output text)
aws sns subscribe --topic-arn $TOPIC --protocol email --notification-endpoint 내메일@example.com
```

메일함에 **AWS Notification - Subscription Confirmation**이 옵니다. 메일의 **Confirm subscription**을 누릅니다.

```bash
aws sns list-subscriptions-by-topic --topic-arn $TOPIC --query 'Subscriptions[].SubscriptionArn' --output text
```

`PendingConfirmation`이 아니라 ARN이 보이면 확인된 것입니다.

### 단계 2 — 알람 만들기

```bash
aws cloudwatch put-metric-alarm --alarm-name devmart-unhealthy-hosts \
  --alarm-description "DevMart 대상 그룹에 건강하지 않은 서버가 있다 — 6교시 런북 참고" \
  --namespace AWS/ApplicationELB --metric-name UnHealthyHostCount \
  --dimensions Name=LoadBalancer,Value=$LB_DIM Name=TargetGroup,Value=$TG_DIM \
  --statistic Maximum --period 60 --evaluation-periods 1 \
  --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold \
  --treat-missing-data notBreaching \
  --alarm-actions $TOPIC --ok-actions $TOPIC \
  --tags Key=Project,Value=devmart Key=Env,Value=lab
aws cloudwatch describe-alarms --alarm-names devmart-unhealthy-hosts --query 'MetricAlarms[0].StateValue'
```

| 옵션 | 뜻 | 4주차 2일차 6교시 |
|---|---|---|
| `--period 60 --evaluation-periods 1` | 1분 동안의 값을 1번 보고 판단 | `for: 1m` |
| `--threshold 1 … GreaterThanOrEqual` | 1대라도 아프면 | `expr: … >= 1` |
| `--treat-missing-data notBreaching` | 데이터가 없으면 정상으로 본다 | — |
| `--ok-actions` | 회복했을 때도 알린다 | `send_resolved: true` |
| `--alarm-description` | 메일에 실린다 — **무엇을 할지**를 적는다 | 런북 링크 |

!!! check "처음 상태"
    ```text
    "INSUFFICIENT_DATA"
    ```
    1~2분 뒤 `OK`가 됩니다.

### 단계 3 — 울려 보기

6교시 실습 13을 **CLI로** 다시 합니다. 이번에는 Session Manager 화면 대신 **Run Command**로 서버 한 대에 명령을 보냅니다.

```bash
ONE=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names devmart-asg \
  --query 'AutoScalingGroups[0].Instances[0].InstanceId' --output text)
aws ssm send-command --instance-ids $ONE --document-name AWS-RunShellScript \
  --parameters 'commands=["docker update --restart=no podinfo","docker stop podinfo"]' \
  --query 'Command.CommandId' --output text
for i in $(seq 10); do date +%T; aws cloudwatch describe-alarms --alarm-names devmart-unhealthy-hosts \
  --query 'MetricAlarms[0].StateValue' --output text; sleep 30; done
```

!!! check "이렇게 바뀝니다"
    ```text
    06:02:10  OK
    06:02:40  OK
    06:03:10  ALARM          ← 메일 도착: "ALARM: devmart-unhealthy-hosts …"
    …
    06:06:40  OK             ← 그룹이 서버를 교체 · 회복 메일 도착
    ```
    메일 본문에 `--alarm-description`의 문장이 실려 옵니다. **새벽 3시에 이 메일을 받은 사람**이 무엇을 해야 할지 알 수 있게 쓰는 것이 4주차 2일차 7교시의 런북 원칙입니다.

!!! tip "Run Command가 Session Manager보다 나은 점"
    한 번에 **여러 서버**(태그로 고르기)에 같은 명령을 보내고, 누가 무엇을 보냈는지가 **CloudTrail과 SSM 기록**에 남습니다(어제 8교시). SSH 열쇠도 22번 포트도 필요 없습니다.

## 실습 17 · 대시보드를 코드로

```bash
mkdir -p ~/devops-lab/aws/w5d2 && cd ~/devops-lab/aws/w5d2
cat > dashboard.json <<EOF
{
  "widgets": [
    {"type":"metric","x":0,"y":0,"width":12,"height":6,"properties":{"title":"요청 수 (5분 합)","region":"ap-northeast-2","stat":"Sum","period":300,
      "metrics":[["AWS/ApplicationELB","RequestCount","LoadBalancer","$LB_DIM"]]}},
    {"type":"metric","x":12,"y":0,"width":12,"height":6,"properties":{"title":"5xx (대상)","region":"ap-northeast-2","stat":"Sum","period":60,
      "metrics":[["AWS/ApplicationELB","HTTPCode_Target_5XX_Count","LoadBalancer","$LB_DIM"]]}},
    {"type":"metric","x":0,"y":6,"width":12,"height":6,"properties":{"title":"응답 시간 p95","region":"ap-northeast-2","stat":"p95","period":60,
      "metrics":[["AWS/ApplicationELB","TargetResponseTime","LoadBalancer","$LB_DIM"]]}},
    {"type":"metric","x":12,"y":6,"width":12,"height":6,"properties":{"title":"건강한 / 아픈 서버","region":"ap-northeast-2","stat":"Minimum","period":60,
      "metrics":[["AWS/ApplicationELB","HealthyHostCount","LoadBalancer","$LB_DIM","TargetGroup","$TG_DIM"],
                 ["AWS/ApplicationELB","UnHealthyHostCount","LoadBalancer","$LB_DIM","TargetGroup","$TG_DIM"]]}}
  ]
}
EOF
aws cloudwatch put-dashboard --dashboard-name devmart --dashboard-body file://dashboard.json
```

!!! check "이렇게 나오면 성공"
    ```text
    {
        "DashboardValidationMessages": []
    }
    ```
    콘솔 **CloudWatch → 대시보드 → devmart**에서 네 그래프가 보입니다. 방금의 알람 때 아픈 서버 그래프가 1로 솟았다 내려온 것이 보입니다. 4주차 2일차 4교시처럼 **대시보드도 파일**로 두면, 내일 Terraform으로 옮기기 쉽습니다.

!!! warn "무료 한도 안에서"
    대시보드는 계정당 3개, 표준 알람은 10개, SNS 메일은 월 1,000건까지 무료입니다(프리 플랜 기준). 오늘 것은 모두 그 안입니다. 그래도 8교시에 **함께 지웁니다** — 알람이 지워진 대상 그룹을 계속 보며 `INSUFFICIENT_DATA`로 남는 것을 막으려고.

!!! academic "학술 노트 — 무엇을 알람으로 만들 것인가"
    구글 SRE의 **롭 이워쇽(Rob Ewaschuk)**은 「My Philosophy on Alerting」(2013, 이후 『Site Reliability Engineering』 6장)에서, 사람을 깨우는 알람은 **"사용자가 지금 아프다"는 증상**이어야 하고, 원인(CPU 높음 · 디스크 70%)이 아니어야 한다고 했습니다. 원인 알람은 사용자에게 아무 일이 없어도 울려서 **알람 피로**를 만들고, 결국 진짜 알람도 무시하게 만든다는 것입니다. 오늘 고른 `UnHealthyHostCount`는 "손님이 아픈 서버로 갈 수 있다"에 가까운 증상이고, 더 좋은 알람은 대시보드의 **5xx 비율 · p95 지연**처럼 손님이 직접 느끼는 숫자입니다.

    - Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.). (2016). *Site Reliability Engineering*. O'Reilly. — 6장 Monitoring Distributed Systems (Ewaschuk).

!!! trend "트렌드 — 관리형 Prometheus · Grafana와 OpenTelemetry"
    CloudWatch만 쓰는 회사도 있지만, 4주차의 PromQL · Grafana 대시보드를 그대로 가져가려는 회사가 많습니다. AWS는 **Amazon Managed Service for Prometheus**와 **Amazon Managed Grafana**를 제공하고, CloudWatch 자체도 **OpenTelemetry**로 지표 · 로그 · 트레이스를 받는 쪽으로 넓히고 있습니다. 4일차의 EKS에서는 metrics-server와 함께 이 선택지를 다시 봅니다. 도구 이름은 달라도 **RED · 증상 알람 · 대시보드는 파일로**라는 원칙은 그대로입니다.

## 정리

- AWS 관리형 서비스는 지표를 **스스로** CloudWatch에 보냅니다. 네임스페이스 · 이름 · **차원**으로 찾습니다.
- **알람 → SNS → 메일**: 기간 · 횟수 · 임계값 · 빈 데이터 처리 · 회복 알림. 설명에는 **할 일**을 적습니다.
- Run Command로 서버에 명령을 보내면 SSH 없이 **기록이 남습니다**.
- 대시보드도 **JSON 파일**로. 알람은 원인보다 **증상**으로.

!!! quiz "확인 문제"
    1. CloudWatch 지표에서 4주차 PromQL의 라벨에 해당하는 것은?
    2. `--treat-missing-data notBreaching`이 없으면 어떤 일이 생길 수 있나요?
    3. 알람의 `--alarm-description`에는 무엇을 적어야 하나요?
    4. "CPU 80% 넘으면 깨워라"보다 "5xx 비율 1% 넘으면 깨워라"가 나은 이유는?
    5. 대상 그룹을 지운 뒤 알람을 남겨 두면 어떻게 되나요?

    ??? answer "정답"
        1. 차원(Dimensions) — 어느 ALB, 어느 대상 그룹
        2. 서버가 없거나 지표가 끊겼을 때 판단이 흔들려, 상황에 따라 엉뚱하게 울리거나 `INSUFFICIENT_DATA`에 머문다
        3. 받은 사람이 무엇을 해야 하는지 — 런북 링크나 첫 확인 명령
        4. 손님이 실제로 아픈 증상이라서 — CPU는 높아도 손님이 멀쩡할 수 있어 알람 피로를 만든다
        5. 볼 지표가 사라져 `INSUFFICIENT_DATA`로 남고, 쓸모없는 알람이 쌓인다

## 참고 문헌

- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.). (2016). *Site Reliability Engineering*. O'Reilly. — Ch. 6.
- Ewaschuk, R. (2013). *My Philosophy on Alerting*. Google.
- AWS Docs. *CloudWatch metrics for your Application Load Balancer*; *Using Amazon CloudWatch alarms*; *put-dashboard — Dashboard body structure*. docs.aws.amazon.com/AmazonCloudWatch
- AWS Docs. *Amazon SNS — Email notifications*; *AWS Systems Manager Run Command*. docs.aws.amazon.com
- AWS. *Amazon CloudWatch pricing — Free tier*. aws.amazon.com/cloudwatch/pricing
