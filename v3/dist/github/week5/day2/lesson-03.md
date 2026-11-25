# 3교시 · Session Manager · 메타데이터 · S3

> [!NOTE]
> **이번 시간에 할 일**
>
> - **Session Manager**로 포트 없이 서버에 들어갑니다.
> - user data가 잘 돌았는지 로그와 `docker ps`로 확인합니다.
> - **인스턴스 메타데이터(IMDSv2)**에서 서버가 자기 자신과 **역할 자격 증명**을 어떻게 얻는지 봅니다.
> - S3 버킷을 만들고, 서버에서 **키 없이** 읽고, **Deny**에 막히는 것을 봅니다.

## 실습 3 · Session Manager로 들어가기

EC2 → 인스턴스 → `devmart-web-1` 체크 → **연결** → **Session Manager** 탭 → **연결**

브라우저 안에 터미널이 열립니다(사용자 `ssm-user`).

```bash
whoami; hostname
sudo docker ps
curl -s localhost:9898/ | head -8
sudo tail -3 /var/log/cloud-init-output.log
```

> **🟢 확인: 확인**
>
> ```text
> ssm-user
> ip-10-0-5-183.ap-northeast-2.compute.internal
> CONTAINER ID   IMAGE                                  COMMAND                  STATUS         PORTS                    NAMES
> 3f2a9c1d8b7e   ghcr.io/stefanprodan/podinfo:6.14.0    "./podinfo --port=98…"   Up 4 minutes   0.0.0.0:9898->9898/tcp   podinfo
> {
>   "hostname": "3f2a9c1d8b7e",
>   "version": "6.14.0",
>   "revision": "…",
>   "color": "#34577c",
>   "logo": "…",
>   "message": "DevMart on EC2",
> …
> Cloud-init v. 22.2.2 finished at … Up 58.31 seconds
> ```
> - user data가 Docker를 깔고 podinfo를 띄웠습니다. 사람은 한 번도 들어오지 않았습니다.
> - 보안 그룹에 22번이 **없는데** 들어왔습니다. 서버 안의 SSM 에이전트가 **밖으로** AWS에 연결을 열어 두고, 우리는 그 연결로 들어온 것입니다. 2교시에 붙인 `AmazonSSMManagedInstanceCore` 정책이 그 권한입니다.

> [!IMPORTANT]
> **SSH 대신 Session Manager**
>
> | | SSH | Session Manager |
> |---|---|---|
> | 열어야 할 포트 | 22 (인바운드) | **없음** |
> | 열쇠 | 키 파일 (잃어버리기 · 새기 쉽다) | IAM 로그인 + MFA |
> | 누가 들어왔나 | 서버 로그를 뒤져야 | CloudTrail에 **누가 · 언제** 남는다 |
> | 4주차에서 | — | `kubectl exec` + RBAC |

## 실습 4 · 메타데이터와 역할 자격 증명

서버는 `169.254.169.254`라는 특별한 주소에서 **자기 자신에 대한 정보**를 얻습니다. IMDSv2는 먼저 **토큰**을 받아야 합니다.

```bash
TOKEN=$(curl -s -X PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
md() { curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/$1; echo; }
md instance-id
md placement/availability-zone
md iam/security-credentials/
md iam/security-credentials/devmart-ec2-role | head -6
curl -s -m 2 http://169.254.169.254/latest/meta-data/instance-id -o /dev/null -w 'v1(토큰 없이): %{http_code}\n'
aws sts get-caller-identity
```

