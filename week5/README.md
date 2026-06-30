# Week 5: AWS 운영 집중

## Overview
Week 5는 Docker, MSA, GitHub Actions, Kubernetes 운영에서 배운 개념을 AWS 계정 안의 실제 cloud resource로 연결한다. 목표는 서비스를 "한 번 띄우는 것"이 아니라, 누가 접근할 수 있고, 어디에 생성되었고, 비용이 어떻게 발생하며, 장애가 났을 때 어떤 증거를 볼 수 있는지 설명하는 것이다.

Terraform/IaC는 본과정에서 분리하고 별도 보강 수업으로 다룬다. 이번 주는 AWS Console과 운영 증거를 기준으로 cloud resource 감각을 먼저 만든다.

## Learning Goals
- AWS 계정 안전장치, IAM, MFA, Budget, Region/AZ, VPC의 운영 경계를 설명한다.
- EC2, Security Group, ALB, ECR/ECS 또는 App Runner, S3, RDS, CloudWatch를 운영 관점으로 연결한다.
- 비용이 발생하는 지점을 예측하고, Budget, Cost Explorer, tag 기반 비용 추적의 필요성을 설명한다.
- Kubernetes의 Service, Ingress, Secret, PV/PVC, observability 개념을 AWS managed service와 비교한다.
- AWS 운영 runbook과 cleanup checklist를 작성한다.

## Schedule Index
| 일차 | 주제 | 핵심 확인 |
|---|---|---|
| Day1 | AWS 계정 안전과 운영 좌표계 | root/MFA, IAM, Budget, Region/AZ, VPC, EC2, S3 preview |
| Day2 | AWS 네트워크와 EC2/ALB | VPC, subnet, route table, security group, EC2, ALB health check |
| Day3 | AWS 컨테이너 실행과 관찰 | ECR, ECS 또는 App Runner, service update, CloudWatch Logs/Metrics |
| Day4 | AWS storage/database/security/cost | S3, RDS, secret, public access, backup/delete protection, 잔여 비용 |
| Day5 | AWS 통합 운영 실습 | dashboard, FinOps, security review, 장애 분석, runbook, portfolio packet |

## Deliverables
- AWS 서비스 매핑 표: compute, network, storage, database, observability, billing
- AWS 계정 안전장치 체크리스트: MFA, IAM, Budget, Region, tag, cleanup
- EC2/Security Group/ALB 실습 evidence
- ECR/ECS 또는 App Runner 실습 evidence
- S3/RDS 실습 또는 시뮬레이션 evidence
- CloudWatch Logs/Metrics/Alarm/Dashboard 확인 흐름
- AWS 운영 runbook과 cleanup checklist
- 전체 과정 portfolio packet 초안

## Environment And Cost Preparation
- 개인 또는 실습용 AWS 계정에 로그인할 수 있어야 한다.
- root 계정에는 MFA를 설정하고, 실습 중에는 root user를 사용하지 않는 것을 원칙으로 한다.
- 실습 Region은 기본적으로 `ap-northeast-2` 서울 리전을 사용한다. 다른 Region을 쓰면 모든 evidence에 Region을 명시한다.
- Budget 또는 비용 알림을 먼저 확인한다.
- 공통 tag 예시: `Course=paperclip`, `Week=5`, `Owner=<student-id>`, `Purpose=lab`.
- 실습 종료 전 EC2, ALB, EIP, NAT Gateway, RDS, S3 object, CloudWatch log retention 등 잔여 비용 지점을 확인한다.

## Official References
| Topic | Reference |
|---|---|
| AWS account root user best practices | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| MFA for AWS account root user | https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-mfa-for-root.html |
| AWS Regions and Availability Zones | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html |
| VPC Security Groups | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html |
| S3 Block Public Access | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html |
| AWS Budgets | https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html |
| Cost Explorer | https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html |
| CloudTrail | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html |

## Glossary
Week 5 용어는 [glossary.md](./glossary.md)를 기준으로 정리한다. 용어를 외우기보다 "어떤 화면, 어떤 이벤트, 어떤 비용 항목으로 확인하는가"를 함께 본다.

## Next Step
Week 5 이후 Terraform 보강 수업에서는 이번 주에 Console로 이해한 AWS resource를 코드로 재현한다. Terraform은 AWS 개념을 대신 배우는 도구가 아니라, 이미 이해한 resource 구성을 재현 가능하게 만드는 도구로 다룬다.
