# 실제 실행 검증 기록

검증일: 2026-07-12 (Asia/Seoul)

## 네트워크와 EKS

| 검증 항목 | 실제 결과 |
|---|---|
| VPC | `10.42.0.0/16` |
| Public subnet | `2a: 10.42.1.0/24`, `2b: 10.42.2.0/24`, `2c: 10.42.3.0/24` |
| Private subnet | `2a: 10.42.11.0/24`, `2b: 10.42.12.0/24`, `2c: 10.42.13.0/24` |
| Managed Node Group | `ACTIVE`, 세 private subnet을 대상으로 구성 |
| 실제 Node | `Ready`, private IP `10.42.12.169`, `ap-northeast-2b` |
| 검증 Pod | `Running`, private IP `10.42.12.81` |

최초 2-AZ로 만든 검증 Cluster에 세 번째 AZ subnet을 추가하려 했을 때 EKS가 `exact set of AZs` 오류로 거부했다. 기존 AZ 집합은 확장할 수 없다는 운영 제약을 확인했다. 최종 예제의 신규 생성 기본값은 처음부터 3-AZ다.

## IRSA

ServiceAccount annotation과 Pod의 STS 결과를 비교했다.

```text
ServiceAccount role:
arn:aws:iam::<account-id>:role/tf-eks-irsa-lab-irsa-reader

Pod caller identity:
arn:aws:sts::<account-id>:assumed-role/tf-eks-irsa-lab-irsa-reader/<session>
```

Node IAM Role이 아니라 IRSA 전용 Role이 반환됐으므로 통과다. 실제 계정 번호와 세션 ID는 강의 증적에서 마스킹했다.

## State 기반 그림

`terraform show -json`과 AWS 조회 결과에서 AZ, CIDR, subnet ID, NAT ID, Node Group 대상 subnet을 추출했다. 그 값을 [`assets/eks-irsa-architecture.drawio`](./assets/eks-irsa-architecture.drawio)에 반영하고 PNG로 변환했다.

## Drift 메모

IRSA admission webhook은 Pod 생성 후 `AWS_ROLE_ARN`, `AWS_WEB_IDENTITY_TOKEN_FILE`, projected token volume을 주입한다. 이는 외부 변경이 아니라 서버 관리 필드이므로 검증 Pod의 해당 필드만 `ignore_changes` 처리했다. 일반 애플리케이션 전체에 포괄적인 `ignore_changes`를 적용하라는 의미는 아니다.

## 삭제 검증

저장한 Destroy Plan은 `0 added, 0 changed, 63 destroyed`였고 적용 완료 후 다음을 확인했다.

| 확인 대상 | 결과 |
|---|---|
| Terraform state | 빈 목록 |
| EKS Cluster | `ResourceNotFoundException` |
| IRSA IAM Role | `NoSuchEntity` |
| 삭제되지 않은 NAT Gateway | 빈 목록 |
| `terminated`가 아닌 실습 EC2 | 빈 목록 |

따라서 이 실행에서는 생성 → Node/Pod/IRSA 검증 → no-change → 전체 삭제 흐름이 실제로 완료됐다.