> **🟢 확인: 확인**
>
> ```text
> i-0a1b2c3d4e5f60718
> ap-northeast-2a
> devmart-ec2-role
> {
>   "Code" : "Success",
>   "LastUpdated" : "2026-11-30T02:31:07Z",
>   "Type" : "AWS-HMAC",
>   "AccessKeyId" : "ASIA…",
>   "SecretAccessKey" : "…",
> v1(토큰 없이): 401
> {
>     "UserId": "AROA…:i-0a1b2c3d4e5f60718",
>     "Account": "123456789012",
>     "Arn": "arn:aws:sts::123456789012:assumed-role/devmart-ec2-role/i-0a1b2c3d4e5f60718"
> }
> ```
> - 역할의 **임시 자격 증명**(`ASIA…`, 만료 시각 있음)이 메타데이터로 나옵니다. 서버 안의 AWS CLI · SDK는 이것을 **자동으로** 씁니다 — 파일에 키를 넣지 않았는데 `aws` 명령이 됩니다.
> - `Arn`이 **assumed-role/devmart-ec2-role/인스턴스ID** — "이 서버가 역할을 맡았다". 4주차 5일차의 `system:serviceaccount:devmart:pod-reader`와 같은 모양의 신원입니다.
> - 토큰 없는 요청(v1)은 **401** — IMDSv2만 허용했기 때문입니다.

> [!WARNING]
> **IMDSv2를 강제하는 이유**
>
> 2019년 Capital One 사고에서 공격자는 웹 앱의 취약점(SSRF)으로 서버가 **메타데이터 주소에 대신 요청**하게 만들어 역할 자격 증명을 빼냈습니다. IMDSv2는 먼저 **PUT으로 토큰**을 받아야 하므로, 단순한 GET만 흉내 낼 수 있는 SSRF로는 자격 증명을 얻기 어렵습니다. 새 인스턴스는 v2만 허용이 기본입니다 — 끄지 않습니다.

## 실습 5 · S3 버킷과 키 없는 읽기

이번에는 **내 노트북 터미널**(Session Manager가 아닌)에서 버킷을 만듭니다.

```bash
ID=$(gh api user -q .login | tr 'A-Z' 'a-z')
B=devmart-assets-$ID
aws s3 mb s3://$B --region ap-northeast-2
echo "DevMart 공지 — $(date +%F)" > /tmp/notice.txt
aws s3 cp /tmp/notice.txt s3://$B/notice.txt
aws s3 ls s3://$B/
aws s3api get-public-access-block --bucket $B --query 'PublicAccessBlockConfiguration'
```

> **🟢 확인: 확인**
>
> ```text
> make_bucket: devmart-assets-niceguy61
> upload: ../tmp/notice.txt to s3://devmart-assets-niceguy61/notice.txt
> 2026-11-30 11:35:02         36 notice.txt
> {
>     "BlockPublicAcls": true,
>     "IgnorePublicAcls": true,
>     "BlockPublicPolicy": true,
>     "RestrictPublicBuckets": true
> }
> ```
> S3 버킷 이름은 **전 세계에서 유일**해야 합니다(그래서 GitHub ID를 붙였다). **퍼블릭 액세스 차단** 네 개가 모두 true — 새 버킷은 기본으로 인터넷에 공개되지 않습니다.

다시 **Session Manager 터미널**(서버 안)로 갑니다.

```bash
B=devmart-assets-niceguy61          # 내 ID로 바꾼다
aws s3 ls s3://$B/
aws s3 cp s3://$B/notice.txt - 
aws s3 rm s3://$B/notice.txt
aws ec2 describe-instances --max-items 1 >/dev/null
```

> **🟢 확인: 확인**
>
> ```text
> 2026-11-30 11:35:02         36 notice.txt
> DevMart 공지 — 2026-11-30
> delete failed: s3://devmart-assets-niceguy61/notice.txt An error occurred (AccessDenied) when calling the DeleteObject operation: User: arn:aws:sts::123456789012:assumed-role/devmart-ec2-role/i-0a1b… is not authorized to perform: s3:DeleteObject on resource: "arn:aws:s3:::devmart-assets-niceguy61/notice.txt" with an explicit deny in an identity-based policy
> An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to perform this operation. …
> ```
> - 읽기는 됩니다 — **키 파일 없이**.
> - 삭제는 **explicit deny**로 막혔습니다 — 1일차 3교시의 Deny 문장이 실제로 동작했습니다. 오류 메시지가 "어떤 정책 종류의 명시적 거절"인지까지 알려 줍니다.
> - EC2 조회는 정책에 **아예 없으므로**(암묵적 거절) 막혔습니다.

