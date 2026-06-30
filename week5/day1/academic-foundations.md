# Week 5 Day 1 Academic And Official Foundations

## 공식 문서 기준
AWS 수업은 Console 화면 암기보다 공식 문서에서 운영 기준을 찾는 능력이 중요하다. 오늘은 다음 공식 문서의 키워드를 기준으로 계정 안전, Region, network, storage, 비용, 감사 로그를 연결한다.

| 주제 | 공식 문서 | 읽을 키워드 |
|---|---|---|
| root user | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html | root user, highly privileged, don't access unless required |
| MFA | https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-mfa-for-root.html | MFA device, root user credentials |
| Region/AZ | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html | separate geographic area, isolated locations |
| Security Group | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html | inbound, outbound, stateful, VPC |
| S3 Block Public Access | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html | account, bucket, override public policies |
| Budget | https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html | cost budget, notification, permissions |
| Cost Explorer | https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html | view and analyze costs and usage |
| CloudTrail | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html | operational auditing, governance, event |
| EC2 lifecycle | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html | stopped, terminated, EBS charges |

## Workforce 기준 연결
| 역량 | 오늘의 행동 | Evidence |
|---|---|---|
| 운영 안전 | root user와 IAM user/role의 사용 범위를 구분한다 | 계정 안전 checklist |
| 비용 인식 | resource 생성 전에 비용 발생 지점과 Budget을 확인한다 | Budget/Cost Explorer note |
| 장애 경계 이해 | Region/AZ를 위치가 아니라 failure boundary로 설명한다 | Region/AZ mapping |
| 접근 제어 | Security Group inbound/outbound rule을 읽는다 | SG rule 관찰 note |
| 감사 가능성 | 누가 어떤 API를 호출했는지 CloudTrail에서 찾을 수 있음을 이해한다 | CloudTrail event history note |

## 오늘의 판단 기준
- "만들 수 있다"보다 "누가, 어디에, 어떤 권한과 비용으로 만들었는가"를 먼저 확인한다.
- public access는 기본값과 exception을 구분한다.
- stop과 terminate는 비용과 복구 가능성 기준으로 구분한다.
- Region은 단순히 가까운 위치가 아니라 장애 범위, 서비스 지원 여부, 비용, data residency를 함께 보는 선택이다.
