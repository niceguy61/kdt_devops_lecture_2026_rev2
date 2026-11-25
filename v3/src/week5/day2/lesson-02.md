# 2교시 · 역할을 붙인 첫 EC2

!!! goal "이번 시간에 할 일"
    - EC2가 쓸 **IAM 역할**(`devmart-ec2-role`)을 만듭니다 — Session Manager 접속 + S3 읽기.
    - **인스턴스 시작** 마법사의 칸을 하나씩 이해하며 EC2를 띄웁니다.
    - **user data**로 서버가 켜질 때 podinfo가 자동으로 뜨게 합니다.
    - 오늘 서버를 **public 서브넷**에 두는 이유와 그 한계를 압니다.

## 실습 1 · EC2 역할

IAM → **역할** → **역할 생성**

1. 신뢰할 수 있는 엔터티 유형: **AWS 서비스**, 사용 사례: **EC2** → 다음
2. 권한 정책: `AmazonSSMManagedInstanceCore` 검색 · 체크 → 다음
3. 역할 이름 `devmart-ec2-role` → **역할 생성**

이어서 S3 정책을 더합니다. 1일차에 읽은 그 JSON입니다.

```bash
mkdir -p ~/devops-lab/aws/w5d2 && cp -r ~/course/labs/week5/day2/* ~/devops-lab/aws/w5d2/
ID=$(gh api user -q .login | tr 'A-Z' 'a-z'); echo $ID
sed "s/YOUR_ID/$ID/g" ~/devops-lab/aws/w5d1/s3-read-only-policy.json > ~/devops-lab/aws/w5d2/s3-policy.json
aws iam put-role-policy --role-name devmart-ec2-role --policy-name devmart-s3-read \
  --policy-document file://$HOME/devops-lab/aws/w5d2/s3-policy.json
aws iam get-role --role-name devmart-ec2-role --query 'Role.AssumeRolePolicyDocument.Statement[0].Principal'
aws iam list-instance-profiles-for-role --role-name devmart-ec2-role --query 'InstanceProfiles[].InstanceProfileName'
```

!!! check "확인"
    ```text
    niceguy61
    {
        "Service": "ec2.amazonaws.com"
    }
    [
        "devmart-ec2-role"
    ]
    ```
    - **신뢰 정책**의 Principal이 `ec2.amazonaws.com` — "EC2 서비스가 이 역할을 맡을 수 있다"(1일차 3교시).
    - 콘솔로 EC2용 역할을 만들면 같은 이름의 **인스턴스 프로파일**이 자동으로 생깁니다. 인스턴스 프로파일은 역할을 EC2에 **꽂는 어댑터**입니다.

## 실습 2 · 인스턴스 시작

EC2 → **인스턴스** → **인스턴스 시작**

| 칸 | 값 | 이유 |
|---|---|---|
| 이름 | `devmart-web-1` | |
| AMI | **Amazon Linux 2023** (기본값, 64비트 x86) | AWS가 관리하는 리눅스 — SSM 에이전트 · AWS CLI가 들어 있다 |
| 인스턴스 유형 | `t3.micro` (프리 티어 사용 가능 표시) | 2 vCPU 버스트 · 1 GiB |
| 키 페어 | **키 페어 없이 계속 진행** | SSH를 쓰지 않는다 (3교시 Session Manager) |
| 네트워크 설정 → **편집** | VPC `devmart-vpc`, 서브넷 `devmart-subnet-public1-ap-northeast-2a` | |
| 퍼블릭 IP 자동 할당 | **활성화** | 아래 '왜 public인가' |
| 방화벽(보안 그룹) | **기존 보안 그룹 선택** → `devmart-app-sg` | 22번 포트 없음 |
| 스토리지 | 기본값 (8 GiB gp3) | |
| 고급 세부 정보 → **IAM 인스턴스 프로파일** | `devmart-ec2-role` | |
| 고급 세부 정보 → 메타데이터 버전 | **V2만(토큰 필수)** (기본값 확인) | 3교시 |
| 고급 세부 정보 → **사용자 데이터** | `user-data.sh` 내용을 붙여 넣기 | 아래 |

```bash
cat ~/devops-lab/aws/w5d2/user-data.sh
```

```bash
#!/bin/bash
set -euxo pipefail
dnf install -y docker
systemctl enable --now docker
docker run -d --name podinfo --restart always -p 9898:9898 \
  -e PODINFO_UI_MESSAGE="DevMart on EC2" \
  ghcr.io/stefanprodan/podinfo:6.14.0
```

오른쪽 **요약**에서 인스턴스 1개 · t3.micro를 확인하고 **인스턴스 시작**.

!!! check "확인 (2~3분)"
    인스턴스 목록에서 `devmart-web-1`이 **실행 중**, 상태 검사 **3/3 검사 통과**(또는 2/2)가 됩니다.
    ```bash
    aws ec2 describe-instances --filters Name=tag:Name,Values=devmart-web-1 Name=instance-state-name,Values=running \
      --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,PublicIpAddress,Placement.AvailabilityZone,IamInstanceProfile.Arn]' --output table
    ```
    ```text
    | i-0a1b2c3d4e5f60718 | 10.0.5.183 | 3.38.○.○ | ap-northeast-2a | arn:aws:iam::…:instance-profile/devmart-ec2-role |
    ```

