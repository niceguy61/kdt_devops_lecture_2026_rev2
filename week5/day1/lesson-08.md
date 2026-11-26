<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [1일차](README.md) › 8/8교시</sub>

# 8교시 · 누가 무엇을 했나 — CloudTrail과 태그 전략

> [!NOTE]
> **이번 시간에 할 일**
>
> - 오늘 내가 한 **클릭과 명령이 모두 기록되어 있다**는 것을 CloudTrail에서 확인합니다.
> - 이벤트 하나를 열어 **누가 · 언제 · 어디서 · 무엇을 · 성공했나**를 읽습니다.
> - 과정 전체에서 쓸 **태그 규칙 네 개**를 정하고, 오늘 만든 자원에 붙입니다.
> - 태그로 **내 것만 한 번에 찾고**, 태그가 빠진 것을 골라냅니다(5일차 "남은 것 찾기"의 연습).

> [!IMPORTANT]
> **로그는 누가 남겨 주나**
>
> 4주차까지는 로그를 우리가 모았습니다(Loki). AWS에서는 **계정 안의 모든 API 호출**을 AWS가 기록합니다. 콘솔 클릭도 결국 API 호출이므로(4교시) 빠짐없이 남습니다. 이 기록이 **CloudTrail**입니다. 사고가 나면 가장 먼저 여는 곳이고, 오늘처럼 아무 일이 없는 날에도 "내 계정에서 나 말고 누가 무엇을 했나"를 보는 곳입니다.

## 실습 16 · 오늘 한 일 되짚기

### 단계 1 — 내가 만든 것들

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=Username,AttributeValue=devops-admin \
  --start-time "$(date -u -d '-8 hours' +%Y-%m-%dT%H:%M:%SZ)" \
  --query 'Events[?starts_with(EventName, `Create`) || starts_with(EventName, `Authorize`)].[EventTime, EventName]' \
  --output table
```

Mac은 시간 부분을 `$(date -u -v-8H +%Y-%m-%dT%H:%M:%SZ)`로 바꿉니다.

> **🟢 확인: 보이는 것 (예 · 최신이 위)**
>
> ```text
> ------------------------------------------------------------
> |                       LookupEvents                       |
> +----------------------------+-----------------------------+
> |  2026-11-30T07:48:12+00:00 |  AuthorizeSecurityGroupIngress |
> |  2026-11-30T07:47:55+00:00 |  CreateSecurityGroup        |
> |  2026-11-30T07:46:30+00:00 |  CreateSecurityGroup        |
> |  2026-11-30T06:12:41+00:00 |  CreateVpcEndpoint          |
> |  2026-11-30T06:12:18+00:00 |  CreateRouteTable           |
> |  2026-11-30T06:12:02+00:00 |  CreateSubnet               |
> |  2026-11-30T06:11:58+00:00 |  CreateVpc                  |
> ```
> 6교시 마법사의 클릭 몇 번이 **API 호출 수십 개**로 남았습니다. 7교시의 보안 그룹도 보입니다. 이벤트가 나타나기까지 **최대 몇 분** 걸릴 수 있습니다.

### 단계 2 — 이벤트 하나 열어 보기

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AuthorizeSecurityGroupIngress \
  --max-results 1 --query 'Events[0].CloudTrailEvent' --output text \
  | jq '{who: .userIdentity.arn, when: .eventTime, from: .sourceIPAddress, how: .userAgent[0:40],
         what: .eventName, ok: (.errorCode // "성공"), rule: .requestParameters.ipPermissions.items[0]}'
```

> **🟢 확인: 보이는 것**
>
> ```text
> {
>   "who": "arn:aws:iam::123456789012:user/devops-admin",
>   "when": "2026-11-30T07:48:12Z",
>   "from": "203.0.113.7",
>   "how": "AWS Internal",
>   "what": "AuthorizeSecurityGroupIngress",
>   "ok": "성공",
>   "rule": { "ipProtocol": "tcp", "fromPort": 9898, "toPort": 9898, "groups": { … } }
> }
> ```

