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
