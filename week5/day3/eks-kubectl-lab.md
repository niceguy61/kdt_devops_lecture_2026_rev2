# Optional Lab: EKS cluster and kubectl connection

이 실습은 Week4에서 배운 Kubernetes 조작 경험을 AWS의 managed Kubernetes인 Amazon EKS로 연결하는 선택 심화 경로다. 기본 W5D3 수업은 ECR, ECS 또는 App Runner, CloudWatch 중심으로 진행한다. EKS는 control plane, node, VPC, IAM, log, 비용 영향이 크므로 강사 계정 또는 비용 통제가 가능한 실습 계정에서만 진행한다.

## 실습 목표
- IAM User access key로 AWS CLI identity를 확인한다.
- Amazon EKS cluster와 local `kubectl`의 연결 경계를 이해한다.
- `aws eks update-kubeconfig`가 kubeconfig에 무엇을 추가하는지 확인한다.
- `kubectl get nodes`, `kubectl get ns`, `kubectl apply`로 EKS cluster 접근을 검증한다.
- 실습 종료 후 cluster, node, load balancer, log, ECR image 잔여 비용을 점검한다.

## 공식 문서 근거
| 주제 | 공식 문서 | 수업에서 볼 질문 |
|---|---|---|
| kubectl 연결 | https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html | kubeconfig는 어떤 cluster endpoint와 AWS identity를 연결하는가 |
| EKS Auto Mode CLI 시작 | https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-cli.html | cluster 생성에는 어떤 IAM/VPC/node 비용 책임이 붙는가 |
| Cluster API server endpoint | https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html | public endpoint와 private endpoint는 어떤 보안 경계를 만드는가 |
| IAM user access key | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html | programmatic access key는 어떻게 만들고 보호하는가 |
| AWS CLI configuration | https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html | access key, default Region, output format은 어디에 저장되는가 |
| Least privilege 준비 | https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html | 랩 이후 AdministratorAccess를 어떻게 줄일 것인가 |

## 인증 원칙
이번 EKS lab은 일단 IAM User Credential을 기본 경로로 사용한다. 랩이 권한 문제로 틀어지지 않게 실습용 IAM user에 `AdministratorAccess` managed policy를 붙인다. 이 방식은 운영 권장 최종 상태가 아니라 교육용 시작점이다.

수업 뒤에는 반드시 least privilege로 줄인다. 예를 들어 EKS cluster 생성/조회, EC2/VPC 관련 리소스, IAM role pass/create, CloudWatch Logs, ECR 등 실제 lab에 필요한 권한만 남기는 방향으로 별도 보강에서 축소한다. 지금은 실습 흐름을 안정적으로 통과하는 것이 우선이다.

## 준비 조건
| 항목 | 확인 명령 또는 화면 |
|---|---|
| IAM user | IAM Console에서 lab 전용 user 생성 |
| AdministratorAccess | lab 전용 user에 `AdministratorAccess` managed policy 연결 |
| Access key | IAM user의 Security credentials 탭에서 access key 생성 |
| AWS CLI profile | `aws configure`로 `default` profile 설정 |
| 현재 identity | `aws sts get-caller-identity` 또는 `aws sts get-caller-identity --profile default` |
| AWS CLI version | `aws --version` |
| kubectl version | `kubectl version --client` |
| Region | `ap-northeast-2` 또는 강사가 지정한 Region |
| IAM 권한 | EKS cluster 조회, kubeconfig 생성, 필요한 경우 EKS/IAM/VPC/EC2 생성 권한 |

민감 정보는 캡처하지 않는다. CLI 출력에서 account ID와 ARN은 수업 evidence로 쓸 수 있지만, access key ID, secret access key, token 값은 기록하지 않는다.

## IAM user와 access key 만들기
이 절차는 root user로 장기 작업을 하기 위한 것이 아니다. root user는 가능하면 쓰지 않고, 관리자 권한을 가진 lab 전용 IAM user를 만들어 CLI 실습에 사용한다.