| 칸 | 사고 조사에서 묻는 것 |
|---|---|
| `userIdentity.arn` | **누가** — 사용자인가, 역할인가, 루트인가 |
| `eventTime` | **언제** — 장애가 시작된 시각과 맞나 |
| `sourceIPAddress` | **어디서** — 우리 회사 · 내 집인가, 낯선 나라인가 |
| `userAgent` | **무엇으로** — 콘솔(`AWS Internal`), CLI(`aws-cli/2…`), Terraform(`APN/1.0 HashiCorp/…`) |
| `errorCode` | **성공했나** — `AccessDenied`가 줄줄이 있으면 누군가 **권한을 더듬고** 있다는 신호 |
| `requestParameters` | **정확히 무엇을** — 어떤 포트를 누구에게 열었나 |

> [!TIP]
> **콘솔로 볼 때**
>
> 검색 `CloudTrail` → **이벤트 기록** → 필터 `사용자 이름 = devops-admin`. 오른쪽 위 톱니로 **소스 IP 주소** · **오류 코드** 칸을 켜면 위 표의 칸이 한눈에 보입니다.

### 단계 3 — 기록은 얼마나 남나

| | 이벤트 기록(Event history) | 추적(Trail) |
|---|---|---|
| 무엇을 | 관리 이벤트(만들기 · 바꾸기 · 지우기 · 로그인) | 관리 + 선택하면 데이터 이벤트(S3 객체 읽기 등) |
| 얼마나 | **90일** | 내가 정한 S3 버킷에 **원하는 만큼** |
| 비용 | 무료 · 설정 없음 | 관리 이벤트 첫 사본은 무료, S3 저장 비용 |
| 실무 | 오늘 같은 확인 | **필수** — 조직 전체 추적을 별도 보안 계정의 잠긴 버킷에 |

이 과정은 계정을 며칠만 쓰므로 이벤트 기록으로 충분합니다. 회사 계정에서는 첫날 추적부터 켭니다.

## 실습 17 · 태그 규칙 정하고 붙이기

### 단계 1 — 이 과정의 태그 규칙

7교시에 `Name`과 `Project`를 붙였습니다. 여기에 둘을 더해 **네 개를 규칙으로** 정합니다.

| 키 | 값 | 묻는 질문 |
|---|---|---|
| `Project` | `devmart` | 어느 서비스의 돈인가 |
| `Owner` | 내 GitHub 아이디 | 문제가 생기면 **누구에게** 묻나 |
| `Env` | `lab` | 지워도 되는가 (`prod`면 절대 안 됨) |
| `ManagedBy` | `console` 또는 `terraform` | **어디서 고쳐야** 하나 — 3일차부터 중요 |

> [!WARNING]
> **태그에 비밀을 넣지 않는다**
>
> 태그는 결제 화면 · 다른 서비스 · 감사 도구 어디서나 **평문으로** 보입니다. 비밀번호나 고객 정보를 넣지 않습니다.

### 단계 2 — 오늘 만든 자원에 한 번에 붙이기

```bash
ME=$(gh api user --jq .login)
VPC=$(aws ec2 describe-vpcs --filters Name=tag:Name,Values=devmart-vpc --query 'Vpcs[0].VpcId' --output text)
IDS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC --query 'Subnets[].SubnetId' --output text)
IDS="$IDS $(aws ec2 describe-route-tables --filters Name=vpc-id,Values=$VPC --query 'RouteTables[].RouteTableId' --output text)"
IDS="$IDS $(aws ec2 describe-security-groups --filters Name=vpc-id,Values=$VPC Name=group-name,Values='devmart-*' --query 'SecurityGroups[].GroupId' --output text)"
IDS="$IDS $(aws ec2 describe-internet-gateways --filters Name=attachment.vpc-id,Values=$VPC --query 'InternetGateways[].InternetGatewayId' --output text)"
echo $VPC $IDS | wc -w
aws ec2 create-tags --resources $VPC $IDS \
  --tags Key=Project,Value=devmart Key=Owner,Value=$ME Key=Env,Value=lab Key=ManagedBy,Value=console
```

> **🟢 확인: 이렇게 나오면 성공**
>
> 숫자(자원 개수, 보통 10개 안팎)가 나오고, `create-tags`는 **아무것도 출력하지 않으면** 성공입니다(1주차 2일차: 조용한 성공).

