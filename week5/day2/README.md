# Week 5 Day 2: AWS 네트워크와 EC2/ALB 운영

## Overview
W5D2는 W5D1에서 만든 AWS 운영 좌표계를 실제 traffic 흐름으로 연결한다. 오늘의 목표는 EC2를 하나 띄우는 데서 끝나지 않는다. 학생은 VPC, public subnet, route table, internet gateway, public IP, Security Group, EC2 web server, ALB, target group, health check를 하나의 요청 경로로 설명해야 한다.

오늘 만드는 resource는 비용이 발생할 수 있다. 특히 ALB는 켜져 있는 시간 동안 비용이 발생할 수 있으므로 수업 종료 전 삭제 또는 유지 사유를 반드시 남긴다.

## Learning Goals
- public subnet이 internet gateway route와 public IP 조건으로 동작한다는 점을 설명한다.
- EC2 launch 시 AMI, instance type, key pair, subnet, public IP, Security Group, tag, user data를 확인한다.
- Security Group rule을 이용해 SSH/HTTP 접속 실패를 분석한다.
- ALB, listener, target group, health check의 역할을 구분한다.
- EC2 instance status, system log, target health, browser/curl 결과를 운영 evidence로 남긴다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day1 요약 + AWS 네트워크 실습 지도 | VPC, public/private subnet, route table, IGW, SG |
| 2교시 | EC2 Console 실습 | AMI, instance type, key pair, subnet, public IP, tag |
| 3교시 | EC2 웹 서버 실행 | user data, HTTP response, public IP/curl |
| 4교시 | Security Group 장애 분석 | 22/80 port, source CIDR, wrong rule, recheck |
| 5교시 | Load Balancing 개념 | ALB, listener, target group, health check, public/private |
| 6교시 | ALB Console 실습 | target group, registered target, ALB DNS 접속 |
| 7교시 | EC2/ALB 운영 관찰 | instance status, system log, target health, failure evidence |
| 8교시 | 구름 EXP 배움일기 | VPC/EC2/SG/ALB evidence와 cleanup |

## Practice Files
| 자료 | 용도 |
|---|---|
| `academic-foundations.md` | 공식 문서 기반 개념 근거와 읽을 키워드 |
| `lesson-01.md` ~ `lesson-08.md` | 교시별 강의 자료 |
| `assets/lesson-01-network-lab-map.png` | Day2 network lab overview |
| `assets/lesson-02-ec2-launch-checklist.png` | EC2 launch checklist |
| `assets/lesson-03-ec2-user-data-web.png` | user data와 web server 흐름 |
| `assets/lesson-04-security-group-debug.png` | Security Group 장애 분석 |
| `assets/lesson-05-alb-concepts.png` | ALB/listener/target group 개념 |
| `assets/lesson-06-alb-console-flow.png` | ALB Console 실습 흐름 |
| `assets/lesson-07-operations-observation.png` | EC2/ALB 운영 관찰 |
| `assets/lesson-08-cleanup-journal.png` | 배움일기와 cleanup board |

## Official References
| Topic | Reference |
|---|---|
| Internet Gateway and public subnet | https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html |
| Subnet route tables | https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html |
| VPC subnet types | https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html |
| EC2 key pairs | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html |
| EC2 Instance Connect | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html |
| EC2 user data | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html |
| EC2 security groups | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html |
| Application Load Balancer | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html |
| ALB target groups | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html |
| ALB target health checks | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html |

## Preparation Checklist
- W5D1 account safety checklist 완료
- 실습 Region: `ap-northeast-2`
- Budget 또는 비용 알림 확인
- key pair 생성/보관 정책 확인
- EC2 Instance Connect 사용 가능 여부 확인
- 오늘 사용할 공통 tag 준비
- 수업 종료 전 ALB/target group/EC2/Security Group 삭제 시간을 확보

## Deliverables
- VPC/public subnet/route table/IGW evidence
- EC2 launch configuration note
- user data 또는 직접 설치 기반 HTTP response evidence
- Security Group 장애 분석 note
- ALB DNS 접속 또는 target health evidence
- cleanup checklist

## End Of Day Checklist
- EC2 instance를 stop 또는 terminate했고 사유를 남겼는가
- ALB, target group, listener를 삭제했는가
- EBS volume, Elastic IP, Security Group, key pair 잔여 상태를 확인했는가
- Budget/Cost Explorer에서 오늘 생성한 비용 지점을 설명할 수 있는가
- Day3 컨테이너 실행 서비스로 넘어가기 전에 image, port, health check 개념을 연결할 수 있는가