1. AWS Console에서 IAM으로 이동한다.
2. 왼쪽 메뉴에서 Users를 연다.
3. Create user를 선택한다.
4. User name에 `paperclip-eks-admin`처럼 수업용 이름을 입력한다.
5. Console access는 필요할 때만 켠다. CLI lab만 한다면 access key가 핵심이다.
6. Permissions 단계에서 Attach policies directly를 선택한다.
7. `AdministratorAccess`를 선택한다.
8. Review and create에서 user 이름과 policy를 확인하고 생성한다.
9. 생성된 user의 Security credentials 탭으로 이동한다.
10. Access keys 섹션에서 Create access key를 선택한다.
11. Use case는 Command Line Interface 또는 CLI를 선택한다.
12. 안내 문구를 확인하고 access key를 생성한다.
13. Access key ID와 Secret access key를 한 번만 안전하게 확인한다.

Secret access key는 다시 볼 수 없다. 노트, GitHub, README, screenshot, 메신저에 붙이지 않는다. 필요한 경우 AWS가 제공하는 CSV를 임시로 내려받되, 수업 종료 후 안전하게 삭제하거나 credential vault에 옮긴다.

## AWS CLI default profile 설정
실습은 일단 `default` profile을 사용한다. 이미 다른 실습 계정이 `default`에 들어 있다면 덮어쓰기 전에 `aws sts get-caller-identity`로 현재 계정을 확인한다.

```bash
aws configure
```

입력값:

```text
AWS Access Key ID [None]: <Access key ID>
AWS Secret Access Key [None]: <Secret access key>
Default region name [None]: ap-northeast-2
Default output format [None]: json
```

설정 후 확인:

```bash
aws sts get-caller-identity
aws configure list
```

확인할 것:

| 항목 | 기대 |
|---|---|
| `Account` | 실습 계정 ID |
| `Arn` | `user/paperclip-eks-admin` 또는 실습용 IAM user ARN |
| `region` | `ap-northeast-2` |
| `access_key` | 일부만 masking되어 표시 |

로컬에는 보통 `~/.aws/credentials`와 `~/.aws/config`에 profile 정보가 저장된다. Windows에서는 사용자 홈 아래 `.aws` 폴더에 저장된다. 파일을 열어볼 수는 있지만 secret 값을 캡처하거나 커밋하지 않는다.

## 변수 예시
Bash 또는 macOS/Linux shell:

```bash
export AWS_PROFILE=default
export AWS_REGION=ap-northeast-2
export CLUSTER_NAME=paperclip-w5d3-eks
```

PowerShell:

```powershell
$env:AWS_PROFILE="default"
$env:AWS_REGION="ap-northeast-2"
$env:CLUSTER_NAME="paperclip-w5d3-eks"
```

## 경로 A: 이미 있는 EKS cluster에 kubectl 연결
이미 생성된 실습용 cluster가 있다면 이 경로를 우선 사용한다. cluster 생성 비용과 대기 시간을 피하면서 kubeconfig와 kubectl 연결 개념을 볼 수 있다.

```bash
aws sts get-caller-identity --profile "$AWS_PROFILE"
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --query "cluster.{name:name,status:status,endpoint:endpoint,version:version}"
aws eks update-kubeconfig \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --alias "$CLUSTER_NAME"
kubectl config current-context
kubectl get nodes
kubectl get ns
```

읽을 지점:

| 출력 | 의미 |
|---|---|
| `describe-cluster.status` | EKS control plane이 접근 가능한 상태인가 |
| `endpoint` | Kubernetes API server 주소 |
| `kubectl config current-context` | 현재 kubectl이 어느 cluster를 바라보는가 |
| `kubectl get nodes` | workload를 실행할 node가 준비되었는가 |

## 경로 B: 새 EKS cluster 생성은 강사 주도
새 cluster 생성은 비용과 권한 영향이 크다. 학생 개인 계정에서는 기본적으로 시뮬레이션이나 강사 화면 공유로 진행하고, 실제 생성은 강사가 명시적으로 승인한 경우에만 한다.

생성 흐름은 다음 질문을 중심으로 읽는다.