!!! term "user data"
    인스턴스가 **처음 켜질 때 한 번** root로 실행되는 스크립트입니다. 2주차의 Dockerfile `RUN`, 3주차의 컨테이너 `command`처럼 "켜지면 할 일"을 적어 둡니다. 로그는 서버 안 `/var/log/cloud-init-output.log`에 남습니다(3교시). 이 스크립트를 쓰는 것이 4교시 **시작 템플릿**의 핵심이 됩니다 — 손으로 설정한 서버는 다시 만들 수 없지만, user data로 설정한 서버는 몇 대든 똑같이 만들 수 있습니다.

## 왜 오늘은 public 서브넷인가

1일차에 "앱은 private에"라고 했습니다. 그런데 오늘 서버는 public 서브넷에 공인 IP를 받았습니다.

| private에 두려면 필요한 것 | 비용 |
|---|---|
| Docker 설치 · 이미지 받기 → **밖으로 나가는 길** = NAT 게이트웨이 | 시간당 약 $0.059 |
| Session Manager → SSM용 **VPC 엔드포인트** 셋 | 엔드포인트당 시간당 약 $0.013 × AZ |

하루 실습에 NAT를 켜는 대신, 오늘은 **public 서브넷 + 공인 IP + 보안 그룹으로 막기**로 갑니다. 들어오는 것은 `devmart-app-sg`가 막습니다(9898은 web-sg에서만, 22는 없음). 4일차 EKS에서는 NAT를 만들고 노드를 **private**에 둡니다. 이 차이를 기억해 두세요 — 실무의 기본은 private입니다.

```bash
PUB=$(aws ec2 describe-instances --filters Name=tag:Name,Values=devmart-web-1 Name=instance-state-name,Values=running --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
curl -s -m 5 http://$PUB:9898/ || echo "막혔다 (정상)"
```

!!! check "확인"
    `막혔다 (정상)` — 공인 IP가 있어도 보안 그룹이 9898을 **ALB에서만** 받으므로 내 노트북에서는 닿지 않습니다. 1일차 7교시의 "SG를 출발지로"가 동작하고 있습니다.

!!! myth "오해 — 서버 설정은 접속해서 하면 된다"
    SSH로 들어가 손으로 패키지를 설치한 서버는 1일차 6교시의 '눈송이'입니다. 그 서버가 죽으면 같은 서버를 다시 만들 수 없습니다. 설정은 **user data · 이미지(AMI) · 나중에는 Terraform**에 두고, 접속은 **확인**할 때만 합니다. 3주차의 "kubectl exec로 고치지 않는다"와 같은 원칙입니다.

!!! academic "학술 노트 — 불변 인프라"
    서버를 고쳐 쓰지 않고 **새로 만들어 바꾸는** 방식을 Fowler(2013)의 *ImmutableServer*, Netflix의 Aminator · Spinnaker 글들이 '**불변 인프라**'(immutable infrastructure)로 정리했습니다. 고쳐 쓰는 서버는 시간이 지날수록 설정이 어긋나고(drift), 불변 서버는 언제나 템플릿과 같습니다. 컨테이너 이미지(2주차)가 그 생각을 애플리케이션 단위로 옮긴 것이고, 오늘의 시작 템플릿 + Auto Scaling이 VM 단위의 구현입니다.

!!! trend "트렌드 2026 — 그래비톤과 플렉스 인스턴스"
    AWS의 ARM 칩 **Graviton**(t4g · m8g 등)은 같은 성능에 20~40% 싼 경우가 많아 새 서비스의 기본 선택지가 되었습니다(이미지가 ARM용으로도 빌드되어 있어야 한다 — podinfo는 멀티 아키텍처). 또 버스트형 t 계열 대신 **flex** 인스턴스(c7i-flex · m7i-flex)가 Free Tier 대상에 들어왔습니다. 오늘은 가장 익숙한 t3.micro를 씁니다.

!!! quiz "확인 문제"
    1. 인스턴스 프로파일은 무엇이고 왜 필요한가요?
    2. 키 페어 없이 시작한 이유는?
    3. user data를 쓰면 무엇이 좋아지나요?
    4. 오늘 서버를 public 서브넷에 둔 이유와, 그래도 밖에서 9898에 못 닿는 이유는?

    ??? answer "정답"
        1. IAM 역할을 EC2에 꽂는 어댑터 — EC2는 역할을 인스턴스 프로파일로만 받는다
        2. SSH를 쓰지 않고 Session Manager로 접속하기 위해 (22번 포트를 열지 않는다)
        3. 서버를 손으로 설정하지 않아도 되고, 같은 서버를 몇 대든 똑같이 만들 수 있다
        4. NAT · SSM 엔드포인트 비용을 피하려고. app-sg가 9898을 web-sg에서만 받기 때문

## 참고 문헌

- AWS Docs. *IAM roles for Amazon EC2 — instance profiles*. docs.aws.amazon.com/IAM
- AWS Docs. *Run commands when you launch an EC2 instance with user data input*. docs.aws.amazon.com/AWSEC2
- Fowler, M. (2013). *ImmutableServer*. martinfowler.com/bliki