### 단계 3 — 태그로 내 것만 찾기

```bash
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Project,Values=devmart Key=Env,Values=lab \
  --query 'ResourceTagMappingList[].ResourceARN' --output text | tr '\t' '\n' | awk -F: '{print $6}' | sort
```

> **🟢 확인: 보이는 것**
>
> ```text
> internet-gateway/igw-0…
> route-table/rtb-0…
> security-group/sg-0…
> …
> subnet/subnet-0…
> vpc/vpc-0f1e2d3c4b5a69788
> ```
> 서비스가 달라도(EC2 · VPC · S3 …) **한 번의 질문**으로 찾습니다. 5일차 마지막 날 "남은 것 찾기"가 이 명령에서 출발합니다.

### 단계 4 — 태그가 빠진 것 골라내기

```bash
aws ec2 describe-security-groups --filters Name=vpc-id,Values=$VPC \
  --query 'SecurityGroups[?!not_null(Tags[?Key==`Owner`].Value)].[GroupId, GroupName]' --output table
```

> **🟢 확인: 보이는 것**
>
> ```text
> |  sg-0a1b2c…  |  default  |
> ```
> VPC를 만들 때 **자동으로 생긴** `default` 보안 그룹은 태그가 없습니다. "누가 만들었는지 모르는 자원"은 이렇게 생깁니다. 4주차 Kyverno가 "limits 없는 배포 금지"를 했듯이, AWS에서는 **태그 정책**(Organizations)이나 3일차의 Terraform `default_tags`로 "태그 없는 자원"을 막습니다.

### 단계 5 — 비용에 태그를 쓰려면 (읽기만)

**결제 및 비용 관리 → 비용 할당 태그**에서 `Project`를 **활성화**해야 Cost Explorer에서 "프로젝트별 비용"으로 볼 수 있습니다. 새 태그 키는 처음 붙인 뒤 **최대 24시간** 지나야 목록에 나타나므로 내일 켭니다. 켠 뒤부터의 비용만 나뉩니다 — **첫날 켜야 하는 이유**입니다.

## 실습 18 · 오늘의 마지막 점검

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin \
  --max-results 5 --query 'Events[].CloudTrailEvent' --output text \
  | jq -r '[.eventTime, .userIdentity.type, (.userIdentity.userName // "root"), .sourceIPAddress, (.responseElements.ConsoleLogin)] | @tsv'
