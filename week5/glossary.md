# Week 5 Glossary

| 용어 | 의미 | 운영 확인 지점 |
|---|---|---|
| AWS account | AWS resource와 billing이 귀속되는 최상위 경계 | Account ID, Billing console, IAM |
| root user | 계정 생성 시 생기는 최상위 권한 identity | root login 사용 여부, MFA 설정 |
| IAM | AWS identity와 permission을 관리하는 서비스 | users, groups, roles, policies |
| MFA | 비밀번호 외 추가 인증 요소 | root/IAM user MFA device |
| Region | AWS resource가 위치하는 지리적 영역 | console 오른쪽 위 Region selector |
| Availability Zone | 한 Region 안의 격리된 데이터센터 묶음 | subnet AZ, EC2 placement |
| VPC | AWS 안의 격리된 virtual network | VPC ID, CIDR, subnet |
| Subnet | VPC CIDR을 나눈 network 구역 | public/private subnet, route table |
| Internet Gateway | VPC가 internet과 통신할 수 있게 하는 gateway | route table target |
| Route Table | subnet traffic의 다음 경로를 정하는 표 | `0.0.0.0/0` target |
| Security Group | resource 단위 stateful firewall | inbound/outbound rules |
| EC2 | AWS virtual server 서비스 | instance state, AMI, type, public IP |
| AMI | EC2 instance를 만들 때 쓰는 machine image | launch template/source image |
| Key Pair | EC2 SSH 접속에 쓰는 key material | `.pem` file, EC2 key pair name |
| User Data | EC2 최초 부팅 시 실행할 bootstrap script | instance details, system log |
| S3 | object storage 서비스 | bucket, object, public access block |
| Public Access Block | S3 public access를 상위에서 차단하는 안전장치 | bucket/account setting |
| Budget | 비용 또는 사용량 기준 알림 | AWS Budgets dashboard |
| Cost Explorer | 비용과 사용량을 분석하는 도구 | service별 cost graph |
| CloudWatch | logs, metrics, alarms, dashboard 서비스 | log group, metric, alarm |
| CloudTrail | AWS API 활동 기록 서비스 | event history, user, source IP |
| Tag | resource metadata | cost allocation, owner, cleanup |
| Stop | EC2 compute 과금은 멈추지만 EBS 등 일부 비용은 남을 수 있는 상태 | instance state, attached EBS |
| Terminate | EC2 instance 삭제. 복구할 수 없는 영구 작업 | termination confirmation |
| ALB | Application Load Balancer. HTTP/HTTPS traffic을 target group으로 분산한다 | listener, target group, DNS name |
| Listener | ALB가 요청을 받을 protocol/port와 rule | HTTP 80, HTTPS 443 |
| Target Group | ALB가 traffic을 보낼 대상 묶음 | registered targets, health check |
| Health Check | target이 traffic을 받을 수 있는지 주기적으로 확인하는 설정 | healthy/unhealthy reason |
| User Data | EC2 최초 부팅 때 실행할 bootstrap script | instance launch details, system log |
| EC2 Instance Connect | browser 또는 CLI 기반 EC2 접속 방식 | EC2 Connect tab |
| Public Subnet | route table에 internet gateway 경로가 있는 subnet | `0.0.0.0/0 -> igw-*` |
| Private Subnet | internet gateway로 직접 route하지 않는 subnet | route table, NAT 필요 여부 |
| ECR | Elastic Container Registry. container image를 저장하는 AWS registry | repository, image tag, push command |
| ECS | Elastic Container Service. container task와 service를 실행하는 AWS orchestration service | cluster, task definition, service |
| App Runner | source code 또는 container image에서 web service를 실행하는 managed service | service, deployment, logs |
| Task Definition | ECS task를 실행하기 위한 image, port, env, resource 정의 | revision, container definition |
| ECS Service | task를 desired count만큼 유지하고 load balancer와 연결할 수 있는 단위 | desired/running count |
| Desired Count | service가 유지하려는 task 수 | desired count, running count |
| Container Port | container 안 process가 listen하는 port | task definition, target group |
| Image Tag | image version을 가리키는 tag | `latest`, semantic tag, digest |
| Rollback | 실패한 배포를 이전 정상 image/tag 또는 revision으로 되돌리는 작업 | previous task definition, deployment history |
| Bucket Policy | S3 bucket에 붙는 resource 기반 접근 정책 | Permissions tab, policy JSON |
| Object Key | S3 object를 식별하는 경로형 이름 | object detail, URL |
| S3 Versioning | 같은 object key의 여러 version을 보존하는 기능 | bucket Properties, object versions |
| Delete Marker | versioning이 켜진 bucket에서 삭제 상태를 표시하는 marker | object versions view |
| Lifecycle Rule | S3 object 전환과 만료를 자동화하는 규칙 | Management tab, transition/expiration |
| Storage Class | S3 object의 비용/접근 특성을 정하는 등급 | object details, lifecycle transition |
| RDS | managed relational database service | DB instance, endpoint, backups |
| DB Instance | RDS에서 database engine이 실행되는 관리 단위 | instance class, status, endpoint |
| DB Subnet Group | RDS가 사용할 subnet 묶음 | RDS connectivity settings |
| Automated Backup | RDS가 retention 기간 동안 관리하는 자동 백업 | Maintenance & backups |
| Manual Snapshot | 사용자가 명시적으로 남기는 RDS 백업 지점 | RDS Snapshots |
| Deletion Protection | RDS instance의 실수 삭제를 막는 설정 | DB instance configuration |
| Final Snapshot | RDS 삭제 시 마지막으로 남길 수 있는 snapshot | delete database dialog |
| Secrets Manager | secret 값을 저장, 접근 제어, rotation할 수 있는 AWS 서비스 | secret details, IAM permission |
| Secret Rotation | credential을 주기적으로 교체하는 절차 | rotation configuration |
| Cost Allocation Tag | 비용을 owner, course, purpose 등으로 분류하기 위한 tag | Billing tag activation, Cost Explorer |
| Runbook | 반복 가능한 운영 절차를 정리한 문서 | trigger, action, verification, cleanup |
| Incident | 서비스 영향이 있는 장애 또는 운영 이벤트 | symptom, scope, evidence, action |
| Postmortem | 장애 후 원인, 영향, 대응, 예방책을 정리하는 리뷰 | timeline, contributing factors, follow-up |
| Evidence Packet | 운영 판단을 뒷받침하는 screenshot, log, metric, event, cost 자료 묶음 | portfolio README, evidence folder |
| Security Review | 접근 권한, 공개 범위, secret, audit 상태를 점검하는 절차 | MFA, IAM, SG, public endpoint, CloudTrail |
| FinOps | cloud 비용을 owner, usage, value 기준으로 관리하는 운영 관점 | Budget, Cost Explorer, tag, forecast |
| Handoff Note | 다음 운영자 또는 다음 수업으로 넘길 상태와 판단 기록 | retained resources, next action, owner |
| Resource Inventory | 계정 안에 남아 있는 resource 목록과 상태 | service list, tag, cost 후보 |
