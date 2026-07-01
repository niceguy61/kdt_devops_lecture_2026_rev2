# 6교시: EC2 첫 관찰

![EC2 observation checklist map](./assets/lesson-06-ec2-observation.png)

## 수업 목표
- EC2 instance를 compute resource 관점으로 읽는다.
- AMI, instance type, key pair, public IP, user data, state를 구분한다.
- stop과 terminate의 비용/복구 차이를 설명한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| AMI | instance의 시작 image다 | OS와 기본 패키지 차이를 설명하지 못한다 | AMI name/id |
| Instance type | compute/memory/network capacity와 비용을 좌우한다 | 필요 이상으로 큰 instance를 켠다 | instance type, pricing |
| Key pair/접속 방식 | Linux EC2 접속의 identity material이다 | key를 잃거나 노출한다 | key pair name, SSH/browser connect |
| Stop vs terminate | stop은 일부 비용이 남고, terminate는 영구 삭제다 | 비용이 계속 나거나 데이터를 잃는다 | instance state, EBS volume |

## EC2는 무엇인가
EC2는 AWS에서 virtual server를 제공하는 service다. Docker container나 Kubernetes Pod보다 아래 계층의 compute에 가깝다. EC2 위에 Docker를 설치할 수도 있고, Kubernetes node로 사용할 수도 있다.

```mermaid
flowchart TB
  EC2["EC2 instance"]
  EC2 --> OS["Operating system from AMI"]
  EC2 --> CPU["vCPU / memory from instance type"]
  EC2 --> Disk["EBS volume"]
  EC2 --> Net["ENI / private IP / optional public IP"]
  EC2 --> SG["Security Group"]
```

## 생성 전 읽을 값
오늘은 실제 생성을 강제하지 않는다. Day2에서 만들기 전에 다음 값을 읽는 법을 익힌다.

| 항목 | 의미 | 위험 |
|---|---|---|
| AMI | 어떤 OS image로 시작하는가 | 문서 명령과 OS가 다르면 실패 |
| Instance type | CPU/memory/network 크기 | 비용 증가 |
| Key pair | SSH 접속 key | 분실/노출 |
| Network | VPC/subnet/public IP | 접속 불가 또는 public 노출 |
| Security Group | 허용 traffic | 22/80 과다 노출 |
| Storage | root EBS size/delete on termination | 잔여 비용 또는 데이터 삭제 |
| Tag | owner/purpose 추적 | cleanup 누락 |

## Stop과 terminate
AWS 공식 문서 기준으로 stopped instance는 compute 사용료가 멈추지만 EBS volume 같은 storage 비용은 남을 수 있다. terminate는 영구 삭제이며 복구할 수 없다.

| 상태 | 의미 | 비용/복구 관점 |
|---|---|---|
| running | instance 실행 중 | compute 비용 발생 |
| stopped | instance 정지 | compute 비용은 멈추지만 EBS 비용 가능 |
| terminated | instance 삭제 | 복구 불가, 연결 불가 |

## User data preview
User data는 instance 최초 부팅 때 실행할 bootstrap script로 자주 사용된다. Day2에서는 간단한 web server를 자동 설치하는 데 사용할 수 있다. 오늘은 "서버에 들어가서 손으로 한 설정"과 "부팅 시 재현되는 설정"이 다르다는 점만 잡는다.

```bash
#!/bin/bash
echo "hello from paperclip w5" > /var/www/html/index.html
```

위 예시는 OS와 web server 설치 상태에 따라 그대로 동작하지 않을 수 있다. Day2에서는 AMI에 맞는 전체 script를 사용한다.


## 생성 전 의사결정 표
| 선택 | 초보자가 자주 하는 실수 | 안전한 판단 |
|---|---|---|
| AMI | 문서와 다른 OS 선택 | 수업 명령과 맞는 AMI 선택 |
| Instance type | 큰 type 선택 | 실습 목적의 작은 type |
| Key pair | 다운로드 후 위치 모름 | 저장 위치와 권한 기록 |
| Public IP | 꺼둔 채 접속 기대 | public 접속 필요 시 enable |
| Storage | terminate 후 data 보존 오해 | EBS delete 옵션 확인 |
| Tag | 이름만 적음 | Owner/Purpose/Week tag 포함 |

## stop이 안전한 삭제가 아닌 이유
stopped 상태는 instance compute는 멈추지만 EBS volume, Elastic IP 연결 상태, snapshot, load balancer 같은 다른 resource 비용은 남을 수 있다. 그래서 수업 종료 checklist는 "EC2 stop" 하나로 끝나면 안 된다. 어떤 resource가 계속 비용을 만들 수 있는지 같이 확인해야 한다.

## user data를 미리 보는 이유
EC2에 접속해서 손으로 설치하면 당장은 성공할 수 있다. 하지만 다른 학생이나 다음 날의 내가 같은 서버를 다시 만들 때 순서가 누락될 수 있다. user data는 완전한 IaC는 아니지만, 최소한 bootstrap 절차를 instance 생성 시점에 묶어 재현성을 높인다.

## 캡처 가이드
EC2 launch summary에서 AMI, instance type, network, SG, storage, tag가 보이도록 캡처한다. private key 내용이나 계정 email은 절대 캡처하지 않는다.

## 운영 판단 연습
| 판단 질문 | 확인 기준 |
|---|---|
| 이 항목에서 가장 먼저 결정할 것은 무엇인가 | running은 instance 상태이지 app 정상 상태가 아니다. |
| 실패했을 때 어느 경계부터 볼 것인가 | public IP와 DNS는 접속 evidence가 된다. |
| 수업 뒤 혼자 재현할 때 필요한 최소 정보는 무엇인가 | stop과 terminate의 비용 차이를 구분한다. |

## 흔한 실패와 첫 확인 위치
| 흔한 실패 | 첫 확인 위치 |
|---|---|
| instance가 running인데 HTTP가 안 된다 | status check, SG, app process를 나누어 본다 |

## Evidence 점검
- 화면에는 민감 정보 대신 resource 이름, Region, 상태값, rule, tag처럼 재현 가능한 값이 보여야 한다.
- 기록에는 "성공했다"보다 어떤 값이 어떤 상태였는지가 남아야 한다.
- 실패를 기록할 때는 증상, 확인한 화면, 수정한 값, 재확인 결과를 한 세트로 남긴다.
- instance state, public IP/DNS, instance type과 tag 중 최소 두 가지는 배움일기에 남긴다.

## Evidence Note
```markdown
# W5D1S6 ec2 observation
- AMI 후보:
- instance type 후보:
- VPC/subnet:
- public IP 필요 여부:
- SG inbound 최소 rule:
- stop과 terminate 차이:
- 남을 수 있는 비용:
```

## 혼자 다시 따라오기
- 최소 재현 경로: EC2 launch 화면에서 실제 launch 직전까지 값을 읽고, 생성하지 않고 취소한다.
- 공식 문서 키워드: `EC2 instance lifecycle`, `stop instance`, `terminate instance`, `security group`.
- 스스로 확인할 화면: EC2 Launch instance, Instance state, Storage tab, Security tab.
- 흔한 실패 3개: key pair를 잃음, stop하면 모든 비용이 0이라고 오해함, terminate를 rollback처럼 생각함.
- 다음 준비 상태: Day2에서 EC2를 만들기 전 AMI/type/network/SG/storage/tag를 설명할 수 있어야 한다.

## 한 줄 요약
```text
EC2는 만들기 전에 AMI, type, network, security group, storage, tag, cleanup 기준을 먼저 읽어야 한다.
```