| 결정 | 확인 질문 |
|---|---|
| Cluster mode | Auto Mode 또는 managed node group 중 무엇을 사용할 것인가 |
| VPC/subnet | default VPC를 쓸 것인가, 전용 VPC를 만들 것인가 |
| IAM role | cluster role과 node role의 권한 범위는 무엇인가 |
| Endpoint access | public endpoint를 열 것인가, private access를 쓸 것인가 |
| Cleanup | cluster와 node, load balancer, EBS volume, log group을 어떻게 지울 것인가 |

## 검증 workload
연결이 된 뒤에는 작은 Deployment와 Service만 배포한다. LoadBalancer type은 실제 cloud load balancer 비용을 만들 수 있으므로 기본 검증은 `ClusterIP`와 `kubectl port-forward`로 한다.

```bash
kubectl create namespace paperclip-eks
kubectl create deployment hello-eks \
  --namespace paperclip-eks \
  --image=nginx:1.27
kubectl expose deployment hello-eks \
  --namespace paperclip-eks \
  --port=80 \
  --target-port=80
kubectl get deploy,svc,pod -n paperclip-eks
kubectl port-forward -n paperclip-eks svc/hello-eks 18080:80
```

다른 terminal에서 확인:

```bash
curl http://localhost:18080
```

## Evidence Note
```markdown
# W5D3 Optional EKS kubectl lab
- AWS profile:
- Region:
- Cluster name:
- Cluster status:
- Kubernetes version:
- kubeconfig context:
- kubectl 검증 명령:
- workload namespace:
- cleanup 상태:
- 비용 또는 보안 주의:
```

## 흔한 실패와 첫 확인 위치
| 증상 | 첫 확인 위치 |
|---|---|
| `kubectl`이 다른 cluster를 본다 | `kubectl config current-context` |
| `You must be logged in to the server` | `aws sts get-caller-identity`, access key 상태, kubeconfig user exec 설정 |
| `AccessDenied` | IAM user policy, EKS access entry 또는 aws-auth 설정 |
| node가 안 보인다 | node group, Auto Mode node 상태, subnet/instance quota |
| public endpoint 접근이 안 된다 | EKS endpoint access 설정과 로컬 네트워크 |

## Cleanup
```bash
kubectl delete namespace paperclip-eks
kubectl config get-contexts
kubectl config delete-context "$CLUSTER_NAME"
```

cluster를 직접 생성했다면 Console 또는 생성 도구에서 다음 항목을 끝까지 확인한다.

| Resource | 확인 |
|---|---|
| EKS cluster | 삭제 완료 또는 유지 사유 |
| Node group / Auto Mode nodes | EC2 instance 잔여 여부 |
| Load balancer | Service type LoadBalancer를 만들었다면 삭제 여부 |
| EBS volume | node나 workload가 만든 volume 잔여 여부 |
| CloudWatch log group | retention 또는 삭제 여부 |
| IAM role/policy | 실습용 권한 잔여 여부 |
| IAM access key | 수업 후 비활성화 또는 삭제 여부 |

## 수업 후 권한 줄이기
이번 lab은 AdministratorAccess로 시작하지만 그대로 오래 두지 않는다.

수업 종료 후 최소한 다음 중 하나를 수행한다.

| 조치 | 목적 |
|---|---|
| access key 비활성화 | 즉시 CLI 사용을 멈춘다 |
| access key 삭제 | 유출 위험을 제거한다 |
| IAM user 삭제 | lab 전용 identity를 정리한다 |
| AdministratorAccess 제거 | 남겨야 한다면 권한을 줄인다 |
| least privilege policy 재설계 | EKS, EC2, IAM, CloudWatch, ECR 중 필요한 action만 허용한다 |

## 한 줄 요약
```text
EKS 실습의 핵심은 cluster 생성 자체가 아니라 IAM user credential, kubeconfig, Kubernetes API endpoint, kubectl evidence, cleanup 비용을 한 흐름으로 연결하고, 수업 뒤 AdministratorAccess를 줄이는 것이다.
```