Session Manager 창은 **종료**를 눌러 닫습니다.

> **❓ 오해 — S3는 웹 서버처럼 열려 있다**
>
> S3 사고 뉴스("수백만 명의 개인정보가 담긴 버킷 공개") 때문에 생긴 인상이지만, 2023년 4월부터 새 버킷은 **퍼블릭 액세스 차단이 기본**입니다. 공개 사고는 누군가 이 차단을 **일부러 끄고** 정책을 잘못 쓴 경우입니다. 공개해야 할 정적 파일은 버킷을 열지 말고 CloudFront 같은 앞단을 둡니다.

> **🎓 학술 노트 — SSRF와 메타데이터 서비스**
>
> 서버가 공격자 대신 내부 주소에 요청하게 만드는 **SSRF**(Server-Side Request Forgery)는 클라우드 메타데이터 서비스와 결합하면서 위험이 커졌고, OWASP Top 10(2021)에 독립 항목(A10)으로 들어갔습니다. Capital One 사고(2019)에 대한 분석(예: 미국 상원 보고서, 다수의 사후 분석)은 ① 과한 역할 권한, ② IMDSv1, ③ WAF 설정 오류가 겹친 결과로 정리합니다. 오늘 한 세 가지 — **좁은 역할 · IMDSv2 · Deny 문장** — 가 각각 그 고리 하나씩을 끊습니다.

> **📈 트렌드 2026 — 데이터 경계**
>
> "우리 계정의 역할은 **우리 계정의 버킷에만**, 우리 VPC에서만 접근할 수 있다"를 조직 전체에 강제하는 **데이터 경계**(data perimeter) — SCP · RCP(리소스 제어 정책) · VPC 엔드포인트 정책의 조합 — 가 AWS 보안의 표준 설계가 되었습니다. 1일차에 만든 S3 게이트웨이 엔드포인트도 그 재료 중 하나입니다.

> **✅ 확인 문제**
>
> 1. 보안 그룹에 22번이 없는데 Session Manager로 들어갈 수 있는 이유는?
> 2. 서버 안의 `aws` 명령은 자격 증명을 어디서 얻나요?
> 3. IMDSv2가 SSRF를 어렵게 만드는 방법은?
> 4. 삭제(AccessDenied)와 EC2 조회(UnauthorizedOperation)가 막힌 이유의 차이는?
>
> <details><summary>정답</summary>
>
> 1. 서버의 SSM 에이전트가 밖으로 AWS에 연결을 열어 두고, 그 연결로 들어오기 때문 (인바운드 포트 불필요)
> 2. 인스턴스 메타데이터(169.254.169.254)의 역할 임시 자격 증명 — SDK · CLI가 자동으로 쓴다
> 3. 먼저 PUT으로 토큰을 받아 헤더에 넣어야 해서 단순 GET만 흉내 내는 SSRF로는 얻기 어렵다
> 4. 삭제는 명시적 Deny에 걸렸고, EC2 조회는 Allow가 없어 암묵적으로 거절됐다
>
> </details>

## 참고 문헌

- AWS Docs. *AWS Systems Manager Session Manager*. docs.aws.amazon.com/systems-manager
- AWS Docs. *Use IMDSv2*, *Retrieve security credentials from instance metadata*. docs.aws.amazon.com/AWSEC2
- AWS Docs. *Blocking public access to your Amazon S3 storage*. docs.aws.amazon.com/AmazonS3
- OWASP (2021). *A10:2021 – Server-Side Request Forgery*. owasp.org/Top10