```

> **🟢 확인: 보이는 것**
>
> ```text
> 2026-11-30T05:31:02Z  IAMUser  devops-admin  203.0.113.7  Success
> 2026-11-30T05:02:44Z  Root     root          203.0.113.7  Success
> ```
> 오늘 루트 로그인은 2교시의 **MFA 설정 때 한 번뿐**이어야 합니다. 루트 로그인이 안 보이면 같은 명령에 `--region us-east-1`을 붙여 봅니다 — 로그인 기록은 로그인한 **엔드포인트의 리전**에 남고, 루트는 보통 버지니아(us-east-1)입니다. 모르는 시각 · 모르는 IP의 로그인이 있으면 즉시 비밀번호를 바꾸고 강사에게 알립니다.

> **🎓 학술 노트 — 보안의 금(Au): 인증 · 인가 · 감사 (Lampson, 2004)**
>
> 분산 시스템 보안의 선구자 **버틀러 램슨(Butler Lampson)**은 「Computer Security in the Real World」(IEEE Computer, 2004)에서 실용적인 보안의 세 기둥을 화학 기호 **Au(금)**로 묶었습니다. **Au**thentication(누구인가) · **Au**thorization(무엇을 해도 되나) · **Au**diting(무엇을 했나). 앞의 둘은 사고를 **막고**, 셋째는 막지 못한 사고를 **알아내고 고친다**는 것입니다. 그는 완벽한 예방은 불가능하므로 **기록을 남기고 나중에 책임을 묻는 것**이 현실 세계 보안의 대부분이라고 강조했습니다. 1주차 4일차 8교시의 인증 · 인가에 오늘 **감사**가 더해졌습니다.
>
> - Lampson, B. W. (2004). Computer security in the real world. *IEEE Computer*, 37(6), 37–46.

> **📈 트렌드 — 기록으로 권한을 줄인다**
>
> CloudTrail 기록은 사고 조사에만 쓰이지 않습니다. **IAM Access Analyzer**는 지난 기록을 보고 "이 역할은 90일 동안 이 권한을 **한 번도 안 썼다**"를 찾아내고, 실제로 쓴 동작만으로 **최소 권한 정책을 만들어** 줍니다. 3교시의 최소 권한을 사람이 짐작으로 하지 않고 **기록으로** 하는 방향입니다. 태그도 마찬가지로, 태그를 기준으로 권한을 주는 **ABAC**(속성 기반 접근 제어 — "`Owner` 태그가 내 이름인 자원만 지울 수 있다")가 늘고 있습니다.

## 정리

- CloudTrail은 계정의 **모든 API 호출**을 남깁니다. 콘솔 클릭도 포함입니다. 이벤트 기록은 90일 · 무료, 실무는 **추적**을 잠긴 버킷에.
- 이벤트에서 **누가 · 언제 · 어디서 · 무엇으로 · 성공했나 · 정확히 무엇을**을 읽습니다.
- 태그 규칙 넷: `Project` · `Owner` · `Env` · `ManagedBy`. 태그로 찾고, **태그가 빠진 것**을 골라냅니다.
- 비용 할당 태그는 **첫날** 켭니다.

> **✅ 확인 문제**
>
> 1. 콘솔에서 클릭으로 만든 보안 그룹도 CloudTrail에 남나요? 이유는?
> 2. 이벤트에 `errorCode: AccessDenied`가 짧은 시간에 수십 개 있습니다. 무엇을 의심하나요?
> 3. 이벤트 기록(Event history)과 추적(Trail)의 차이 두 가지는?
> 4. `ManagedBy` 태그가 3일차부터 중요해지는 이유는?
> 5. Lampson의 Au 세 가지는?
>
> <details><summary>정답</summary>
>
> 1. 남습니다. 콘솔도 결국 같은 API를 부르기 때문입니다(4교시).
> 2. 누군가(사람이든 훔친 열쇠든) 권한을 더듬어 보고 있다 — 출처 IP와 신원을 바로 확인
> 3. 보관 기간(90일 vs 원하는 만큼), 대상(관리 이벤트만 vs 데이터 이벤트까지 선택), 저장 위치(AWS 화면 vs 내 S3)
> 4. Terraform이 관리하는 자원을 콘솔에서 고치면 다음 `apply` 때 되돌아가거나 어긋남이 생기므로, 어디서 고쳐야 하는지 알려 준다
> 5. Authentication(인증) · Authorization(인가) · Auditing(감사)
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - kind에서 AWS로 옮길 때 바뀌는 것 셋, 그대로인 것 셋
> - 루트 · IAM 사용자 · IAM 역할을 한 문장씩, 4주차의 무엇과 닮았나
> - 오늘 읽은 정책 JSON에서 Deny 문장이 하는 일
> - 내 VPC 그림을 손으로 그리고, public과 private을 가르는 한 줄을 적기
> - 이번 주 비용 계산표에서 가장 무서운 줄과, 그것을 막는 내 습관
> - 내일 전에 궁금한 것: 오늘 VPC는 비어 있다. 여기에 **서버를 띄우고, 여러 대로 늘리고, 하나가 죽어도 손님이 모르게** 하려면 무엇이 필요할까?

## 참고 문헌

- Lampson, B. W. (2004). Computer security in the real world. *IEEE Computer*, 37(6).
- AWS Docs. *Viewing events with CloudTrail Event history*; *CloudTrail record contents*; *Creating a trail*. docs.aws.amazon.com/awscloudtrail
- AWS Docs. *Tagging AWS resources — Best practices*; *Resource Groups Tagging API — GetResources*; *Using cost allocation tags*. docs.aws.amazon.com
- AWS Docs. *IAM Access Analyzer — unused access, policy generation*; *ABAC for AWS*. docs.aws.amazon.com/IAM

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 보안 그룹 · NACL + 비용 점검](lesson-07.md) | [⬆️ 1일차 목차](README.md) | [5주차 2일차 목차](../day2/README.md) ➡️ |
