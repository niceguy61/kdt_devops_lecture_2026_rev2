# Week 5 Day 2 Academic And Official Foundations

## 공식 문서 기준
오늘 수업은 AWS network와 load balancing을 실제 traffic evidence로 읽는 날이다. 아래 공식 문서를 기준으로 public subnet, EC2 접속, user data, Security Group, ALB target health를 확인한다.

| 주제 | 공식 문서 | 읽을 키워드 |
|---|---|---|
| Internet Gateway | https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html | public subnet, public IP, internet gateway |
| Route Table | https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html | local route, custom route table, internet gateway route |
| Subnet types | https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html | public subnet, private subnet |
| EC2 key pairs | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html | public key, private key, SSH |
| EC2 Instance Connect | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html | console connect, public IP |
| EC2 user data | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html | launch, script, bootstrap |
| EC2 Security Groups | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html | virtual firewall, inbound, outbound |
| ALB | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html | listener, target group, health check |
| Target groups | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html | registered targets, protocol, port |
| Health checks | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html | healthy, unhealthy, enabled AZ |

## Workforce 기준 연결
| 역량 | 오늘의 행동 | Evidence |
|---|---|---|
| 네트워크 경로 분석 | public IP, route table, IGW, SG를 순서대로 확인한다 | traffic path note |
| 접근 제어 | SSH/HTTP inbound rule을 최소 범위로 설정하고 분석한다 | SG debug note |
| 자동화 기초 | EC2 user data로 bootstrap을 재현한다 | user data/system log |
| 운영 관찰 | instance status와 target health를 연결해 본다 | EC2/ALB evidence |
| 비용 통제 | ALB/EC2/EBS 잔여 비용을 cleanup한다 | cleanup checklist |

## 오늘의 판단 기준
- public subnet은 "이름이 public"이라서가 아니라 route table에 internet gateway 경로가 있어서 public이다.
- EC2에 public IP가 없으면 internet에서 직접 접속할 수 없다.
- Security Group은 application bug보다 먼저 확인해야 하는 network gate다.
- ALB 접속 성공은 target health와 listener/target group 설정이 모두 맞아야 한다.
- cleanup은 선택 과제가 아니라 cloud 실습의 일부다.
