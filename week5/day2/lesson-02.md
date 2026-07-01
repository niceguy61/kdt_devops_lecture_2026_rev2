# 2교시: EC2 Console 실습

![EC2 launch checklist](./assets/lesson-02-ec2-launch-checklist.png)

## 수업 목표
- EC2 launch 화면의 주요 설정을 운영 기준으로 읽는다.
- key pair, subnet, public IP, Security Group, storage, tag를 생성 전 확인한다.
- EC2 Instance Connect와 SSH client 접속 조건을 구분한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Launch checklist | EC2는 클릭 한 번이 아니라 여러 운영 선택의 묶음이다 | 잘못된 subnet/SG/type으로 비용과 접속 문제가 생긴다 | launch summary |
| Key pair | Linux instance 접속 identity material이다 | private key 분실 또는 노출 | key pair name, local file |
| Public IP | internet 직접 접속 조건이다 | instance running인데 외부 접속이 안 된다 | network settings |
| Tag | owner와 cleanup 추적 기준이다 | 실습 resource가 남는다 | Tags tab |

## EC2 launch 순서
Console에서 EC2를 만들 때는 다음 순서로 읽는다.

| 단계 | 확인 |
|---|---|
| Name and tags | `Course=paperclip`, `Week=5`, `Day=2`, `Owner=<id>` |
| AMI | 수업 OS와 명령이 맞는지 |
| Instance type | 비용 통제 가능한 작은 type |
| Key pair | 새로 만들면 안전하게 보관, 기존 key 재사용 시 소유 확인 |
| Network settings | VPC, public subnet, auto-assign public IP |
| Security Group | SSH/HTTP inbound 최소 허용 |
| Storage | root volume size와 delete on termination |
| Advanced details | user data 사용 여부 |

## 접속 방식
AWS 공식 문서 기준으로 EC2 key pair는 public/private key 기반 credential이다. Linux instance에서는 private key로 SSH 접속을 증명한다. EC2 Instance Connect를 사용할 수 있으면 browser 기반 접속도 가능하다.

| 방식 | 장점 | 확인할 것 |
|---|---|---|
| EC2 Instance Connect | browser에서 빠르게 접속 가능 | instance OS/Region/subnet/public IP/SG 조건 |
| SSH client | 현업 환경과 유사 | private key 권한, username, local network |
| Session Manager | 운영 친화적 | SSM agent, IAM role, VPC endpoint 또는 internet route |

Day2는 EC2 Instance Connect 또는 SSH 중 가능한 방식으로 접속한다. 둘 다 실패하면 먼저 Security Group과 public IP를 확인한다.

## Security Group 최소 예시
| 목적 | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | 내 IP 또는 교육장 CIDR |
| HTTP | TCP | 80 | 수업 중 임시 `0.0.0.0/0` 가능, 종료 전 삭제 |

`0.0.0.0/0`은 모든 IPv4 source를 뜻한다. SSH 22를 전체 공개로 오래 유지하지 않는다.

## Evidence Note
```markdown
# W5D2S2 EC2 launch
- Instance name:
- AMI:
- Instance type:
- Key pair:
- VPC/subnet:
- Public IP auto-assign:
- Security Group inbound:
- Tags:
- Storage:
```

## 혼자 다시 따라오기
- 최소 재현 경로: EC2 launch 화면에서 summary까지 값을 채운 뒤, 실제 launch 전 모든 항목을 소리 내어 설명한다.
- 공식 문서 키워드: `EC2 key pairs`, `EC2 Instance Connect`, `launch instance`, `security groups`.
- 스스로 확인할 화면: EC2 launch summary, Instances list, Security tab.
- 흔한 실패 3개: key pair 파일을 잃음, public IP를 끔, default SG에 의존함.
- 다음 준비 상태: launch summary를 보고 비용/접속/cleanup 위험을 설명할 수 있어야 한다.

## 한 줄 요약
```text
EC2 launch는 AMI/type/key/network/SG/storage/tag를 한 번에 결정하는 운영 선택이다.
```
