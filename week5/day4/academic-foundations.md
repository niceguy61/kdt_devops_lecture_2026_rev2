# Week 5 Day 4 Academic Foundations

## 학습 근거
Storage와 database는 compute보다 운영 책임이 무겁다. EC2 instance나 container task는 재생성할 수 있지만, S3 object와 RDS database는 데이터 보존, 공개 범위, backup, restore, 비용, 법적 책임과 연결된다. 그래서 W5D4는 resource 생성보다 안전한 접근, 복구 가능성, 비용 회수, credential 보호를 중심으로 본다.

## 공식 문서 읽기 키워드
| 주제 | 공식 문서에서 확인할 키워드 | 수업에서 연결할 질문 |
|---|---|---|
| S3 Block Public Access | account-level, bucket-level, public policy, ACL | 공개가 필요한가, 아니면 임시 실습인가 |
| S3 Versioning | version ID, delete marker, suspended | 삭제가 정말 삭제인가, 이전 버전은 남는가 |
| S3 Lifecycle | transition, expiration, storage class | 오래된 object는 비용을 계속 만드는가 |
| RDS subnet group | VPC, subnet, Availability Zone | DB가 public internet에 노출될 필요가 있는가 |
| RDS backup | automated backup, backup retention, point-in-time restore | 장애 후 어느 시점으로 되돌릴 수 있는가 |
| RDS deletion protection | final snapshot, delete workflow | 삭제 전 마지막 복구 지점을 남길 것인가 |
| Secrets Manager | secret value, rotation, IAM policy | credential이 코드와 노트에 남지 않는가 |
| Cost Explorer | service filter, tag filter, time range | 어떤 resource가 비용을 만들었는가 |

## AWS 공식 자료
- Amazon S3 Block Public Access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
- Amazon S3 bucket policies: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html
- Amazon S3 Versioning: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
- Managing your storage lifecycle: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
- Amazon RDS DB instances: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.html
- Working with a DB instance in a VPC: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html
- Working with automated backups: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html
- Deleting a DB instance: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_DeleteInstance.html
- AWS Secrets Manager User Guide: https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html
- Cost allocation tags: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html
- What is Cost Explorer: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html

## 운영 판단 기준
| 판단 | 좋은 기준 | 위험한 기준 |
|---|---|---|
| S3 공개 | 필요한 path만 제한적으로 공개하고 public access 근거를 남긴다 | 실습 편의를 위해 bucket 전체를 공개한다 |
| RDS 접근 | application SG에서 DB port로만 허용한다 | DB port를 `0.0.0.0/0`에 연다 |
| backup | retention, snapshot, restore 기준을 함께 기록한다 | backup이 켜져 있을 것이라고 추측한다 |
| secret | IAM permission과 audit event로 접근을 통제한다 | password를 README, screenshot, git에 남긴다 |
| cost | tag와 service filter로 비용 원인을 추적한다 | Console에서 눈에 보이는 resource만 삭제한다 |
