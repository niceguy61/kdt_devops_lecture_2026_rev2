# 4교시 · AWS CLI와 aws login

!!! goal "이번 시간에 할 일"
    - AWS CLI v2를 설치합니다(2.32 이상).
    - **접속 키를 만들지 않고** `aws login`으로 CLI에 로그인합니다.
    - "나는 누구인가"를 CLI로 확인하고, `--query`로 원하는 값만 뽑습니다.
    - 콘솔에서 한 일을 CLI로 **다시 읽어** 봅니다.

## 왜 CLI인가

콘솔은 처음 배우기 좋고, CLI는 **반복 · 기록 · 자동화**에 좋습니다. 3주차에 `kubectl`이 그랬듯, 이번 주 확인 작업은 대부분 CLI로 합니다. 그리고 3일차의 Terraform도 **같은 로그인**을 씁니다.

## 실습 7 · 설치

**Linux · WSL2 Ubuntu (bash)** — x86_64 기준. ARM이면 파일 이름의 `x86_64`를 `aarch64`로 바꿉니다.

```bash
cd /tmp
curl -sSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip -q -o awscliv2.zip
sudo ./aws/install --update
rm -rf aws awscliv2.zip
```

- `unzip`이 없다는 오류가 나면 2주차 1일차의 기본 도구 설치(`sudo apt install -y unzip`)를 먼저 합니다
- `--update` : 이미 깔려 있으면 덮어써 최신으로

**Mac (터미널 · Homebrew)**

```bash
brew install awscli
```

**확인 (공통)**

```bash
aws --version
```

!!! check "확인"
    ```text
    aws-cli/2.3○.○ Python/3.13.○ Linux/6.○ exe/x86_64.ubuntu.24
    ```
    **2.32.0 이상**이어야 `aws login`이 있습니다. 예전에 설치한 v1(`aws-cli/1.…`)이 나오면 `pip uninstall awscli` 후 다시 설치합니다.

