# 8교시: 구름 EXP 배움일기

![AWS cleanup and learning journal board](./assets/lesson-08-cleanup-journal.png)

## 수업 목표
- 오늘 만든 EC2/ALB/network evidence를 정리한다.
- 비용이 남는 resource를 cleanup한다.
- Day3 ECR/ECS/App Runner 수업으로 이어질 질문을 남긴다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Cleanup audit | EC2/ALB/EBS는 실습 후 비용이 남을 수 있다 | 수업 후 비용 발생 | EC2, ALB, target group, EBS |
| Traffic evidence | 다음 수업 컨테이너 배포의 기준이 된다 | ECS/ALB 연결 때 다시 헤맨다 | ALB DNS, target health |
| Failure note | 장애 주입과 복구가 운영 학습의 핵심이다 | 성공 화면만 남고 판단력이 안 는다 | SG drill note |

## 배움일기 템플릿
```markdown
# W5D2 AWS network and EC2/ALB

## 1. 오늘 만든 resource
- Region:
- EC2:
- Security Group:
- Target Group:
- ALB:

## 2. Traffic path
Browser/curl -> ? -> ? -> ? -> EC2 web server

## 3. 성공 evidence
- EC2 public IP curl:
- ALB DNS curl:
- Target health:

## 4. 장애 분석
- 주입한 실패:
- 실패 증상:
- 확인한 위치:
- 복구 방법:
- recheck 결과:

## 5. Cleanup
- EC2:
- ALB:
- Target Group:
- Security Group:
- EBS:
- Key Pair:

## 6. Day3 질문
-
-
```

## Cleanup 순서
수업 resource를 삭제하는 경우 다음 순서를 권장한다.

| 순서 | 대상 | 확인 |
|---|---|---|
| 1 | ALB listener/load balancer | deleted 또는 deleting |
| 2 | Target group | unused 후 delete |
| 3 | EC2 instance | stop 또는 terminate |
| 4 | EBS volume | delete on termination 또는 detached volume 확인 |
| 5 | Security Group | default가 아닌 실습 SG 삭제 |
| 6 | Key Pair | 필요 없으면 삭제, local private key도 관리 |
| 7 | Cost/Billing | 비용 항목 확인 |

## 유지하는 경우
Day3에서 같은 EC2를 이어 쓸 수는 있다. 하지만 유지한다면 다음을 남긴다.

| 유지 대상 | 유지 사유 | 예상 비용 | 삭제 예정 |
|---|---|---|---|
| EC2 |  |  |  |
| ALB |  |  |  |
| EBS |  |  |  |

ALB는 특히 "잠깐 남겨둔다"가 비용으로 이어질 수 있다. 남기려면 사유와 삭제 예정 시각을 적는다.


## cleanup audit가 중요한 이유
cloud 실습은 종료 버튼을 누르는 순간 끝나지 않는다. ALB, EBS, Elastic IP, log group, snapshot, NAT Gateway처럼 눈에 잘 안 띄는 resource가 비용을 만든다. 그래서 cleanup은 별도 과제가 아니라 실습의 마지막 단계다.

## 삭제 전 확인할 관계
| resource | 의존 관계 | 삭제 순서 힌트 |
|---|---|---|
| ALB | listener, target group | ALB 삭제 후 TG 삭제 |
| Target Group | registered target | ALB 연결 해제 후 삭제 |
| EC2 | EBS, SG, key pair | terminate/stop 결정 |
| EBS | EC2 root/data volume | detached volume 확인 |
| SG | EC2/ALB attached 여부 | 연결 해제 후 삭제 |

## Day3 연결
D3에서는 EC2에 직접 설치한 app 대신 container image를 service가 실행한다. 따라서 오늘의 ALB, target group, health check, port 개념이 그대로 다시 등장한다. Day2 배움일기에 port와 health check를 정리해두면 Day3가 훨씬 쉬워진다.

## 좋은 cleanup 기록
"삭제함"이라고만 쓰지 말고 resource 이름, 상태, 삭제 시각, 유지 사유를 적는다. 비용이 걱정되는 resource는 Cost Explorer에서 service별 비용으로 다시 확인한다.

## 운영 판단 연습
| 판단 질문 | 확인 기준 |
|---|---|
| 이 항목에서 가장 먼저 결정할 것은 무엇인가 | 삭제는 EC2 하나로 끝나지 않는다. |
| 실패했을 때 어느 경계부터 볼 것인가 | ALB와 target group도 별도 resource다. |
| 수업 뒤 혼자 재현할 때 필요한 최소 정보는 무엇인가 | 삭제 후 검색 결과까지 확인해야 한다. |

## 흔한 실패와 첫 확인 위치
| 흔한 실패 | 첫 확인 위치 |
|---|---|
| 인스턴스만 terminate하고 ALB를 남긴다 | EC2, Load Balancers, Target Groups를 모두 검색한다 |

## Evidence 점검
- 화면에는 민감 정보 대신 resource 이름, Region, 상태값, rule, tag처럼 재현 가능한 값이 보여야 한다.
- 기록에는 "성공했다"보다 어떤 값이 어떤 상태였는지가 남아야 한다.
- 실패를 기록할 때는 증상, 확인한 화면, 수정한 값, 재확인 결과를 한 세트로 남긴다.
- 삭제 전 목록, 삭제 후 검색, Budget/Billing 확인 중 최소 두 가지는 배움일기에 남긴다.

## 혼자 다시 따라오기
- 최소 재현 경로: 배움일기 템플릿의 traffic path와 cleanup 항목을 먼저 채운다.
- 공식 문서 키워드: `EC2 instance lifecycle`, `Application Load Balancer`, `target group`, `security group`.
- 스스로 확인할 화면: EC2 Instances, Load Balancers, Target Groups, Volumes, Security Groups.
- 흔한 실패 3개: ALB만 삭제하고 target group을 남김, EC2 stop 후 EBS 비용을 잊음, key pair/private key 관리 상태를 안 남김.
- 다음 준비 상태: Day3에서 container image를 ALB 뒤에 붙일 때 listener/target group/health check 개념을 재사용할 수 있어야 한다.

## 한 줄 요약
```text
W5D2의 끝은 ALB 접속 성공이 아니라 evidence 정리와 cleanup audit이다.
```
