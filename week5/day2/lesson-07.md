# 7교시: EC2/ALB 운영 관찰

![EC2 and ALB operations observation](./assets/lesson-07-operations-observation.png)

## 수업 목표
- EC2 instance status, system log, Security Group, ALB target health를 연결해 본다.
- 접속 실패를 사용자 관점, load balancer 관점, target 관점으로 나눈다.
- CloudWatch/CloudTrail로 넘어갈 관찰 질문을 만든다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Layered observation | 사용자 요청은 여러 계층을 지난다 | 한 화면만 보고 결론 낸다 | browser, ALB, target, EC2 |
| Target health reason | ALB가 왜 target을 unhealthy로 보는지 알려준다 | ALB 문제인지 app 문제인지 모른다 | target health reason |
| System log | boot/user data 실패를 확인할 수 있다 | user data 실패를 app 문제로 본다 | EC2 system log |
| Audit preview | 누가 rule을 바꿨는지 추적해야 한다 | 변경 원인을 찾지 못한다 | CloudTrail event history |

## 관찰 순서
```text
1. 사용자 증상: browser/curl 결과
2. ALB 상태: active, listener, DNS
3. Target group: target health, reason
4. EC2 상태: running, status checks
5. Network gate: ALB SG, EC2 SG, route/subnet
6. App 상태: web server process, user data/system log
7. 변경 추적: CloudTrail preview
```

## 장애 예시
| 사용자 증상 | 가능한 원인 | 첫 확인 |
|---|---|---|
| ALB DNS timeout | ALB SG, subnet, DNS propagation | ALB SG inbound |
| 503 | no healthy target | Target health |
| EC2 public IP는 됨, ALB는 안 됨 | listener/TG/health check | Listener, TG |
| EC2 public IP도 안 됨 | SG/public IP/app | EC2 SG, instance |
| 갑자기 접속 안 됨 | 누군가 SG 변경 | CloudTrail event |

## Evidence를 남기는 방식
장애 분석은 "아마 SG 문제"로 끝내지 않는다.

```markdown
증상: ALB DNS 접속 시 503
증거1: ALB active
증거2: target group target unhealthy
증거3: health check path /health, app은 / 만 응답
조치: health check path를 / 로 변경
재확인: target healthy, curl 200
```

## CloudWatch/CloudTrail preview
Day3 이후 CloudWatch Logs/Metrics를 더 다루지만, 오늘도 위치는 확인한다.

| 도구 | 오늘 수준 |
|---|---|
| CloudWatch Metrics | ALB/EC2 metric 위치 확인 |
| CloudWatch Logs | app log 수집은 preview |
| CloudTrail | SG/ALB/EC2 API 변경 이벤트 확인 |


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | 정상 요청 경로 확인 | ALB curl 200 |
| 10~20분 | target health reason 분석 | healthy reason |
| 20~30분 | EC2 status/system log 연결 | status checks/log |
| 30~40분 | CloudTrail 변경 추적 preview | SG event |
| 40~50분 | incident note 작성 | symptom/evidence/fix |

## 관찰을 계층으로 나누기
사용자 증상 하나에 여러 계층이 숨어 있다. ALB 503은 app code 문제일 수도 있지만, target group에 healthy target이 없는 문제일 수도 있다. EC2 public IP는 되는데 ALB는 안 되면 ALB/listener/target group을 본다. 둘 다 안 되면 app 또는 EC2 network를 본다.

## 운영 incident note 예시
```markdown
증상: ALB DNS 접속 시 503
영향: public endpoint에서 web page 접근 불가
증거: ALB active, target group unhealthy
원인 후보: health check path mismatch
조치: health check path / 로 변경
재확인: target healthy, curl 200
예방: app health endpoint와 target group 설정을 runbook에 기록
```

## CloudTrail preview
Security Group rule을 누가 바꿨는지는 CloudWatch Logs가 아니라 CloudTrail에서 찾는다. Event history에서 `AuthorizeSecurityGroupIngress`, `RevokeSecurityGroupIngress` 같은 API event를 검색할 수 있다.

## 캡처 가이드
장애 분석 캡처는 전후가 있어야 한다. 실패 curl, unhealthy target, 수정한 설정, 성공 curl을 한 묶음으로 남긴다.

## 강사 보강 노트
이 교시는 `운영 관찰`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| CloudWatch에 데이터가 바로 없으면 실패로 봄 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| CloudTrail을 app log로 착각함 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| Billing data 지연을 모름 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

## 실습 중 멈춤 포인트
- 첫 번째 멈춤: 학생이 resource를 생성하기 전에 이름, Region, tag, 예상 비용 발생 지점을 말하게 한다.
- 두 번째 멈춤: 성공 화면이 나온 직후 resource ID와 상태값을 evidence note에 적게 한다.
- 세 번째 멈춤: 실패나 지연이 생기면 새로 클릭하기 전에 이전 단계의 화면과 명령을 다시 보게 한다.
- 네 번째 멈춤: 정리 단계에서 "삭제했다"가 아니라 "검색해도 남아 있지 않다"를 확인하게 한다.

## 확인 질문
1. 오늘 만든 resource가 어느 Region과 어느 계정 경계에 있는가?
2. 이 resource가 비용을 만들기 시작하는 시점은 언제인가?
3. 접속이 실패하면 app, network, permission 중 무엇을 먼저 확인할 것인가?
4. 수업이 끝난 뒤 남겨도 되는 resource와 지워야 하는 resource는 무엇인가?

## 제출 evidence 기준
| evidence | 좋은 예 | 부족한 예 |
|---|---|---|
| 화면 캡처 | EC2 status check | 성공 toast만 보이는 캡처 |
| 설정 기록 | ALB target health | "기본값 사용"이라고만 적음 |
| 운영 판단 | CloudTrail event history | "잘 됨", "안 됨"으로만 적음 |

## Evidence Note
```markdown
# W5D2S7 operations observation
- User symptom:
- ALB status:
- Listener:
- Target health:
- EC2 status checks:
- SG checked:
- System log checked:
- Recheck result:
```

## 혼자 다시 따라오기
- 최소 재현 경로: ALB DNS 응답 하나를 기준으로 target health와 EC2 status를 함께 기록한다.
- 공식 문서 키워드: `check target health`, `EC2 system log`, `CloudTrail event history`.
- 스스로 확인할 화면: Target health, EC2 Status checks, EC2 System log, CloudTrail Event history.
- 흔한 실패 3개: ALB active만 보고 정상이라고 판단함, target health reason을 안 봄, 변경자를 추적하지 않음.
- 다음 준비 상태: 장애를 사용자 증상, ALB, target, EC2, SG, app으로 나눠 설명할 수 있어야 한다.

## 한 줄 요약
```text
운영 관찰은 한 화면의 초록불이 아니라 요청 경로 전체의 evidence를 연결하는 일이다.
```
