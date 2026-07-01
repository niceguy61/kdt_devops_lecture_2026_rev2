# 5교시: Load Balancing 개념

![Application Load Balancer concepts](./assets/lesson-05-alb-concepts.png)

## 수업 목표
- ALB, listener, target group, health check의 역할을 구분한다.
- public endpoint와 private target의 경계를 이해한다.
- Kubernetes Service/Ingress/Gateway와 ALB의 연결점을 설명한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| ALB | HTTP/HTTPS 요청을 여러 target으로 분산하는 entry point다 | EC2 public IP에만 의존한다 | ALB DNS name |
| Listener | ALB가 어떤 protocol/port로 요청을 받을지 정한다 | 80/443 접속 실패 원인을 못 찾는다 | listener rules |
| Target Group | ALB가 traffic을 보낼 대상 묶음이다 | instance와 ALB 연결을 설명하지 못한다 | registered targets |
| Health Check | healthy target에만 traffic을 보내기 위한 판단이다 | ALB는 떠 있는데 503이 난다 | target health |

## ALB 요청 흐름
```mermaid
flowchart LR
  User["Browser"] --> DNS["ALB DNS"]
  DNS --> Listener["Listener :80"]
  Listener --> TG["Target Group"]
  TG --> H["Health Check"]
  TG --> EC2A["EC2 target A"]
  TG --> EC2B["EC2 target B"]
```

AWS 공식 문서 기준으로 target group은 EC2 같은 target으로 protocol/port에 맞춰 요청을 보낸다. ALB health check는 target이 traffic을 받을 수 있는지 주기적으로 확인한다.

## Public ALB와 private target
처음에는 단순화를 위해 public subnet의 EC2를 target으로 사용한다. 운영 환경에서는 ALB는 public subnet에 두고 app target은 private subnet에 두는 구조도 자주 쓴다.

| 구성 | 의미 |
|---|---|
| Internet-facing ALB | internet에서 접근 가능한 ALB |
| Internal ALB | VPC 내부에서만 접근 |
| Public subnet | ALB 같은 public endpoint 배치 |
| Private subnet | app/DB target 배치 |
| Security Group | ALB -> target traffic 허용 |

## Kubernetes와 비교
| Kubernetes | AWS ALB |
|---|---|
| Service | target group과 일부 역할 유사 |
| Ingress/Gateway | listener/rule과 연결 가능 |
| readinessProbe | target health check와 목적 유사 |
| EndpointSlice | registered target 목록과 비교 가능 |
| kube-proxy/routing | ALB data plane과 계층이 다름 |

비교는 이해를 돕기 위한 것이다. Kubernetes object와 ALB resource는 같은 계층이 아니다.

## ALB 비용 주의
ALB는 실습이 끝나도 남아 있으면 비용이 발생할 수 있다. target group만 비워도 ALB 자체가 남으면 비용이 계속될 수 있다. Day2 종료 전 삭제 확인을 반드시 한다.


## ALB가 해결하는 운영 문제
EC2 public IP에 직접 접속하면 instance 교체, 장애, 확장 때 사용자가 영향을 바로 받는다. ALB는 사용자가 보는 endpoint와 backend target을 분리한다. target을 추가하거나 교체해도 사용자는 ALB DNS를 기준으로 접근한다. 이 분리가 load balancing의 핵심이다.

## Health check는 배포 품질 gate다
Health check는 단순 ping이 아니다. 사용자가 받을 traffic을 target에 보내도 되는지 판단하는 gate다. path가 틀리거나 app port가 다르면 target은 unhealthy가 되고 ALB는 traffic을 보내지 않는다. Kubernetes readinessProbe를 배운 이유가 여기서 다시 등장한다.

## ALB 구성요소별 질문
| 구성요소 | 질문 |
|---|---|
| ALB | internet-facing인가 internal인가 |
| Listener | 어떤 port/protocol로 받는가 |
| Rule | 어떤 요청을 어디로 보내는가 |
| Target Group | 어떤 대상과 port로 보내는가 |
| Health Check | 어떤 path/status를 정상으로 보는가 |
| SG | user -> ALB, ALB -> target이 열려 있는가 |

## 비용 경계
ALB는 target이 없거나 traffic이 없어도 생성되어 있으면 비용이 발생할 수 있다. 실습 후 삭제하지 않는 ALB는 초보 cloud 비용 사고의 좋은 예시다.

## 운영 판단 연습
| 판단 질문 | 확인 기준 |
|---|---|
| 이 항목에서 가장 먼저 결정할 것은 무엇인가 | ALB는 listener, rule, target group, health check의 조합이다. |
| 실패했을 때 어느 경계부터 볼 것인가 | target health는 사용자 접속 가능성과 연결된다. |
| 수업 뒤 혼자 재현할 때 필요한 최소 정보는 무엇인가 | health check path와 port가 app과 맞아야 한다. |

## 흔한 실패와 첫 확인 위치
| 흔한 실패 | 첫 확인 위치 |
|---|---|
| ALB DNS가 있으면 끝났다고 생각한다 | target health reason을 확인한다 |

## Evidence 점검
- 화면에는 민감 정보 대신 resource 이름, Region, 상태값, rule, tag처럼 재현 가능한 값이 보여야 한다.
- 기록에는 "성공했다"보다 어떤 값이 어떤 상태였는지가 남아야 한다.
- 실패를 기록할 때는 증상, 확인한 화면, 수정한 값, 재확인 결과를 한 세트로 남긴다.
- listener, target group, health check path 중 최소 두 가지는 배움일기에 남긴다.

## Evidence Note
```markdown
# W5D2S5 ALB concept
- ALB type:
- Listener:
- Target group protocol/port:
- Health check path:
- Public endpoint:
- 비용 cleanup 대상:
```

## 혼자 다시 따라오기
- 최소 재현 경로: ALB, listener, target group, health check를 그림으로 그리고 각 역할을 한 줄씩 적는다.
- 공식 문서 키워드: `Application Load Balancer`, `listener`, `target group`, `health check`.
- 스스로 확인할 화면: EC2 Load Balancers, Target Groups, Health checks.
- 흔한 실패 3개: ALB DNS와 EC2 public IP를 혼동함, target group port가 app port와 다름, health check path가 실제 응답 path와 다름.
- 다음 준비 상태: ALB 503이 나면 target health부터 확인해야 한다는 점을 설명할 수 있어야 한다.

## 한 줄 요약
```text
ALB는 public entry point이고, target group과 health check가 실제 traffic 대상을 결정한다.
```
