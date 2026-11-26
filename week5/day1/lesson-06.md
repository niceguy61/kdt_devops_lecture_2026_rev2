[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [1일차](README.md)

# 6교시 · 콘솔로 VPC 만들기

> [!NOTE]
> **이번 시간에 할 일**
>
> - **VPC 생성 마법사**(VPC 등)로 5교시 설계대로 VPC를 만듭니다.
> - 만들어진 것 — 서브넷 · 라우팅 테이블 · IGW · 엔드포인트 — 을 하나씩 열어 봅니다.
> - CLI로 같은 것을 **다시 읽어** 설계와 맞는지 검증합니다.
> - 클릭으로 만든 것의 **기록 문제**를 느껴 봅니다.

## 실습 11 · 마법사로 만들기

콘솔(서울 리전 확인!) → 검색 `VPC` → **VPC 대시보드** → **VPC 생성**.

| 칸 | 값 |
|---|---|
| 생성할 리소스 | **VPC 등** (VPC and more) |
| 이름 태그 자동 생성 | 체크, `devmart` |
| IPv4 CIDR 블록 | `10.0.0.0/16` |
| IPv6 CIDR 블록 | 없음 |
| 테넌시 | 기본값 |
| 가용 영역(AZ) 수 | **2** → AZ 사용자 지정에서 `ap-northeast-2a`, `ap-northeast-2c` |
| 퍼블릭 서브넷 수 | 2 |
| 프라이빗 서브넷 수 | 2 |
| 서브넷 CIDR 블록 사용자 지정 | 펼쳐서 5교시 값과 같은지 확인 (10.0.0.0/20 · 10.0.16.0/20 · 10.0.128.0/20 · 10.0.144.0/20) |
| **NAT 게이트웨이** | **없음** ← 반드시 확인 |
| VPC 엔드포인트 | **S3 게이트웨이** |
| DNS 옵션 | 호스트 이름 · 확인 **둘 다 체크** (EKS에 필요) |

오른쪽 **미리 보기**에 서브넷 넷, 라우팅 테이블 셋, 네트워크 연결(IGW · S3 엔드포인트)이 선으로 그려집니다. 5교시 그림과 비교한 뒤 **VPC 생성**.

> **🟢 확인: 확인**
>
> "VPC 생성 워크플로" 화면에 초록 체크가 열 개 남짓 차례로 찍힙니다 — VPC, DNS 설정, 서브넷 넷, IGW 생성 · 연결, 라우팅 테이블 셋과 경로, 엔드포인트. **VPC 보기**를 누릅니다.

> [!WARNING]
> **NAT를 실수로 만들었다면**
>
> 마법사 기본값이 'AZ당 1개'인 경우가 있습니다. 만들어졌다면 바로 **VPC → NAT 게이트웨이**에서 삭제하고, **탄력적 IP**에서 NAT용으로 할당된 주소도 **릴리스**합니다(둘 다 시간당 요금). 7교시 `check-account.sh`가 확인해 줍니다.

## 실습 12 · 하나씩 열어 보기

**VPC → 리소스 맵** 탭이 가장 좋은 지도입니다. 서브넷 → 라우팅 테이블 → 네트워크 연결이 선으로 이어져 있습니다.

| 열어 볼 곳 | 확인할 것 |
|---|---|
| **서브넷** | 넷, 각자의 AZ와 CIDR. public 서브넷의 **퍼블릭 IPv4 주소 자동 할당** — 마법사는 '아니요'로 둔다 |
| **라우팅 테이블** | 셋: `devmart-rtb-public`(public 둘 연결), `devmart-rtb-private1-ap-northeast-2a`, `…private2-…2c` |
| public 라우팅 테이블의 **라우팅** 탭 | `10.0.0.0/16 → local`, `0.0.0.0/0 → igw-…` |
| private 라우팅 테이블의 **라우팅** 탭 | `10.0.0.0/16 → local`, `pl-… → vpce-…`(S3) — **0.0.0.0/0이 없다** |
| **인터넷 게이트웨이** | `devmart-igw`, 상태 Attached |
| **엔드포인트** | `devmart-vpce-s3`, 유형 Gateway |

> [!IMPORTANT]
> **local 경로**
>
> 모든 라우팅 테이블 맨 위의 `10.0.0.0/16 → local`은 지울 수 없습니다. **VPC 안의 서브넷끼리는 언제나 서로 닿는다**는 뜻입니다. 막고 싶으면 라우팅이 아니라 보안 그룹 · NACL(7교시)로 막습니다.

## 실습 13 · CLI로 검증

```bash
VPC=$(aws ec2 describe-vpcs --filters Name=tag:Name,Values=devmart-vpc --query 'Vpcs[0].VpcId' --output text)
echo $VPC
aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC \
  --query 'sort_by(Subnets,&CidrBlock)[].[Tags[?Key==`Name`]|[0].Value,AvailabilityZone,CidrBlock,MapPublicIpOnLaunch]' --output table
aws ec2 describe-route-tables --filters Name=vpc-id,Values=$VPC \
  --query 'RouteTables[].[Tags[?Key==`Name`]|[0].Value, join(`, `, Routes[].[DestinationCidrBlock || DestinationPrefixListId, GatewayId][] )]' --output table
```

> **🟢 확인: 확인**
>
> ```text
> vpc-0f1e2d3c4b5a69788
> ------------------------------------------------------------------------------------------
> |                                      DescribeSubnets                                    |
> +-----------------------------------------------+------------------+----------------+------+
> |  devmart-subnet-public1-ap-northeast-2a       |  ap-northeast-2a |  10.0.0.0/20   | False|
> |  devmart-subnet-public2-ap-northeast-2c       |  ap-northeast-2c |  10.0.16.0/20  | False|
> |  devmart-subnet-private1-ap-northeast-2a      |  ap-northeast-2a |  10.0.128.0/20 | False|
> |  devmart-subnet-private2-ap-northeast-2c      |  ap-northeast-2c |  10.0.144.0/20 | False|
> +-----------------------------------------------+------------------+----------------+------+
> …
> |  devmart-rtb-public                    |  10.0.0.0/16, local, 0.0.0.0/0, igw-0a1b…   |
> |  devmart-rtb-private1-ap-northeast-2a  |  10.0.0.0/16, local, pl-78a54011, vpce-0c…  |
> |  devmart-rtb-private2-ap-northeast-2c  |  10.0.0.0/16, local, pl-78a54011, vpce-0c…  |
> ```
> 5교시 설계표와 한 줄씩 맞춰 봅니다. 마지막 칸(`MapPublicIpOnLaunch`)이 모두 False — 내일 EC2를 띄울 때 공인 IP를 **직접** 정합니다.

## 클릭의 대가

지금 VPC는 클릭 20번쯤으로 만들어졌습니다. 질문을 던져 봅니다.

| 질문 | 지금 답할 수 있나 |
|---|---|
| 내일 동료가 같은 VPC를 다른 계정에 만들려면? | 오늘 표를 보고 **다시 20번 클릭** |
| 누군가 콘솔에서 라우팅 하나를 바꿨다면? | 알 수 없다 — 4주차 3일차의 **어긋남(drift)** |
| 무엇을 언제 왜 바꿨나? | CloudTrail 이벤트를 뒤져야 한다 |
| 다 지우려면? | 의존 순서대로 하나씩 (엔드포인트 → 서브넷 → IGW 분리 → …) |

3주차 Kubernetes에서 `kubectl run` 대신 YAML 파일을 쓰게 된 것, 4주차에 Git이 원하는 상태가 된 것과 같은 길을 AWS에서도 갑니다 — **3일차 Terraform**에서 이 VPC를 코드 몇십 줄로 다시 만들고, 한 명령으로 지웁니다. 오늘 만든 VPC는 **무료**이므로 2일차 실습까지 그대로 둡니다.

> [!TIP]
> **CloudTrail로 '누가 만들었나' 보기**
>
> 검색 `CloudTrail` → **이벤트 기록** → 이벤트 이름 `CreateVpc`. 방금 `devops-admin`이 만든 기록이 보입니다. 계정의 모든 API 호출(콘솔 클릭 포함)이 90일 동안 무료로 남습니다 — AWS판 감사 로그입니다.

> **🎓 학술 노트 — 클릭옵스와 재현성**
>
> 수작업 설정의 재현성 문제는 Burgess(4주차 3일차)뿐 아니라 Morris의 *Infrastructure as Code*(O'Reilly, 2016; 3판 2025)가 정리한 '**눈송이 서버**'(snowflake server) — 손으로 하나하나 다듬어 똑같이 다시 만들 수 없는 서버 — 개념으로 널리 알려졌습니다. 콘솔 클릭으로 만든 VPC는 눈송이 네트워크입니다. Morris는 IaC의 목표를 "**쉽게 다시 만들 수 있는**(reproducible) · **버릴 수 있는**(disposable) 시스템"으로 요약합니다.

> **📈 트렌드 2026 — 콘솔에서 코드로 내보내기**
>
> AWS는 콘솔에서 만든 자원을 **IaC 코드로 뽑아 주는** 기능(CloudFormation IaC generator, 콘솔의 'Infrastructure Composer로 내보내기')을 넓혀 왔고, Terraform도 `terraform query`(1.14+) · import 블록 생성으로 기존 자원을 코드로 가져오는 흐름을 강화했습니다. "처음엔 콘솔로 익히고, 굳히는 것은 코드로"가 현실적인 경로입니다 — 이번 주의 순서이기도 합니다.

> **✅ 확인 문제**
>
> 1. 마법사에서 NAT를 '없음'으로 한 이유와, 실수로 만들었을 때 지울 것 둘은?
> 2. 모든 라우팅 테이블의 local 경로는 무슨 뜻인가요?
> 3. private 라우팅 테이블에 있는 `pl-… → vpce-…`는 무엇인가요?
> 4. 콘솔로 만든 VPC의 문제 셋은?
>
> <details><summary>정답</summary>
>
> 1. 켜 두기만 해도 시간당 요금. NAT 게이트웨이와 그 탄력적 IP
> 2. VPC 안 서브넷끼리는 언제나 서로 닿는다
> 3. S3로 가는 게이트웨이 엔드포인트 경로 (인터넷을 거치지 않는 무료 샛길)
> 4. 다시 만들기 어렵다, 어긋나도 모른다, 변경 기록과 삭제 순서를 사람이 기억해야 한다
>
> </details>

## 참고 문헌

- AWS Docs. *Create a VPC (VPC and more)*, *VPC resource map*, *Gateway endpoints for Amazon S3*. docs.aws.amazon.com/vpc
- AWS Docs. *Viewing events with CloudTrail Event history*. docs.aws.amazon.com/awscloudtrail
- Morris, K. (2025). *Infrastructure as Code*, 3rd ed. O'Reilly.

---

⬅️ 이전: [5교시 · VPC의 구성 요소](lesson-05.md) &nbsp;|&nbsp; [⬆️ 1일차 목차](README.md) &nbsp;|&nbsp; 다음: [7교시 · 보안 그룹 · NACL + 비용 점검](lesson-07.md) ➡️