!!! tip "다른 설치 방법 — winget · 직접 다운로드"
    | 방법 | 어디서 | 명령 · 주소 |
    |---|---|---|
    | winget | Windows PowerShell | `winget install -e --id Amazon.AWSCLI` |
    | 직접 다운로드 | 브라우저 | Windows `AWSCLIV2.msi` · macOS `AWSCLIV2.pkg` — [설치 안내](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |

    winget은 **Windows 쪽**에 설치하므로 PowerShell에서만 보입니다. 수업 명령은 WSL Ubuntu(bash)에서 치므로, Windows 사용자도 위의 **WSL 방법**으로 설치합니다. Windows에 따로 깐 aws는 자격 증명을 `C:\Users\내이름\.aws`에, WSL의 aws는 `~/.aws`에 저장합니다 — 서로 공유하지 않습니다. 전체 목록은 **부록 A · 도구 설치 가이드**.

## 실습 8 · aws login

```bash
aws login --region ap-northeast-2
```

1. 브라우저가 열리고 AWS 로그인 화면이 나옵니다. 이미 콘솔에 `devops-admin`으로 로그인되어 있으면 **그 세션을 고르기만** 하면 됩니다.
2. "CLI에 자격 증명을 줄까요?" → **허용**.
3. 터미널로 돌아오면 완료 메시지가 보입니다.

!!! tip "WSL · 원격 서버에서 브라우저가 안 열리면"
    `aws login --remote`를 씁니다. 터미널에 나온 **주소**를 내 PC 브라우저에 붙여 넣어 로그인하고, 화면에 나온 **코드**를 터미널에 입력합니다.

```bash
aws sts get-caller-identity
aws configure get region
cat ~/.aws/config
ls ~/.aws/
```

!!! check "확인"
    ```text
    {
        "UserId": "AIDA…",
        "Account": "123456789012",
        "Arn": "arn:aws:iam::123456789012:user/devops-admin"
    }
    ap-northeast-2
    [default]
    login_session = arn:aws:iam::123456789012:user/devops-admin
    region = ap-northeast-2
    config  login
    ```
    - `Arn`이 **user/devops-admin** — 루트가 아닙니다(루트라면 `:root`).
    - `~/.aws/credentials` 파일이 **없습니다.** 영구 키가 디스크에 없다는 뜻입니다. 대신 `~/.aws/login/` 아래 캐시에 **짧게 사는 자격 증명**이 있고, CLI가 15분마다 알아서 바꿉니다. 로그인 세션 자체는 몇 시간 뒤 끝나며, 그때 `aws login`을 다시 합니다.

!!! key "aws configure와 무엇이 다른가"
    예전 교재의 `aws configure`는 IAM 사용자의 **접속 키**(Access Key ID + Secret)를 `~/.aws/credentials`에 **영구히** 적습니다. 노트북을 잃어버리거나, 그 파일이 Git에 들어가면 끝입니다. `aws login`은 콘솔 로그인(MFA 포함)을 그대로 쓰고, 디스크에는 짧은 자격 증명만 남깁니다. 3교시 트렌드의 "사람은 로그인"입니다.

## 실습 9 · CLI로 읽기

`--query`는 JMESPath라는 작은 문법으로 응답 JSON에서 원하는 값만 뽑습니다(4주차 `kubectl -o jsonpath`와 같은 생각).

```bash
aws iam list-groups-for-user --user-name devops-admin --query 'Groups[].GroupName' --output text
aws iam list-attached-group-policies --group-name admins --output table
aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled'
aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName' --output text
aws ec2 describe-vpcs --query 'Vpcs[].[VpcId,CidrBlock,IsDefault]' --output table
```

!!! check "확인"
    ```text
    admins
    ---------------------------------------------------------------------------
    |                        ListAttachedGroupPolicies                        |
    +-------------------------------------------------------------------------+
    ||                           AttachedPolicies                            ||
    |+--------------------------------------------+--------------------------+|
    ||                 PolicyArn                  |       PolicyName         ||
    |+--------------------------------------------+--------------------------+|
    ||  arn:aws:iam::aws:policy/AdministratorAccess|  AdministratorAccess    ||
    …
    1
    ap-northeast-2a  ap-northeast-2b  ap-northeast-2c  ap-northeast-2d
    -----------------------------------------------
    |                DescribeVpcs                 |
    +------------------------+----------------+------+
    |  vpc-0a1b2c3d4e5f6a7b8 |  172.31.0.0/16 | True |
    +------------------------+----------------+------+
    ```
    - 루트 MFA가 **1**(켜짐)입니다.
    - 가용 영역 넷이 보입니다(1교시).
    - 아무것도 안 만들었는데 VPC가 하나 있습니다 — **기본 VPC**(`IsDefault True`, 172.31.0.0/16). 5교시에서 이야기합니다.

```bash
~/devops-lab/aws/w5d1/check-account.sh
```

7교시까지 이 스크립트의 VPC 칸에 내 VPC가 한 줄 늘어나게 됩니다.

!!! tip "Terraform · SDK가 login을 모를 때"
    `aws login` 자격 증명은 최신 AWS SDK와 도구가 읽습니다. 혹시 오래된 도구가 "자격 증명이 없다"고 하면, 지금의 임시 자격 증명을 환경 변수로 꺼내 줍니다.
    ```bash
    eval "$(aws configure export-credentials --format env)"
    env | grep ^AWS_ | sed 's/=.*/=…/'
    ```
    `AWS_ACCESS_KEY_ID`(ASIA로 시작 — 임시 키) · `AWS_SECRET_ACCESS_KEY` · `AWS_SESSION_TOKEN`이 생깁니다. 이 셸에서만, 몇십 분 동안만 유효합니다. 3일차에 다시 씁니다.

!!! academic "학술 노트 — 짧게 사는 자격 증명"
    자격 증명의 수명을 짧게 하는 생각은 MIT의 **Kerberos**(Steiner 외, USENIX 1988)에서 체계화되었습니다. 비밀번호로 한 번 인증하면 몇 시간짜리 **티켓**을 받고, 이후의 접근은 티켓으로 합니다 — 비밀번호는 네트워크에 다시 나가지 않습니다. `aws login` · STS · Kubernetes의 bound token(4주차 5일차)은 모두 이 '티켓' 모델의 후손입니다. 도둑맞아도 **곧 쓸모없어지는** 열쇠가 영구 열쇠보다 안전합니다.

!!! trend "트렌드 2026 — 코딩 에이전트와 클라우드 자격 증명"
    AI 코딩 도구가 터미널에서 `aws` 명령을 실행하는 일이 흔해지면서, "에이전트가 쓰는 자격 증명을 어떻게 좁히나"가 새 주제가 되었습니다. AWS는 새 가입 경험에서 **프로젝트 단위로 AI 도구를 연결**하는 흐름을 내놓았고, 일반적으로는 에이전트에 **읽기 전용 역할**을 주고 쓰기는 사람이 확인하는 방식이 권장됩니다. 오늘 만든 `devops-admin` 세션을 아무 도구에나 그대로 넘기지 않는 습관이 중요합니다.

!!! quiz "확인 문제"
    1. `aws login`과 `aws configure`(접속 키)의 차이는?
    2. `get-caller-identity`의 Arn이 `:root`로 끝나면 무엇을 해야 하나요?
    3. 아무것도 만들지 않았는데 있던 VPC는 무엇인가요?
    4. 임시 자격 증명을 환경 변수로 꺼내는 명령은?

    ??? answer "정답"
        1. login은 콘솔 로그인(MFA 포함)으로 짧게 사는 자격 증명을 받고 자동 교체한다. configure는 영구 키를 파일에 적는다
        2. 루트로 로그인한 것이므로 로그아웃하고 devops-admin으로 다시 로그인한다
        3. 기본 VPC (172.31.0.0/16, IsDefault True)
        4. `aws configure export-credentials --format env`

## 참고 문헌

- AWS Docs. *Installing or updating the latest version of the AWS CLI*. docs.aws.amazon.com/cli
- AWS Docs. *Login for AWS local development using console credentials*. docs.aws.amazon.com/cli
- AWS (2025-11-19). *AWS enables developers to use console credentials for AWS CLI and SDK authentication*. aws.amazon.com/about-aws/whats-new
- Steiner, J. G., Neuman, C. & Schiller, J. I. (1988). *Kerberos: An Authentication Service for Open Network Systems*. USENIX Winter Conference.
